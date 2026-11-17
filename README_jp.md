# Flask Live Streaming with SSD Object Detection and Tracking

## 概要

Raspberry Pi に接続された USB カメラの映像を TCP/IP 経由で PC に送信し、PC 上で SSD（Single Shot Detector）による物体検出およびトラッキングを実施した後、Flask を利用して Web ブラウザへライブ配信するサンプルです。

構成は以下の通りです。

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

主な機能：

* USBカメラ映像の取得
* TCP/IPによる映像転送
* SSD（MobileNetベース）による物体検出
* トラッキングによるID付与
* Flaskによるライブ映像配信
* ブラウザから閲覧可能

---

## 動作環境

### Raspberry Pi側

* Raspberry Pi 4 / 5
* Raspberry Pi OS
* Python 3.9 以上
* USBカメラ

### PC側

* Windows 10 / 11
* Ubuntu 22.04 などのLinux環境
* Python 3.9 以上

### 動作確認ライブラリ

| ライブラリ       | バージョン例   |
| ----------- | -------- |
| Flask       | 3.x      |
| OpenCV      | 4.x      |
| PyTorch     | 2.x      |
| TorchVision | 0.15以上推奨 |
| Pillow      | 最新版      |
| NumPy       | 最新版      |
| FilterPy    | 最新版      |

※ 使用する torchvision のバージョンによって SSD モデルの呼び出し方法が異なる場合があります。

---

## 環境構築手順

### Raspberry Pi側

#### 1. Pythonライブラリのインストール

```bash
pip install opencv-python
```

#### 2. USBカメラの接続確認

```bash
ls /dev/video*
```

例：

```bash
/dev/video0
```

---

### PC側

#### 1. Pythonライブラリのインストール

```bash
pip install flask
pip install opencv-python
pip install torch torchvision
pip install pillow
pip install numpy
pip install filterpy
```

または

```bash
pip install -r requirements.txt
```

---

#### 2. ファイアウォール設定

TCPポート

```text
9999
```

HTTPポート

```text
5000
```

を許可してください。

---

## 実行手順

### 1. PC側サーバ起動

```bash
python flask_video_server.py
```

起動すると以下のようなメッセージが表示されます。

```text
TCP server listening...
 * Running on http://0.0.0.0:5000
```

---

### 2. Raspberry Pi側クライアント起動

```bash
python raspi_camera_client.py --server-ip <サーバのIPアドレス>
```

正常に接続すると以下のように表示されます。

```text
Connected to server
```

---

### 3. ブラウザでアクセス

以下へアクセスします。

```text
http://<サーバのIPアドレス>:5000/
```

例：

```text
http://192.168.1.100:5000/
```

---

## 動作結果

正常に動作した場合、ブラウザ上に Raspberry Pi のカメラ映像が表示されます。

SSD により物体が検出されると、以下のような表示が行われます。

```text
ID 0
ID 1
ID 2
```

### 表示内容

* 緑色の矩形
* トラッキングID
* ライブ映像

例：

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

同一人物が移動した場合でも、トラッキングが継続している間は同じ ID が表示されます。

---

## 注意事項

* CPU環境では SSD 推論負荷が高く、フレームレートが低下する場合があります。
* GPU環境では大幅な高速化が期待できます。
* ネットワーク帯域を節約するため、JPEG圧縮率や解像度を調整してください。
* トラッキング精度はカメラ画質や検出精度に依存します。

---

## ライセンス

本プロジェクトは MIT License の下で公開しています。

---

## 参考

* [Flask Official Website](https://flask.palletsprojects.com/?utm_source=chatgpt.com)
* [PyTorch Official Website](https://pytorch.org/?utm_source=chatgpt.com)
* [OpenCV Official Website](https://opencv.org/?utm_source=chatgpt.com)

---

# コントリビューション

このプロジェクトが役に立つと感じたら、以下のことをしていただけると嬉しいです。

- ⭐ このリポジトリにスターを付ける
- 🍴 カスタマイズする場合はフォークする
- 🐛 Issues でバグを報告する
