import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. SETTINGS & INTERFACE
# ==========================================
st.set_page_config(page_title="BioAdaptive System Pro", layout="wide")

# Custom CSS for a clean look
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { border-radius: 10px; height: 3em; }
    .report-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #11CAA0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA DICTIONARY & LOGIC
# ==========================================
CURRICULUM = {
    "ม.4 เทอม 1": ["1. การศึกษาชีววิทยา", "2. เคมีที่เป็นพื้นฐานของสิ่งมีชีวิต", "3. เซลล์และการทำงานของเซลล์"],
    "ม.4 เทอม 2": ["4. โครโมโซมและสารพันธุกรรม", "5. การถ่ายทอดลักษณะทางพันธุกรรม", "6. เทคโนโลยีทางดีเอ็นเอ", "7. วิวัฒนาการ"],
    "ม.5 เทอม 1": ["8. การสืบพันธุ์ของพืชดอก", "9. โครงสร้างและหน้าที่ของพืชดอก", "10. การลำเลียงของพืช", "11. การสังเคราะห์ด้วยแสง", "12. การควบคุมการเจริญเติบโตของพืช"],
    "ม.5 เทอม 2": ["13. ระบบย่อยอาหาร", "14. ระบบหายใจ", "15. ระบบหมุนเวียนเลือดและน้ำเหลือง", "16. ระบบภูมิคุ้มกัน", "17. ระบบขับถ่าย"],
    "ม.6 เทอม 1": ["18. ระบบประสาทและอวัยวะรับความรู้สึก", "19. การเคลื่อนที่ของสิ่งมีชีวิต", "20. ระบบต่อมไร้ท่อ", "21. ระบบสืบพันธุ์และการเจริญเติบโต", "22. พฤติกรรมของสัตว์"],
    "ม.6 เทอม 2": ["23. ความหลากหลายทางชีวภาพ", "24. ระบบนิเวศและประชากร", "25. มนุษย์กับความยั่งยืนของทรัพยากร"]
}

def get_grade_info(percent):
    if percent >= 80: return "4.0", "#8B00FF"
    elif percent >= 70: return "3.0", "#0000FF"
    elif percent >= 60: return "2.0", "#FFFF00"
    elif percent >= 50: return "1.0", "#FF4500"
    else: return "0", "#FF0000"

# ==========================================
# 3. INITIALIZING SESSION STATE
# ==========================================
if 'user_db' not in st.session_state:
    st.session_state.user_db = pd.DataFrame(columns=[
        "รหัสประจำตัว", "คำนำหน้า", "ชื่อ", "นามสกุล", "ชั้น", "เลขที่", "รูปถ่าย", "เบอร์โทร", "Facebook", "Line"
    ])

if 'learning_log' not in st.session_state:
    st.session_state.learning_log = pd.DataFrame(columns=[
        "รหัสประจำตัว", "บทเรียน", "Pre_Pct", "Mid_Pct", "Post_Pct", "พัฒนาการ", "ระดับ", "สี_Hex"
    ])

# State สำหรับการจัดการ Workflow ลงทะเบียน
if 'reg_stage' not in st.session_state:
    st.session_state.reg_stage = "fill"  # "fill" or "confirm"
if 'temp_user' not in st.session_state:
    st.session_state.temp_user = None

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧬 BioAdaptive")
menu = st.sidebar.selectbox("เมนูการใช้งาน", ["🎓 ส่วนของนักเรียน", "👨‍🏫 ส่วนของคุณครู"])

# ==========================================
# 5. STUDENT SECTION
# ==========================================
if menu == "🎓 ส่วนของนักเรียน":
    st.header("🎓 ระบบผู้เรียนชีววิทยา")
    t_reg, t_learn = st.tabs(["📝 ลงทะเบียน", "📖 เข้าสู่บทเรียน/โปรไฟล์"])

    with t_reg:
        if st.session_state.reg_stage == "fill":
            st.subheader("กรอกข้อมูลการลงทะเบียน")
            with st.form("reg_form"):
                c1, c2 = st.columns(2)
                with c1:
                    sid = st.text_input("รหัสประจำตัว*", placeholder="เช่น 67001")
                    title = st.selectbox("คำนำหน้า", ["นาย", "นางสาว", "เด็กชาย", "เด็กหญิง"])
                    fname = st.text_input("ชื่อ")
                    lname = st.text_input("นามสกุล")
                with c2:
                    grade_lvl = st.selectbox("ชั้น", ["ม.4", "ม.5", "ม.6"])
                    no = st.number_input("เลขที่", 1, 50, 1)
                    phone = st.text_input("เบอร์โทรศัพท์")
                    img = st.file_uploader("รูปถ่าย", type=['jpg', 'png', 'jpeg'])
                
                st.write("---")
                cx, cy = st.columns(2)
                fb = cx.text_input("Facebook Name")
                ln = cy.text_input("Line ID")
                
                if st.form_submit_button("🔍 ตรวจสอบข้อมูล"):
                    if sid and fname:
                        if sid in st.session_state.user_db["รหัสประจำตัว"].values:
                            st.error("รหัสนี้ถูกใช้งานแล้ว!")
                        else:
                            st.session_state.temp_user = {
                                "รหัสประจำตัว": sid, "คำนำหน้า": title, "ชื่อ": fname, "นามสกุล": lname,
                                "ชั้น": grade_lvl, "เลขที่": int(no), "รูปถ่าย": img.getvalue() if img else None,
                                "เบอร์โทร": phone, "Facebook": fb, "Line": ln
                            }
                            st.session_state.reg_stage = "confirm"
                            st.rerun()
                    else:
                        st.warning("กรุณากรอกข้อมูลสำคัญ (รหัสและชื่อ)")

        elif st.session_state.reg_stage == "confirm":
            st.subheader("ตรวจสอบความถูกต้อง")
            u = st.session_state.temp_user
            with st.container():
                st.markdown(f"""
                <div class="report-card">
                    <h3>ยืนยันข้อมูลโปรไฟล์</h3>
                    <p><b>ชื่อ-นามสกุล:</b> {u['คำนำหน้า']}{u['ชื่อ']} {u['นามสกุล']} (เลขที่ {u['เลขที่']})</p>
                    <p><b>ระดับชั้น:</b> {u['ชั้น']} | <b>รหัส:</b> {u['รหัสประจำตัว']}</p>
                    <p><b>การติดต่อ:</b> โทร {u['เบอร์โทร']} | FB: {u['Facebook']} | Line: {u['Line']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if u['รูปถ่าย']: st.image(u['รูปถ่าย'], width=150)

                b1, b2 = st.columns(2)
                if b1.button("✅ ยืนยันและบันทึกข้อมูล", use_container_width=True):
                    st.session_state.user_db = pd.concat([st.session_state.user_db, pd.DataFrame([u])], ignore_index=True)
                    st.success("ลงทะเบียนสำเร็จแล้ว!")
                    st.session_state.reg_stage
