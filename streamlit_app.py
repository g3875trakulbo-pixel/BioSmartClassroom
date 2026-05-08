import streamlit as st

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="BioAdaptive AI", layout="wide", initial_sidebar_state="expanded")

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Prompt', sans-serif; }
        
        :root {
            --dark-green: #006837;
            --light-green: #8CC63F;
            --yellow: #FBB040;
        }

        .grade-header {
            padding: 15px; border-radius: 10px; color: white;
            font-weight: bold; margin-top: 20px;
        }
        .m4 { background-color: var(--dark-green); border-left: 10px solid var(--yellow); }
        .m5 { background-color: #2E7D32; border-left: 10px solid var(--light-green); }
        .m6 { background-color: #43A047; border-left: 10px solid #C0CA33; }
        
        .stButton>button {
            border-radius: 20px; background-color: var(--dark-green); color: white;
            transition: 0.3s; width: 100%; height: 3em; font-weight: bold;
        }
        .stButton>button:hover { background-color: var(--light-green); border: none; color: white; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. COMPLETE QUESTION BANK (25 LESSONS) ---
QUIZ_BANK = {
    "ม.4-บทที่ 1: การศึกษาชีววิทยา": [{"q": "ขั้นตอนใดที่นำไปสู่การตั้งสมมติฐาน?", "a": ["การทดลอง", "การสังเกต", "การสรุปผล"], "correct": "การสังเกต"}],
    "ม.4-บทที่ 2: เคมีพื้นฐานของสิ่งมีชีวิต": [{"q": "หน่วยย่อยของ DNA คือ?", "a": ["กลูโคส", "นิวคลีโอไทด์", "กรดอะมิโน"], "correct": "นิวคลีโอไทด์"}],
    "ม.4-บทที่ 3: เซลล์และการทำงาน": [{"q": "ส่วนใดควบคุมการเข้าออกของสาร?", "a": ["ผนังเซลล์", "เยื่อหุ้มเซลล์", "ไรโบโซม"], "correct": "เยื่อหุ้มเซลล์"}],
    "ม.4-บทที่ 4: โครโมโซมและสารพันธุกรรม": [{"q": "Down Syndrome เกิดจากอะไร?", "a": ["โครโมโซมเกิน", "โครโมโซมขาด", "สลับที่"], "correct": "โครโมโซมเกิน"}],
    "ม.4-บทที่ 5: การถ่ายทอดลักษณะทางพันธุกรรม": [{"q": "Genotype แบบพาหะคือ?", "a": ["AA", "aa", "Aa"], "correct": "Aa"}],
    "ม.4-บทที่ 6: เทคโนโลยีทางดีเอ็นเอ": [{"q": "เอนไซม์ที่ใช้ตัดสาย DNA คือ?", "a": ["ไลเกส", "เอนไซม์ตัดจำเพาะ", "อะไมเลส"], "correct": "เอนไซม์ตัดจำเพาะ"}],
    "ม.4-บทที่ 7: วิวัฒนาการ": [{"q": "หลักฐานที่น่าเชื่อถือที่สุดในปัจจุบัน?", "a": ["ซากดึกดำบรรพ์", "ข้อมูลระดับโมเลกุล", "ภูมิศาสตร์"], "correct": "ข้อมูลระดับโมเลกุล"}],
    "ม.5-บทที่ 8: การสืบพันธุ์ของพืชดอก": [{"q": "ส่วนใดเจริญไปเป็นเมล็ด?", "a": ["รังไข่", "ออวุล", "กลีบดอก"], "correct": "ออวุล"}],
    "ม.5-บทที่ 9: โครงสร้างพืชดอก": [{"q": "เนื้อเยื่อลำเลียงน้ำคือ?", "a": ["Phloem", "Xylem", "Epidermis"], "correct": "Xylem"}],
    "ม.5-บทที่ 10: การลำเลียงของพืช": [{"q": "การคายน้ำส่วนใหญ่เกิดที่ใด?", "a": ["ราก", "ลำต้น", "ปากใบ"], "correct": "ปากใบ"}],
    "ม.5-บทที่ 11: การสังเคราะห์ด้วยแสง": [{"q": "ตัวรับอิเล็กตรอนสุดท้ายในปฏิกิริยาแสง?", "a": ["ATP", "NADPH", "NADP+"], "correct": "NADP+"}],
    "ม.5-บทที่ 12: การควบคุมการเติบโตพืช": [{"q": "ฮอร์โมนที่ช่วยให้ผลไม้สุก?", "a": ["ออกซิน", "เอทิลีน", "ไซโทไคนิน"], "correct": "เอทิลีน"}],
    "ม.5-บทที่ 13: ระบบย่อยอาหาร": [{"q": "ย่อยโปรตีนเริ่มที่ใด?", "a": ["ปาก", "กระเพาะ", "ลำไส้ใหญ่"], "correct": "กระเพาะ"}],
    "ม.5-บทที่ 14: ระบบหายใจ": [{"q": "บริเวณแลกเปลี่ยนแก๊สในปอดคือ?", "a": ["หลอดลม", "ถุงลม", "ขั้วปอด"], "correct": "ถุงลม"}],
    "ม.5-บทที่ 15: ระบบหมุนเวียนเลือด": [{"q": "เลือด O2 ต่ำเข้าหัวใจห้องใดก่อน?", "a": ["บนซ้าย", "บนขวา", "ล่างซ้าย"], "correct": "บนขวา"}],
    "ม.5-บทที่ 16: ระบบภูมิคุ้มกัน": [{"q": "วัคซีนคือภูมิคุ้มกันแบบใด?", "a": ["รับมา", "ก่อเอง", "ธรรมชาติ"], "correct": "ก่อเอง"}],
    "ม.5-บทที่ 17: ระบบขับถ่าย": [{"q": "ส่วนที่ทำหน้าที่กรองเลือดคือ?", "a": ["โบว์แมนส์", "โกลเมอรูลัส", "ท่อรวม"], "correct": "โกลเมอรูลัส"}],
    "ม.6-บทที่ 18: ระบบประสาท": [{"q": "สมองที่คุมการทรงตัวคือ?", "a": ["เซรีบรัม", "เซรีเบลลัม", "ไฮโพทาลามัส"], "correct": "เซรีเบลลัม"}],
    "ม.6-บทที่ 19: การเคลื่อนที่": [{"q": "อะมีบาเคลื่อนที่โดยใช้อะไร?", "a": ["แฟลเจลลา", "เท้าเทียม", "ซิเลีย"], "correct": "เท้าเทียม"}],
    "ม.6-บทที่ 20: ระบบต่อมไร้ท่อ": [{"q": "อินซูลินสร้างจากที่ใด?", "a": ["ตับ", "ตับอ่อน", "ต่อมหมวกไต"], "correct": "ตับอ่อน"}],
    "ม.6-บทที่ 21: ระบบสืบพันธุ์": [{"q": "ปฏิสนธิมักเกิดที่ใด?", "a": ["มดลูก", "ท่อนำไข่", "รังไข่"], "correct": "ท่อนำไข่"}],
    "ม.6-บทที่ 22: พฤติกรรมสัตว์": [{"q": "พฤติกรรมที่มีมาแต่กำเนิดคือ?", "a": ["Innate", "Learning", "Insight"], "correct": "Innate"}],
    "ม.6-บทที่ 23: ความหลากหลายทางชีวภาพ": [{"q": "อาณาจักรที่มีเซลล์โพรแคริโอต?", "a": ["Monera", "Protista", "Fungi"], "correct": "Monera"}],
    "ม.6-บทที่ 24: ระบบนิเวศและประชากร": [{"q": "ปรสิตคือความสัมพันธ์แบบใด?", "a": ["+/+", "+/0", "+/-"], "correct": "+/-"}],
    "ม.6-บทที่ 25: มนุษย์และความยั่งยืน": [{"q": "ทรัพยากรที่ใช้แล้วหมดไป?", "a": ["แสงแดด", "น้ำมัน", "น้ำ"], "correct": "น้ำมัน"}]
}

# --- 3. PAGE FUNCTIONS ---
def show_landing():
    st.markdown("<h1 style='text-align:center; color:#006837;'>🧬 BioAdaptive AI Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>ระบบวิเคราะห์และปรับเปลี่ยนเนื้อหาชีววิทยา รายบุคคล</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("### 🎓 สำหรับนักเรียน\nลงทะเบียนเพื่อเริ่มต้นบทเรียน AI")
        if st.button("เข้าสู่ระบบนักเรียน"):
            st.session_state.page = "register"
            st.rerun()
    with col2:
        st.warning("### 👨‍🏫 สำหรับคุณครู\nวิเคราะห์ข้อมูลสถิติของนักเรียน")
        if st.button("เข้าสู่ระบบแอดมิน"):
            st.info("ระบบแอดมินกำลังอยู่ในช่วงพัฒนา")

    st.divider()
    st.markdown("### 📚 ภาพรวมหลักสูตร 25 บทเรียน")
    c1, c2, c3 = st.columns(3)
    for g, color, col in [("ม.4", "m4", c1), ("ม.5", "m5", c2), ("ม.6", "m6", c3)]:
        with col:
            st.markdown(f'<div class="grade-header {color}">ระดับชั้น {g}</div>', unsafe_allow_html=True)
            lessons = [k for k in QUIZ_BANK.keys() if g in k]
            for l in lessons: st.caption(f"• {l.split(': ')[1]}")

def show_register():
    st.markdown("<h2 style='text-align:center;'>📝 ลงทะเบียนเข้าเรียน</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("reg_form"):
            name = st.text_input("ชื่อ-นามสกุล")
            sid = st.text_input("เลขที่ / รหัสประจำตัว")
            grade = st.selectbox("ระดับชั้น", ["ม.4", "ม.5", "ม.6"])
            if st.form_submit_button("ยืนยันการลงทะเบียน"):
                if name and sid:
                    st.session_state.user = {"name": name, "id": sid, "grade": grade}
                    st.session_state.page = "lesson"
                    st.rerun()
                else:
                    st.error("กรุณากรอกข้อมูลให้ครบ")
        if st.button("⬅️ กลับ"):
            st.session_state.page = "landing"
            st.rerun()

def show_lesson():
    user = st.session_state.user
    st.sidebar.success(f"👤 นักเรียน: {user['name']}")
    st.sidebar.caption(f"ชั้น: {user['grade']} | เลขที่: {user['id']}")
    
    # Filter lessons by student's grade
    lesson_options = [k for k in QUIZ_BANK.keys() if user['grade'] in k]
    selected = st.sidebar.selectbox("เลือกบทเรียนที่ต้องการ", lesson_options)
    
    if st.sidebar.button("🏠 กลับหน้าหลัก / ออกจากระบบ"):
        st.session_state.clear()
        st.session_state.page = "landing"
        st.rerun()

    st.title(f"📖 {selected}")
    score_key = f"score_{selected}"
    
    if score_key not in st.session_state:
        st.subheader("📝 Pre-test วิเคราะห์ระดับ")
        q_data = QUIZ_BANK[selected][0]
        with st.form(f"f_{selected}"):
            ans = st.radio(q_data["q"], q_data["a"])
            if st.form_submit_button("ส่งคำตอบเพื่อวิเคราะห์"):
                score = 100 if ans == q_data["correct"] else 0
                st.session_state[score_key] = score
                st.rerun()
    else:
        score = st.session_state[score_key]
        lv, clr = ("Bloom (Advanced) 🌸", "#006837") if score == 100 else ("Seed (Beginner) 🌱", "#FBB040")
        
        st.markdown(f"""
            <div style="background-color:{clr}; padding:20px; border-radius:15px; color:white;">
                <h3>ระดับของคุณ: {lv}</h3>
                <p>ผลการวิเคราะห์: AI กำลังปรับปรุงเนื้อหาให้เหมาะกับความรู้พื้นฐานของคุณ</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.subheader("📚 เนื้อหาสำหรับคุณ")
        st.info("กำลังโหลดเนื้อหาแบบ Adaptive Learning...")
        
        if st.button("🔄 ทำการทดสอบใหม่"):
            del st.session_state[score_key]
            st.rerun()

# --- 4. MAIN ---
def main():
    apply_custom_style()
    if "page" not in st.session_state:
        st.session_state.page = "landing"
        
    if st.session_state.page == "landing":
        show_landing()
    elif st.session_state.page == "register":
        show_register()
    elif st.session_state.page == "lesson":
        show_lesson()

if __name__ == "__main__":
    main()
