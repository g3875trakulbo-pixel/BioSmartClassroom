import streamlit as st

def login_page():
    # กำหนด CSS เพื่อปรับจานสีให้เป็น เขียว-ขาว-เหลือง ตามภาพต้นฉบับ
    st.markdown("""
        <style>
        /* พื้นหลังหลัก */
        .stApp {
            background-color: #F0F4F1;
        }
        /* ปรับแต่งปุ่ม */
        div.stButton > button:first-child {
            background-color: #006837;
            color: white;
            border-radius: 10px;
            border: none;
            width: 100%;
            height: 3em;
        }
        div.stButton > button:hover {
            background-color: #8CC63F;
            color: white;
        }
        /* ปรับแต่งหัวข้อ */
        h1, h2, h3 {
            color: #006837 !important;
        }
        /* กล่องลงทะเบียน/ล็อคอิน */
        .auth-container {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            border-bottom: 5px solid #FBB040; /* เส้นขอบเหลืองด้านล่าง */
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🧬 BioSmart Adaptive Learning")
    
    # สร้าง Tab สำหรับเลือกระหว่าง เข้าสู่ระบบ กับ ลงทะเบียน
    tab1, tab2 = st.tabs(["เข้าสู่ระบบ", "ลงทะเบียนใหม่"])

    with tab1:
        st.subheader("ยินดีต้อนรับกลับเข้าสู่บทเรียน")
        with st.container():
            username = st.text_input("ชื่อผู้ใช้งาน / อีเมล", key="login_user")
            password = st.text_input("รหัสผ่าน", type="password", key="login_pass")
            if st.button("เข้าสู่ระบบ"):
                if username and password:
                    st.session_state.authenticated = True
                    st.session_state.name = username
                    st.session_state.role = "Student" # สมมติเป็นนักเรียน
                    st.rerun()
                else:
                    st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

    with tab2:
        st.subheader("ลงทะเบียนเพื่อรับรหัสเข้าเรียน")
        st.write("กรุณากรอกข้อมูลด้านล่าง ระบบ AI จะสร้างรหัสเข้าเรียน (Student ID) ให้คุณโดยอัตโนมัติ")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                fullname = st.text_input("ชื่อ-นามสกุล")
                email = st.text_input("อีเมล")
            with col2:
                grade = st.selectbox("ระดับชั้น", ["ม.4", "ม.5", "ม.6"])
                new_password = st.text_input("กำหนดรหัสผ่าน", type="password")
            
            submit_reg = st.form_submit_button("ยืนยันการลงทะเบียน")
            
            if submit_reg:
                if fullname and email and new_password:
                    # จำลองการสร้างรหัสเข้าเรียน
                    import random
                    student_id = f"BIO-{random.randint(1000, 9999)}"
                    
                    st.success(f"ลงทะเบียนสำเร็จ! 🎉")
                    st.balloons()
                    
                    # ส่วนของการรับรหัสเข้าเรียน
                    st.info(f"**รหัสเข้าเรียนของคุณคือ: {student_id}**")
                    st.warning("⚠️ โปรดจดจำรหัสนี้เพื่อใช้ในการส่งออกรายงาน (Export PDF/Excel)")
                else:
                    st.warning("กรุณากรอกข้อมูลให้ครบทุกช่อง")

# สำหรับทดสอบรันหน้าเดียว
if __name__ == "__main__":
    login_page()
