import cv2
import numpy as np
import socket

cap = cv2.VideoCapture(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PC_IP = "192.168.0.50"
PC_PORT = 5005

print("Sender PING til PC...")
sock.sendto(b"PING", (PC_IP, PC_PORT))

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 80, 80])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        cnt = contours[0]
        x, y, w, h = cv2.boundingRect(cnt)
        cx = x + w // 2
        cy = y + h // 2

        dx = cx - 320
        dy = cy - 240
        msg = f"{dx},{dy}".encode()
        sock.sendto(msg, (PC_IP, PC_PORT))
