import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import random
from datetime import datetime
import io
from PyPDF2 import PdfReader  # For PDF text extraction

# Simulated AI response function (replace with actual AI integration if available)
def get_gemini_response(prompt):
    return f"AI Response to: {prompt[:50]}... (simulated response)"

# Simulated AI functions (replace with your actual AI logic)
def enhance_resume_section(content, section):
    return f"Enhanced {section}: {content.strip()} (AI-enhanced)"

def heatmap_analysis(resume_text):
    return {"Contact": 90, "Summary": 80, "Experience": 70, "Education": 85, "Skills": 60}

def analyze_keywords(resume_text, job_desc):
    return {"present": ["Python", "AI"], "missing": ["Java", "Cloud"]}

def match_job_description(resume_text, job_desc):
    return random.randint(60, 95)

def generate_career_roadmap(resume_text):
    return "Career Roadmap: Step 1 - Enhance skills, Step 2 - Apply to jobs..."

def generate_salary_negotiation_strategy(resume_text, job_desc):
    return "Negotiation Strategy: Highlight AI skills, ask for 10% above market rate."

# Session state initialization
if 'current_resume' not in st.session_state:
    st.session_state['current_resume'] = ""
if 'transformed_resume' not in st.session_state:
    st.session_state['transformed_resume'] = ""
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = True
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Landing Page"
if 'user_level' not in st.session_state:
    st.session_state['user_level'] = 1
if 'achievements' not in st.session_state:
    st.session_state['achievements'] = []
if 'career_missions' not in st.session_state:
    st.session_state['career_missions'] = ["Complete your first resume enhancement"]

# Utility Functions
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""  # Handle None case
    return text

def split_resume_into_sections(text):
    essential_sections = ["Contact", "Summary", "Experience", "Education", "Skills"]
    optional_sections = ["Projects", "Certifications", "Awards", "Publications"]
    sections = {section: "" for section in essential_sections + optional_sections}
    current_section = None
    lines = text.split("\n")
    for line in lines:
        line = line.strip().lower()
        for section in essential_sections + optional_sections:
            if section.lower() in line:
                current_section = section
                break
        if not current_section and line:
            if "university" in line or "degree" in line:
                current_section = "Education"
            elif "company" in line or "worked" in line:
                current_section = "Experience"
            elif "skill" in line or "proficient" in line:
                current_section = "Skills"
            elif "@" in line or "phone" in line:
                current_section = "Contact"
        if current_section and line:
            sections[current_section] += line + "\n"
    missing_sections = [s for s in essential_sections if not sections[s].strip()]
    return sections, missing_sections

def generate_pdf(resume_text, template="Standard", color="black", font="Arial"):
    styles = getSampleStyleSheet()
    styles['Title'].fontName = font
    styles['Heading1'].fontName = font
    styles['BodyText'].fontName = font
    if template == "Executive":
        styles['Title'].fontSize = 24
        styles['Title'].textColor = color
    elif template == "Creative":
        styles['Title'].fontSize = 20
        styles['Title'].textColor = color
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    story.append(Paragraph("Resume", styles['Title']))
    story.append(Spacer(1, 12))
    for section, content in split_resume_into_sections(resume_text)[0].items():
        if content.strip():
            story.append(Paragraph(section, styles['Heading1']))
            story.append(Paragraph(content, styles['BodyText']))
            story.append(Spacer(1, 12))
    doc.build(story)
    buffer.seek(0)
    return buffer

def calculate_ats_score(resume_text, job_desc=None):
    sections, missing_sections = split_resume_into_sections(resume_text)
    score = 100
    if missing_sections:
        score -= 20 * len(missing_sections)
    if job_desc:
        keywords = analyze_keywords(resume_text, job_desc)
        missing_keywords = len(keywords['missing'])
        score -= 5 * missing_keywords  # Corrected syntax
    return max(0, score)

def generate_critique(resume_text):
    return get_gemini_response(f"Critique this resume:\n{resume_text}")

def generate_encouragement():
    return random.choice([
        "You're doing amazing! A few tweaks, and you'll land your dream job!",
        "Great work! Your potential is shining—keep pushing forward!",
        "You're on fire! Focus on your strengths, and success is yours!"
    ])

