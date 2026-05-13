import streamlit as st

# 1. การตั้งค่าหน้าเว็บและธีม
st.set_page_config(page_title="BioSmartClassroom - Profile", layout="wide", page_icon="🐸")

# 2. Custom CSS เพื่อคุมธีม เขียว-ขาว และเส้นประตามภาพร่าง
st.markdown("""
    <style>
    /* พื้นหลังหลัก */
    .stApp { background-color: #F8FFF8; }
    
    /* สไตล์ Sidebar สีเขียว */
    [data-testid="stSidebar"] {
        background-color: #E0EEDC;
        border-right: 3px solid #7CB342;
    }
    
    /* กล่องเนื้อหาหลัก ขอบมน สีขาว ขอบเขียว */
    .main-box {
        background-color: white;
        border: 2px solid #8BC34A;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* กล่องแสดงรหัส BIO-ID (สีแดงตามภาพร่าง) */
    .id-display {
        background-color: #FFFFFF;
        border: 2px solid #D32F2F;
        border-radius: 10px;
        color: #D32F2F;
        font-weight: bold;
        padding: 15px;
        text-align: center;
        font-size: 28px;
        margin-top: 10px;
    }
    
    /* หัวข้อสีเขียวเข้ม */
    h1, h2, h3 { color: #33691E; font-family: 'Sarabun', sans-serif; }
    
    /* ปรับแต่งปุ่ม */
    .stButton>button {
        background-color: #689F38;
        color: white;
        border-radius: 10px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ส่วนหัว (Header) พร้อมมาสคอต ---
col_h1, col_h2, col_h3 = st.columns([1, 4, 1])
with col_h1:
    st.image("https://img.freepik.com/free-vector/tree-frog-cartoon-style_1308-111132.jpg", width=120) # รูปกบต้นไม้
with col_h2:
    st.markdown("<h1 style='text-align: center;'>ห้องเรียนชีววิทยาออนไลน์<br>BioSmartClassroom</h1>", unsafe_allow_html=True)
with col_h3:
    st.image("https://img.freepik.com/free-vector/chameleon-cartoon-style_1308-111467.jpg", width=130) # รูปคาเมเลี่ยน

# --- 4. Sidebar (เมนูและคำแนะนำ) ---
with st.sidebar:
    st.button("🏠 กลับหน้าแรก")
    st.markdown("---")
    st.markdown("### 🟢 ประวัติการเข้าเรียน")
    st.info("""
    - ให้นักเรียนใส่ข้อมูลให้ครบถ้วน
    - ตรวจสอบข้อมูลแล้วบันทึกก่อนเข้าห้องเรียน
    - จดจำรหัสเข้าห้องเรียน (BIO-ID)
    """)

# --- 5. ส่วนลงทะเบียน (User Registration) ---
st.markdown("<h2 style='text-align: center; background-color: #DCEDC8; padding: 10px; border-radius: 15px;'>ส่วนของนักเรียน (User)</h2>", unsafe_allow_html=True)

col_img, col_info = st.columns([1, 2])

with col_img:
    st.markdown('<div class="main-box" style="text-align: center; height: 380px;">', unsafe_allow_html=True)
    st.write("**อัปโหลดรูปภาพนักเรียน**")
    uploaded_photo = st.file_uploader("เลือกไฟล์ภาพ...", type=['jpg', 'png', 'jpeg'])
    if uploaded_photo:
        st.image(uploaded_photo, width=180)
    else:
        st.markdown("<div style='height: 180px; border: 2px dashed #A5D6A7; border-radius: 10px; margin-top: 20px; padding-top: 70px; color: #888;'>พื้นที่แสดงรูปภาพ</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_info:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.write("**ข้อมูลนักเรียน**")
    std_id = st.text_input("เลขประจำตัวนักเรียน", placeholder="เช่น 12345")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        title = st.selectbox("คำนำหน้า", ["นาย", "นางสาว", "เด็กชาย", "เด็กหญิง"])
    with c2:
        fname = st.text_input("ชื่อนักเรียน")
    
    lname = st.text_input("นามสกุล")
    
    c3, c4, c5 = st.columns(3)
    with c3: grade = st.text_input("ชั้น ม.")
    with c4: room = st.text_input("ห้อง")
    with c5: no = st.text_input("เลขที่")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. ส่วนแสดงผลโปรไฟล์ (Profile Preview) ---
st.markdown("### 👤 ข้อมูลนักเรียน (Profile)")
st.markdown('<div class="main-box">', unsafe_allow_html=True)
cp1, cp2 = st.columns([1, 3])
with cp1:
    st.markdown("<div style='border: 1px solid #ddd; height: 150px; border-radius: 10px; display: flex; align-items: center; justify-content: center;'>ภาพนักเรียน</div>", unsafe_allow_html=True)
with cp2:
    st.write(f"**เลขประจำตัวนักเรียน:** {std_id if std_id else '..........'}")
    st.write(f"**ชื่อ-นามสกุล:** {title}{fname} {lname}")
    st.write(f"**ชั้นมัธยมศึกษาปีที่:** {grade if grade else '..'} **ห้อง:** {room if room else '..'} **เลขที่:** {no if no else '..'}")
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. ปุ่มยืนยันและรหัสเข้าห้องเรียน ---
if st.button("✅ ตรวจสอบ / บันทึกข้อมูล / รับรหัสเข้าห้องเรียน"):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    st.write("รหัสของคุณคือ :")
    # สร้างรหัส BIO-ID ตามรูปแบบในภาพร่าง
    generated_id = f"BIO-41-41-2569-{std_id if std_id else 'XXXXX'}"
    st.markdown(f'<div class="id-display">{generated_id}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# มาสคอตนักเรียน (มุมขวาล่าง)
_, col_m = st.columns([4, 1])
with col_m:
    st.image("https://img.freepik.com/free-vector/student-character-design_23-2148488349.jpg", width=130)
