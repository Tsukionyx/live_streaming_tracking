from flask import Flask, Response, render_template_string
import socket
import threading
import struct
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models.detection import ssdlite320_mobilenet_v3_large
from PIL import Image

# =====================
# Flask
# =====================
app = Flask(__name__)

latest_frame = None
lock = threading.Lock()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SSD Object Detection</title>
</head>
<body>
    <h1>SSD (MobileNet) Object Detection</h1>
    <img src="/video_feed">
</body>
</html>
"""

# =====================
# PyTorch SSD (MobileNet)
# =====================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ssdlite320_mobilenet_v3_large(pretrained=True)
model.eval()
model.to(device)

# COCOラベル（91クラス）
COCO_CLASSES = [
    "__background__", "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
    "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
    "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
    "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass",
    "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich",
    "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    "chair", "couch", "potted plant", "bed", "dining table", "toilet",
    "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

transform = transforms.Compose([
    transforms.Resize((320, 320)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

SCORE_THRESHOLD = 0.5

# =====================
# TCP Server
# =====================
def tcp_server():
    global latest_frame

    HOST = "0.0.0.0"
    PORT = 9999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    print("TCP server listening...")
    conn, addr = s.accept()
    print(f"Connected from {addr}")

    data = b""

    while True:
        # フレームサイズ
        while len(data) < 4:
            packet = conn.recv(4096)
            if not packet:
                return
            data += packet

        frame_size = struct.unpack(">I", data[:4])[0]
        data = data[4:]

        while len(data) < frame_size:
            data += conn.recv(4096)

        frame_data = data[:frame_size]
        data = data[frame_size:]

        # JPEG → OpenCV
        np_img = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # SSD物体検出
        frame = run_ssd(frame)

        # JPEG化
        ret, jpg = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        with lock:
            latest_frame = jpg.tobytes()

# =====================
# SSD 推論
# =====================
def run_ssd(frame):
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    input_tensor = transform(pil_img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)[0]

    boxes = outputs["boxes"]
    labels = outputs["labels"]
    scores = outputs["scores"]

    for box, label, score in zip(boxes, labels, scores):
        if score < SCORE_THRESHOLD:
            continue

        x1, y1, x2, y2 = box.cpu().numpy()

        # 元画像サイズにスケール
        x1 = int(x1 * w / 320)
        x2 = int(x2 * w / 320)
        y1 = int(y1 * h / 320)
        y2 = int(y2 * h / 320)

        class_name = COCO_CLASSES[label]
        text = f"{class_name} {score:.2f}"

        # 枠描画
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, text, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2)

    return frame

# =====================
# Flask Streaming
# =====================
def generate_frames():
    global latest_frame
    while True:
        with lock:
            frame = latest_frame
        if frame is None:
            continue

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               frame + b"\r\n")

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    t = threading.Thread(target=tcp_server, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5000, threaded=True)
