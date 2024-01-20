import cv2
from datetime import datetime as dt
from datetime import timedelta
from sqlalchemy import create_engine, text, select, update
from sqlalchemy.orm import Session

# from .igorm_2023.tbot.models import Pupils
# from .igorm_2023.tbot.config import db_data
from models import Pupils
from config import db_data

HOURS = 2
engine = create_engine(db_data, echo=True)

cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if data:
        with Session(engine) as session:
            query = select(Pupils.pupil_id, Pupils.pupil_name, Pupils.last_generated_code_date).where(Pupils.last_generated_code == data)
            new_user = session.execute(query).fetchone()
            print(new_user)
            if new_user:
                now = dt.now()
                user_date = new_user[2]
                if user_date - dt.now() < timedelta(hours=HOURS):
                    print("Пришел", new_user[1], now)
                    query = update(Pupils).where(Pupils.last_generated_code == data).values(last_visit=now, last_generated_code=0)
                    session.execute(query)
                    session.commit()
                    break
                else:
                    print("Слишком поздно!", new_user[1], now)
            else:
                print("Нет такого ученика")
        # break
    
    cv2.imshow("QRCODEscanner", img)
    if cv2.waitKey(1) == ord("q"):
        break