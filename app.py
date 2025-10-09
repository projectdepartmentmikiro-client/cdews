import os
import time
import threading
import requests
import cv2
import numpy as np
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from flask import Flask, Response, render_template, jsonify, request, send_from_directory, url_for
import atexit

app = Flask(__name__)
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (1280, 720)}))
camera.start()
DATA_DIR = "data"
SAMPLE_DIR = os.path.join(DATA_DIR, "samples")
os.makedirs(SAMPLE_DIR, exist_ok=True)
sample_image_lock = threading.Lock()
sample_image = None
freeze_lock = threading.Lock()
freeze_image = None
freeze_mode = False
last_sample_data_lock = threading.Lock()
last_sample_data = {"timestamp": "", "sample_image_filename": "", "egg_count": "", "user_name": "", "device_id": ""}

def safe_filename(prefix: str) -> str:
    return f"{prefix}_{time.strftime('%Y%m%d-%H%M%S')}.jpg"

def send_sample_to_colab(sample_path: str, retries: int = 3):
    colab_url = "https://9f043a11b5e6.ngrok-free.app/predict"
    for attempt in range(retries):
        try:
            with open(sample_path, "rb") as f:
                files = {"file": (os.path.basename(sample_path), f, "image/jpeg")}
                response = requests.post(colab_url, files=files, timeout=10)
            if response.status_code == 200:
                data = response.json()
                with last_sample_data_lock:
                    last_sample_data["egg_count"] = data.get("egg_count", 0)
                return
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(2)

def blink_led(duration=2, speed=0.1):
    end_time = time.time() + duration
    while time.time() < end_time:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(speed)

def capture_sample(user_name: str, device_id: str):
    global sample_image, freeze_image, freeze_mode
    try:
        GPIO.output(LED_PIN, GPIO.HIGH)
        frame = camera.capture_array()
        sample_filename = safe_filename(device_id)
        sample_path = os.path.join(SAMPLE_DIR, sample_filename)
        cv2.imwrite(sample_path, frame)
        with sample_image_lock:
            sample_image = frame.copy()
        with freeze_lock:
            freeze_image = frame.copy()
            freeze_mode = True
        with last_sample_data_lock:
            last_sample_data.update({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "sample_image_filename": sample_filename,
                "egg_count": "",
                "user_name": user_name,
                "device_id": device_id
            })
        threading.Thread(target=send_sample_to_colab, args=(sample_path,), daemon=True).start()
        threading.Thread(target=blink_led, args=(4, 0.2), daemon=True).start()
        time.sleep(3)
        with freeze_lock:
            freeze_mode = False
    finally:
        GPIO.output(LED_PIN, GPIO.LOW)

def generate_frames():
    global freeze_mode, freeze_image
    while True:
        with freeze_lock:
            frame = freeze_image.copy() if freeze_mode and freeze_image is not None else camera.capture_array()
        ret, jpeg = cv2.imencode(".jpg", frame)
        if ret:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n"
        time.sleep(0.05)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/capture", methods=["POST"])
def capture():
    data = request.get_json()
    user_name = data.get("user_name", "unknown_user")
    device_id = data.get("device_id", "unknown_device")
    threading.Thread(target=capture_sample, args=(user_name, device_id), daemon=True).start()
    return jsonify({"status": "capturing", "user_name": user_name, "device_id": device_id})

@app.route("/last_sample")
def last_sample():
    with last_sample_data_lock:
        data = last_sample_data.copy()
        data["sample_image_url"] = url_for("serve_sample", filename=data["sample_image_filename"]) if data["sample_image_filename"] else None
    return jsonify(data)

@app.route("/samples/<filename>")
def serve_sample(filename):
    return send_from_directory(SAMPLE_DIR, filename)

@atexit.register
def cleanup():
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
    camera.stop()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
