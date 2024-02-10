import cv2
from datetime import datetime as dt
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from uuid import uuid4

from models import Pupils
from config import db_data



HOURS = 2
engine = create_engine(db_data, echo=True)

cap = cv2.VideoCapture(0)
# инициализация qr-reader
detector = cv2.QRCodeDetector()

while True:
    _, img = cap.read()
    try:
        data, bbox, _ = detector.detectAndDecode(img)
    except:
        continue
    # чтение qr-кода
    if data:
        with Session(engine) as session:
            try:
                query = select(
                    Pupils.pupil_id,
                    Pupils.pupil_name,
                    Pupils.last_generated_code_date,
                    Pupils.last_visit,
                    Pupils.out_time,
                    ).where(Pupils.last_generated_code == data)
                new_user = session.execute(query).one()
            except:
                continue
            if new_user:
                id = new_user.pupil_id
                now = dt.now()
                print("++++++++++++++++++++++++++++++++++++++")
                print("Пришел", new_user.pupil_name, now.strftime("%d.%m.%Y %H:%M:%S"))
                print("++++++++++++++++++++++++++++++++++++++")

                if new_user.last_visit is not None and now.day - new_user.last_visit.day == 0:
                    query = update(Pupils).where(Pupils.pupil_id == id).values(out_time=now, last_generated_code=str(uuid4()))
                else:
                    query = update(Pupils).where(Pupils.pupil_id == id).values(last_visit=now, last_generated_code=str(uuid4()))
                session.execute(query)
                session.commit()

    
    if cv2.waitKey(1) == ord("q"):
        # остановка чтения
        break