# UI Enhancements
def apply_theme():
    if st.session_state['dark_mode']:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
            color: #e0e0e0;
        }
        .stButton>button {
            background: linear-gradient(45deg, #00ffcc, #00ccff);
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
        }
        .stTextInput>div>input, .stTextArea>div>textarea {
            background: #333;
            color: #e0e0e0;
            border: 1px solid #555;
            border-radius: 5px;
        }
        .stSelectbox, .stMultiselect {
            background: #333;
            color: #e0e0e0;
        }
        .stProgress .st-bo {
            background-color: #00ccff;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            color: #333;
        }
        .stButton>button {
            background: linear-gradient(45deg, #ff6b6b, #ff8e53);
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }
        </style>
        """, unsafe_allow_html=True)

# Landing Page with Logo
def render_landing_page():
    # Add logo at the top of the Landing Page
    st.image("logo.png", caption="CareerAI - Empowering Your Career Journey", width=200)
    st.title("🚀 Resume Enhancer & AI-Powered Job Matching Platform")
    st.markdown("**Transform Your Resume. Unlock Your Career Potential.**")
    st.write("Welcome to the future of job applications—where AI meets career growth! Our platform enhances your resume, optimizes it for ATS, and matches it with jobs to maximize your hiring chances.")
    st.markdown("✨ **Upload. Optimize. Match. Get Hired.**")
    st.button("Enhance My Resume Now", on_click=lambda: st.session_state.update({'current_page': 'Dashboard'}))

    st.markdown("---")
    st.subheader("🌟 Our Vision")
    st.write("**Empowering Every Job Seeker with AI-Powered Career Intelligence**")
    st.write("We envision a world where AI bridges skills and opportunities, giving every professional a fair shot at success.")
    st.button("Get Started Today", on_click=lambda: st.session_state.update({'current_page': 'Dashboard'}))

    st.markdown("---")
    st.subheader("📝 About Us")
    st.write("Built by AI enthusiasts and career strategists, we’re here to fix the flawed hiring process—99% of resumes fail ATS. Our AI eliminates these barriers.")
    st.button("Explore Features", on_click=lambda: st.session_state.update({'current_page': 'Dashboard'}))

    st.markdown("---")
    st.subheader("🔑 Core Commitments")
    for commitment in ["AI Innovation", "ATS Compliance", "Data-Driven Insights", "Global Accessibility", "Personalized Coaching"]:
        st.markdown(f"- **{commitment}**")
    st.button("Try AI Enhancement", on_click=lambda: st.session_state.update({'current_page': 'Resume Enhancement'}))

    st.markdown("---")
    st.subheader("🔥 Core Features")
    st.markdown("""
    - **Resume Enhancement**: AI-powered editing, ATS optimization, and templates.
    - **Job Matching**: Smart matching with skill gap analysis.
    - **Career Insights**: Market trends and salary benchmarks.
    - **Interview Prep**: AI-generated questions and speech analysis.
    """)
    st.button("Enhance My Resume", on_click=lambda: st.session_state.update({'current_page': 'Resume Enhancement'}))

    st.markdown("---")
    st.subheader("👤 Meet Our Founders")
    founders = [
        ("Suraj Kumar", "Great careers are built, not found."),
        ("Mehak", "Your resume is your career story—let’s perfect it."),
        ("Manish Yadav", "Hiring is about skills, not keywords."),
        ("Aakash Kumar Kundan", "Every job seeker deserves a fair chance."),
        ("Vinay Gautam", "AI enhances human potential."),
        ("Khushi Verma", "Technology should feel like magic.")
    ]
    for name, quote in founders:
        st.markdown(f"**{name}**: *'{quote}'*")
    st.button("Join the AI Revolution", on_click=lambda: st.session_state.update({'current_page': 'Dashboard'}))

# Dashboard Page
def render_dashboard():
    st.image("logo.png", caption="CareerAI Dashboard", width=150)
    st.title("📊 Dashboard")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        st.session_state['current_resume'] = text
        st.session_state['achievements'].append("Resume Uploaded")

    if st.session_state['current_resume']:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("📝 Your Resume")
            sections, missing_sections = split_resume_into_sections(st.session_state['current_resume'])
            for section, content in sections.items():
                with st.expander(section, expanded=True):
                    st.markdown(f"**{section}**")
                    if content.strip():
                        st.write(content)
                    else:
                        st.write("*(Missing)*")
        with col2:
            st.subheader("📈 Live Heatmap")
            heatmap = heatmap_analysis(st.session_state['current_resume'])
            df_heatmap = pd.DataFrame(list(heatmap.items()), columns=['Section', 'Score'])
            fig = px.bar(df_heatmap, x='Section', y='Score', color='Score', 
                         color_continuous_scale='RdYlGn', range_color=[0, 100])
            st.plotly_chart(fig)
            for missing in missing_sections:
                st.markdown(f"<span style='color:red'>{missing}: Missing</span>", unsafe_allow_html=True)

# Resume Enhancement Page
def render_resume_enhancement():
    st.image("logo.png", caption="Resume Enhancement", width=150)
    st.title("✍️ Resume Enhancement")
    tabs = st.tabs(["Autopilot", "Heatmap", "Rewrite Battle", "Portfolio", "Designer"])
    
    templates = ["Standard", "Executive", "Creative"]
    colors = {"Standard": "black", "Executive": "navy", "Creative": "teal"}
    fonts = ["Arial", "Times New Roman", "Helvetica"]

    with tabs[0]:  # Autopilot
        st.subheader("🤖 Autopilot")
        template = st.selectbox("Choose Template", templates)
        color = st.selectbox("Color Scheme", list(colors.values()))
        font = st.selectbox("Font", fonts)
        if st.button("Enhance Resume"):
            st.session_state['transformed_resume'] = enhance_resume_section(st.session_state['current_resume'], "all")
            pdf_buffer = generate_pdf(st.session_state['transformed_resume'], template, color, font)
            st.download_button("Download Enhanced Resume", pdf_buffer, "enhanced_resume.pdf", "application/pdf")
            display_enhancement_feedback()

    with tabs[1]:  # Heatmap
        st.subheader("📈 Heatmap")
        if st.session_state['current_resume']:
            heatmap = heatmap_analysis(st.session_state['current_resume'])
            fig = px.bar(pd.DataFrame(list(heatmap.items()), columns=['Section', 'Score']),
                         x='Section', y='Score', color='Score', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig)

    with tabs[2]:  # Rewrite Battle
        st.subheader("⚔️ Rewrite Battle")
        versions = ["Executive", "Creative", "Technical"]
        cols = st.columns(3)
        for col, version in zip(cols, versions):
            with col:
                if st.button(f"Generate {version}"):
                    result = get_gemini_response(f"Rewrite resume as {version}:\n{st.session_state['current_resume']}")
                    st.text_area(version, result, height=150)
                    template = st.selectbox(f"Template for {version}", templates, key=f"t_{version}")
                    color = st.selectbox(f"Color for {version}", list(colors.values()), key=f"c_{version}")
                    font = st.selectbox(f"Font for {version}", fonts, key=f"f_{version}")
                    if st.button(f"Download {version}"):
                        pdf_buffer = generate_pdf(result, template, color, font)
                        st.download_button(f"Download {version} Resume", pdf_buffer, f"{version.lower()}_resume.pdf", "application/pdf")

    with tabs[3]:  # Portfolio
        st.subheader("🌐 Portfolio")
        template = st.selectbox("Portfolio Template", ["Minimalist", "Professional", "Creative"])
        color = st.selectbox("Portfolio Color", ["white", "blue", "green"])
        if st.button("Generate Portfolio"):
            html = get_gemini_response(f"Generate {template} portfolio HTML with {color} scheme:\n{st.session_state['current_resume']}")
            st.download_button("Download Portfolio", html, "portfolio.html", "text/html")

    with tabs[4]:  # Designer
        st.subheader("🎨 Designer")
        if st.session_state['current_resume']:
            sections, _ = split_resume_into_sections(st.session_state['current_resume'])
            order = st.multiselect("Reorder Sections", list(sections.keys()), default=list(sections.keys()))
            template = st.selectbox("Designer Template", templates)
            color = st.selectbox("Designer Color", list(colors.values()))
            font = st.selectbox("Designer Font", fonts)
            if st.button("Apply Design"):
                new_resume = "\n\n".join([f"{s}\n{sections[s]}" for s in order])
                st.session_state['transformed_resume'] = new_resume
                pdf_buffer = generate_pdf(new_resume, template, color, font)
                st.download_button("Download Designed Resume", pdf_buffer, "designed_resume.pdf", "application/pdf")
                display_enhancement_feedback()

def display_enhancement_feedback():
    ats_score = calculate_ats_score(st.session_state['transformed_resume'])
    st.metric("ATS Score", f"{ats_score}%")
    st.write("**Critique**")
    st.write(generate_critique(st.session_state['transformed_resume']))
    st.write("**Suggestions/Feedback**")
    st.write("Consider adding more projects to boost your Experience section.")
    st.write("**Encouragement**")
    st.write(generate_encouragement())
    if st.button("Chat with AI"):
        st.session_state['current_page'] = "Career Assistant"

# Job Matching Page
def render_job_matching():
    st.image("logo.png", caption="Job Matching", width=150)
    st.title("🎯 Job Matching")
    tabs = st.tabs(["Smart Matching", "Career Simulator", "Hidden Jobs"])
    with tabs[0]:
        jd_source = st.radio("JD Source", ["Text", "Upload PDF"])
        job_desc = st.text_area("Enter Job Description") if jd_source == "Text" else extract_text_from_pdf(st.file_uploader("Upload JD PDF", type=['pdf']) or io.BytesIO(b""))
        resume_source = st.radio("Resume Source", ["Current", "Upload"])
        resume_text = st.session_state['current_resume'] if resume_source == "Current" else extract_text_from_pdf(st.file_uploader("Upload Resume", type=['pdf']) or io.BytesIO(b""))
        if job_desc and resume_text and st.button("Match"):
            score = match_job_description(resume_text, job_desc)
            st.metric("Matching Score", f"{score}%")
            st.write("**Feedback**")
            st.write(analyze_keywords(resume_text, job_desc))
            if st.button("Chat about Matching"):
                st.session_state['current_page'] = "Career Assistant"
    with tabs[1]:
        if st.button("Generate Career Simulator"):
            roadmap = generate_career_roadmap(st.session_state['current_resume'])
            st.write(roadmap)
            st.download_button("Download Roadmap", roadmap, "roadmap.txt")
    with tabs[2]:
        st.write(get_gemini_response(f"Analyze hidden job opportunities:\n{st.session_state['current_resume']}"))

# Interview Coaching Page
def render_interview_coaching():
    st.image("logo.png", caption="Interview Coaching", width=150)
    st.title("🎤 Interview Coaching")
    tabs = st.tabs(["Mock Interview", "Speech Trainer"])
    with tabs[0]:
        if st.button("Start Mock Interview"):
            question = get_gemini_response(f"Generate interview question:\n{st.session_state['current_resume']}")
            st.write(question)
            answer = st.text_area("Your Answer")
            if answer and st.button("Evaluate"):
                st.write(get_gemini_response(f"Evaluate answer:\n{answer}"))
    with tabs[1]:
        st.write("Speech Trainer (Text-based for now)")
        answer = st.text_area("Record Answer (type for simulation)")
        if answer and st.button("Analyze Speech"):
            st.write(get_gemini_response(f"Analyze speech:\n{answer}"))

# Career Assistant Page
def render_career_assistant():
    st.image("logo.png", caption="Career Assistant", width=150)
    st.title("🤖 Career Assistant")
    tabs = st.tabs(["Chat", "Salary Negotiation", "LinkedIn Enhancer"])
    with tabs[0]:
        for msg in st.session_state['chat_history']:
            st.markdown(f"**{msg['role'].capitalize()} ({msg['time']})**: {msg['content']}")
        user_input = st.text_input("Ask a question:")
        if st.button("Send"):
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state['chat_history'].append({"role": "user", "content": user_input, "time": timestamp})
            response = get_gemini_response(user_input)
            st.session_state['chat_history'].append({"role": "assistant", "content": response, "time": timestamp})
            st.experimental_rerun()
    with tabs[1]:
        jd = st.text_area("Enter JD") or extract_text_from_pdf(st.file_uploader("Upload JD", type=['pdf']) or io.BytesIO(b""))
        if jd and st.button("Negotiate"):
            st.write(generate_salary_negotiation_strategy(st.session_state['current_resume'], jd))
    with tabs[2]:
        if st.button("Enhance LinkedIn"):
            st.write(get_gemini_response(f"Optimize for LinkedIn:\n{st.session_state['current_resume']}"))

# Sidebar with Logo
def render_sidebar():
    with st.sidebar:
        st.image("logo.png", caption="CareerAI", width=100)  # Sidebar logo
        st.write(f"Level: {st.session_state['user_level']}")
        st.write("Achievements:", ", ".join(st.session_state['achievements']) or "None")
        st.write("Mission:", st.session_state['career_missions'][-1])
        st.progress(st.session_state['user_level'] / 10)
        for page in ["Landing Page", "Dashboard", "Resume Enhancement", "Job Matching", "Interview Coaching", "Career Assistant"]:
            st.button(page, on_click=lambda p=page: st.session_state.update({'current_page': p}))
        st.checkbox("Dark Mode", value=st.session_state['dark_mode'], on_change=lambda: st.session_state.update({'dark_mode': not st.session_state['dark_mode']}))

# Main App
def main():
    apply_theme()
    render_sidebar()
    pages = {
        "Landing Page": render_landing_page,
        "Dashboard": render_dashboard,
        "Resume Enhancement": render_resume_enhancement,
        "Job Matching": render_job_matching,
        "Interview Coaching": render_interview_coaching,
        "Career Assistant": render_career_assistant
    }
    pages[st.session_state['current_page']]()

if __name__ == "__main__":
    st.set_page_config(page_title="Resume Enhancer", layout="wide")
    main()