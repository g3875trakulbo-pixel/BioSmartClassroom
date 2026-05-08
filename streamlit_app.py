import streamlit as st
import pandas as pd
import plotly.express as px
import random
import string
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 1. CONFIGURATION & UI THEME ---
st.set_page_config(page_title="BioSmartClassroom", page_icon="🌿", layout="wide")

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }
        .stApp { background-color: #ffffff; }
        .stSidebar { background-color: #f1f8e9; border-right: 1px solid #dcedc8; }
        
        /* สไตล์ปุ่มหลัก */
        .stButton>button {
            width: 100%; border-radius: 12px; height: 3.5em;
            background-color: #2e7d32; color: white; border: none; 
            font-weight: bold; transition: 0.3s;
        }
        .stButton>button:hover { 
            background-color: #fdd835; color: #1b5e20; 
            border: 1px solid #2e7d32; transform: translateY(-2px);
        }
        
        /* การ์ดและกล่องเนื้อหา */
        .bio-container {
            background: #ffffff; padding: 30px; border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); 
            border-top: 10px solid #2e7d32; margin-bottom: 25px;
        }
        .ai-badge {
            display: inline-block; padding: 5px 15px; border-radius: 20px;
            font-weight: bold; margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- 2. DATABASE CONNECTION (GOOGLE SHEETS) ---
def get_google_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # ใช้ Secrets จาก Streamlit Cloud เพื่อความปลอดภัย
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        # เปิดไฟล์ฐานข้อมูล
        sheet = client.open("BioSmart_Database").sheet1
        return sheet
    except Exception as e:
        st.error(f"⚠️ การเชื่อมต่อฐานข้อมูลล้มเหลว: {e}")
        return None

# --- 3. CORE LOGIC FUNCTIONS ---
def generate_access_code():
    return f"BIO-{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}"

def ai_analyze_student(pct):
    if pct >= 80: return "ระดับสูง (Advanced)", "🟢", "เน้นภารกิจวิเคราะห์สังเคราะห์และนวัตกรรม"
    elif pct >= 50: return "ระดับกลาง (Intermediate)", "🟡", "เน้นการแก้ปัญหาและประยุกต์ใช้ความรู้"
    return "ระดับพื้นฐาน (Basic)", "🟠", "เน้นการปูพื้นฐานมโนทัศน์และสรุปใจความสำคัญ"

# --- 4. DATASET: 67 LESSONS (ม.4 - ม.6) ---
# โครงสร้างเตรียมไว้ให้คุณครูเติมเนื้อหาให้ครบทั้ง 67 เรื่อง
curriculum = {
    "ม.4 เทอม 1": {
        "1. การศึกษาชีววิทยา": ["1.1 ธรรมชาติของสิ่งมีชีวิต", "1.2 วิธีการทางวิทยาศาสตร์", "1.3 สะเต็มศึกษา"],
        "2. เคมีพื้นฐาน": ["2.1 อะตอมและธาตุ", "2.2 น้ำ", "2.3 สารประกอบคาร์บอน", "2.4 ปฏิกิริยาเคมี"],
        "3. เซลล์": ["3.1 กล้องจุลทรรศน์", "3.2 โครงสร้างเซลล์", "3.3 การลำเลียงสาร", "3.4 การหายใจระดับเซลล์", "3.5 การแบ่งเซลล์"]
    },
    "ม.4 เทอม 2": {
        "4. โครโมโซม": ["4.1 โครโมโซม", "4.2 สารพันธุกรรม", "4.3 สมบัติพันธุกรรม", "4.4 มิวเทชัน"],
        "5. พันธุกรรม": ["5.1 เมนเดล", "5.2 ส่วนขยายเมนเดล", "5.3 ยีนบนโครโมโซม"],
        "6. เทคโนโลยี DNA": ["6.1 พันธุวิศวกรรม", "6.2 ขนาด DNA", "6.3 การประยุกต์ใช้", "6.4 ชีวจริยธรรม"],
        "7. วิวัฒนาการ": ["7.1 หลักฐาน", "7.2 แนวคิด", "7.3 ประชากร", "7.4 แอลลีล", "7.5 กำเนิดสปีชีส์"]
    }
    # คุณครูสามารถเพิ่ม ม.5 เทอม 1/2 และ ม.6 เทอม 1/2 ลงใน Dictionary นี้ได้จนครบ 67 เรื่อง
}

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=120)
    st.title("BioSmart Classroom")
    st.markdown("---")
    role = st.radio("เลือกสถานะเข้าใช้งาน:", ["นักเรียน (Student Area)", "คุณครู (Admin Area)"])
    st.caption("Version 3.0 | Secure & Real-time")

# --- 6. STUDENT AREA (Integrated One-Page Flow) ---
if role == "นักเรียน (Student Area)":
    st.title("🌿 ห้องเรียนออนไลน์อัจฉริยะ (พื้นที่นักเรียน)")
    
    # ส่วนที่ 1: ต้อนรับและลงทะเบียน
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    st.subheader("1️⃣ ลงทะเบียน / เข้าสู่ระบบ")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        name = st.text_input("ชื่อ-นามสกุล", placeholder="ระบุชื่อจริง-นามสกุล")
        grade = st.selectbox("ระดับชั้น", ["มัธยมศึกษาปีที่ 4", "มัธยมศึกษาปีที่ 5", "มัธยมศึกษาปีที่ 6"])
    with col2:
        room_info = st.text_input("ห้อง/เลขที่", placeholder="เช่น 4/1 เลขที่ 10")
        if st.button("ลงทะเบียนและรับรหัส (Access Code)"):
            if name and room_info:
                new_code = generate_access_code()
                st.session_state['user_code'] = new_code
                st.session_state['user_name'] = name
                
                # บันทึกข้อมูลตั้งต้นไปที่ Google Sheets
                sheet = get_google_sheet()
                if sheet:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sheet.append_row([now, new_code, name, grade, room_info, 0, 0, "Pending"])
                    st.success(f"ลงทะเบียนสำเร็จ! รหัสของคุณคือ: **{new_code}** (โปรดจดไว้)")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")
    st.markdown('</div>', unsafe_allow_html=True)

    # ส่วนที่ 2: บทเรียน 5E และ AI วิเคราะห์ (ปลดล็อคเมื่อมีรหัส)
    current_code = st.session_state.get('user_code', '')
    if current_code:
        st.divider()
        st.subheader(f"🧬 บทเรียนอัจฉริยะ | รหัสของคุณ: {current_code}")
        
        st.markdown('<div class="bio-container">', unsafe_allow_html=True)
        # เลือกบทเรียน
        term_choice = st.selectbox("เลือกภาคเรียน", list(curriculum.keys()))
        topic_main = st.selectbox("เลือกบทหลัก", list(curriculum[term_choice].keys()))
        topic_sub = st.selectbox("เลือกบทเรียนย่อย (Active Learning)", curriculum[term_choice][topic_main])
        
        # ขั้นที่ 1: วิเคราะห์ก่อนเรียน
        st.markdown("#### 📝 Step 1: วิเคราะห์ความรู้พื้นฐาน")
        pre_pct = st.slider("ทำแบบทดสอบก่อนเรียน (คะแนนร้อยละ %)", 0, 100, step=5)
        
        if st.button("ส่งผลให้ AI ประมวลผล"):
            level, icon, advice = ai_analyze_student(pre_pct)
            st.session_state['my_level'] = level
            
            # อัปเดตข้อมูลในแถวเดิมโดยใช้ Unique ID
            sheet = get_google_sheet()
            if sheet:
                try:
                    cell = sheet.find(current_code)
                    sheet.update_cell(cell.row, 6, pre_pct) # คอลัมน์ PreTestPct
                    sheet.update_cell(cell.row, 8, level)   # คอลัมน์ Level
                    st.balloons()
                except: st.error("ไม่สามารถอัปเดตข้อมูลได้")

        # ขั้นที่ 2: บทเรียน 5E ตามระดับ
        if 'my_level' in st.session_state:
            st.write("---")
            lv = st.session_state['my_level']
            st.markdown(f"#### 💡 แผนการเรียนสำหรับกลุ่ม: {lv}")
            
            t1, t2, t3, t4, t5 = st.tabs(["E1: Engage", "E2: Explore", "E3: Explain", "E4: Elaborate", "E5: Evaluate"])
            with t1:
                st.write("ชมวิดีโอและสถานการณ์จำลองเพื่อกระตุ้นความสนใจในเรื่อง", topic_sub)
            with t2:
                st.info(f"ภาระงานระดับ {lv}: ให้นักเรียนปฏิบัติกิจกรรมตามใบงานอัจฉริยะ")
                st.button(f"📥 ดาวน์โหลดใบงานและแบบบันทึก (Level: {lv})")
            with t5:
                st.write("ประเมินความรู้หลังเรียน")
                post_pct = st.number_input("คะแนนหลังเรียนที่ได้ (%)", 0, 100)
                if st.button("บันทึกผลการเรียนลงฐานข้อมูล"):
                    sheet = get_google_sheet()
                    if sheet:
                        try:
                            cell = sheet.find(current_code)
                            sheet.update_cell(cell.row, 7, post_pct) # คอลัมน์ PostTestPct
                            st.success("บันทึกคะแนนร้อยละสำเร็จ ระบบ AI กำลังประมวลผลสรุปผลเรียน")
                        except: st.error("เกิดข้อผิดพลาดในการบันทึก")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. ADMIN AREA (Real-time Teacher Dashboard) ---
elif role == "คุณครู (Admin Area)":
    st.title("👨‍🏫 ระบบบริหารจัดการและแดชบอร์ดครู")
    
    admin_pwd = st.sidebar.text_input("รหัสผ่านครู (Password)", type="password")
    if admin_pwd == "bio123": # คุณครูสามารถเปลี่ยนรหัสได้ที่นี่
        sheet = get_google_sheet()
        if sheet:
            # ดึงข้อมูลดิบทั้งหมดแบบ Real-time
            with st.spinner("กำลังดึงข้อมูลล่าสุดจาก Google Sheets..."):
                all_data = sheet.get_all_records()
                df = pd.DataFrame(all_data)
            
            if not df.empty:
                # ส่วนสรุปตัวเลข (Metrics)
                c1, c2, c3 = st.columns(3)
                c1.metric("นักเรียนทั้งหมด", f"{len(df)} คน")
                c2.metric("คะแนนเฉลี่ยหลังเรียน", f"{df['PostTestPct'].mean():.2f} %")
                c3.metric("พัฒนาการเฉลี่ย (Gain)", f"{(df['PostTestPct'] - df['PreTestPct']).mean():.1f} %")
                
                # ส่วนแดชบอร์ดกราฟ
                st.markdown('<div class="bio-container">', unsafe_allow_html=True)
                st.subheader("📊 รายงานวิเคราะห์ผลการเรียน (หน่วยร้อยละ %)")
                
                # กราฟเปรียบเทียบก่อน-หลัง
                fig = px.bar(df, x='Name', y=['PreTestPct', 'PostTestPct'],
                             barmode='group',
                             labels={'value': 'ร้อยละ (%)', 'variable': 'การทดสอบ', 'Name': 'ชื่อนักเรียน'},
                             color_discrete_map={'PreTestPct': '#fdd835', 'PostTestPct': '#2e7d32'})
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ตารางข้อมูลและปุ่มพิมพ์ออก
                with st.expander("🔍 ตรวจสอบฐานข้อมูลนักเรียนรายบุคคล"):
                    st.dataframe(df, use_container_width=True)
                    st.button("🖨️ พิมพ์รายงานสรุปผลรายชั้นเรียน (Print Out)")
            else:
                st.info("ยังไม่มีข้อมูลนักเรียนลงทะเบียนในระบบ")
    else:
        st.warning("กรุณากรอกรหัสผ่านเพื่อเข้าใช้งานระบบหลังบ้าน")
