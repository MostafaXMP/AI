import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import datetime, date

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UniReg — Course Registration System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --navy: #0B1628;
    --blue: #1A3A6B;
    --accent: #3B82F6;
    --gold: #F59E0B;
    --green: #10B981;
    --red: #EF4444;
    --light: #F8FAFC;
    --card: #FFFFFF;
    --border: #E2E8F0;
    --text: #1E293B;
    --muted: #64748B;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
}

.main { background: #F1F5F9; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--navy) !important;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stRadio label { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] .stRadio label:hover { color: white !important; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 60%, #1E40AF 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '🎓';
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.15;
}
.hero h1 { color: white !important; margin: 0; font-size: 1.9rem; }
.hero p { color: #93C5FD; margin: 0.3rem 0 0; font-size: 1rem; }

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    flex: 1;
    min-width: 140px;
    border-left: 4px solid var(--accent);
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
}
.metric-card .num { font-size: 2rem; font-weight: 800; font-family: 'Syne', sans-serif; color: var(--navy); }
.metric-card .label { color: var(--muted); font-size: 0.85rem; margin-top: 0.2rem; }
.metric-card.gold { border-left-color: var(--gold); }
.metric-card.green { border-left-color: var(--green); }
.metric-card.red { border-left-color: var(--red); }

