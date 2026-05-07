import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="BioAdaptive Learning AI",
    layout="wide"
)

# ==================================================
# DATABASE
# ==================================================

@st.cache_resource
def init_db():

    conn = sqlite3.connect(
        "bio_adaptive_v3.db",
        check_same_thread=False
    )

    c = conn.cursor()

    # ตารางนักเรียน
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            sid TEXT PRIMARY KEY,
            fname TEXT,
            lname TEXT,
            grade_lvl TEXT,
            level TEXT
        )
    """)

    # ตารางผลการเรียน
    c.execute("""
        CREATE TABLE IF NOT EXISTS learning_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sid TEXT,
            chapter TEXT,
            score REAL,
            timestamp DATETIME
        )
    """)

    conn.commit()

    return conn


conn = init_db()

# ==================================================
# PLACEMENT TEST
# ==================================================

PLACEMENT_QUESTIONS = [

    {
        "q": "หน่วยที่เล็กที่สุดของสิ่งมีชีวิตคืออะไร?",
        "a": [
            "อะตอม",
            "เซลล์",
            "เนื้อเยื่อ",
            "อวัยวะ"
        ],
        "c": "เซลล์"
    },

    {
        "q": "กระบวนการใดที่พืชสร้างอาหาร?",
        "a": [
            "การหายใจ",
            "การคายน้ำ",
            "การสังเคราะห์ด้วยแสง",
            "การดูดซึม"
        ],
        "c": "การสังเคราะห์ด้วยแสง"
    },

    {
        "q": "มนุษย์มีโครโมโซมกี่แท่ง?",
        "a": [
            "23 แท่ง",
            "44 แท่ง",
            "46 แท่ง",
            "48 แท่ง"
        ],
        "c": "46 แท่ง"
    }
]

# ==================================================
# LESSON DATA
# ==================================================

LESSON_DATA = {

    "1. การศึกษาชีววิทยา": {

        "content": """
ชีววิทยาคือการศึกษาเกี่ยวกับสิ่งมีชีวิต
โดยใช้กระบวนการทางวิทยาศาสตร์
        """,

        "quiz": [

            {
                "q": "ข้อใดไม่ใช่กระบวนการทางวิทยาศาสตร์?",

                "a": [
                    "การสังเกต",
                    "การตั้งสมมติฐาน",
                    "การใช้โชคชะตา",
                    "การสรุปผล"
                ],

                "c": "การใช้โชคชะตา"
            }

        ]
    },

    "2. เคมีที่เป็นพื้นฐานของสิ่งมีชีวิต": {

        "content": """
น้ำเป็นสารประกอบสำคัญในเซลล์
และสิ่งมีชีวิตทุกชนิด
        """,

        "quiz": [

            {
                "q": "พันธะที่ยึดเหนี่ยวโมเลกุลน้ำคือ?",

                "a": [
                    "พันธะไอออนิก",
                    "พันธะไฮโดรเจน",
                    "พันธะโลหะ",
                    "พันธะโควาเลนต์"
                ],

                "c": "พันธะไฮโดรเจน"
            }

        ]
    }

}

# ==================================================
# HELPER FUNCTION
# ==================================================

def get_student_level(score, total):

    percent = (score / total) * 100

    if percent >= 80:
        return "Advanced"

    elif percent >= 50:
        return "Intermediate"

    else:
        return "Beginner"

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🧬 BioAdaptive v3")

    menu = st.radio(

        "เมนูหลัก",

        [
            "👤 ลงทะเบียน",
            "📝 วิเคราะห์ระดับ",
            "📖 บทเรียน",
            "📊 รายงานครู"
        ]
    )

# ==================================================
# REGISTER
# ==================================================

if menu == "👤 ลงทะเบียน":

    st.header("👤 ลงทะเบียนนักเรียน")

    with st.form("register_form"):

        sid = st.text_input("รหัสนักเรียน")
        fname = st.text_input("ชื่อ")
        lname = st.text_input("นามสกุล")

        grade = st.selectbox(
            "ระดับชั้น",
            ["ม.4", "ม.5", "ม.6"]
        )

        submit = st.form_submit_button("บันทึก")

        if submit:

            if sid == "":

                st.error("กรุณากรอกรหัสนักเรียน")

            else:

                c = conn.cursor()

                c.execute(
                    """
                    INSERT OR REPLACE INTO students
                    (sid, fname, lname, grade_lvl)
                    VALUES (?, ?, ?, ?)
                    """,
                    (sid, fname, lname, grade)
                )

                conn.commit()

                st.success("✅ บันทึกข้อมูลสำเร็จ")

# ==================================================
# PLACEMENT TEST
# ==================================================

elif menu == "📝 วิเคราะห์ระดับ":

    st.header("📝 แบบทดสอบวิเคราะห์ระดับ")

    sid = st.text_input("รหัสนักเรียน")

    if sid:

        score = 0

        with st.form("placement_form"):

            for i, q in enumerate(PLACEMENT_QUESTIONS):

                ans = st.radio(
                    f"{i+1}. {q['q']}",
                    q["a"],
                    key=f"p_{i}"
                )

                if ans == q["c"]:
                    score += 1

            submit = st.form_submit_button("ส่งคำตอบ")

            if submit:

                level = get_student_level(
                    score,
                    len(PLACEMENT_QUESTIONS)
                )

                c = conn.cursor()

                c.execute(
                    """
                    UPDATE students
                    SET level=?
                    WHERE sid=?
                    """,
                    (level, sid)
                )

                conn.commit()

                st.success(
                    f"✅ ระดับของคุณคือ {level}"
                )

# ==================================================
# LESSON
# ==================================================

elif menu == "📖 บทเรียน":

    st.header("📖 ระบบบทเรียน")

    sid = st.text_input("รหัสนักเรียน")

    if sid:

        user = pd.read_sql(
            "SELECT * FROM students WHERE sid=?",
            conn,
            params=(sid,)
        )

        if not user.empty:

            level = user.iloc[0]["level"]

            if pd.isna(level):
                level = "ยังไม่ได้ประเมิน"

            st.info(
                f"""
