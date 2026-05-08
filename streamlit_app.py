import streamlit as st
import pandas as pd
import random
import string
from datetime import datetime

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="BioSmartClassroom", page_icon="🌿", layout="wide")

def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }
        .main { background-color: #ffffff; }
        .stButton>button { 
            width: 100%; background-color: #2e7d32; color: white; 
            border-radius: 10px; border: none; height: 3em;
        }
        .stButton>button:hover { background-color: #fdd835; color: black; border: 2px solid #2e7d32; }
        .sidebar .sidebar-content { background-color: #f1f8e9; }
        .card { 
            padding: 20px; border-radius: 15px; background: #ffffff;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #2e7d32;
            margin-bottom: 20px;
        }
        .ai-badge {
            padding: 5px 15px; border-radius: 20px; font-weight: bold;
            display: inline-block; margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. DATABASE / LESSON DATA ---
# โครงสร้างแบบ Nested Dictionary เพื่อรองรับ 67 บทเรียน
# (ตัวอย่างบางส่วน - คุณครูสามารถก๊อปปี้เพิ่มจนครบ 67 เรื่องได้ในส่วนนี้)
curriculum_db = {
    "ม.4 เทอม 1": {
        "บทที่ 1 การศึกษาชีววิทยา": ["1.1 ธรรมชาติของสิ่งมีชีวิต", "1.2 การศึกษาชีววิทยาและวิธีการทางวิทยาศาสตร์", "1.3 กิจกรรมสะเต็มศึกษา"],
        "บทที่ 2 เคมีพื้นฐาน": ["2.1 อะตอม ธาตุ และสารประกอบ", "2.2 น้ำ", "2.3 สารประกอบคาร์บอน", "2.4 ปฏิกิริยาเคมีในเซลล์"],
        "บทที่ 3 เซลล์และการทำงาน": ["3.1 กล้องจุลทรรศน์", "3.2 โครงสร้างและหน้าที่เซลล์", "3.3 การลำเลียงสาร", "3.4 การหายใจระดับเซลล์", "3.5 การแบ่งเซลล์"]
    },
    "ม.4 เทอม 2": {
        "บทที่ 4 โครโมโซมและพันธุกรรม": ["4.1 โครโมโซม", "4.2 สารพันธุกรรม", "4.3 สมบัติของสารพันธุกรรม", "4.4 มิวเทชัน"],
        "บทที่ 5 การถ่ายทอดลักษณะ": ["5.1 พันธุศาสตร์เมนเดล", "5.2 ส่วนขยายเมนเดล", "5.3 ยีนบนโครโมโซมเดียวกัน"]
    }
    # คุณครูเติม ม.5 ม.6 ต่อที่นี่ตามแพทเทิร์นเดียวกัน...
}

# --- 3. HELPER FUNCTIONS ---
def get_ai_level(score):
    if score >= 8: return "Advanced (กลุ่มเก่ง)", "#C8E6C9", "🟢"
    elif score >= 5: return "Intermediate (กลุ่มกลาง)", "#FFF9C4", "🟡"
    return "Basic (กลุ่มเสริมสร้าง)", "#FFCCBC", "🟠"

def save_to_gsheets(data):
    # ส่วนนี้จะใส่โค้ดเชื่อมต่อ gspread ในอนาคต
    st.toast(f"บันทึกข้อมูล {data['name']} ลง Google Sheets สำเร็จ!", icon="✅")

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=120)
    st.title("BioSmart Classroom")
    st.write("🌿 Smart Learning with AI")
    st.divider()
    user_role = st.selectbox("เลือกประเภทผู้ใช้", ["นักเรียน (User)", "ครูผู้สอน (Admin)"])
    
    if user_role == "นักเรียน (User)":
        mode = st.radio("เมนู", ["หน้าแรก", "ลงทะเบียน/รับรหัส", "เข้าห้องเรียน (5E Mode)", "ผลการเรียน"])
    else:
        mode = st.radio("เมนูแอดมิน", ["จัดการข้อมูลนักเรียน", "Dashboard วิเคราะห์รายชั้น", "ออกข้อสอบ/ใบงาน"])

# --- 5. MAIN CONTENT LOGIC ---

# -- 5.1 หน้าแรก --
if mode == "หน้าแรก":
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.image("https://via.placeholder.com/400x500.png?text=Biology+Teacher", use_container_width=True)
    with col2:
        st.title("ยินดีต้อนรับสู่ ห้องเรียนอัจฉริยะชีววิทยา")
        st.subheader("BioSmartClassroom")
        st.markdown("""
        ---
        **ระดับชั้นที่เปิดสอน:** มัธยมศึกษาปีที่ 4 - 6  
        **วิธีการเรียน:** ระบบวิเคราะห์รายบุคคลด้วย AI และการสอนแบบ Active Learning 5E
        
        **ขั้นตอนการใช้งาน:**
        1. **ลงทะเบียน** เพื่อบันทึกข้อมูลและรับ Access Code
        2. **เลือกบทเรียน** ตามชั้นและเทอมที่ต้องการ
        3. **ทำ Pre-test** เพื่อให้ AI จัดกลุ่มระดับความรู้
        4. **เรียนรู้** ผ่านภารกิจ 5E ที่ออกแบบมาเพื่อคุณโดยเฉพาะ
        """)
        st.success("ออกแบบมาเพื่อให้ชีววิทยาเป็นเรื่องง่ายและสนุก!")

# -- 5.2 ลงทะเบียน --
elif mode == "ลงทะเบียน/รับรหัส":
    st.header("📝 ลงทะเบียนนักเรียนใหม่")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("reg_form", clear_on_submit=False):
            c1, c2 = st.columns(2)
            with c1:
                prefix = st.selectbox("คำนำหน้า", ["นาย", "นางสาว", "เด็กชาย", "เด็กหญิง"])
                fname = st.text_input("ชื่อ (ไม่ต้องมีคำนำหน้า)")
                lname = st.text_input("นามสกุล")
                level = st.selectbox("ระดับชั้น", ["ม.4", "ม.5", "ม.6"])
            with c2:
                room = st.text_input("ห้อง (เช่น 1, 2, 3)")
                no = st.number_input("เลขที่", min_value=1)
                social = st.text_input("Line ID / Facebook")
                photo = st.file_uploader("อัปโหลดภาพถ่ายนักเรียน", type=['jpg', 'png'])
            
            submitted = st.form_submit_button("ตรวจสอบและบันทึกข้อมูล")
        
        if submitted:
            # จำลองรหัสที่ไม่ซ้ำ
            access_code = f"BIO-{level[1:]}-{room}-{no}-{''.join(random.choices(string.ascii_uppercase, k=3))}"
            st.session_state['user_code'] = access_code
            
            st.markdown("### 🔍 ตรวจสอบข้อมูลก่อนยืนยัน")
            st.write(f"**ชื่อ-สกุล:** {prefix}{fname} {lname} | **ชั้น:** {level}/{room} เลขที่ {no}")
            st.write(f"**การติดต่อ:** {social}")
            
            if st.button("ยืนยันความถูกต้องและบันทึกข้อมูล"):
                save_to_gsheets({"name": fname, "code": access_code})
                st.balloons()
                st.markdown(f"""
                <div style="background-color:#fff3e0; padding:20px; border-radius:10px; border:2px solid #ff9800;">
                    <h3 style="color:#e65100; margin:0;">🔐 รหัสเข้าเรียนของคุณคือ: {access_code}</h3>
                    <p>กรุณาบันทึกรหัสนี้ไว้เพื่อใช้เข้าห้องเรียนในครั้งถัดไป</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -- 5.3 เข้าห้องเรียน --
elif mode == "เข้าห้องเรียน (5E Mode)":
    st.header("🧬 ระบบจัดการเรียนรู้อัจฉริยะ")
    
    # ส่วนเช็ครหัส
    auth_code = st.text_input("กรุณากรอกรหัสเข้าเรียน (Access Code):", placeholder="BIO-X-X-XXX")
    
    if auth_code:
        st.success("รหัสถูกต้อง! ยินดีต้อนรับเข้าสู่ระบบการเรียน")
        
        col1, col2 = st.columns(2)
        with col1:
            grade_choice = st.selectbox("เลือกชั้น/เทอม", list(curriculum_db.keys()))
        with col2:
            main_topic = st.selectbox("เลือกบทเรียนหลัก", list(curriculum_db[grade_choice].keys()))
            
        sub_topic = st.selectbox("เลือกหัวเรื่องย่อย (จาก 67 เรื่อง)", curriculum_db[grade_choice][main_topic])
        
        st.divider()
        
        # ขั้นที่ 1: Pre-test
        st.subheader("📝 ขั้นที่ 1: วิเคราะห์ความรู้ก่อนเรียน")
        st.info("ทำแบบทดสอบ 10 ข้อ เพื่อให้ AI ออกแบบภารกิจที่เหมาะสมกับคุณ")
        pre_score = st.slider("จำลองผลคะแนนสอบ (0-10)", 0, 10)
        
        if st.button("ประมวลผลด้วย AI"):
            level_text, color, icon = get_ai_level(pre_score)
            st.session_state['student_level'] = level_text
            
            st.markdown(f"""
                <div class="ai-badge" style="background-color:{color};">
                    {icon} AI จัดกลุ่มคุณอยู่ใน: {level_text}
                </div>
            """, unsafe_allow_html=True)
            
            # ขั้นที่ 2: บทเรียน 5E
            st.subheader(f"💡 บทเรียน Active Learning (5E) สำหรับ {sub_topic}")
            tabs = st.tabs(["E1: Engage", "E2: Explore", "E3: Explain", "E4: Elaborate", "E5: Evaluate"])
            
            with tabs[0]:
                st.write("### การสร้างความสนใจ")
                st.write("ดูวิดีโอปรากฏการณ์จริง และตั้งคำถามที่น่าสนใจ...")
                
            with tabs[1]:
                st.write("### การสำรวจและค้นหา")
                st.info(f"ภารกิจระดับ {level_text}: ให้นักเรียนดาวน์โหลดไฟล์ Lab และบันทึกผล")
                st.button(f"📥 ดาวน์โหลดใบงานระดับ {level_text}")
                st.text_area("บันทึกสรุปผลการสำรวจ:")
                
            with tabs[2]:
                st.write("### การอธิบาย")
                if "Basic" in level_text:
                    st.warning("คำแนะนำเพิ่มเติม: แนะนำให้ทบทวนหัวข้อ 'พื้นฐานเซลล์' เพิ่มเติมจากสรุปหน้า 10")
                st.success("ยินดีด้วย! คำตอบของคุณถูกต้องครบถ้วนในประเด็นหลัก")
                
            with tabs[4]:
                st.write("### การวัดผลหลังเรียน")
                post_score = st.number_input("คะแนนสอบหลังเรียน (Post-test)", 0, 10)
                if st.button("ส่งผลงานและบันทึก"):
                    st.success("บันทึกผลการเรียนลง Dashboard เรียบร้อยแล้ว")

# -- 5.4 สรุปผล (Dashboard) --
elif mode == "ผลการเรียน":
    st.header("📊 รายงานสรุปผลการเรียนอัจฉริยะ")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("คะแนนเฉลี่ย Pre-test", "4.5", "+10%")
    c2.metric("คะแนนเฉลี่ย Post-test", "8.2", "+45%")
    c3.metric("ความก้าวหน้า", "85%", "Green")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("📈 กราฟเปรียบเทียบพัฒนาการ")
    chart_data = pd.DataFrame({
        'หัวข้อบทเรียน': ['บทที่ 1', 'บทที่ 2', 'บทที่ 3'],
        'ก่อนเรียน': [4, 5, 3],
        'หลังเรียน': [8, 9, 7]
    })
    st.line_chart(chart_data.set_index('หัวข้อบทเรียน'))
    
    if st.button("🖨️ พิมพ์ใบรายงานผลการเรียน (Print Report)"):
        st.write("ระบบกำลังเตรียมไฟล์ PDF สำหรับดาวน์โหลด...")
