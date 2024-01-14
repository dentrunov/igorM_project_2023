import cv2

cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if data:
        print(data)
        a = data
        break

    cv2.imshow("QRCODEscanner", img)
    if cv2.waitKey(1) == ord("q"):
        break