ชื่อ: {user.iloc[0]['fname']}
ระดับ: {level}
                """
            )

            chapter = st.selectbox(
                "เลือกบทเรียน",
                list(LESSON_DATA.keys())
            )

            tab1, tab2 = st.tabs([
                "📚 เนื้อหา",
                "✍️ แบบทดสอบ"
            ])

            # ======================================
            # CONTENT
            # ======================================

            with tab1:

                st.subheader(chapter)

                if level == "Beginner":

                    st.warning(
                        "💡 ระบบแนะนำเนื้อหาพื้นฐาน"
                    )

                st.write(
                    LESSON_DATA[chapter]["content"]
                )

            # ======================================
            # QUIZ
            # ======================================

            with tab2:

                score = 0

                with st.form(f"quiz_{chapter}"):

                    for i, q in enumerate(
                        LESSON_DATA[chapter]["quiz"]
                    ):

                        ans = st.radio(
                            q["q"],
                            q["a"],
                            key=f"quiz_{i}"
                        )

                        if ans == q["c"]:
                            score += 1

                    submit = st.form_submit_button(
                        "บันทึกคะแนน"
                    )

                    if submit:

                        percent = (
                            score /
                            len(
                                LESSON_DATA[chapter]["quiz"]
                            )
                        ) * 100

                        c = conn.cursor()

                        c.execute(
                            """
                            INSERT INTO learning_logs
                            (sid, chapter, score, timestamp)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                sid,
                                chapter,
                                percent,
                                datetime.now()
                            )
                        )

                        conn.commit()

                        st.success(
                            f"✅ คะแนนของคุณ {percent}%"
                        )

                        st.balloons()

        else:

            st.error("❌ ไม่พบรหัสนักเรียน")

# ==================================================
# TEACHER DASHBOARD
# ==================================================

elif menu == "📊 รายงานครู":

    st.header("👨‍🏫 Dashboard คุณครู")

    pwd = st.text_input(
        "รหัสผ่าน",
        type="password"
    )

    if pwd == "admin123":

        # ======================================
        # STUDENT TABLE
        # ======================================

        st.subheader("📋 รายชื่อนักเรียน")

        df_students = pd.read_sql(
            """
            SELECT
                sid,
                fname,
                lname,
                grade_lvl,
                level
            FROM students
            """,
            conn
        )

        st.dataframe(
            df_students,
            use_container_width=True
        )

        # ======================================
        # CHART
        # ======================================

        st.subheader("📈 กราฟระดับความรู้")

        if not df_students.empty:

            level_count = (
                df_students["level"]
                .fillna("ยังไม่ได้ประเมิน")
                .value_counts()
                .reset_index()
            )

            level_count.columns = [
                "Level",
                "Count"
            ]

            fig = px.bar(
                level_count,
                x="Level",
                y="Count",
                text="Count",
                title="จำนวนนักเรียนแต่ละระดับ"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ======================================
        # LEARNING LOGS
        # ======================================

        st.subheader("📚 ประวัติการเรียน")

        df_logs = pd.read_sql(
            """
            SELECT
                sid,
                chapter,
                score,
                timestamp
            FROM learning_logs
            """,
            conn
        )

        st.dataframe(
            df_logs,
            use_container_width=True
        )

    elif pwd != "":

        st.error("❌ รหัสผ่านไม่ถูกต้อง")