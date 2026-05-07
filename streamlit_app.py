import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. DATABASE & SETUP
# ==========================================

@st.cache_resource
def init_db():
    conn = sqlite3.connect(
        'bio_adaptive_v3.db',
        check_same_thread=False
    )

    c = conn.cursor()

    # ตารางนักเรียน
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            sid TEXT PRIMARY KEY,
            title TEXT,
            fname TEXT,
            lname TEXT,
            grade_lvl TEXT,
            no INTEGER,
            level TEXT,
            img BLOB
        )
    ''')

    # ตารางบันทึกผลการเรียน
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sid TEXT,
            chapter TEXT,
            pre_p REAL,
            post_p REAL,
            grade TEXT,
            timestamp DATETIME
        )
    ''')

    conn.commit()
    return conn


conn = init_db()

# ==========================================
# 2. PLACEMENT TEST
# ==========================================

PLACEMENT_QUESTIONS = [
    {
        "q": "หน่วยที่เล็กที่สุดของสิ่งมีชีวิตคืออะไร?",
        "a": ["อะตอม", "เซลล์", "เนื้อเยื่อ", "อวัยวะ"],
        "c": "เซลล์"
    },
    {
        "q": "กระบวนการใดที่พืชสร้างอาหาร?",
        "a": ["การหายใจ", "การคายน้ำ", "การสังเคราะห์ด้วยแสง", "การดูดซึม"],
        "c": "การสังเคราะห์ด้วยแสง"
    },
    {
        "q": "มนุษย์มีโครโมโซมกี่แท่ง?",
        "a": ["23 แท่ง", "44 แท่ง", "46 แท่ง", "48 แท่ง"],
        "c": "46 แท่ง"
    }
]

# ==========================================
# 3. LESSON DATA
# ==========================================

LESSON_DATA = {