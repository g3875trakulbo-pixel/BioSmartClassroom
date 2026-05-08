import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import string
from datetime import datetime

# --- 1. SETTINGS & UI THEME ---
st.set_page_config(page_title="BioSmartClassroom", page_icon="🌿", layout="wide")

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }
        .main { background-color: #ffffff; }
        .stSidebar { background-color: #f1f8e9; border-right: 1px solid #dcedc8; }
        /* สไตล์ปุ่ม */
        .stButton>button {
            width: 100%; border-radius: 12px; height: 3em;
            background-color: #2e7d32; color: white; border: none; transition: 0.3s;
        }
        .stButton>button:hover { background-color: #fdd835; color: #1b5e20; transform: scale(1.02); }
        /* การ์ดรายงานผล */
        .bio-card {
            background: white; padding: 25px; border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 6px solid #2e7d32;
            margin-bottom: 20px;
        }
        .metric-box { text-align: center; padding: 10px; background: #f9fbe7; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# --- 2. DATASET: 67 LESSONS STRUCTURE ---
# โครงสร้างบทเรียนครบทั้ง ม.4-ม.6 (ตัวอย่างโครงสร้างหลักที่สามารถเพิ่มเนื้อหาได้จนครบ)
curriculum_data = {
    "ม.4 ภาคเรียนที่ 1": {
        "1. การศึกษาชีววิทยา": ["1.1 ธรรมชาติของสิ่งมีชีวิต", "1.2 วิธีการทางวิทยาศาสตร์", "1.3 กิจกรรมสะเต็มศึกษา"],
        "2. เคมีพื้นฐาน": ["2.1 อะตอมและธาตุ", "2.2 น้ำ", "2.3 สารประกอบคาร์บอน", "2.4 ปฏิกิริยาเคมีในเซลล์"],
        "3. เซลล์ของสิ่งมีชีวิต": ["3.1 กล้องจุลทรรศน์", "3.2 โครงสร้างเซลล์", "3.3 การลำเลียงสาร", "3.4 การหายใจระดับเซลล์", "3.5 การแบ่งเซลล์"]
    },
    "ม.4 ภาคเรียนที่ 2": {
        "4. โครโมโซมและพันธุกรรม": ["4.1 โครโมโซม", "4.2 สารพันธุกรรม", "4.3 สมบัติสารพันธุกรรม", "4.4 มิวเทชัน"],
        "5. พันธุศาสตร์": ["5.1 เมนเดล", "5.2 ส่วนขยายเมนเดล", "5.3 ยีนบนโครโมโซมเดียวกัน"],
        "6. เทคโนโลยี DNA": ["6.1 พันธุวิศวกรรม", "6.2 การหาขนาด DNA", "6.3 การประยุกต์ใช้", "6.4 ชีวจริยธรรม"],
        "7. วิวัฒนาการ": ["7.1 หลักฐานวิวัฒนาการ", "7.2 แนวคิดวิวัฒนาการ", "7.3 พันธุศาสตร์ประชากร", "7.4 ปัจจัยการเปลี่ยนแปลง", "7.5 กำเนิดสปีชีส์"]
    },
    "ม.5 ภาคเรียนที่ 1": {
        "8. สืบพันธุ์พืชดอก": ["8.1 โครงสร้างดอก", "8.2 วัฏจักรชีวิต", "8.3 การสืบพันธุ์อาศัยเพศ", "8.4 การใช้ประโยชน์ผล/เมล็ด"],
        "9. การเจริญเติบโตพืช": ["9.1 เนื้อเยื่อพืช", "9.2 ราก", "9.3 ลำต้น", "9.4 ใบ"],
        "10. การลำเลียงพืช": ["10.1 ลำเลียงน้ำ", "10.2 คายน้ำ", "10.3 ลำเลียงธาตุ", "10.4 ลำเลียงอาหาร"],
        "11. สังเคราะห์แสง": ["11.1 การศึกษา", "11.2 กระบวนการ", "11.3 โฟโตเรสไพเรชัน", "11.4 การเพิ่มคาร์บอน", "11.5 ปัจจัยที่มีผล"],
        "12. การควบคุมพืช": ["12.1 ฮอร์โมนพืช", "12.2 การงอก", "12.3 การตอบสนอง", "12.4 สภาวะเครียด"]
    },
    "ม.5 ภาคเรียนที่ 2": {
        "13. ระบบย่อยอาหาร": ["13.1 การย่อยของสัตว์", "13.2 การย่อยของมนุษย์"],
        "14. ระบบหายใจ": ["14.1 การแลกแก๊สสัตว์", "14.2 โครงสร้างมนุษย์", "14.3 การลำเลียงแก๊ส", "14.4 การหายใจ"],
        "15. ระบบหมุนเวียนเลือด": ["15.1 การลำเลียงสารสัตว์", "15.2 การลำเลียงสารมนุษย์", "15.3 ระบบน้ำเหลือง"],
        "16. ระบบภูมิคุ้มกัน": ["16.1 กลไกป้องกัน", "16.2 การเสริมภูมิ", "16.3 ความผิดปกติ"],
        "17. ระบบขับถ่าย": ["17.1 ขับถ่ายสัตว์", "17.2 ขับถ่ายมนุษย์", "17.3 หน่วยไต", "17.4 การรักษาดุลยภาพน้ำ", "17.5 ความผิดปกติ"]
    },
    "ม.6 ภาคเรียนที่ 1": {
        "18. ระบบประสาท": ["18.1 การรับรู้สัตว์", "18.2 เซลล์ประสาท", "18.3 ศูนย์ควบคุมมนุษย์", "18.4 การทำงานประสาท", "18.5 อวัยวะรับความรู้สึก"],
        "19. การเคลื่อนที่": ["19.1 เซลล์เดียว", "19.2 สัตว์ไม่มีกระดูก", "19.3 สัตว์มีกระดูก", "19.4 มนุษย์"],
        "20. ระบบต่อมไร้ท่อ": ["20.1 การทำงานร่วมประสาท", "20.2 ต่อมไร้ท่อ", "20.3 ฮอร์โมน", "20.4 สมดุลฮอร์โมน"],
        "21. ระบบสืบพันธุ์": ["21.1 สัตว์", "21.2 มนุษย์", "21.3 การเจริญเติบโต"],
        "22. พฤติกรรมสัตว์": ["22.1 การศึกษา", "22.2 กลไก", "22.3 ประเภทพฤติกรรม", "22.4 ความสัมพันธ์ประสาท", "22.5 การสื่อสาร"]
    },
    "ม.6 ภาคเรียนที่ 2": {
        "23. ความหลากหลาย": ["23.1 ความหลากหลายชีวภาพ", "23.2 ความหลากหลายสิ่งมีชีวิต", "23.3 การศึกษา"],
        "24. ระบบนิเวศ": ["24.1 ระบบนิเวศ", "24.2 ไบโอม", "24.3 การเปลี่ยนแปลงแทนที่", "24.4 ประชากร"],
        "25. ทรัพยากรยั่งยืน": ["25.1 ประเภททรัพยากร", "25.2 การจัดการปัญหา", "25.3 การอนุรักษ์เพื่อความยั่งยืน"]
    }
}

# --- 3. HELPER FUNCTIONS ---
def get_ai_level(pct):
    if pct >= 80: return "ระดับสูง (Advanced)", "🟢", "ให้เน้นภารกิจวิเคราะห์ขั้นสูงและโครงงานเชิงนวัตกรรม"
    elif pct >= 50: return "ระดับกลาง (Intermediate)", "🟡", "ให้เน้นภารกิจการแก้ปัญหาและการอธิบายความสัมพันธ์"
    else: return "ระดับพื้นฐาน (Basic)", "🟠", "ให้เน้นภารกิจการสรุปมโนทัศน์สำคัญและสื่อภาพจำลองพื้นฐาน"

def generate_unique_code():
    return f"BIO-{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}"

# --- 4. SIDEBAR (AUTO-COLLAPSE ON MOBILE) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=120)
    st.title("BioSmart System")
    user_role = st.selectbox("สถานะผู้ใช้งาน", ["นักเรียน (User)", "คุณครู (Admin)"])
    st.divider()
    
    if user_role == "นักเรียน (User)":
        menu = st.radio("เมนูหลัก", ["หน้าแรก", "ลงทะเบียน", "เข้าห้องเรียน 5E", "แดชบอร์ดผลการเรียน"])
    else:
        menu = st.radio("เมนูครู", ["แผงควบคุมรายชั้น", "ฐานข้อมูล Google Sheets", "พิมพ์รายงานสรุปผล"])

# --- 5. PAGE LOGIC ---

# -- หน้าแรก --
if menu == "หน้าแรก":
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.image("https://via.placeholder.com/400x500.png?text=Biology+Teacher", caption="ครูผู้เชี่ยวชาญด้านนวัตกรรมชีววิทยา")
    with col2:
        st.title("🌿 BioSmartClassroom")
        st.subheader("ห้องเรียนออนไลน์อัจฉริยะวิชาชีววิทยา")
        st.markdown("""
        ยินดีต้อนรับสู่ระบบการเรียนรู้ยุคใหม่ที่ออกแบบมาเพื่อนักเรียนระดับมัธยมศึกษาตอนปลาย (ม.4-ม.6) 
        โดยใช้ระบบวิเคราะห์ AI เพื่อปรับเนื้อหาให้เหมาะสมกับความรู้พื้นฐานของนักเรียนแต่ละบุคคล
        
        **สถิติการเรียนรู้ที่ได้รับ:**
        * 📊 ผลการวิเคราะห์ก่อนเรียน - ระหว่างเรียน - หลังเรียน (หน่วยร้อยละ %)
        * 🧬 บทเรียนแบบ Active Learning 5E ครบ 67 หัวข้อ
        * 📝 ภาระงานแบ่งตามความสามารถ 3 ระดับ
        """)
        st.info("💡 เริ่มต้นใช้งานโดยการลงทะเบียนเพื่อรับ Access Code ประจำตัว")

# -- หน้าลงทะเบียน --
elif menu == "ลงทะเบียน":
    st.header("📝 ลงทะเบียนนักเรียนใหม่")
    with st.form("reg_form"):
        c1, c2 = st.columns(2)
        with c1:
            title = st.selectbox("คำนำหน้า", ["นาย", "นางสาว", "เด็กชาย", "เด็กหญิง"])
            fname = st.text_input("ชื่อ")
            lname = st.text_input("นามสกุล")
            level = st.selectbox("ระดับชั้น", ["ม.4", "ม.5", "ม.6"])
            room = st.text_input("ห้อง")
            no = st.number_input("เลขที่", min_value=1)
        with c2:
            contact_line = st.text_input("Line ID")
            contact_fb = st.text_input("Facebook")
            photo = st.file_uploader("อัปโหลดภาพนักเรียน")
        
        btn_check = st.form_submit_button("ตรวจสอบข้อมูล")

    if btn_check:
        st.markdown('<div class="bio-card">', unsafe_allow_html=True)
        st.subheader("🔍 ตรวจสอบข้อมูลก่อนบันทึก")
        st.write(f"ชื่อ-สกุล: {title}{fname} {lname} | ชั้น: {level}/{room} เลขที่: {no}")
        st.write(f"ช่องทางติดต่อ: Line: {contact_line} | FB: {contact_fb}")
        
        if st.button("ยืนยันการบันทึกข้อมูล (ลง Google Sheet)"):
            new_code = generate_unique_code()
            st.balloons()
            st.success(f"บันทึกสำเร็จ! รหัสเข้าเรียนของคุณคือ: **{new_code}**")
            st.warning("โปรดจดบันทึกรหัสนี้ไว้เพื่อใช้แสดงตัวตนในระบบ")
        st.markdown('</div>', unsafe_allow_html=True)

# -- หน้าเข้าบทเรียน --
elif menu == "เข้าห้องเรียน 5E":
    st.header("🧬 ระบบการเรียนรู้อัจฉริยะรายบุคคล")
    access_input = st.text_input("กรอกรหัสเข้าเรียน (Access Code):", placeholder="เช่น BIO-A123")
    
    if access_input:
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            term_sel = st.selectbox("เลือกชั้น/ภาคเรียน", list(curriculum_data.keys()))
        with c2:
            topic_main = st.selectbox("เลือกบทหลัก", list(curriculum_data[term_sel].keys()))
            
        topic_sub = st.selectbox("เลือกหัวเรื่องย่อย (จาก 67 บทเรียน)", curriculum_data[term_sel][topic_main])
        
        st.markdown(f"### 📍 บทเรียน: {topic_sub}")
        
        # ส่วนวิเคราะห์ก่อนเรียน
        st.markdown('<div class="bio-card">', unsafe_allow_html=True)
        st.subheader("📝 ขั้นที่ 1: แบบทดสอบวิเคราะห์ก่อนเรียน (Pre-test)")
        raw_pre = st.slider("จำลองคะแนนก่อนเรียน (เต็ม 10)", 0, 10)
        pre_pct = (raw_pre / 10) * 100
        
        if st.button("ประมวลผล AI"):
            level_name, color, ai_note = get_ai_level(pre_pct)
            st.session_state['bio_level'] = level_name
            st.markdown(f"**AI วิเคราะห์ผล:** {color} {level_name} (พื้นฐานร้อยละ {pre_pct:.2f}%)")
            st.info(f"💡 คำแนะนำสำหรับคุณ: {ai_note}")
        st.markdown('</div>', unsafe_allow_html=True)

        if 'bio_level' in st.session_state:
            st.write("---")
            st.subheader("💡 บทเรียนแบบ 5E และภารกิจประจำกลุ่ม")
            tabs = st.tabs(["E1: Engage", "E2: Explore", "E3: Explain", "E4: Elaborate", "E5: Evaluate"])
            
            with tabs[1]:
                st.write(f"**ภาระงานระดับ {st.session_state['bio_level']}:**")
                st.write("ให้นักเรียนทำใบงานและบันทึกผลการเรียนรู้ลงในระบบ")
                st.button(f"📥 ดาวน์โหลดใบงาน/แบบบันทึกกิจกรรม (ระดับ {st.session_state['bio_level']})")
                work_score = st.slider("คะแนนใบงาน/ระหว่างเรียน (เต็ม 10)", 0, 10)
                st.write(f"คะแนนใบงาน: **ร้อยละ {(work_score/10)*100:.2f}**")
            
            with tabs[4]:
                st.write("**แบบทดสอบหลังเรียน (Post-test):**")
                raw_post = st.number_input("กรอกคะแนนหลังเรียนที่ได้:", 0, 10)
                if st.button("บันทึกคะแนนรวมลง Google Sheet"):
                    st.success(f"บันทึกร้อยละ {(raw_post/10)*100:.2f}% ลงฐานข้อมูลแล้ว")

# -- หน้าแดชบอร์ด --
elif menu == "แดชบอร์ดผลการเรียน":
    st.header("📊 สรุปรายงานผลการเรียนอัจฉริยะ")
    st.write("นักเรียน: **นายสมชาย เรียนดี** | รหัส: **BIO-X452**")
    
    # คำนวณร้อยละจำลอง
    perf_data = pd.DataFrame({
        'ช่วงการวัด': ['ก่อนเรียน', 'ใบงาน/ระหว่างเรียน', 'หลังเรียน'],
        'คะแนนร้อยละ (%)': [30.0, 75.0, 95.0]
    })
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig = px.bar(perf_data, x='ช่วงการวัด', y='คะแนนร้อยละ (%)', 
                     color='ช่วงการวัด', color_discrete_sequence=px.colors.qualitative.Prism,
                     text='คะแนนร้อยละ (%)', range_y=[0, 105])
        st.plotly_chart(fig, use_container_width=True)
        
    with col_b:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.write("พัฒนาการ")
        st.title("+65%")
        st.write("เทียบจากก่อนเรียน")
        st.markdown('</div>', unsafe_allow_html=True)
        st.button("🖨️ พิมพ์รายงานผลรายบุคคล (Print)")

elif menu == "แผงควบคุมรายชั้น":
    st.header("👨‍🏫 แดชบอร์ดวิเคราะห์สถิติสำหรับครู")
    grade_sel = st.selectbox("เลือกชั้นเรียน:", ["ม.4/1", "ม.4/2", "ม.5/1", "ม.6/1"])
    topic_sel = st.selectbox("เลือกหัวข้อบทเรียน:", ["1.1 ธรรมชาติของสิ่งมีชีวิต", "1.2 วิธีการทางวิทยาศาสตร์"])
    
    # จำลองตารางข้อมูลครู
    df_admin = pd.DataFrame({
        'เลขที่': [1, 2, 3, 4],
        'ชื่อ-สกุล': ['สมชาย รักดี', 'สมหญิง มานะ', 'มานะ อดทน', 'ปิติ ชูใจ'],
        'ก่อนเรียน (%)': [30, 60, 40, 50],
        'ระหว่างเรียน (%)': [75, 85, 70, 80],
        'หลังเรียน (%)': [95, 98, 85, 90]
    })
    st.dataframe(df_admin, use_container_width=True)
    st.button("📂 Export ข้อมูลร้อยละไป Google Sheets")
