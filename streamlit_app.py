import streamlit as st
import pandas as pd
from modules import teacher_db, student_db, adaptive, export_tools

# การตั้งค่าหน้าจอ
st.set_page_config(page_title="Biology Adaptive Learning", layout="wide")

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_navigation()

def show_login_page():
    st.title("🧬 Biology Adaptive Learning Platform")
    with st.form("login_form"):
        user_type = st.selectbox("สถานะ", ["นักเรียน", "อาจารย์"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("เข้าสู่ระบบ"):
            st.session_state.logged_in = True
            st.session_state.user_type = user_type
            st.rerun()

def show_navigation():
    st.sidebar.title(f"ผู้ใช้งาน: {st.session_state.user_type}")
    
    if st.session_state.user_type == "อาจารย์":
        menu = ["Dashboard", "จัดการหลักสูตร", "วิเคราะห์ห้องเรียน", "Export ศูนย์รายงาน"]
        choice = st.sidebar.radio("เมนูหลัก", menu)
        
        if choice == "Dashboard":
            teacher_db.show()
        elif choice == "จัดการหลักสูตร":
            st.header("📚 Course Management (25 Lessons)")
            # แสดงบทเรียน ม.4-ม.6 ที่สร้างไว้ในไฟล์ Excel ก่อนหน้า
        elif choice == "วิเคราะห์ห้องเรียน":
            st.header("📊 Analytics & AI Insights")
            # ดึงข้อมูลจากฐานข้อมูลมาทำ Heatmap
            
    else: # ฝั่งนักเรียน
        menu = ["บทเรียนของฉัน", "ทำแบบทดสอบ", "รายงานผลการเรียน"]
        choice = st.sidebar.radio("เมนูหลัก", menu)
        
        if choice == "บทเรียนของฉัน":
            adaptive.show_adaptive_content() # AI เลือกบทเรียนที่เหมาะสม
        elif choice == "ทำแบบทดสอบ":
            st.header("📝 Quiz & Assessment")
            # ระบบ Pre-test / Post-test

    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

if __name__ == "__main__":
    main()
