import streamlit as st
import pandas as pd
import plotly.express as px
import random
import string

# --- 1. CONFIG & UI THEME ---
st.set_page_config(page_title="BioSmartClassroom", page_icon="🌿", layout="wide")

def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }
        .stApp { background-color: #ffffff; }
        .stSidebar { background-color: #f1f8e9; }
        .stButton>button {
            width: 100%; border-radius: 10px; background-color: #2e7d32; color: white;
            height: 3em; font-weight: bold; border: none; transition: 0.3s;
        }
        .stButton>button:hover { background-color: #fdd835; color: #1b5e20; border: 1px solid #2e7d32; }
        .bio-container {
            background: #ffffff; padding: 25px; border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-top: 8px solid #2e7d32;
        }
        .ai-result {
            background-color: #fffde7; padding: 15px; border-radius: 10px;
            border: 1px solid #fdd835; margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. DATASET (โครงสร้าง 67 บทเรียนย่อย) ---
# (หมายเหตุ: ในโค้ดจริงคุณครูสามารถย้ายข้อมูลนี้ไปไว้ในไฟล์ Excel หรือ JSON แยกต่างหากได้)
curriculum = {
    "ม.4 เทอม 1": {
        "1. การศึกษาชีววิทยา": ["1.1 ธรรมชาติของสิ่งมีชีวิต", "1.2 วิธีการทางวิทยาศาสตร์", "1.3 สะเต็มศึกษา"],
        "2. เคมีพื้นฐาน": ["2.1 อะตอมและธาตุ", "2.2 น้ำ", "2.3 สารประกอบคาร์บอน", "2.4 ปฏิกิริยาเคมี"],
        "3. เซลล์": ["3.1 กล้องจุลทรรศน์", "3.2 โครงสร้างเซลล์", "3.3 การลำเลียงสาร", "3.4 การหายใจระดับเซลล์", "3.5 การแบ่งเซลล์"]
    },
    "ม.4 เทอม 2": {
        "4. โครโมโซม": ["4.1 โครโมโซม", "4.2 สารพันธุกรรม", "4.3 สมบัติพันธุกรรม", "4.4 มิวเทชัน"],
        "5. พันธุกรรม": ["5.1 เมนเดล", "5.2 ส่วนขยายเมนเดล", "5.3 ยีนบนโครโมโซม"],
        "6. เทคโนโลยี DNA": ["6.1 พันธุวิศวกรรม", "6.2 ขนาด DNA", "6.3 ประยุกต์ใช้", "6.4 ชีวจริยธรรม"],
        "7. วิวัฒนาการ": ["7.1 หลักฐาน", "7.2 แนวคิด", "7.3 ประชากร", "7.4 แอลลีล", "7.5 กำเนิดสปีชีส์"]
    },
    # ครูสามารถเพิ่ม ม.5 (บทที่ 8-17) และ ม.6 (บทที่ 18-25) ได้ตามรูปแบบนี้
}

# --- 3. LOGIC FUNCTIONS ---
def generate_access_code():
    return f"BIO-{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}"

def ai_classify(score_pct):
    if score_pct >= 80: return "กลุ่มเก่ง (Advanced)", "🟢", "มอบหมายภาระงานวิเคราะห์และสังเคราะห์ (Level 3)"
    elif score_pct >= 50: return "กลุ่มกลาง (Intermediate)", "🟡", "มอบหมายภาระงานประยุกต์ใช้ความรู้ (Level 2)"
    return "กลุ่มพื้นฐาน (Basic)", "🟠", "มอบหมายภาระงานเสริมสร้างมโนทัศน์ (Level 1)"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=120)
    st.title("BioSmart Classroom")
    st.write("🌿 นวัตกรรมเรียนรู้อัจฉริยะ")
    st.divider()
    role = st.selectbox("เลือกประเภทผู้ใช้", ["นักเรียน (Student Area)", "คุณครู (Admin Area)"])
    st.caption("ระบบโดย GitHub & Streamlit")

# --- 5. MAIN CONTENT ---

# --- หน้าส่วนของนักเรียน (Student Area) ---
if role == "นักเรียน (Student Area)":
    st.title("🌿 ห้องเรียนสำหรับนักเรียน")
    
    # ส่วนที่ 1: ลงทะเบียน (แสดงเป็น Expander เพื่อความคลีน)
    with st.expander("📝 ขั้นตอนที่ 1: ลงทะเบียนและรับรหัสเข้าเรียน", expanded=not st.session_state.get('registered', False)):
        st.markdown('<div class="bio-container">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            title = st.selectbox("คำนำหน้า", ["นาย", "นางสาว"])
            fname = st.text_input("ชื่อ")
            lname = st.text_input("นามสกุล")
            grade = st.selectbox("ระดับชั้น", ["ม.4", "ม.5", "ม.6"])
        with c2:
            room_no = st.text_input("ห้อง/เลขที่ (เช่น 1/15)")
            social = st.text_input("ช่องทางการติดต่อ (Line/FB)")
            st.file_uploader("อัปโหลดรูปนักเรียน")
            
        if st.button("ยืนยันการลงทะเบียน"):
            if fname and lname:
                st.session_state['user_code'] = generate_access_code()
                st.session_state['registered'] = True
                st.session_state['user_name'] = f"{title}{fname} {lname}"
                st.balloons()
            else:
                st.error("กรุณากรอกชื่อและนามสกุล")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get('registered'):
        st.success(f"สวัสดีคุณ {st.session_state['user_name']} | รหัสเข้าเรียนของคุณคือ: {st.session_state['user_code']}")
        
        # ส่วนที่ 2: เข้าสู่บทเรียน 5E
        st.divider()
        st.subheader("🧪 ขั้นตอนที่ 2: เลือกบทเรียนและทำภารกิจ 5E")
        
        with st.container():
            st.markdown('<div class="bio-container">', unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                term_sel = st.selectbox("เลือกภาคเรียน", list(curriculum.keys()))
                topic_main = st.selectbox("เลือกบทหลัก", list(curriculum[term_sel].keys()))
            with cc2:
                topic_sub = st.selectbox("เลือกหัวเรื่องย่อย (67 บทเรียน)", curriculum[term_sel][topic_main])
                st.write("") # Spacer
                start_btn = st.button("✨ เริ่มต้นการวิเคราะห์ AI")
            
            if start_btn:
                st.session_state['lesson_active'] = True
            
            if st.session_state.get('lesson_active'):
                st.markdown("#### 📝 แบบทดสอบวิเคราะห์ความรู้ก่อนเรียน")
                pre_score = st.slider("ผลการสอบก่อนเรียน (ร้อยละ %)", 0, 100, step=10)
                
                lv_name, icon, task_desc = ai_classify(pre_score)
                st.markdown(f"""
                <div class="ai-result">
                    <h4>{icon} AI Analysis: คุณอยู่ใน {lv_name}</h4>
                    <p><b>คำแนะนำภารกิจ:</b> {task_desc}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # บทเรียน 5E
                st.write("---")
                t1, t2, t3, t4, t5 = st.tabs(["Engage", "Explore", "Explain", "Elaborate", "Evaluate"])
                with t1:
                    st.write("🎥 รับชมสื่อกระตุ้นความสนใจในหัวข้อ:", topic_sub)
                with t2:
                    st.write("📥 **ดาวน์โหลดภาระงาน:**")
                    st.button(f"ใบงาน Active Learning ({lv_name})")
                with t5:
                    st.write("📊 **สรุปผลการเรียน**")
                    post_score = st.number_input("คะแนนหลังเรียน (%)", 0, 100)
                    if st.button("บันทึกผลการเรียนลง Google Sheets"):
                        st.toast("บันทึกข้อมูลสำเร็จ!")
            st.markdown('</div>', unsafe_allow_html=True)

# --- หน้าส่วนของคุณครู (Admin Area) ---
elif role == "คุณครู (Admin Area)":
    st.title("👨‍🏫 ระบบจัดการสำหรับครูผู้สอน")
    
    # ระบบล็อคเบื้องต้น
    pwd = st.sidebar.text_input("รหัสผ่านแอดมิน", type="password")
    if pwd == "bio123": # ครูสามารถเปลี่ยนรหัสตรงนี้ได้
        tab_dash, tab_sheet = st.tabs(["📈 แดชบอร์ดสรุปผล", "🗃️ จัดการฐานข้อมูล"])
        
        with tab_dash:
            st.subheader("สถิติภาพรวมร้อยละ (%)")
            m1, m2, m3 = st.columns(3)
            m1.metric("นักเรียนในระบบ", "128 คน", "+5")
            m2.metric("เฉลี่ยพัฒนาการ", "+24%", "Green")
            m3.metric("บทเรียนที่ใช้งานสูงสุด", "พันธุกรรม")
            
            # กราฟ
            df = pd.DataFrame({
                'ห้อง': ['ม.4/1', 'ม.4/2', 'ม.4/3', 'ม.4/4'],
                'คะแนนเฉลี่ยหลังเรียน (%)': [88, 75, 82, 79]
            })
            fig = px.bar(df, x='ห้อง', y='คะแนนเฉลี่ยหลังเรียน (%)', color='ห้อง', text='คะแนนเฉลี่ยหลังเรียน (%)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("---")
            st.subheader("📋 รายงานผลรายบุคคล")
            raw_data = pd.DataFrame({
                'เลขที่': [1, 2, 3],
                'ชื่อ': ['สมชาย', 'สมหญิง', 'มานะ'],
                'ก่อนเรียน': [40, 60, 30],
                'หลังเรียน': [90, 95, 80],
                'ระดับ AI': ['Basic', 'Intermediate', 'Basic']
            })
            st.table(raw_data)
            st.button("🖨️ Export / Print รายงานสรุป")

        with tab_sheet:
            st.subheader("เชื่อมต่อ Google Sheets")
            st.info("สถานะ: 🟢 เชื่อมต่อกับไฟล์ 'BioSmart_Database' แล้ว")
            st.link_button("🌐 เปิด Google Sheets เพื่อตรวจสอบข้อมูล", "https://docs.google.com/spreadsheets/d/...")
            if st.button("🛠️ Reset รหัสเข้าเรียนนักเรียนทั้งหมด"):
                st.warning("คำเตือน: ข้อมูลรหัสจะถูกลบและสร้างใหม่")
    else:
        st.warning("กรุณากรอกรหัสผ่านที่แถบด้านข้างเพื่อเข้าถึงส่วนของครู")
