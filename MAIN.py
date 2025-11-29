import cv2
import numpy as np
import socket

cap = cv2.VideoCapture(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PC_IP = "192.168.0.50"
PC_PORT = 5005

print("Sender PING til PC...")
sock.sendto(b"PING", (PC_IP, PC_PORT))

# Midtpunkt på kamera (640x480)
MID_X = 320
MID_Y = 240

# Blåfargeområde i HSV
lower_blue = np.array([90, 80, 80])
upper_blue = np.array([130, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ----------------------
    # FINN OBJEKT (som før)
    # ----------------------
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        cnt = contours[0]
        x, y, w, h = cv2.boundingRect(cnt)

        # Senter av objektet
        cx = x + w // 2
        cy = y + h // 2

        # dx/dy relativt til midten av kamera
        dx = cx - MID_X
        dy = cy - MID_Y

        # Send posisjonen til PC
        msg = f"{dx},{dy}".encode()
        sock.sendto(msg, (PC_IP, PC_PORT))

    # ----------------------------------------
    # SJEKK OM MIDTPUNKTET ER PÅ NOE BLÅTT
    # ----------------------------------------
    mid_pixel = hsv[MID_Y, MID_X]
    h, s, v = mid_pixel

    if (lower_blue[0] <= h <= upper_blue[0] and
        lower_blue[1] <= s <= upper_blue[1] and
        lower_blue[2] <= v <= upper_blue[2]):
        
        # Midten treffer blått → send varsel
        sock.sendto(b"OBJECT_FOUND", (PC_IP, PC_PORT))
        print("Midten er på objekt → OBJECT_FOUND sendt")
    else:
        print("Midten er IKKE på objekt")
