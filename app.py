import streamlit as st

# การตั้งค่าหน้าเว็บ
st.set_page_config(page_title="BioSmartClassroom", layout="wide")

# --- ส่วนหัว (Header) ---
st.title("🐸 ห้องเรียนชีววิทยาออนไลน์ (BioSmartClassroom)")
st.write("เวอร์ชั่น 1.10.05.26 | พัฒนาโดย นายตระกูล บุญชิต")

# --- แถบเมนูด้านข้าง (Sidebar Menu) ---
with st.sidebar:
    st.header("เมนู (Menu)")
    user_role = st.radio("เลือกสถานะผู้ใช้งาน", ["ส่วนของนักเรียน (User)", "ส่วนของคุณครู (Admin)"])
    
    st.divider()
    st.subheader("ข่าวสาร (News)")
    st.info("อัปเดตล่าสุด: 10.05.2026 \n\nระบบรองรับการเรียนรู้แบบ 5E เต็มรูปแบบแล้ว!")

# --- ส่วนแสดงเนื้อหาหลัก (Main Content) ---
col1, col2 = st.columns([1, 1])

with col1:
    with st.expander("📖 คู่มือการใช้ (Manual)", expanded=True):
        st.markdown("""
        **คำแนะนำ:** ห้องเรียนนี้เป็นนวัตกรรมการจัดการเรียนการสอนที่ปรับเปลี่ยนตาม
        ความสามารถของนักเรียน (**Differential Instruction**) โดยมี AI ช่วยในการออกแบบ
        
        **วิธีใช้งาน:**
        1. เลือกเมนูที่เกี่ยวข้องกับผู้ใช้ด้านซ้ายมือ
        2. ปฏิบัติตามคำแนะนำในแต่ละบทเรียน
        """)

with col2:
    st.subheader("📸 ภาพกิจกรรมและผลงาน")
    # ส่วนนี้ไว้ใส่รูปภาพหรือ Progress Bar ของนักเรียน
    st.image("https://via.placeholder.com/400x300.png?text=Student+Activities", caption="พื้นที่แสดงผลงานนักเรียน")

# --- ตัวอย่างส่วนเนื้อหา (ถ้าเป็นนักเรียน) ---
if user_role == "ส่วนของนักเรียน (User)":
    st.divider()
    st.header("บทเรียนสำหรับคุณ")
    tab1, tab2, tab3 = st.tabs(["5E Learning", "แบบทดสอบ", "ส่งงาน"])
    
    with tab1:
        st.subheader("บทที่ 1.1: ธรรมชาติของสิ่งมีชีวิต")
        st.video("https://www.youtube.com/watch?v=example") # ใส่ลิงก์วิดีโอสอนจริง
