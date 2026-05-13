import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="BioSmart Classroom Pro", layout="wide")

# ปรับแต่งความสวยงาม (Dark Mode Theme)
st.markdown("""
    <style>
    .main { background-color: #0b140d; }
    h1, h2, h3 { color: #4ade80 !important; font-family: 'Mitr', sans-serif; }
    .stButton>button { background-color: #22c55e; color: white; width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🔬 BioSmart Classroom Pro")

# แถบเมนูด้านข้าง
menu = st.sidebar.radio("เลือกโหมดการใช้งาน", ["🎓 สำหรับนักเรียน", "👨‍🏫 สำหรับครู (Dashboard)"])

if menu == "🎓 สำหรับนักเรียน":
    st.header("บทเรียนชีววิทยาอัจฉริยะ")
    name = st.text_input("กรอกชื่อ-นามสกุล ของคุณ", placeholder="ตัวอย่าง: สมชาย ใจดี")
    
    st.divider()
    
    # ตัวอย่างบทเรียน 5E (ขั้น Explain)
    st.subheader("📖 บทเรียน: การรักษาดุลยภาพ (Homeostasis)")
    st.info("""
    **เนื้อหาสำคัญ:** ร่างกายมนุษย์มีการควบคุมสภาพแวดล้อมภายในให้คงที่เสมอ เช่น 
    - อุณหภูมิร่างกาย (37°C)
    - ระดับน้ำในร่างกาย
    - ค่าความเป็นกรด-ด่าง (pH) ในเลือด
    """)
    
    # ขั้น Evaluate (ทำแบบทดสอบ)
    st.write("---")
    st.write("🎯 **แบบทดสอบความเข้าใจ**")
    q1 = st.radio("เมื่อเราออกกำลังกายจนตัวร้อน ร่างกายจะขับเหงื่อเพื่ออะไร?", 
                  ["เพื่อให้ผิวชุ่มชื้น", "เพื่อลดอุณหภูมิร่างกาย", "เพื่อขับสารพิษ"])
    
    # คำนวณคะแนน (ตัวอย่างข้อเดียว)
    score = 1 if q1 == "เพื่อลดอุณหภูมิร่างกาย" else 0
    
    if st.button("ส่งคะแนนเข้าสู่ระบบ"):
        if name:
            # ส่งข้อมูลไปที่ Backend (FastAPI)
            payload = {"student_name": name, "lesson_id": 1, "score": score}
            try:
                res = requests.post("http://localhost:8000/submit", json=payload)
                result = res.json()
                st.success(f"บันทึกข้อมูลเรียบร้อย! {result['recommendation']}")
                st.balloons()
            except:
                st.error("ไม่สามารถเชื่อมต่อกับ Server ได้ (อย่าลืมรัน uvicorn main:app นะครับ)")
        else:
            st.warning("กรุณากรอกชื่อก่อนส่งข้อมูล")

else:
    st.header("📊 ระบบวิเคราะห์ผลการเรียน (ครู)")
    
    try:
        # ดึงข้อมูลจาก Backend
        res = requests.get("http://localhost:8000/stats")
        if res.status_code == 200 and res.json():
            data = res.json()
            df = pd.DataFrame(data)
            
            # แสดงกราฟวิเคราะห์ข้อมูล
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("ตารางคะแนนล่าสุด")
                st.dataframe(df[["student_name", "score"]], use_container_width=True)
            
            with col2:
                st.subheader("กราฟสรุปภาพรวม")
                fig = px.bar(df, x="student_name", y="score", color="score",
                             labels={"student_name": "ชื่อนักเรียน", "score": "คะแนน"},
                             color_continuous_scale="Greens")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ยังไม่มีข้อมูลนักเรียนในขณะนี้")
    except:
        st.error("ไม่สามารถเชื่อมต่อกับ Server ได้")
