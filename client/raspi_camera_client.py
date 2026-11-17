import cv2
import socket
import struct
import argparse


def parse_arguments():
    """
    コマンドライン引数を解析する。

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Raspberry Pi Camera TCP Client"
    )

    parser.add_argument(
        "--server-ip",
        required=True,
        help="接続先サーバIPアドレス"
    )

    parser.add_argument(
        "--server-port",
        type=int,
        default=9999,
        help="接続先サーバポート番号 (default: 9999)"
    )

    parser.add_argument(
        "--camera-id",
        type=int,
        default=0,
        help="使用するカメラID (default: 0)"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=640,
        help="映像の横幅 (default: 640)"
    )

    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="映像の高さ (default: 480)"
    )

    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=80,
        choices=range(1, 101),
        metavar="[1-100]",
        help="JPEG品質 (default: 80)"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    cap = cv2.VideoCapture(args.camera_id)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(
        f"Connecting to "
        f"{args.server_ip}:{args.server_port}"
    )

    sock.connect((args.server_ip, args.server_port))

    print("Connected")

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            encode_param = [
                int(cv2.IMWRITE_JPEG_QUALITY),
                args.jpeg_quality
            ]

            result, jpg = cv2.imencode(
                ".jpg",
                frame,
                encode_param
            )

            if not result:
                continue

            data = jpg.tobytes()

            sock.sendall(
                struct.pack(">I", len(data)) + data
            )

    except KeyboardInterrupt:
        print("Stopped by user")

    finally:
        cap.release()
        sock.close()
        print("Disconnected")


if __name__ == "__main__":
    main()
