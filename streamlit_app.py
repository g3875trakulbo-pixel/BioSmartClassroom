import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. การตั้งค่าหน้าจอและ Theme (Interface Tuning)
# ==========================================
st.set_page_config(page_title="BioAdaptive System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F0F2F6; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #11CAA0; color: white; }
    .stExpander { background-color: white; border-radius: 10px; border: 1px solid #ddd; }
    .report-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #005088; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. ฐานข้อมูลบทเรียน (Curriculum Data)
# ==========================================
CURRICULUM = {
    "ม.4 เทอม 1": ["1. การศึกษาชีววิทยา", "2. เคมีที่เป็นพื้นฐานของสิ่งมีชีวิต", "3. เซลล์และการทำงานของเซลล์"],
    "ม.4 เทอม 2": ["4. โครโมโซมและสารพันธุกรรม", "5. การถ่ายทอดลักษณะทางพันธุกรรม", "6. เทคโนโลยีทางดีเอ็นเอ", "7. วิวัฒนาการ"],
    "ม.5 เทอม 1": ["8. การสืบพันธุ์ของพืชดอก", "9. โครงสร้างและหน้าที่ของพืชดอก", "10. การลำเลียงของพืช", "11. การสังเคราะห์ด้วยแสง", "12. การควบคุมการเจริญเติบโตของพืช"],
    "ม.5 เทอม 2": ["13. ระบบย่อยอาหาร", "14. ระบบหายใจ", "15. ระบบหมุนเวียนเลือดและน้ำเหลือง", "16. ระบบภูมิคุ้มกัน", "17. ระบบขับถ่าย"],
    "ม.6 เทอม 1": ["18. ระบบประสาทและอวัยวะรับความรู้สึก", "19. การเคลื่อนที่ของสิ่งมีชีวิต", "20. ระบบต่อมไร้ท่อ", "21. ระบบสืบพันธุ์และการเจริญเติบโต", "22. พฤติกรรมของสัตว์"],
    "ม.6 เทอม 2": ["23. ความหลากหลายทางชีวภาพ", "24. ระบบนิเวศและประชากร", "25. มนุษย์กับความยั่งยืนของทรัพยากร"]
}

# ==========================================
# 3. INITIAL DATABASE SETUP
# ==========================================
if 'user_db' not in st.session_state:
    st.session_state.user_db = pd.DataFrame(columns=[
        "รหัสประจำตัว", "คำนำหน้า", "ชื่อ", "นามสกุล", "ชั้น", "เลขที่", "รูปถ่าย", "เบอร์โทร", "Facebook", "Line"
    ])

if 'learning_log' not in st.session_state:
    st.session_state.learning_log = pd.DataFrame(columns=[
        "รหัสประจำตัว", "บทเรียน", "Pre_Pct", "Mid_Pct", "Post_Pct", "พัฒนาการ", "ระดับ", "สี_Hex"
    ])

def get_grade_info(percent):
    if percent >= 80: return "4.0", "ม่วง", "#8B00FF"
    elif percent >= 75: return "3.5", "คราม", "#4B0082"
    elif percent >= 70: return "3.0", "น้ำเงิน", "#0000FF"
    elif percent >= 65: return "2.5", "เขียว", "#008000"
    elif percent >= 60: return "2.0", "เหลือง", "#FFFF00"
    elif percent >= 55: return "1.5", "แสด", "#FF8C00"
    elif percent >= 50: return "1.0", "แสด(ส้ม)", "#FF4500"
    else: return "0", "แดง", "#FF0000"

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧬 BioAdaptive System")
menu = st.sidebar.radio("เมนูการใช้งาน", ["🎓 ส่วนของนักเรียน", "👨‍🏫 ส่วนของคุณครู"])

# ==========================================
# 5. STUDENT SECTION
# ==========================================
if menu == "🎓 ส่วนของนักเรียน":
    st.header("🎓 ส่วนของผู้เรียน")
    t_reg, t_learn = st.tabs(["📝 ลงทะเบียน", "📖 เข้าสู่บทเรียน/โปรไฟล์"])

    with t_reg:
        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            with c1:
                sid = st.text_input("รหัสประจำตัว*")
                title = st.selectbox("คำนำหน้า", ["นาย", "นางสาว", "เด็กชาย", "เด็กหญิง"])
                fname = st.text_input("ชื่อ")
                lname = st.text_input("นามสกุล")
            with c2:
                grade_lvl = st.selectbox("ชั้น", ["ม.4", "ม.5", "ม.6"])
                no = st.number_input("เลขที่", 1, 50, 1)
                phone = st.text_input("เบอร์โทรศัพท์")
                img = st.file_uploader("รูปถ่าย", type=['jpg', 'png', 'jpeg'])
            
            st.write("---")
            st.write("🔗 **ข้อมูลติดต่อโซเชียล**")
            cx, cy = st.columns(2)
            fb = cx.text_input("Facebook")
            line = cy.text_input("Line ID")
            
            if st.form_submit_button("✅ บันทึกโปรไฟล์"):
                if sid and fname:
                    img_data = img.getvalue() if img else None
                    new_user = {
                        "รหัสประจำตัว": sid, "คำนำหน้า": title, "ชื่อ": fname, "นามสกุล": lname,
                        "ชั้น": grade_lvl, "เลขที่": int(no), "รูปถ่าย": img_data,
                        "เบอร์โทร": phone, "Facebook": fb, "Line": line
                    }
                    st.session_state.user_db = pd.concat([st.session_state.user_db, pd.DataFrame([new_user])], ignore_index=True)
                    st.success("บันทึกข้อมูลเรียบร้อย!")
                else: st.error("กรุณากรอกรหัสและชื่อ")

        # ส่วนตรวจสอบข้อมูลตอนท้าย
        if not st.session_state.user_db.empty:
            st.markdown("### 🔍 ตรวจสอบข้อมูลโปรไฟล์ล่าสุด")
            latest = st.session_state.user_db.iloc[-1]
            with st.expander("คลิกเพื่อดูรายละเอียดโปรไฟล์ของคุณ", expanded=True):
                col_img, col_info = st.columns([1, 2])
                with col_img:
                    if latest["รูปถ่าย"]: st.image(latest["รูปถ่าย"], use_container_width=True)
                with col_info:
                    st.write(f"**ชื่อ-นามสกุล:** {latest['ชื่อ']} {latest['นามสกุล']}")
                    st.write(f"**ชั้น:** {latest['ชั้น']} | **เลขที่:** {latest['เลขที่']}")
                    st.write(f"**รหัส:** {latest['รหัสประจำตัว']}")
                    st.write(f"**FB:** {latest['Facebook']} | **Line:** {latest['Line']}")

    with t_learn:
        login_id = st.text_input("Login ด้วยรหัสประจำตัว:")
        if login_id:
            user_data = st.session_state.user_db[st.session_state.user_db["รหัสประจำตัว"] == login_id]
            if not user_data.empty:
                student = user_data.iloc[0]
                st.info(f"ยินดีต้อนรับ: {student['ชื่อ']} (ชั้น {student['ชั้น']})")
                
                # --- การเลือกระดับและบทเรียนตามภาพ ---
                grade_select = st.selectbox("เลือกชั้นปีและเทอม:", [k for k in CURRICULUM.keys() if student['ชั้น'] in k])
                chapter_select = st.selectbox("เลือกบทเรียน:", CURRICULUM[grade_select])
                
                st.write("---")
                st.subheader("📊 กรอกคะแนนสอบ (%)")
                sc1, sc2, sc3 = st.columns(3)
                pre_p = sc1.number_input("คะแนนก่อนเรียน (%)", 0, 100, 0)
                mid_p = sc2.number_input("คะแนนระหว่างเรียน (%)", 0, 100, 0)
                post_p = sc3.number_input("คะแนนหลังเรียน (%)", 0, 100, 0)
                
                if st.button("🚀 ส่งคะแนนและประมวลผล"):
                    grd, col_name, hex_code = get_grade_info(post_p)
                    new_log = {
                        "รหัสประจำตัว": login_id, "บทเรียน": chapter_select, 
                        "Pre_Pct": pre_p, "Mid_Pct": mid_p, "Post_Pct": post_p, 
                        "พัฒนาการ": post_p - pre_p, "ระดับ": grd, "สี_Hex": hex_code
                    }
                    st.session_state.learning_log = pd.concat([st.session_state.learning_log, pd.DataFrame([new_log])], ignore_index=True)
                    st.success(f"บันทึกสำเร็จ! คุณอยู่ใน ระดับ {grd}")

                # ส่วนแสดงผลลัพธ์รายบุคคล
                st.markdown("### 🏆 ผลการเรียนและโปรไฟล์ของคุณ")
                scores = st.session_state.learning_log[st.session_state.learning_log["รหัสประจำตัว"] == login_id]
                if not scores.empty:
                    st.table(scores[["บทเรียน", "Pre_Pct", "Post_Pct", "พัฒนาการ", "ระดับ"]])
            else: st.error("ไม่พบรหัสประจำตัว")

# ==========================================
# 6. TEACHER SECTION
# ==========================================
elif menu == "👨‍🏫 ส่วนของคุณครู":
    st.header("👨‍🏫 ระบบจัดการสำหรับครู")
    if st.text_input("รหัสผ่าน Admin", type="password") == "admin123":
        t_all, t_chap = st.tabs(["👥 รายชื่อนักเรียนทั้งหมด", "📚 รายงานแยกบทเรียน"])
        
        with t_all:
            if not st.session_state.user_db.empty:
                st.dataframe(st.session_state.user_db.drop(columns=["รูปถ่าย"]), use_container_width=True)
            else: st.info("ยังไม่มีข้อมูลนักเรียน")

        with t_chap:
            all_chap_list = []
            for v in CURRICULUM.values(): all_chap_list.extend(v)
            sel_chap = st.selectbox("เลือกบทเรียนเพื่อดูคะแนนทั้งห้อง:", list(set(all_chap_list)))
            
            ch_data = st.session_state.learning_log[st.session_state.learning_log["บทเรียน"] == sel_chap]
            if not ch_data.empty:
                full_view = pd.merge(ch_data, st.session_state.user_db, on="รหัสประจำตัว")
                st.table(full_view[["เลขที่", "ชื่อ", "นามสกุล", "Pre_Pct", "Post_Pct", "พัฒนาการ", "ระดับ"]])
            else: st.info("ยังไม่มีข้อมูลในบทนี้")