/* Section header */
.sec-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--navy);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-green { background: #D1FAE5; color: #065F46; }
.badge-red { background: #FEE2E2; color: #991B1B; }
.badge-blue { background: #DBEAFE; color: #1E40AF; }
.badge-gold { background: #FEF3C7; color: #92400E; }

/* Login card */
.login-wrap {
    max-width: 420px;
    margin: 4rem auto;
    background: white;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px rgba(11,22,40,0.12);
}

/* stButton tweaks */
div[data-testid="stButton"] > button {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}

/* Logout button inside sidebar */
section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    background: #1E3A5F !important;
    color: #F8FAFC !important;
    border: 1px solid #3B82F6 !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: #EF4444 !important;
    border-color: #EF4444 !important;
    color: white !important;
}

/* Table */
.styled-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.styled-table th {
    background: var(--navy);
    color: white;
    padding: 0.6rem 1rem;
    text-align: left;
    font-family: 'Syne', sans-serif;
}
.styled-table td { padding: 0.6rem 1rem; border-bottom: 1px solid var(--border); }
.styled-table tr:hover td { background: #F8FAFC; }
</style>
""", unsafe_allow_html=True)

# ─── Database Setup ──────────────────────────────────────────────────────────
DB = "university.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student','admin','faculty')),
        university_id TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        credits INTEGER NOT NULL,
        capacity INTEGER NOT NULL,
        instructor_id INTEGER,
        schedule TEXT,
        room TEXT,
        semester TEXT NOT NULL,
        prerequisite_id INTEGER,
        FOREIGN KEY(instructor_id) REFERENCES users(id),
        FOREIGN KEY(prerequisite_id) REFERENCES courses(id)
    );

    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        semester TEXT NOT NULL,
        enrolled_at TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        UNIQUE(student_id, course_id, semester),
        FOREIGN KEY(student_id) REFERENCES users(id),
        FOREIGN KEY(course_id) REFERENCES courses(id)
    );

    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        semester TEXT NOT NULL,
        grade REAL,
        FOREIGN KEY(student_id) REFERENCES users(id),
        FOREIGN KEY(course_id) REFERENCES courses(id)
    );

    CREATE TABLE IF NOT EXISTS enrollment_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        semester TEXT UNIQUE NOT NULL,
        max_credits INTEGER NOT NULL DEFAULT 21,
        min_credits INTEGER NOT NULL DEFAULT 12,
        add_deadline TEXT NOT NULL,
        drop_deadline TEXT NOT NULL
    );
    """)

    # Seed data
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        users = [
            ("Admin User", "admin@uni.edu", hash_pw("admin123"), "admin", "ADM-001"),
            ("Ahmed Hassan", "ahmed@uni.edu", hash_pw("student123"), "student", "STU-001"),
            ("Sara Mohamed", "sara@uni.edu", hash_pw("student123"), "student", "STU-002"),
            ("Dr. Khaled Nour", "khaled@uni.edu", hash_pw("faculty123"), "faculty", "FAC-001"),
            ("Dr. Rania Saleh", "rania@uni.edu", hash_pw("faculty123"), "faculty", "FAC-002"),
        ]
        c.executemany("INSERT INTO users(name,email,password,role,university_id) VALUES(?,?,?,?,?)", users)

    c.execute("SELECT COUNT(*) FROM courses")
    if c.fetchone()[0] == 0:
        courses = [
            ("CS101", "Introduction to Programming", "Computer Science", 3, 30, 4, "Sun/Tue 9:00-10:30", "Hall A1", "Fall 2026", None),
            ("CS201", "Data Structures", "Computer Science", 3, 25, 4, "Mon/Wed 11:00-12:30", "Hall B2", "Fall 2026", 1),
            ("CS301", "Database Systems", "Computer Science", 3, 20, 5, "Sun/Tue 1:00-2:30", "Lab C1", "Fall 2026", 2),
            ("MATH101", "Calculus I", "Mathematics", 4, 35, 5, "Mon/Wed/Thu 8:00-9:00", "Hall D3", "Fall 2026", None),
            ("ENG101", "Technical Writing", "English", 2, 40, None, "Tue/Thu 10:00-11:00", "Hall E1", "Fall 2026", None),
            ("CS401", "Software Engineering", "Computer Science", 3, 20, 4, "Mon/Wed 2:00-3:30", "Lab C2", "Fall 2026", 3),
        ]
        c.executemany("""INSERT INTO courses(code,name,department,credits,capacity,instructor_id,
                         schedule,room,semester,prerequisite_id) VALUES(?,?,?,?,?,?,?,?,?,?)""", courses)

    c.execute("SELECT COUNT(*) FROM enrollments")
    if c.fetchone()[0] == 0:
        enrollments = [
            (2, 1, "Fall 2026", datetime.now().isoformat(), "active"),
            (2, 4, "Fall 2026", datetime.now().isoformat(), "active"),
            (3, 1, "Fall 2026", datetime.now().isoformat(), "active"),
            (3, 5, "Fall 2026", datetime.now().isoformat(), "active"),
        ]
        c.executemany("INSERT INTO enrollments(student_id,course_id,semester,enrolled_at,status) VALUES(?,?,?,?,?)", enrollments)

    c.execute("SELECT COUNT(*) FROM grades")
    if c.fetchone()[0] == 0:
        grades = [
            (2, 1, "Spring 2026", 85.0),
            (2, 4, "Spring 2026", 90.0),
            (3, 1, "Spring 2026", 78.0),
        ]
        c.executemany("INSERT INTO grades(student_id,course_id,semester,grade) VALUES(?,?,?,?)", grades)

    c.execute("SELECT COUNT(*) FROM enrollment_rules")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO enrollment_rules(semester,max_credits,min_credits,add_deadline,drop_deadline)
                      VALUES('Fall 2026', 21, 12, '2026-09-15', '2026-10-15')""")

    conn.commit()
    conn.close()

# ─── Auth ────────────────────────────────────────────────────────────────────
def login(uid, pw):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, role FROM users WHERE university_id=? AND password=?",
              (uid, hash_pw(pw)))
    row = c.fetchone()
    conn.close()
    return row  # (id, name, role) or None

# ─── Helpers ─────────────────────────────────────────────────────────────────
def get_courses(semester="Fall 2026"):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT c.id, c.code, c.name, c.department, c.credits, c.capacity,
               c.schedule, c.room, c.semester,
               c.instructor_id,
               u.name as instructor,
               p.name as prerequisite,
               (SELECT COUNT(*) FROM enrollments e
                WHERE e.course_id=c.id AND e.semester=c.semester AND e.status='active') as enrolled
        FROM courses c
        LEFT JOIN users u ON u.id=c.instructor_id
        LEFT JOIN courses p ON p.id=c.prerequisite_id
        WHERE c.semester=?
    """, conn, params=(semester,))
    conn.close()
    return df

def get_student_enrollments(student_id, semester="Fall 2026"):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT c.id, c.code, c.name, c.credits, c.schedule, c.room,
               u.name as instructor, e.enrolled_at
        FROM enrollments e
        JOIN courses c ON c.id=e.course_id
        LEFT JOIN users u ON u.id=c.instructor_id
        WHERE e.student_id=? AND e.semester=? AND e.status='active'
    """, conn, params=(student_id, semester))
    conn.close()
    return df

def get_student_grades(student_id):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT c.name, c.credits, g.semester, g.grade
        FROM grades g
        JOIN courses c ON c.id=g.course_id
        WHERE g.student_id=?
    """, conn, params=(student_id,))
    conn.close()
    return df

def get_faculty_courses(faculty_id, semester="Fall 2026"):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT c.id, c.code, c.name, c.schedule,
               (SELECT COUNT(*) FROM enrollments e
                WHERE e.course_id=c.id AND e.semester=c.semester AND e.status='active') as enrolled,
               c.capacity
        FROM courses c WHERE c.instructor_id=? AND c.semester=?
    """, conn, params=(faculty_id, semester))
    conn.close()
    return df

def get_enrolled_students(course_id, semester="Fall 2026"):
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT u.university_id, u.name, u.email, e.enrolled_at
        FROM enrollments e
        JOIN users u ON u.id=e.student_id
        WHERE e.course_id=? AND e.semester=? AND e.status='active'
    """, conn, params=(course_id, semester))
    conn.close()
    return df

