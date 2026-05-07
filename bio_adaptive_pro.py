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
    conn = sqlite3.connect('bio_adaptive_v3.db', check_same_thread=False)
    c = conn.cursor()
    # เพิ่ม column 'level' เพื่อเก็บระดับความรู้ (Beginner, Intermediate, Advanced)
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (sid TEXT PRIMARY KEY, title TEXT, fname TEXT, lname TEXT,
                  grade_lvl TEXT, no INTEGER, level TEXT, img BLOB)''')
    c.execute('''CREATE TABLE IF NOT EXISTS learning_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, sid TEXT, chapter TEXT,
                  pre_p REAL, post_p REAL, grade TEXT, timestamp DATETIME)''')
    conn.commit()
    return conn

conn = init_db()

# คลังข้อสอบวิเคราะห์ระดับ (Placement Test)
PLACEMENT_QUESTIONS = [
    {"q": "หน่วยที่เล็กที่สุดของสิ่งมีชีวิตคืออะไร?", "a": ["อะตอม", "เซลล์", "เนื้อเยื่อ", "อวัยวะ"], "c": "เซลล์"},
    {"q": "กระบวนการใดที่พืชสร้างอาหาร?", "a": ["การหายใจ", "การคายน้ำ", "การสังเคราะห์ด้วยแสง", "การดูดซึม"], "c": "การสังเคราะห์ด้วยแสง"},
    {"q": "มนุษย์มีโครโมโซมกี่แท่ง?", "a": ["23 แท่ง", "44 แท่ง", "46 แท่ง", "48 แท่ง"], "c": "46 แท่ง"}
]

# คลังเนื้อหาและแบบทดสอบรายบท (ตัวอย่าง)
LESSON_DATA = {
    "1. การศึกษาชีววิทยา": {
        "content": "ชีววิทยาคือการศึกษาเกี่ยวกับสิ่งมีชีวิต โดยใช้กระบวนการทางวิทยาศาสตร์...",
        "quiz": [
            {"q": "ข้อใดไม่ใช่กระบวนการทางวิทยาศาสตร์?", "a": ["การสังเกต", "การตั้งสมมติฐาน", "การใช้โชคชะตา", "การสรุปผล"], "c": "การใช้โชคชะตา"}
        ]
    },
    "2. เคมีที่เป็นพื้นฐานของสิ่งมีชีวิต": {
        "content": "น้ำเป็นสารประกอบอนินทรีย์ที่สำคัญที่สุดในเซลล์...",
        "quiz": [
            {"q": "พันธะที่ยึดเหนี่ยวโมเลกุลน้ำคือ?", "a": ["พันธะไอออนิก", "พันธะไฮโดรเจน", "พันธะโควาเลนต์", "พันธะโลหะ"], "c": "พันธะไฮโดรเจน"}
        ]
    }
}

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def get_student_level(score, total):
    percent = (score / total) * 100
    if percent >= 80: return "Advanced (เชี่ยวชาญ)"
    elif percent >= 50: return "Intermediate (ปานกลาง)"
    else: return "Beginner (พื้นฐาน)"

# ==========================================
# 3. INTERFACE
# ==========================================
st.set_page_config(page_title="BioAdaptive Learning AI", layout="wide")

with st.sidebar:
    st.title("🧬 BioAdaptive v3")
    menu = st.radio("เมนูหลัก", ["👤 ข้อมูลนักเรียน", "📝 วิเคราะห์ระดับ", "📖 บทเรียน & ทดสอบ", "📊 รายงานผล (ครู)"])

# ==========================================
# 4. LOGIC SECTIONS
# ==========================================

# --- SECTION: ลงทะเบียน ---
if menu == "👤 ข้อมูลนักเรียน":
    st.header("👤 ลงทะเบียนนักเรียนใหม่")
    with st.form("reg_form"):
        sid = st.text_input("รหัสประจำตัว*")
        fname = st.text_input("ชื่อ")
        lname = st.text_input("นามสกุล")
        grade = st.selectbox("ชั้น", ["ม.4", "ม.5", "ม.6"])
        if st.form_submit_button("บันทึกข้อมูล"):
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO students (sid, fname, lname, grade_lvl) VALUES (?,?,?,?)", (sid, fname, lname, grade))
            conn.commit()
            st.success("ลงทะเบียนสำเร็จ! โปรดไปที่เมนู 'วิเคราะห์ระดับ'")

# --- SECTION: วิเคราะห์ระดับ (Placement Test) ---
elif menu == "📝 วิเคราะห์ระดับ":
    st.header("📝 แบบทดสอบวิเคราะห์ความรู้พื้นฐาน")
    student_id = st.text_input("กรอกรหัสประจำตัวเพื่อเริ่มสอบ:")
    
    if student_id:
        st.info("คำแนะนำ: ผลคะแนนนี้จะใช้จัดกลุ่มเนื้อหาที่เหมาะสมกับคุณ")
        score = 0
        with st.form("placement_form"):
            for i, q in enumerate(PLACEMENT_QUESTIONS):
                ans = st.radio(f"{i+1}. {q['q']}", q['a'], key=f"p_{i}")
                if ans == q['c']: score += 1
            
            if st.form_submit_button("ส่งคำตอบ"):
                level = get_student_level(score, len(PLACEMENT_QUESTIONS))
                c = conn.cursor()
                c.execute("UPDATE students SET level=? WHERE sid=?", (level, student_id))
                conn.commit()
                st.success(f"วิเคราะห์เสร็จสิ้น! ระดับของคุณคือ: {level}")

# --- SECTION: บทเรียน & แบบทดสอบรายบท ---
elif menu == "📖 บทเรียน & ทดสอบ":
    st.header("📖 ระบบเรียนรู้แบบปรับเหมาะ")
    sid = st.text_input("รหัสประจำตัว:")
    
    if sid:
        user = pd.read_sql("SELECT * FROM students WHERE sid=?", conn, params=(sid,))
        if not user.empty:
            level = user.iloc[0]['level']
            st.write(f"สวัสดีคุณ **{user.iloc[0]['fname']}** | ระดับปัจจุบัน: `{level or 'ยังไม่ได้ทดสอบ'}`")
            
            chapter = st.selectbox("เลือกบทเรียน", list(LESSON_DATA.keys()))
            
            t_study, t_quiz = st.tabs(["📚 เนื้อหาบทเรียน", "✍️ แบบทดสอบหลังเรียน"])
            
            with t_study:
                st.subheader(chapter)
                # ปรับเนื้อหาตามระดับ
                if level == "Beginner (พื้นฐาน)":
                    st.warning("💡 ระบบเน้นเนื้อหาพื้นฐานและคำศัพท์สำคัญให้คุณ")
                st.write(LESSON_DATA[chapter]["content"])
                
            with t_quiz:
                st.subheader(f"Quiz: {chapter}")
                q_score = 0
                with st.form(f"quiz_{chapter}"):
                    for i, q in enumerate(LESSON_DATA[chapter]["quiz"]):
                        ans = st.radio(q['q'], q['a'], key=f"q_{chapter}_{i}")
                        if ans == q['c']: q_score += 1
                    
                    if st.form_submit_button("บันทึกคะแนน"):
                        final_p = (q_score / len(LESSON_DATA[chapter]["quiz"])) * 100
                        c = conn.cursor()
                        c.execute("INSERT INTO learning_logs (sid, chapter, post_p, timestamp) VALUES (?,?,?,?)",
                                  (sid, chapter, final_p, datetime.now()))
                        conn.commit()
                        st.balloons()
                        st.success(f"บันทึกคะแนนเรียบร้อย: {final_p}%")
        else:
            st.error("ไม่พบรหัสประจำตัวนี้ในระบบ")

# --- SECTION: ครู ---
elif menu == "📊 รายงานผล (ครู)":
    st.header("👨‍🏫 แผงควบคุมสำหรับคุณครู")
    pwd = st.text_input("รหัสผ่าน", type="password")
    if pwd == "admin123":
        st.subheader("รายชื่อและการแบ่งกลุ่ม")
        st.dataframe(pd.read_sql("SELECT sid, fname, level FROM students", conn), use_container_width=
