import streamlit as st
import random

# --- 1. SETTINGS & CSS ---
st.set_page_config(page_title="BioAdaptive AI", layout="wide")

def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;700&display=swap');
        
        html, body, [class*="st-"] {
            font-family: 'Prompt', sans-serif;
        }
        
        /* Main Color Palette */
        :root {
            --dark-green: #006837;
            --light-green: #8CC63F;
            --yellow: #FBB040;
        }

        /* Customize Buttons */
        div.stButton > button:first-child {
            background-color: var(--dark-green);
            color: white;
            border-radius: 10px;
            border: none;
            height: 3em;
            width: 100%;
        }
        
        div.stButton > button:hover {
            background-color: var(--light-green);
            border: none;
        }

        /* Grade Headers */
        .grade-header {
            padding: 15px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            margin-top: 20px;
        }
        .m4 { background-color: var(--dark-green); border-left: 10px solid var(--yellow); }
        .m5 { background-color: #2E7D32; border-left: 10px solid var(--light-green); }
        .m6 { background-color: #43A047; border-left: 10px solid #C0CA33; }
        
        /* Infographic Boxes */
        .info-box {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            border-bottom: 5px solid var(--yellow);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. PAGES ---

def landing_page():
    st.markdown("<h1 style='text-align: center; color: #006837;'>🧬 BioAdaptive AI Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>ระบบบริหารจัดการเรียนรู้อัจฉริยะ วิชาชีววิทยา ม.4-6</p>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='info-box'><h3>🎓 สำหรับนักเรียน</h3><p>เข้าสู่บทเรียนวิเคราะห์ตัวตน และรับแผนการเรียนเฉพาะบุคคลที่ AI ออกแบบให้</p></div>", unsafe_allow_html=True)
        if st.button("เข้าสู่ระบบ / ลงทะเบียนนักเรียน"):
            st.session_state.page = "auth"
            st.rerun()
            
    with col2:
        st.markdown("<div class='info-box'><h3>👨‍🏫 สำหรับคุณครู</h3><p>ระบบแอดมิน ติดตามความก้าวหน้า Heatmap และ Export รายงานรายห้อง</p></div>", unsafe_allow_html=True)
        if st.button("เข้าสู่ระบบแอดมิน"):
            st.warning("ส่วนของคุณครูกำลังอยู่ในการพัฒนา")

    st.markdown("### 📚 รายละเอียดหลักสูตร (25 Lessons)")
    
    # M.4 Content
    st.markdown('<div class="grade-header m4">ชั้นมัธยมศึกษาปีที่ 4</div>', unsafe_allow_html=True)
    with st.expander("เปิดดูเนื้อหา ม.4 (บทที่ 1-7)"):
        st.write("**เทอม 1:** 1.การศึกษาชีววิทยา | 2.เคมีพื้นฐานของสิ่งมีชีวิต | 3.เซลล์และการทำงาน")
        st.write("**เทอม 2:** 4.โครโมโซมและสารพันธุกรรม | 5.การถ่ายทอดลักษณะทางพันธุกรรม | 6.เทคโนโลยี DNA | 7.วิวัฒนาการ")

    # M.5 Content
    st.markdown('<div class="grade-header m5">ชั้นมัธยมศึกษาปีที่ 5</div>', unsafe_allow_html=True)
    with st.expander("เปิดดูเนื้อหา ม.5 (บทที่ 8-17)"):
        st.write("**เทอม 1:** 8.การสืบพันธุ์พืชดอก | 9.โครงสร้างพืช | 10.การลำเลียง | 11.การสังเคราะห์ด้วยแสง | 12.การตอบสนองของพืช")
        st.write("**เทอม 2:** 13.ระบบย่อยอาหาร | 14.ระบบหายใจ | 15.ระบบหมุนเวียนเลือด | 16.ระบบภูมิคุ้มกัน | 17.ระบบขับถ่าย")

    # M.6 Content
    st.markdown('<div class="grade-header m6">ชั้นมัธยมศึกษาปีที่ 6</div>', unsafe_allow_html=True)
    with st.expander("เปิดดูเนื้อหา ม.6 (บทที่ 18-25)"):
        st.write("**เทอม 1:** 18.ระบบประสาท | 19.การเคลื่อนที่ | 20.ระบบต่อมไร้ท่อ | 21.การสืบพันธุ์ | 22.พฤติกรรมสัตว์")
        st.write("**เทอม 2:** 23.ความหลากหลายทางชีวภาพ | 24.ระบบนิเวศและประชากร | 25.มนุษย์กับความยั่งยืน")

def auth_page():
    st.button("⬅️ กลับหน้าหลัก", on_click=lambda: st.session_state.update({"page": "landing"}))
    
    tab1, tab2 = st.tabs(["เข้าสู่ระบบ", "ลงทะเบียนใหม่"])
    
    with tab1:
        st.subheader("เข้าสู่ระบบ")
        st.text_input("ชื่อผู้ใช้งาน")
        st.text_input("รหัสผ่าน", type="password")
        if st.button("Login"):
            st.session_state.page = "lesson"
            st.rerun()
            
    with tab2:
        st.subheader("ลงทะเบียนเพื่อรับรหัสเข้าเรียน")
        with st.form("reg_form"):
            name = st.text_input("ชื่อ-นามสกุล")
            email = st.text_input("อีเมล")
            grade = st.selectbox("ระดับชั้น", ["ม.4", "ม.5", "ม.6"])
            if st.form_submit_button("ยืนยันการลงทะเบียน"):
                student_id = f"BIO-{random.randint(1000, 9999)}"
                st.success(f"ลงทะเบียนสำเร็จ! รหัสเข้าเรียนของคุณคือ: {student_id}")
                st.info("กรุณาใช้ชื่อผู้ใช้งานที่ลงทะเบียนเพื่อเข้าสู่ระบบ")

def lesson_page():
    st.sidebar.title("🧬 Bio-Menu")
    if st.sidebar.button("Log out"):
        st.session_state.page = "landing"
        st.rerun()

    st.title("บทเรียนอัจฉริยะ (Adaptive Lesson)")
    
    # จำลองคะแนน Pre-test (ในระบบจริงจะมาจากฐานข้อมูล)
    score = st.sidebar.slider("คะแนนวิเคราะห์ก่อนเรียน (%)", 0, 100, 50)
    
    # AI Logic: จัดระดับผู้เรียน (Step 2)
    if score < 40:
        level, color, icon = "Beginner (Seed 🌱)", "#FBB040", "เน้นปูพื้นฐานและวิดีโอ"
    elif score <= 75:
        level, color, icon = "Intermediate (Sprout 🌿)", "#8CC63F", "เนื้อหามาตรฐานและ Lab จำลอง"
    else:
        level, color, icon = "Advanced (Bloom 🌸)", "#006837", "เนื้อหาเชิงวิเคราะห์และโจทย์ท้าทาย"

    st.markdown(f"<div style='background-color:{color}; padding:20px; border-radius:15px; color:white;'><h2>ระดับของคุณ: {level}</h2><p>AI เลือกบทเรียนแบบ: {icon}</p></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # ตัวอย่างเนื้อหาบทที่ 4 (ตามภาพต้นฉบับ)
    st.header("บทที่ 4: โครโมโซมและสารพันธุกรรม")
    
    t1, t2, t3 = st.tabs(["📖 เนื้อหาบทเรียน", "🧪 กิจกรรม AI", "📊 รายงานผล"])
    
    with t1:
        if "Advanced" in level:
            st.subheader("4.1 การวิเคราะห์โครงสร้าง DNA เชิงลึก")
            st.write("ในระดับนี้ คุณจะได้ศึกษาพันธะเคมีที่ซับซ้อนและการจำลองตัวของ DNA...")
        else:
            st.subheader("4.1 โครโมโซมคืออะไร?")
            st.write("มาดูวิดีโออธิบายโครงสร้างของโครโมโซมแบบเข้าใจง่ายกันครับ...")
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder

    with t2:
        st.subheader("🎯 กิจกรรมที่ AI เลือกให้คุณ")
        if "Beginner" in level:
            st.write("กิจกรรม: จับคู่ส่วนประกอบของนิวคลีโอไทด์")
        else:
            st.write("กิจกรรม: ออกแบบโปรโตคอลการสกัด DNA จากพืช")

    with t3:
        st.subheader("📉 ความก้าวหน้าส่วนบุคคล")
        st.progress(score/100)
        st.write(f"คุณทำคะแนนสะสมในบทนี้ได้ {score}%")
        if st.button("Export PDF Report"):
            st.success("ระบบกำลังสร้างไฟล์ PDF... กรุณารอสักครู่")

# --- 3. MAIN APP CONTROLLER ---
def main():
    local_css()
    
    if "page" not in st.session_state:
        st.session_state.page = "landing"
        
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "auth":
        auth_page()
    elif st.session_state.page == "lesson":
        lesson_page()

if __name__ == "__main__":
    main()