def enroll_student(student_id, course_id, semester="Fall 2026"):
    conn = get_conn()
    c = conn.cursor()
    try:
        # Check capacity
        c.execute("""SELECT capacity,
                    (SELECT COUNT(*) FROM enrollments e WHERE e.course_id=? AND e.semester=? AND e.status='active') as cnt
                    FROM courses WHERE id=?""", (course_id, semester, course_id))
        row = c.fetchone()
        if row[1] >= row[0]:
            return False, "Course is full."
        # Check max credit limit
        rules = get_enrollment_rules(semester)
        c.execute("""SELECT COALESCE(SUM(cr.credits),0) FROM enrollments e
                       JOIN courses cr ON cr.id=e.course_id
                       WHERE e.student_id=? AND e.semester=? AND e.status='active'""", (student_id, semester))
        current_credits = c.fetchone()[0]
        c.execute("SELECT credits FROM courses WHERE id=?", (course_id,))
        new_credits = c.fetchone()[0]
        if current_credits + new_credits > rules["max_credits"]:
            return False, f"Credit limit exceeded. Max allowed: {rules['max_credits']} credits (you have {current_credits})."

        # Check prereq
        c.execute("SELECT prerequisite_id FROM courses WHERE id=?", (course_id,))
        prereq = c.fetchone()[0]
        if prereq:
            c.execute("""SELECT id FROM enrollments WHERE student_id=? AND course_id=? AND status='active'
                         UNION SELECT id FROM grades WHERE student_id=? AND course_id=?""",
                      (student_id, prereq, student_id, prereq))
            if not c.fetchone():
                conn2 = get_conn()
                pname = conn2.execute("SELECT name FROM courses WHERE id=?", (prereq,)).fetchone()[0]
                conn2.close()
                return False, f"Missing prerequisite: {pname}"
        c.execute("INSERT INTO enrollments(student_id,course_id,semester,enrolled_at,status) VALUES(?,?,?,?,?)",
                  (student_id, course_id, semester, datetime.now().isoformat(), "active"))
        conn.commit()
        return True, "Successfully registered!"
    except sqlite3.IntegrityError:
        return False, "Already registered in this course."
    finally:
        conn.close()

def get_enrollment_rules(semester="Fall 2026"):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT max_credits, min_credits, add_deadline, drop_deadline FROM enrollment_rules WHERE semester=?", (semester,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"max_credits": row[0], "min_credits": row[1], "add_deadline": row[2], "drop_deadline": row[3]}
    return {"max_credits": 21, "min_credits": 12, "add_deadline": "2026-09-15", "drop_deadline": "2026-10-15"}

def drop_course(student_id, course_id, semester="Fall 2026"):
    conn = get_conn()
    c = conn.cursor()
    # Guard: never drop a course that has a recorded grade
    c.execute("SELECT id FROM grades WHERE student_id=? AND course_id=?", (student_id, course_id))
    if c.fetchone():
        conn.close()
        return False, "Cannot drop a completed course with a recorded grade."
    # Check drop deadline
    rules = get_enrollment_rules(semester)
    today = date.today().isoformat()
    if today > rules["drop_deadline"]:
        conn.close()
        return False, f"Drop deadline has passed ({rules['drop_deadline']}). Cannot drop this course."

    c.execute("UPDATE enrollments SET status='dropped' WHERE student_id=? AND course_id=? AND semester=?",
              (student_id, course_id, semester))
    conn.commit()
    conn.close()
    return True, "Course dropped successfully." 

# ─── Pages ───────────────────────────────────────────────────────────────────

