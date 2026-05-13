import streamlit as st

# 1. ตั้งค่าหน้าเว็บและ Favicon
st.set_page_config(
    page_title="BioSmartClassroom",
    layout="wide",
    page_icon="🐸"
)

# 2. Custom CSS เพื่อคุมธีม เขียว-ขาว และใส่ Mascot ตามจุดต่างๆ
st.markdown("""
    <style>
    /* พื้นหลังหลักธีมขาว-เขียวอ่อน */
    .stApp {
        background-color: #F8FFF8;
    }
    
    /* สไตล์ Sidebar สีเขียวตามภาพต้นฉบับ */
    [data-testid="stSidebar"] {
        background-color: #E0EEDC;
        border-right: 3px solid #7CB342;
    }
    
    /* กล่องเนื้อหา ขอบมน สีขาว ขอบเขียว */
    .main-container {
        background-color: white;
        border: 2px solid #8BC34A;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* ตกแต่งหัวข้อ */
    h1, h2, h3 {
        color: #33691E;
        font-family: 'Sarabun', sans-serif;
    }
    
    /* เส้นประในส่วน News */
    .news-line {
        border-bottom: 1px dashed #9E9E9E;
        margin: 5px 0;
        height: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ส่วน Header (กบต้นไม้ + ชื่อระบบ + คาเมเลี่ยน) ---
col_h1, col_h2, col_h3 = st.columns([1, 4, 1])
with col_h1:
    st.image("https://img.freepik.com/free-vector/tree-frog-cartoon-style_1308-111132.jpg", width=120) # รูปกบต้นไม้
with col_h2:
    st.markdown("<h1 style='text-align: center;'>ห้องเรียนชีววิทยาออนไลน์<br>BioSmartClassroom</h1>", unsafe_allow_html=True)
with col_h3:
    st.image("https://img.freepik.com/free-vector/chameleon-cartoon-style_1308-111467.jpg", width=120) # รูปคาเมเลี่ยน

# --- 4. Sidebar (เมนู และ ข่าวสาร) ---
with st.sidebar:
    st.markdown("### 🟢 เมนู (Menu)")
    user_role = st.radio("", ["ส่วนของนักเรียน (User)", "ส่วนของคุณครู (Admin)"])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📰 ข่าวสาร (News)")
    with st.container():
        st.write("BioSmartClassroom")
        st.write("เวอร์ชัน 1.10.05.26")
        for _ in range(5): # เส้นประตามแบบ
            st.markdown('<div class="news-line"></div>', unsafe_allow_html=True)
        st.write("วันที่พัฒนา: 10.05.2026")
        st.write("ผู้พัฒนา: นายตระกูล บุญชิต")

# --- 5. พื้นที่เนื้อหาหลัก (Manual & Activities) ---
col_main1, col_main2 = st.columns([1.2, 1])

with col_main1:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📗 คู่มือการใช้ (Manual)")
    st.info("""**คำแนะนำ:** นวัตกรรมการเรียนรู้แบบ Differential Instruction โดยใช้ AI ช่วยออกแบบ""")
    st.write("วิธีใช้งาน: เลือกส่วนที่เกี่ยวข้องจากเมนูด้านข้าง แล้วปฏิบัติตามคำแนะนำ")
    st.markdown('</div>', unsafe_allow_html=True)

with col_main2:
    st.markdown('<div class="main-container" style="min-height: 400px;">', unsafe_allow_html=True)
    st.subheader("🖼️ ภาพกิจกรรมและผลงาน")
    st.write("พื้นที่แสดงผลงานนักเรียน...")
    
    # วางรูปครูและนักเรียนที่มุมขวาล่างของกล่องกิจกรรม
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c2:
        st.image("https://img.freepik.com/free-vector/teacher-and-student-concept_23-2148522365.jpg", caption="ครูและนักเรียน")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. ส่วนเนื้อหาบทเรียน ---
if user_role == "ส่วนของนักเรียน (User)":
    st.divider()
    st.header("🧬 เริ่มต้นการเรียนรู้")
    tabs = st.tabs(["5E Learning", "แบบทดสอบ", "สะสมผลงาน"])
    with tabs[0]:
        st.success("ยินดีต้อนรับเข้าสู่บทเรียนชีววิทยา! เลือกหัวข้อที่ AI แนะนำด้านล่าง")
