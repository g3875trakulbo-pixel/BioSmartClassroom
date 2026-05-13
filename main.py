from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

# --- 1. ตั้งค่าฐานข้อมูล SQLite ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./biosmart_pro.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. สร้างโครงสร้างตารางเก็บคะแนน ---
class Score(Base):
    __tablename__ = "learning_scores"
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    lesson_id = Column(Integer)
    score = Column(Integer)

# สร้างไฟล์ฐานข้อมูลจริง
Base.metadata.create_all(bind=engine)

# --- 3. ตั้งค่า FastAPI ---
app = FastAPI()

# รูปแบบข้อมูลที่รับจากหน้าเว็บ
class QuizSubmission(BaseModel):
    student_name: str
    lesson_id: int
    score: int

# ฟังก์ชันเชื่อมต่อ Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API สำหรับรับคะแนนจากนักเรียน
@app.post("/submit")
def submit_score(submission: QuizSubmission, db: Session = Depends(get_db)):
    new_score = Score(
        student_name=submission.student_name,
        lesson_id=submission.lesson_id,
        score=submission.score
    )
    db.add(new_score)
    db.commit()
    # ส่งคำแนะนำกลับไปตามคะแนน (Logic อัจฉริยะเบื้องต้น)
    msg = "เยี่ยมมาก! คุณเข้าใจบทเรียนนี้อย่างดี" if submission.score >= 1 else "ลองกลับไปทบทวนเนื้อหาในขั้นตอน Explain อีกครั้งนะ"
    return {"status": "success", "recommendation": msg}

# API สำหรับดึงคะแนนทั้งหมดให้ครูดู
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return db.query(Score).all()
