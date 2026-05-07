
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
import base64

# ==========================================
# 1. DATABASE CONFIGURATION (SQLite)
# ==========================================
def init_db():
    conn = sqlite3.connect('bio_adaptive.db', check_same_thread=False)
    c = conn.cursor()
    # Table นักเรียน
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (sid TEXT PRIMARY KEY, title TEXT, fname TEXT, lname TEXT,
                  grade_lvl TEXT, no INTEGER, phone TEXT, fb TEXT, line TEXT, img BLOB)''')
    # Table คะแนน
    c.execute('''CREATE TABLE IF NOT EXISTS learning_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, sid TEXT, chapter TEXT,
                  pre_p REAL, mid_p REAL, post_p REAL, progress REAL, grade TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    return conn

conn = init_db()

def get_grade_info(percent):
    if percent >= 80: return "4.0", "#8B00FF"
    elif percent >= 75: return "3.5", "#4B0082"
    elif percent >= 70: return "3.0", "#0000FF"
    elif percent >= 65: return "2.5", "#008000"
    elif percent >= 60: return "2.0", "#FFFF00"
    elif percent >= 55: return "1.5", "#FF8C00"
    elif percent >= 50: return "1.0", "#FF4500"
    else: return "0", "#FF0000"

# ==========================================
# 2. INTERFACE SETTING
# ==========================================
st.set_page_config(page_title="BioAdaptive Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background-color: #10B981; color: white; font-weight: bold; }
    .status-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 15px; border-left: 5px solid #10B981; }
    </style>
    """, unsafe_allow_html=True)

CURRICULUM = {
    "ม.4 เทอม 1": ["1. การศึกษาชีววิทยา", "2. เคมีที่เป็นพื้นฐานของสิ่งมีชีวิต", "3. เซลล์และการทำงานของเซลล์"],
    "ม.4 เทอม 2": ["4. โครโมโซมและสารพันธุกรรม", "5. การถ่ายทอดลักษณะทางพันธุกรรม", "6. เทคโนโลยีทางดีเอ็นเอ", "7. วิวัฒนาการ"],
    "ม.5 เทอม 1": ["8. การสืบพันธุ์ของพืชดอก", "9. โครงสร้างและหน้าที่ของพืชดอก", "10. การลำเลียงของพืช", "11. การสังเคราะห์ด้วยแสง", "12. การควบคุมการเจริญเติบโตของพืช"],
    "ม.5 เทอม 2": ["13. ระบบย่อยอาหาร", "14. ระบบหายใจ", "15. ระบบหมุนเวียนเลือดและน้ำเหลือง", "16. ระบบภูมิคุ้มกัน", "17. ระบบขับถ่าย"],
    "ม.6 เทอม 1": ["18. ระบบประสาทและอวัยวะรับความรู้สึก", "19. การเคลื่อนที่ของสิ่งมีชีวิต", "20. ระบบต่อมไร้ท่อ", "21. ระบบสืบพันธุ์และการเจริญเติบโต", "22. พฤติกรรมของสัตว์"],
    "ม.6 เทอม 2": ["23. ความหลากหลายทางชีวภาพ", "24. ระบบนิเวศและประชากร", "25. มนุษย์กับความยั่งยืนของทรัพยากร"]
}

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.title("🧬 BioAdaptive v2")
    st.info("ระบบเรียนรู้ชีววิทยาแบบปรับเหมาะ")
    menu = st.radio("เลือกโหมดการใช้งาน", ["🎓 นักเรียน (Student)", "👨‍🏫 คุณครู (Teacher Admin)"])

# ==========================================
# 4. STUDENT SECTION
# ==========================================
if menu == "🎓 นักเรียน (Student)":
    st.header("🎓 พื้นที่แห่งการเรียนรู้")
    t_reg, t_learn = st.tabs(["📝 ลงทะเบียน / แก้ไขข้อมูล", "📖 เข้าสู่บทเรียนและประเมินผล"])

    with t_reg:
        st.subheader("ข้อมูลส่วนตัว")
        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            sid = c1.text_input("รหัสประจำตัว*")
            title = c1.selectbox("คำนำหน้า", ["นาย", "นางสาว", "เด็กชาย", "เด็กหญิง"])
            fname = c1.text_input("ชื่อ")
            lname = c1.text_input("นามสกุล")
            
            grade_lvl = c2.selectbox("ชั้นมัธยมปีที่", ["ม.4", "ม.5", "ม.6"])
            no = c2.number_input("เลขที่", 1, 50, 1)
            phone = c2.text_input("เบอร์โทร")
            img_file = c2.file_uploader("อัปโหลดรูปโปรไฟล์", type=['jpg','png','jpeg'])

            st.write("--- 🔗 Social Contact")
            cx, cy = st.columns(2)
            fb = cx.text_input("Facebook")
            line = cy.text_input("Line ID")

            if st.form_submit_button("💾 บันทึกข้อมูลลงฐานข้อมูล"):
                if sid and fname:
                    img_data = img_file.read() if img_file else None
                    try:
                        c = conn.cursor()
                        c.execute("INSERT OR REPLACE INTO students VALUES (?,?,?,?,?,?,?,?,?,?)", 
                                  (sid, title, fname, lname, grade_lvl, int(no), phone, fb, line, img_data))
                        conn.commit()
                        st.success(f"บันทึกข้อมูลของ {fname} เรียบร้อยแล้ว!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else: st.warning("กรุณากรอก รหัส และ ชื่อ")

    with t_learn:
        login_id = st.text_input("ระบุรหัสประจำตัวเพื่อเข้าเรียน:", placeholder="Ex: 65001")
        if login_id:
            user_res = pd.read_sql(f"SELECT * FROM students WHERE sid='{login_id}'", conn)
            if not user_res.empty:
                student = user_res.iloc[0]
                st.markdown(f"""
                <div class='status-card'>
                    <h3>ยินดีต้อนรับคุณ {student['fname']} {student['lname']}</h3>
                    <p>ชั้น {student['grade_lvl']} เลขที่ {student['no']}</p>
                </div>
                """, unsafe_allow_html=True)

                col_learn, col_profile = st.columns([2, 1])
                
                with col_learn:
                    st.subheader("📚 เลือกบทเรียนที่ต้องการประเมิน")
                    grade_key = st.selectbox("เทอมการศึกษา", [k for k in CURRICULUM.keys() if student['grade_lvl'] in k])
                    chapter = st.selectbox("ชื่อบทเรียน", CURRICULUM[grade_key])
                    
                    with st.expander("✍️ บันทึกคะแนนสอบ", expanded=True):
                        s1, s2, s3 = st.columns(3)
                        pre = s1.number_input("Pre-test (%)", 0, 100, 0)
                        mid = s2.number_input("Mid-term (%)", 0, 100, 0)
                        post = s3.number_input("Post-test (%)", 0, 100, 0)
                        
                        if st.button("🚀 ส่งผลการประเมิน"):
                            grd, _ = get_grade_info(post)
                            progress = post - pre
                            c = conn.cursor()
                            c.execute("INSERT INTO learning_logs (sid, chapter, pre_p, mid_p, post_p, progress, grade, timestamp) VALUES (?,?,?,?,?,?,?,?)",
                                      (login_id, chapter, pre, mid, post, progress, grd, datetime.now()))
                            conn.commit()
                            st.balloons()
                            st.success(f"เกรดของคุณคือ: {grd}")

                with col_profile:
                    if student['img']:
                        st.image(student['img'], caption="โปรไฟล์ผู้เรียน", use_container_width=True)
                    
                    st.subheader("📊 ประวัติการเรียน")
                    logs = pd.read_sql(f"SELECT chapter, post_p, grade FROM learning_logs WHERE sid='{login_id}'", conn)
                    if not logs.empty:
                        st.dataframe(logs, hide_index=True)

# ==========================================
# 5. TEACHER SECTION
# ==========================================
elif menu == "👨‍🏫 คุณครู (Teacher Admin)":
    st.header("👨‍🏫 ระบบบริหารจัดการและวิเคราะห์ข้อมูล")
    pwd = st.text_input("Master Password", type="password")
    
    if pwd == "admin123":
        t_dash, t_manage = st.tabs(["📈 Dashboard & Analytics", "🗂 จัดการรายชื่อ"])
        
        with t_dash:
            st.subheader("ภาพรวมผลคะแนนทั้งห้อง")
            all_logs = pd.read_sql("SELECT * FROM learning_logs", conn)
            if not all_logs.empty:
                # วิเคราะห์คะแนนเฉลี่ยรายบท
                avg_scores = all_logs.groupby('chapter')[['pre_p', 'post_p']].mean().reset_index()
                fig = px.bar(avg_scores, x='chapter', y=['pre_p', 'post_p'], barmode='group', 
                             title="เปรียบเทียบคะแนน Pre vs Post รายบทเรียน")
                st.plotly_chart(fig, use_container_width=True)

                # แสดงตารางพร้อมข้อมูลเด็ก
                all_std = pd.read_sql("SELECT sid, fname, lname, no FROM students", conn)
                merged = pd.merge(all_logs, all_std, on='sid')
                st.write("รายละเอียดคะแนนรายบุคคล:")
                st.dataframe(merged[['no', 'fname', 'chapter', 'pre_p', 'post_p', 'progress', 'grade']], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลการสอบในระบบ")

        with t_manage:
            st.subheader("รายชื่อนักเรียนที่ลงทะเบียน")
            std_list = pd.read_sql("SELECT sid, title, fname, lname, grade_lvl, no, phone FROM students", conn)
            st.dataframe(std_list, use_container_width=True)
            
            if st.button("🗑 ล้างฐานข้อมูลทั้งหมด (อันตราย)"):
                c = conn.cursor()
                c.execute("DELETE FROM students")
                c.execute("DELETE FROM learning_logs")
                conn.commit()
                st.rerun()
    elif pwd:
        st.error("รหัสผ่านไม่ถูกต้อง")