def page_login():
    st.markdown("""
    <div style='text-align:center; padding: 2rem 0 1rem;'>
        <div style='font-size:3rem;'>🎓</div>
        <h1 style='font-family:Syne,sans-serif; font-size:2rem; color:#0B1628; margin:0.3rem 0;'>UniReg</h1>
        <p style='color:#64748B;'>University Course Registration System</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.container():
            st.markdown("#### Sign In")
            uid = st.text_input("University ID", placeholder="e.g. STU-001")
            pw = st.text_input("Password", type="password", placeholder="••••••••")
            st.caption("Demo → Student: STU-001 / student123 | Admin: ADM-001 / admin123 | Faculty: FAC-001 / faculty123")
            if st.button("Login →", use_container_width=True, type="primary"):
                result = login(uid, pw)
                if result:
                    st.session_state.user_id = result[0]
                    st.session_state.user_name = result[1]
                    st.session_state.user_role = result[2]
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

def page_student_dashboard():
    uid = st.session_state.user_id
    name = st.session_state.user_name

    st.markdown(f"""
    <div class='hero'>
        <h1>Welcome back, {name.split()[0]}! 👋</h1>
        <p>Fall 2026 — University Course Registration System</p>
    </div>
    """, unsafe_allow_html=True)

    enrolled = get_student_enrollments(uid)
    all_courses = get_courses()
    grades = get_student_grades(uid)
    total_credits = enrolled['credits'].sum() if not enrolled.empty else 0
    def score_to_gpa(avg):
        if avg >= 90: return 4.0
        elif avg >= 80: return 3.0
        elif avg >= 70: return 2.0
        elif avg >= 60: return 1.0
        return 0.0
    gpa = score_to_gpa(grades['grade'].mean()) if not grades.empty else 0.0

    st.markdown(f"""
    <div class='metric-row'>
        <div class='metric-card'><div class='num'>{len(enrolled)}</div><div class='label'>Enrolled Courses</div></div>
        <div class='metric-card gold'><div class='num'>{total_credits}</div><div class='label'>Total Credits</div></div>
        <div class='metric-card green'><div class='num'>{gpa}</div><div class='label'>Current GPA</div></div>
        <div class='metric-card red'><div class='num'>{len(all_courses)}</div><div class='label'>Total Courses</div></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📚 Register for Courses", "🗑️ Drop a Course", "📅 My Schedule", "🕓 Registration History"])

    # ── Tab 1: Register ──────────────────────────────────────────────────────
    with tab1:
        st.markdown("<div class='sec-header'>Available Courses — Fall 2026</div>", unsafe_allow_html=True)
        enrolled_ids = set(enrolled['id'].tolist()) if not enrolled.empty else set()

        search = st.text_input("🔍 Search by name, code, or department", "")
        display = all_courses.copy()
        if search:
            display = display[display.apply(lambda r: search.lower() in r['name'].lower()
                              or search.lower() in r['code'].lower()
                              or search.lower() in r['department'].lower(), axis=1)]

        available = display[~display['id'].isin(enrolled_ids)]
        if available.empty:
            st.info("You are registered in all available courses.")
        for _, row in available.iterrows():
            seats_left = row['capacity'] - row['enrolled']
            with st.expander(f"**{row['code']}** — {row['name']}  |  {row['department']}  |  {row['credits']} cr"):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"📖 **Prereq:** {row['prerequisite'] or 'None'}")
                c2.markdown(f"👨‍🏫 **Instructor:** {row['instructor'] or 'TBA'}")
                c3.markdown(f"🕐 **Schedule:** {row['schedule']}")
                c1.markdown(f"🏫 **Room:** {row['room']}")
                c2.markdown(f"👥 **Seats:** {seats_left}/{row['capacity']} left")
                if seats_left == 0:
                    st.markdown("<span class='badge badge-red'>Full — No seats available</span>", unsafe_allow_html=True)
                else:
                    if st.button(f"Register for {row['code']}", key=f"reg_{row['id']}"):
                        ok, msg = enroll_student(uid, row['id'])
                        if ok:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

    # ── Tab 2: Drop ──────────────────────────────────────────────────────────
    with tab2:
        st.markdown("<div class='sec-header'>Currently Enrolled Courses</div>", unsafe_allow_html=True)
        if enrolled.empty:
            st.info("You are not enrolled in any courses this semester.")
        else:
            # Courses with existing grades = already completed, cannot be dropped
            conn = get_conn()
            graded_ids = set(pd.read_sql_query(
                "SELECT course_id FROM grades WHERE student_id=?", conn, params=(uid,)
            )['course_id'].tolist())
            conn.close()

            for _, row in enrolled.iterrows():
                c1, c2, c3 = st.columns([3, 2, 1])
                c1.markdown(f"**{row['code']}** — {row['name']}")
                c2.markdown(f"\U0001f550 {row['schedule']}")
                if row['id'] in graded_ids:
                    c3.markdown("<span class='badge badge-gold'>Completed ✓</span>", unsafe_allow_html=True)
                else:
                    if c3.button("Drop", key=f"drop_{row['id']}", type="secondary"):
                        ok, msg = drop_course(uid, row['id'])
                        if ok:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

    # ── Tab 3: Schedule ──────────────────────────────────────────────────────
    with tab3:
        st.markdown("<div class='sec-header'>My Weekly Schedule — Fall 2026</div>", unsafe_allow_html=True)

        # Only show active courses that are NOT already graded (past semesters)
        conn = get_conn()
        graded_ids = set(pd.read_sql_query(
            "SELECT course_id FROM grades WHERE student_id=?", conn, params=(uid,)
        )['course_id'].tolist())
        conn.close()

        active_schedule = enrolled[~enrolled['id'].isin(graded_ids)]

        if active_schedule.empty:
            st.info("No active courses in your schedule this semester.")
        else:
            for _, row in active_schedule.iterrows():
                st.markdown(f"""
                <div style='background:white;border-radius:10px;padding:1rem 1.2rem;
                     margin-bottom:0.7rem;border-left:4px solid #3B82F6;
                     box-shadow:0 1px 6px rgba(0,0,0,0.06);'>
                    <strong>{row['code']}</strong> — {row['name']}<br>
                    <span style='color:#64748B;font-size:0.88rem;'>📅 {row['schedule']} &nbsp;|&nbsp; 🏫 {row['room']} &nbsp;|&nbsp; 👨‍🏫 {row['instructor'] or 'TBA'}</span>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 4: Registration History ─────────────────────────────────────────
    with tab4:
        st.markdown("<div class='sec-header'>Registration History — All Semesters</div>", unsafe_allow_html=True)
        conn = get_conn()
        history = pd.read_sql_query("""
            SELECT c.code, c.name, c.credits, c.department,
                   e.semester, e.enrolled_at, e.status,
                   g.grade
            FROM enrollments e
            JOIN courses c ON c.id=e.course_id
            LEFT JOIN grades g ON g.student_id=e.student_id AND g.course_id=e.course_id
            WHERE e.student_id=?
            ORDER BY e.enrolled_at DESC
        """, conn, params=(uid,))
        conn.close()

        if history.empty:
            st.info("No registration history found.")
        else:
            for _, row in history.iterrows():
                if row['status'] == 'active':
                    badge = "<span class='badge badge-green'>Active</span>"
                elif row['status'] == 'dropped':
                    badge = "<span class='badge badge-red'>Dropped</span>"
                else:
                    badge = "<span class='badge badge-blue'>Completed</span>"

                grade_txt = f"{row['grade']:.1f}%" if pd.notna(row['grade']) else "—"
                c1, c2, c3, c4, c5 = st.columns([1.2, 2.5, 1.2, 1, 1])
                c1.markdown(f"**{row['code']}**")
                c2.write(row['name'])
                c3.write(row['semester'])
                c4.write(grade_txt)
                c5.markdown(badge, unsafe_allow_html=True)

def page_gpa():
    uid = st.session_state.user_id
    st.markdown("""<div class='hero'><h1>📊 Grades & GPA</h1><p>Academic performance overview</p></div>""", unsafe_allow_html=True)

    grades = get_student_grades(uid)
    if grades.empty:
        st.info("No grade records found.")
        return

    def letter(g):
        if g >= 90: return "A"
        elif g >= 80: return "B"
        elif g >= 70: return "C"
        elif g >= 60: return "D"
        return "F"

    grades['Letter'] = grades['grade'].apply(letter)
    def to_gpa(avg):
        # 90-100 -> ~4.0, 80-89 -> ~3.0, 70-79 -> ~2.0, 60-69 -> ~1.0, <60 -> 0
        if avg >= 90: return 4.0
        elif avg >= 80: return 3.0
        elif avg >= 70: return 2.0
        elif avg >= 60: return 1.0
        return 0.0
    gpa_val = to_gpa(grades['grade'].mean())

    st.markdown(f"""
    <div class='metric-row'>
        <div class='metric-card green'><div class='num'>{gpa_val}</div><div class='label'>Cumulative GPA (4.0)</div></div>
        <div class='metric-card'><div class='num'>{len(grades)}</div><div class='label'>Courses Completed</div></div>
        <div class='metric-card gold'><div class='num'>{int(grades['grade'].mean())}%</div><div class='label'>Average Score</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-header'>Transcript</div>", unsafe_allow_html=True)
    for _, row in grades.iterrows():
        badge_cls = "badge-green" if row['Letter'] in ['A','B'] else "badge-gold" if row['Letter']=='C' else "badge-red"
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        c1.write(row['name'])
        c2.write(row['semester'])
        c3.write(f"{row['grade']:.1f}%")
        c4.markdown(f"<span class='badge {badge_cls}'>{row['Letter']}</span>", unsafe_allow_html=True)

    st.bar_chart(grades.set_index('name')['grade'])

def get_faculty_list():
    conn = get_conn()
    df = pd.read_sql_query("SELECT id, name FROM users WHERE role='faculty'", conn)
    conn.close()
    return df

def page_admin():
    st.markdown("""<div class='hero'><h1>⚙️ Admin Panel</h1><p>Manage courses, users, and enrollment</p></div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📚 Manage Courses", "👥 All Students", "📈 Reports", "⚙️ Enrollment Rules"])

    with tab1:
        # ── Course Catalog with Edit/Delete ──────────────────────────────────
        st.markdown("<div class='sec-header'>Course Catalog</div>", unsafe_allow_html=True)
        courses = get_courses()
        faculty_df = get_faculty_list()
        faculty_map = {int(k): v for k, v in zip(faculty_df['id'], faculty_df['name'])}  # id -> name
        faculty_options = {row['name']: row['id'] for _, row in faculty_df.iterrows()}  # name -> id

        for _, course in courses.iterrows():
            has_enrollments = course['enrolled'] > 0
            with st.expander(f"**{course['code']}** — {course['name']}  |  👥 {course['enrolled']}/{course['capacity']}  |  👨‍🏫 {course['instructor'] or 'TBA'}"):
                with st.form(key=f"edit_{course['id']}"):
                    ec1, ec2 = st.columns(2)
                    new_name     = ec1.text_input("Course Name", value=course['name'])
                    new_dept     = ec2.text_input("Department",  value=course['department'])
                    new_credits  = ec1.number_input("Credits",   value=int(course['credits']),  min_value=1, max_value=6)
                    new_capacity = ec2.number_input(f"Capacity (min: {int(course['enrolled'])} enrolled)", value=int(course['capacity']), min_value=max(1, int(course['enrolled'])), max_value=200)
                    new_schedule = ec1.text_input("Schedule",    value=course['schedule'] or "")
                    new_room     = ec2.text_input("Room",        value=course['room'] or "")

                    # Instructor dropdown
                    instr_names = ["None"] + list(faculty_options.keys())
                    current_instr_name = faculty_map.get(int(course['instructor_id'])) if pd.notna(course['instructor_id']) else None
                    default_idx = instr_names.index(current_instr_name) if current_instr_name in instr_names else 0
                    new_instr_name = st.selectbox("Instructor", instr_names, index=default_idx)
                    new_instr_id = faculty_options.get(new_instr_name) if new_instr_name != "None" else None

                    bc1, bc2 = st.columns([1, 1])
                    save_btn   = bc1.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                    delete_btn = bc2.form_submit_button("🗑️ Delete Course",  type="secondary", use_container_width=True)

                    if save_btn:
                        conn = get_conn()
                        conn.execute("""UPDATE courses SET name=?, department=?, credits=?, capacity=?,
                                         schedule=?, room=?, instructor_id=? WHERE id=?""",
                                     (new_name, new_dept, new_credits, new_capacity,
                                      new_schedule, new_room, new_instr_id, course['id']))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ {course['code']} updated!")
                        st.rerun()

                    if delete_btn:
                        if has_enrollments:
                            st.error(f"❌ Cannot delete — {course['enrolled']} student(s) currently enrolled.")
                        else:
                            conn = get_conn()
                            conn.execute("DELETE FROM courses WHERE id=?", (course['id'],))
                            conn.commit()
                            conn.close()
                            st.success(f"🗑️ {course['code']} deleted.")
                            st.rerun()

        # ── Add New Course ────────────────────────────────────────────────────
        st.markdown("<div class='sec-header'>Add New Course</div>", unsafe_allow_html=True)
        with st.form("add_course"):
            c1, c2 = st.columns(2)
            code     = c1.text_input("Course Code")
            name     = c2.text_input("Course Name")
            dept     = c1.text_input("Department")
            credits  = c2.number_input("Credits",  1, 6, 3)
            capacity = c1.number_input("Capacity", 5, 100, 30)
            schedule = c2.text_input("Schedule (e.g. Mon/Wed 9:00-10:30)")
            room     = c1.text_input("Room")

            instr_names_add = ["None"] + list(faculty_options.keys())
            chosen_instr = st.selectbox("Instructor", instr_names_add)
            chosen_instr_id = faculty_options.get(chosen_instr) if chosen_instr != "None" else None

            # Prerequisite dropdown
            all_courses_list = get_courses()
            prereq_options = {"None": None}
            prereq_options.update({f"{r['code']} — {r['name']}": int(r['id']) for _, r in all_courses_list.iterrows()})
            chosen_prereq_label = st.selectbox("Prerequisite", list(prereq_options.keys()))
            chosen_prereq_id = prereq_options[chosen_prereq_label]

            submitted = st.form_submit_button("➕ Add Course", type="primary")
            if submitted and code and name:
                conn = get_conn()
                try:
                    conn.execute("""INSERT INTO courses(code,name,department,credits,capacity,
                                     instructor_id,schedule,room,semester,prerequisite_id)
                                     VALUES(?,?,?,?,?,?,?,?,'Fall 2026',?)""",
                                 (code, name, dept, credits, capacity,
                                  chosen_instr_id, schedule, room, chosen_prereq_id))
                    conn.commit()
                    st.success(f"✅ Course {code} added!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Course code already exists.")
                finally:
                    conn.close()

    with tab2:
        st.markdown("<div class='sec-header'>User Management</div>", unsafe_allow_html=True)

        user_tab1, user_tab2 = st.tabs(["\U0001f393 Students", "\U0001f468\u200d\U0001f3eb Instructors"])

        with user_tab1:
                conn = get_conn()
                users_df = pd.read_sql_query(
                    "SELECT id, university_id, name, email FROM users WHERE role=?",
                    conn, params=('student',))
                conn.close()

                if users_df.empty:
                    st.info("No Students registered yet.")
                else:
                    for _, u in users_df.iterrows():
                        uc1, uc2, uc3, uc4 = st.columns([1.5, 2, 2.5, 1])
                        uc1.markdown(f"**{u['university_id']}**")
                        uc2.write(u['name'])
                        uc3.write(u['email'])
                        if uc4.button("\U0001f5d1\ufe0f Remove", key=f"del_student_{int(u['id'])}"):
                            conn2 = get_conn()
                            c2 = conn2.cursor()
                            if 'student' == "student":
                                c2.execute("SELECT COUNT(*) FROM enrollments WHERE student_id=? AND status='active'", (int(u['id']),))
                                active = c2.fetchone()[0]
                                if active > 0:
                                    conn2.close()
                                    st.error(f"\u274c Cannot remove — {u['name']} has {active} active enrollment(s).")
                                    st.stop()
                            elif 'student' == "faculty":
                                c2.execute("SELECT COUNT(*) FROM courses WHERE instructor_id=? AND semester='Fall 2026'", (int(u['id']),))
                                assigned = c2.fetchone()[0]
                                if assigned > 0:
                                    conn2.close()
                                    st.error(f"\u274c Cannot remove — {u['name']} is assigned to {assigned} course(s).")
                                    st.stop()
                            conn2.execute("DELETE FROM users WHERE id=?", (int(u['id']),))
                            conn2.commit()
                            conn2.close()
                            st.success(f"{u['name']} removed.")
                            st.rerun()

                st.markdown("<div class='sec-header'>Add New Student</div>", unsafe_allow_html=True)
                with st.form("add_student"):
                    fc1, fc2 = st.columns(2)
                    new_name  = fc1.text_input("Full Name")
                    new_uid   = fc2.text_input("University ID", placeholder="e.g. FAC-003")
                    new_email = fc1.text_input("Email")
                    new_pw    = fc2.text_input("Password", type="password")
                    add_btn   = st.form_submit_button("\u2795 Add Student", type="primary")
                    if add_btn:
                        if not all([new_name, new_uid, new_email, new_pw]):
                            st.error("Please fill in all fields.")
                        else:
                            conn3 = get_conn()
                            try:
                                conn3.execute(
                                    "INSERT INTO users(name,email,password,role,university_id) VALUES(?,?,?,?,?)",
                                    (new_name, new_email, hash_pw(new_pw), 'student', new_uid))
                                conn3.commit()
                                st.success(f"\u2705 Student {new_name} added!")
                                st.rerun()
                            except sqlite3.IntegrityError as e:
                                if "email" in str(e):
                                    st.error("Email already exists.")
                                else:
                                    st.error("University ID already exists.")
                            finally:
                                conn3.close()

        with user_tab2:
                conn = get_conn()
                users_df = pd.read_sql_query(
                    "SELECT id, university_id, name, email FROM users WHERE role=?",
                    conn, params=('faculty',))
                conn.close()

                if users_df.empty:
                    st.info("No Instructors registered yet.")
                else:
                    for _, u in users_df.iterrows():
                        uc1, uc2, uc3, uc4 = st.columns([1.5, 2, 2.5, 1])
                        uc1.markdown(f"**{u['university_id']}**")
                        uc2.write(u['name'])
                        uc3.write(u['email'])
                        if uc4.button("\U0001f5d1\ufe0f Remove", key=f"del_faculty_{int(u['id'])}"):
                            conn2 = get_conn()
                            c2 = conn2.cursor()
                            if 'faculty' == "student":
                                c2.execute("SELECT COUNT(*) FROM enrollments WHERE student_id=? AND status='active'", (int(u['id']),))
                                active = c2.fetchone()[0]
                                if active > 0:
                                    conn2.close()
                                    st.error(f"\u274c Cannot remove — {u['name']} has {active} active enrollment(s).")
                                    st.stop()
                            elif 'faculty' == "faculty":
                                c2.execute("SELECT COUNT(*) FROM courses WHERE instructor_id=? AND semester='Fall 2026'", (int(u['id']),))
                                assigned = c2.fetchone()[0]
                                if assigned > 0:
                                    conn2.close()
                                    st.error(f"\u274c Cannot remove — {u['name']} is assigned to {assigned} course(s).")
                                    st.stop()
                            conn2.execute("DELETE FROM users WHERE id=?", (int(u['id']),))
                            conn2.commit()
                            conn2.close()
                            st.success(f"{u['name']} removed.")
                            st.rerun()

                st.markdown("<div class='sec-header'>Add New Instructor</div>", unsafe_allow_html=True)
                with st.form("add_faculty"):
                    fc1, fc2 = st.columns(2)
                    new_name  = fc1.text_input("Full Name")
                    new_uid   = fc2.text_input("University ID", placeholder="e.g. FAC-003")
                    new_email = fc1.text_input("Email")
                    new_pw    = fc2.text_input("Password", type="password")
                    add_btn   = st.form_submit_button("\u2795 Add Instructor", type="primary")
                    if add_btn:
                        if not all([new_name, new_uid, new_email, new_pw]):
                            st.error("Please fill in all fields.")
                        else:
                            conn3 = get_conn()
                            try:
                                conn3.execute(
                                    "INSERT INTO users(name,email,password,role,university_id) VALUES(?,?,?,?,?)",
                                    (new_name, new_email, hash_pw(new_pw), 'faculty', new_uid))
                                conn3.commit()
                                st.success(f"\u2705 Instructor {new_name} added!")
                                st.rerun()
                            except sqlite3.IntegrityError as e:
                                if "email" in str(e):
                                    st.error("Email already exists.")
                                else:
                                    st.error("University ID already exists.")
                            finally:
                                conn3.close()

    with tab3:
        st.markdown("<div class='sec-header'>Enrollment Statistics</div>", unsafe_allow_html=True)
        courses = get_courses()
        courses['fill_pct'] = (courses['enrolled'] / courses['capacity'] * 100).round(1)
        st.bar_chart(courses.set_index('code')['enrolled'])
        st.dataframe(courses[['code','name','enrolled','capacity','fill_pct']].rename(
            columns={'fill_pct':'Fill %'}), use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("<div class='sec-header'>Enrollment Rules — Fall 2026</div>", unsafe_allow_html=True)
        rules = get_enrollment_rules()
        with st.form("edit_rules"):
            r1, r2 = st.columns(2)
            new_max   = r1.number_input("Max Credits per Semester", value=rules["max_credits"], min_value=1, max_value=30)
            new_min   = r2.number_input("Min Credits per Semester", value=rules["min_credits"], min_value=1, max_value=30)
            new_add   = r1.text_input("Add Deadline (YYYY-MM-DD)",  value=rules["add_deadline"])
            new_drop  = r2.text_input("Drop Deadline (YYYY-MM-DD)", value=rules["drop_deadline"])
            save_rules = st.form_submit_button("💾 Save Rules", type="primary")
            if save_rules:
                import re
                date_ok = re.match(r'\d{4}-\d{2}-\d{2}', new_add) and re.match(r'\d{4}-\d{2}-\d{2}', new_drop)
                if new_min >= new_max:
                    st.error("Min credits must be less than Max credits.")
                elif not date_ok:
                    st.error("Dates must be in YYYY-MM-DD format.")
                elif new_add >= new_drop:
                    st.error("Add deadline must be before drop deadline.")
                else:
                    conn = get_conn()
                    conn.execute("""INSERT INTO enrollment_rules(semester,max_credits,min_credits,add_deadline,drop_deadline)
                                     VALUES('Fall 2026',?,?,?,?)
                                     ON CONFLICT(semester) DO UPDATE SET
                                     max_credits=excluded.max_credits,
                                     min_credits=excluded.min_credits,
                                     add_deadline=excluded.add_deadline,
                                     drop_deadline=excluded.drop_deadline""",
                                 (new_max, new_min, new_add, new_drop))
                    conn.commit()
                    conn.close()
                    st.success("✅ Enrollment rules updated!")
                    st.rerun()

        st.markdown("<div class='sec-header'>Current Rules Summary</div>", unsafe_allow_html=True)
        rules = get_enrollment_rules()
        st.markdown(f"""
        <div class='metric-row'>
            <div class='metric-card gold'><div class='num'>{rules['max_credits']}</div><div class='label'>Max Credits</div></div>
            <div class='metric-card'><div class='num'>{rules['min_credits']}</div><div class='label'>Min Credits</div></div>
            <div class='metric-card green'><div class='num'>{rules['add_deadline']}</div><div class='label'>Add Deadline</div></div>
            <div class='metric-card red'><div class='num'>{rules['drop_deadline']}</div><div class='label'>Drop Deadline</div></div>
        </div>
        """, unsafe_allow_html=True)

def page_faculty():
    uid = st.session_state.user_id
    name = st.session_state.user_name
    st.markdown(f"""<div class='hero'><h1>👨‍🏫 Faculty Portal</h1><p>{name} — Fall 2026</p></div>""", unsafe_allow_html=True)

    my_courses = get_faculty_courses(uid)
    if my_courses.empty:
        st.info("No courses assigned to you this semester.")
        return

    st.markdown("<div class='sec-header'>My Courses</div>", unsafe_allow_html=True)
    selected = st.selectbox("Select a course to view enrolled students",
                            my_courses['id'].tolist(),
                            format_func=lambda i: my_courses.loc[my_courses['id']==i, 'name'].values[0])

    row = my_courses[my_courses['id'] == selected].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Course Code", row['code'])
    c2.metric("Enrolled", f"{row['enrolled']} / {row['capacity']}")
    c3.metric("Schedule", row['schedule'])

    st.markdown("<div class='sec-header'>Enrolled Students</div>", unsafe_allow_html=True)
    students = get_enrolled_students(selected)
    if students.empty:
        st.info("No students enrolled yet.")
    else:
        st.dataframe(students[['university_id','name','email','enrolled_at']],
                     use_container_width=True, hide_index=True)

# ─── Main App ────────────────────────────────────────────────────────────────
def main():
    init_db()

    if 'user_id' not in st.session_state:
        page_login()
        return

    role = st.session_state.user_role
    name = st.session_state.user_name

    with st.sidebar:
        st.markdown(f"""
        <div style='padding:1rem 0 1.5rem;'>
            <div style='font-size:2.5rem; text-align:center;'>🎓</div>
            <div style='text-align:center; font-family:Syne,sans-serif; font-size:1.1rem; font-weight:700;'>UniReg</div>
            <hr style='border-color:#1E3A5F; margin:0.8rem 0;'>
            <div style='font-size:0.85rem; color:#94A3B8;'>Logged in as</div>
            <div style='font-weight:600;'>{name}</div>
            <div style='font-size:0.8rem; color:#60A5FA; text-transform:capitalize;'>{role}</div>
        </div>
        """, unsafe_allow_html=True)

        if role == 'student':
            page = st.radio("Navigation", ["🏠 Dashboard", "📊 Grades & GPA"], label_visibility="collapsed")
        elif role == 'admin':
            page = st.radio("Navigation", ["⚙️ Admin Panel"], label_visibility="collapsed")
        elif role == 'faculty':
            page = st.radio("Navigation", ["👨‍🏫 Faculty Portal"], label_visibility="collapsed")

        st.markdown("<hr style='border-color:#1E3A5F; margin-top:2rem;'>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if role == 'student':
        if page == "🏠 Dashboard":
            page_student_dashboard()
        else:
            page_gpa()
    elif role == 'admin':
        page_admin()
    elif role == 'faculty':
        page_faculty()

if __name__ == "__main__":
    main()