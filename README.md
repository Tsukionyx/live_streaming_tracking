# Flask Live Streaming with SSD Object Detection and Tracking

## Overview

This project demonstrates how to stream video from a USB camera connected to a Raspberry Pi to a PC over TCP/IP, perform real-time object detection using an SSD (Single Shot Detector) model and object tracking on the PC, and then deliver the processed video to a web browser using Flask.

System architecture:

```text
+---------------------+
| Raspberry Pi        |
| USB Camera          |
+----------+----------+
           |
           | TCP/IP
           v
+---------------------+
| PC                  |
| Flask Server        |
| SSD Object Detection|
| Object Tracking     |
+----------+----------+
           |
           | HTTP
           v
+---------------------+
| Web Browser         |
+---------------------+
```

### Features

* Capture video from a USB camera
* Transfer video frames over TCP/IP
* Real-time object detection using an SSD (MobileNet-based) model
* Multi-object tracking with persistent object IDs
* Live video streaming using Flask
* View the processed video from any web browser

---

## System Requirements

### Raspberry Pi

* Raspberry Pi 4 or Raspberry Pi 5
* Raspberry Pi OS
* Python 3.9 or later
* USB camera

### PC

* Windows 10 / 11
* Ubuntu 22.04 or other Linux distributions
* Python 3.9 or later

### Tested Libraries

| Library     | Version                     |
| ----------- | --------------------------- |
| Flask       | 3.x                         |
| OpenCV      | 4.x                         |
| PyTorch     | 2.x                         |
| TorchVision | 0.15 or later (recommended) |
| Pillow      | Latest                      |
| NumPy       | Latest                      |
| FilterPy    | Latest                      |

> **Note:** The SSD model initialization may differ depending on the installed version of TorchVision.

---

## Installation

### Raspberry Pi

### 1. Install the required Python package

```bash
pip install opencv-python
```

### 2. Verify that the USB camera is detected

```bash
ls /dev/video*
```

Example:

```bash
/dev/video0
```

---

### PC

### 1. Install the required Python packages

```bash
pip install flask
pip install opencv-python
pip install torch torchvision
pip install pillow
pip install numpy
pip install filterpy
```

Or install everything at once:

```bash
pip install -r requirements.txt
```

---

### 2. Configure the firewall

Allow the following ports:

**TCP**

```text
9999
```

**HTTP**

```text
5000
```

---

## Usage

### 1. Start the server on the PC

```bash
python flask_video_server.py
```

You should see output similar to:

```text
TCP server listening...
 * Running on http://0.0.0.0:5000
```

---

### 2. Start the Raspberry Pi client

```bash
python raspi_camera_client.py --server-ip <SERVER_IP_ADDRESS>
```

If the connection is successful, the following message will be displayed:

```text
Connected to server
```

---

### 3. Open the web browser

Access:

```text
http://<SERVER_IP_ADDRESS>:5000/
```

Example:

```text
http://192.168.1.100:5000/
```

---

## Expected Results

When everything is working correctly, the live camera stream from the Raspberry Pi will be displayed in your web browser.

Detected objects will be assigned tracking IDs, for example:

```text
ID 0
ID 1
ID 2
```

### Displayed Information

* Green bounding boxes
* Tracking IDs
* Live video stream

Example:

```text
+-----------------------+
|                       |
|    [ ID 0 ]           |
|   +-----------+       |
|   | Person    |       |
|   +-----------+       |
|                       |
+-----------------------+
```

As long as tracking is maintained, the same object will retain the same tracking ID even while moving.

---

## Notes

* SSD inference can be computationally expensive on CPU-only systems, resulting in a lower frame rate.
* A CUDA-enabled GPU can significantly improve performance.
* To reduce network bandwidth usage, consider lowering the image resolution or increasing JPEG compression.
* Tracking accuracy depends on image quality and object detection performance.

---

## License

This project is licensed under the MIT License.

---

## References

* Flask Official Documentation: https://flask.palletsprojects.com/
* PyTorch Official Website: https://pytorch.org/
* OpenCV Official Website: https://opencv.org/

---

# Contributing

If you find this project useful, I'd appreciate it if you:

- ⭐ Star this repository
- 🍴 Fork it if you customize it
- 🐛 Report bugs via Issues
- 💡 Share ideas via Discussions
