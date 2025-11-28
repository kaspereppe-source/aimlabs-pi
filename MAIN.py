import cv2
import socket

UDP_IP = "192.168.2.1"    # PC IP (statisk)
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

path = ""  # sett inn cascade filsti
obj = "target"

scale = 2
min_neig = 4

cascade = cv2.CascadeClassifier(path)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

center_x = 320
center_y = 240

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detect = cascade.detectMultiScale(gray, scale, min_neig)

    if len(detect) > 0:
        x, y, w, h = detect[0]
        cx = x + w/2
        cy = y + h/2

        dx = int(cx - center_x)
        dy = int(cy - center_y)

        msg = f"{dx},{dy}"
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))

cap.release()
