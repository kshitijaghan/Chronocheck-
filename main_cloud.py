# main_cloud.py - CHRONOCHECK (Bilingual Version)
import streamlit as st

# ========== API INTEGRATION ==========

# Define DummyAPI first (as fallback)
class DummyAPI:
    def qna_medical(self, question):
        return {"success": True, "message": f"**Answer:** This would come from your Q&A Langflow flow.\n\nQuestion: {question}"}
    
    def analyze_report(self, user_message, uploaded_files=None):
        if uploaded_files:
            file_names = ", ".join([f.name for f in uploaded_files])
            return {"success": True, "message": f"**Report Analysis:** Analysis for uploaded file(s): {file_names}\n\nAI analysis of your medical report.\n\nMessage: {user_message}"}
        else:
            return {"success": True, "message": f"**Report Analysis:** {user_message}"}
    
    def find_hospitals(self, query, location=""):
        return {"success": True, "message": f"**Hospital Recommendations:**\n\nLooking for: {query} in {location if location else 'your area'}"}
    
    def explain_medicines(self, user_message, uploaded_files=None):
        if uploaded_files:
            file_names = ", ".join([f.name for f in uploaded_files])
            return {"success": True, "message": f"**Medicine Explanation:** Analysis for uploaded file(s): {file_names}\n\nAI analysis of your prescription.\n\nMessage: {user_message}"}
        else:
            return {"success": True, "message": f"**Medicine Explanation:** {user_message}"}
    
    def analyze_bill(self, user_message, uploaded_files=None):
        audit_report = """**Medical Billing Audit Report**

| Bill Item | Billed Price (₹) | Standard/Ref Price (₹) | Potential Overcharge (₹) | Auditor's Expert Analysis |
|-----------|------------------|------------------------|--------------------------|---------------------------|
| Complete Blood Count (CBC) | ₹1,200.00 | ₹200.00 | **₹1,000.00** | Overcharged by 500% |
| Ultrasound Abdomen | ₹1,500.00 | ₹850.00 | **₹650.00** | Overcharged by 76.47% |
| CT Scan Abdomen | ₹4,500.00 | Not found | ₹0.00 | Not audited |

**📊 Summary of Savings**
**Total Potential Overcharge: ₹1,650.00**

**✅ Audit Conclusion**
The bill is inflated due to overcharging for certain items."""
        
        return {
            "success": True,
            "message": audit_report,
            "demo_mode": True
        }

# Now try to import the real API
try:
    from cloud_langflow_api import CloudLangflowAPI
    api = CloudLangflowAPI()
except Exception as e:
    st.error(f"Failed to initialize API: {str(e)}. Using demo mode.")
    api = DummyAPI()

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="CHRONOCHECK",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(37, 99, 235, 0.3);
        border: 1px solid rgba(37, 99, 235, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #2563eb, #10b981);
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
    }
    
    .stTextArea textarea {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #475569;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    
    .chat-bubble-user {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 15px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .chat-bubble-ai {
        background: rgba(30, 41, 59, 0.8);
        color: white;
        padding: 15px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 0;
        max-width: 80%;
        border: 1px solid #334155;
    }
    
    .bilingual-toggle {
        display: flex;
        justify-content: flex-end;
        margin: 10px 0;
        padding: 5px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
    }
    
    .language-badge {
        display: inline-block;
        background: linear-gradient(45deg, #2563eb, #10b981);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8em;
        margin-right: 10px;
        font-weight: 600;
    }
    
    .file-card {
        background: rgba(37, 99, 235, 0.1);
        border: 1px solid #2563eb;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .dashboard-card {
        text-align: center;
        padding: 25px 20px;
        background: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s;
        height: 100%;
        cursor: pointer;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        border-color: #2563eb;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.2);
    }
    
    .dashboard-icon {
        font-size: 3.5em;
        margin-bottom: 15px;
    }
    
    .dashboard-title {
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 10px;
        color: #f1f5f9;
    }
    
    .dashboard-desc {
        font-size: 0.9em;
        color: #94a3b8;
        line-height: 1.4;
    }
    
    .app-title {
        font-size: 2.3em;
        font-weight: 800;
        background: linear-gradient(90deg, #2563eb, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        white-space: nowrap;
        margin: 0;
    }
    
    .tagline {
        color: #94a3b8;
        font-size: 1.1em;
        letter-spacing: 1px;
        margin: 5px 0 20px 0;
    }
    
    .demo-mode {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        color: #fbbf24;
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ========== BILINGUAL RESPONSE COMPONENT ==========
def display_bilingual_response(selected_language: str, response_text: str, english_response: str = None):
    """
    Display response with language toggle
    If english_response is None, it means we only have one response
    """
    
    # If selected language is English, just show the response normally
    if selected_language == "English":
        st.markdown(response_text)
        return
    
    # For non-English languages, provide toggle between languages
    st.markdown(f'<span class="language-badge">🌐 {selected_language}</span>', unsafe_allow_html=True)
    
    # Create tabs for language switching
    tab1, tab2 = st.tabs([f"🌐 {selected_language}", "🇬🇧 English"])
    
    with tab1:
        st.markdown(response_text)
    
    with tab2:
        if english_response:
            st.markdown(english_response)
        else:
            # If no English response provided, show note
            st.info("English version not available. Showing original response.")
            st.markdown(response_text)

# ========== LANGUAGE SELECTOR COMPONENT ==========
def language_selector_component(key_suffix=""):
    """Reusable language selector for all agents"""
    languages = [
        "English", 
        "Hindi (हिंदी)", 
        "Marathi (मराठी)", 
        "Tamil (தமிழ்)", 
        "Telugu (తెలుగు)", 
        "Bengali (বাংলা)",
        "Gujarati (ગુજરાતી)",
        "Kannada (ಕನ್ನಡ)",
        "Malayalam (മലയാളം)",
        "Punjabi (ਪੰਜਾਬੀ)"
    ]
    
    selected_language = st.selectbox(
        "🌍 Response Language",
        languages,
        index=0,
        help="The AI will provide the response in your selected language",
        key=f"language_{key_suffix}"
    )
    
    # Return just the language name without the script part
    return selected_language.split(" (")[0]

# ========== SESSION STATE FOR NAVIGATION ==========
if 'selected_tool' not in st.session_state:
    st.session_state.selected_tool = "📊 Dashboard"

# ========== SIDEBAR ==========
with st.sidebar:
    # App Name & Tagline
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div class="app-title">CHRONOCHECK</div>
        <div class="tagline">CHECK • CARE • CLARITY</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show connection status
    if api and not isinstance(api, DummyAPI):
        st.sidebar.success("✅ Connected to Cloud Langflow")
    
    st.markdown("---")
    
    # Navigation
    page_options = [
        "📊 Dashboard",
        "🧠 Medical Q&A",
        "📄 Report Analyzer", 
        "🏥 Hospital Finder",
        "💊 Medicine Explainer",
        "💰 Bill Auditor"
    ]
    
    selected_page = st.radio(
        "Navigate to:",
        page_options,
        index=page_options.index(st.session_state.selected_tool) if st.session_state.selected_tool in page_options else 0,
        label_visibility="collapsed"
    )
    
    st.session_state.selected_tool = selected_page

# ========== DASHBOARD PAGE ==========
if st.session_state.selected_tool == "📊 Dashboard":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 2.8em; margin-bottom: 10px;">Welcome to CHRONOCHECK</h1>
        <p style="font-size: 1.2em; color: #94a3b8; max-width: 800px; margin: 0 auto;">
            Your comprehensive AI-powered medical assistant. Five specialized tools for better healthcare decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🛠️ Available Tools")
    
    tools = [
        {
            "icon": "🧠",
            "title": "Medical Q&A",
            "description": "Ask medical questions and get AI-powered answers instantly.",
            "color": "#2563eb",
            "page": "🧠 Medical Q&A"
        },
        {
            "icon": "📄", 
            "title": "Report Analyzer",
            "description": "Upload your medical report and get AI analysis.",
            "color": "#10b981",
            "page": "📄 Report Analyzer"
        },
        {
            "icon": "🏥",
            "title": "Hospital Finder",
            "description": "Find specialized hospitals based on your medical needs and location.",
            "color": "#8b5cf6",
            "page": "🏥 Hospital Finder"
        },
        {
            "icon": "💊",
            "title": "Medicine Explainer",
            "description": "Upload your prescription and get detailed medicine explanations.",
            "color": "#f59e0b",
            "page": "💊 Medicine Explainer"
        },
        {
            "icon": "💰",
            "title": "Bill Auditor",
            "description": "Upload your medical bill and get cost analysis.",
            "color": "#ef4444",
            "page": "💰 Bill Auditor"
        }
    ]
    
    cols = st.columns(5)
    for idx, tool in enumerate(tools):
        with cols[idx]:
            st.markdown(f"""
            <div class="dashboard-card" style="border-color: {tool['color']};">
                <div class="dashboard-icon">{tool['icon']}</div>
                <div class="dashboard-title">{tool['title']}</div>
                <div class="dashboard-desc">{tool['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("", key=f"dashboard_btn_{idx}", help=f"Go to {tool['title']}"):
                st.session_state.selected_tool = tool['page']
                st.rerun()
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 🚀 Quick Start Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>📋 Step 1: Select</h3>
            <p>Choose the tool that matches your need from the dashboard or sidebar.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>📤 Step 2: Upload/Input</h3>
            <p>Upload a file or enter your query directly.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>⚡ Step 3: Analyze</h3>
            <p>Get instant AI-powered insights and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

# ========== MEDICAL Q&A PAGE ==========
elif st.session_state.selected_tool == "🧠 Medical Q&A":
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top: 0;">🧠 Medical Q&A Assistant</h2>
        <p>Ask medical questions and get AI-powered answers in your preferred language</p>
    </div>
    """, unsafe_allow_html=True)

    # Language and Expertise Selection
    col1, col2 = st.columns(2)
    
    with col1:
        language = language_selector_component("qna")
    
    with col2:
        expertise = st.selectbox(
            "📚 Response Level",
            ["Patient-Friendly", "Medical Student", "Professional"],
            index=0,
            help="Choose how detailed and technical the explanation should be",
            key="expertise_qna"
        )

    st.markdown("---")
    st.markdown("### 💬 Your Medical Question")
    
    question = st.text_area(
        "Enter your question here:",
        height=150,
        placeholder="Type your medical question in any language...\n\nExamples:\n- What are symptoms of diabetes?\n- Explain what HbA1c means\n- मुझे सिरदर्द क्यों होता है?",
        key="qna_question"
    )

    if st.button("🔍 Get Medical Answer", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("⚠️ Please enter a question")
        else:
            with st.spinner(f"🔬 Getting answer in {language}..."):
                # Build enhanced prompt with language and expertise
                enhanced_question = question
                
                # Add expertise instruction
                if expertise == "Patient-Friendly":
                    enhanced_question += "\n\nPlease provide a simple, easy-to-understand explanation suitable for patients."
                elif expertise == "Medical Student":
                    enhanced_question += "\n\nPlease provide a moderately detailed explanation suitable for medical students."
                elif expertise == "Professional":
                    enhanced_question += "\n\nPlease provide a detailed, professional-level explanation with complete medical terminology."
                
                # Add language instruction for selected language
                if language != "English":
                    enhanced_question += f"\n\nIMPORTANT: Provide the complete answer in {language} language only."
                
                # Also request English version for bilingual display
                english_question = question
                if expertise == "Patient-Friendly":
                    english_question += "\n\nPlease provide a simple, easy-to-understand explanation suitable for patients."
                elif expertise == "Medical Student":
                    english_question += "\n\nPlease provide a moderately detailed explanation suitable for medical students."
                elif expertise == "Professional":
                    english_question += "\n\nPlease provide a detailed, professional-level explanation with complete medical terminology."
                
                # Get response in selected language
                result = api.qna_medical(enhanced_question)
                
                # Get English response if language is not English
                english_result = None
                if language != "English" and result.get("success"):
                    english_result = api.qna_medical(english_question)

                st.markdown("---")
                
                if result.get("success"):
                    st.success("✅ Answer Ready!")
                    
                    st.markdown(
                        f'<div class="chat-bubble-user"><strong>Your Question:</strong><br>{question}</div>',
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(f"**Response Level:** {expertise}")
                    
                    # Display bilingual response
                    if language == "English":
                        st.markdown(result["message"])
                    else:
                        display_bilingual_response(
                            language, 
                            result["message"],
                            english_result["message"] if english_result and english_result.get("success") else None
                        )
                    
                    if result.get("demo_mode"):
                        st.markdown('<div class="demo-mode">⚠️ Demo Mode: Using sample response</div>', unsafe_allow_html=True)
                    
                    st.info("💡 **Note:** This is AI-generated information. Please consult a healthcare professional for medical advice.")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")

# ========== REPORT ANALYZER PAGE ==========
elif st.session_state.selected_tool == "📄 Report Analyzer":
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top: 0;">📄 Medical Report Analyzer</h2>
        <p>Upload your medical report and get AI-powered analysis in your preferred language</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language Selection
    language = language_selector_component("report")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "📤 Upload Medical Reports",
        type=['txt', 'pdf', 'docx', 'jpg', 'png', 'jpeg'],
        accept_multiple_files=True,
        help="Upload your medical reports for AI analysis"
    )
    
    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")
        for file in uploaded_files:
            st.markdown(f"""
            <div class="file-card">
                📄 {file.name} ({(len(file.getvalue()) / 1024):.1f} KB)
            </div>
            """, unsafe_allow_html=True)
    
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Comprehensive Analysis", "Abnormal Values Only", "Risk Assessment", "Quick Summary"]
    )
    
    additional_notes = st.text_area(
        "Additional instructions (optional):",
        height=100,
        placeholder="E.g., Focus on liver function tests, Explain medical terms, etc."
    )
    
    if st.button("🔬 Analyze Report", type="primary", use_container_width=True):
        if not uploaded_files and not additional_notes:
            st.warning("⚠️ Please upload a report or enter instructions")
        else:
            with st.spinner(f"📊 Analyzing report in {language}..."):
                # Build analysis message with language instruction
                analysis_msg = f"{analysis_type}"
                if additional_notes:
                    analysis_msg += f" | Notes: {additional_notes}"
                
                if language != "English":
                    analysis_msg += f"\n\nIMPORTANT: Provide the complete analysis in {language} language only."
                
                # Get response in selected language
                result = api.analyze_report(analysis_msg, uploaded_files)
                
                # Get English response if language is not English
                english_result = None
                if language != "English" and result.get("success"):
                    english_analysis_msg = f"{analysis_type}"
                    if additional_notes:
                        english_analysis_msg += f" | Notes: {additional_notes}"
                    english_result = api.analyze_report(english_analysis_msg, uploaded_files)
                
                st.markdown("---")
                
                if result.get("success"):
                    st.success("✅ Analysis Complete!")
                    st.markdown("### 📋 Analysis Results")
                    
                    # Display bilingual response
                    if language == "English":
                        st.markdown(result["message"])
                    else:
                        display_bilingual_response(
                            language,
                            result["message"],
                            english_result["message"] if english_result and english_result.get("success") else None
                        )
                    
                    if result.get("demo_mode"):
                        st.markdown('<div class="demo-mode">⚠️ Demo Mode: Using sample response</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

# ========== HOSPITAL FINDER PAGE ==========
elif st.session_state.selected_tool == "🏥 Hospital Finder":
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top: 0;">🏥 Hospital Finder</h2>
        <p>Find specialized hospitals in your preferred language</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language Selection
    language = language_selector_component("hospital")
    
    col1, col2 = st.columns(2)
    
    with col1:
        query = st.text_input(
            "🩺 What medical service do you need?",
            placeholder="e.g., Cardiac surgery, Neurology, Emergency care..."
        )
        
        location = st.selectbox(
            "📍 Select City:",
            ["Pune", "Mumbai", "Aurangabad", "Nagpur", "Nashik", "Kolhapur", "Indore", "Bhopal", "Delhi", "Chennai", "Lucknow"]
        )
    
    with col2:
        specializations = st.multiselect(
            "🏷️ Specializations (optional):",
            ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Oncology", "General Surgery", "Emergency"]
        )
    
    st.markdown("---")
    
    if st.button("🔍 Find Hospitals", type="primary", use_container_width=True):
        if not query:
            st.warning("⚠️ Please enter what medical service you need")
        else:
            with st.spinner(f"🏥 Searching hospitals in {language}..."):
                # Build search query with language instruction
                search_query = f"Find hospitals for: {query} in {location}"
                if specializations:
                    search_query += f" specializing in {', '.join(specializations)}"
                
                if language != "English":
                    search_query += f"\n\nIMPORTANT: Provide the complete response in {language} language only."
                
                # Get response in selected language
                result = api.find_hospitals(search_query, location)
                
                # Get English response if language is not English
                english_result = None
                if language != "English" and result.get("success"):
                    english_search_query = f"Find hospitals for: {query} in {location}"
                    if specializations:
                        english_search_query += f" specializing in {', '.join(specializations)}"
                    english_result = api.find_hospitals(english_search_query, location)
                
                st.markdown("---")
                
                if result.get("success"):
                    st.success("✅ Search Complete!")
                    st.markdown("### 🏥 Recommended Hospitals")
                    
                    # Display bilingual response
                    if language == "English":
                        st.markdown(result["message"])
                    else:
                        display_bilingual_response(
                            language,
                            result["message"],
                            english_result["message"] if english_result and english_result.get("success") else None
                        )
                    
                    if result.get("demo_mode"):
                        st.markdown('<div class="demo-mode">⚠️ Demo Mode: Using sample response</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Search failed: {result.get('error', 'Unknown error')}")

# ========== MEDICINE EXPLAINER PAGE ==========
elif st.session_state.selected_tool == "💊 Medicine Explainer":
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top: 0;">💊 Medicine Explainer</h2>
        <p>Upload your prescription and get medicine explanations in your preferred language</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language Selection
    language = language_selector_component("medicine")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "📤 Upload Prescription",
        type=['txt', 'pdf', 'docx', 'jpg', 'png', 'jpeg'],
        accept_multiple_files=True,
        help="Upload your prescription for AI analysis"
    )
    
    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")
        for file in uploaded_files:
            st.markdown(f"""
            <div class="file-card">
                💊 {file.name} ({(len(file.getvalue()) / 1024):.1f} KB)
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        detail_level = st.select_slider(
            "📊 Detail Level:",
            options=["Basic", "Moderate", "Detailed"],
            value="Moderate"
        )
        include_generics = st.checkbox("💰 Find Generic Alternatives", True)
    
    with col2:
        check_interactions = st.checkbox("⚠️ Check Drug Interactions", True)
        include_side_effects = st.checkbox("📋 List Side Effects", True)
    
    additional_notes = st.text_area(
        "Additional instructions (optional):",
        height=80,
        placeholder="E.g., Focus on diabetes medicines, Check for allergies, etc."
    )
    
    if st.button("🔬 Explain Medicines", type="primary", use_container_width=True):
        if not uploaded_files and not additional_notes:
            st.warning("⚠️ Please upload a prescription or enter instructions")
        else:
            with st.spinner(f"💊 Analyzing prescription in {language}..."):
                # Build analysis message with language
                analysis_parts = [f"{detail_level} medicine analysis"]
                if include_generics:
                    analysis_parts.append("Include generic alternatives")
                if check_interactions:
                    analysis_parts.append("Check drug interactions")
                if include_side_effects:
                    analysis_parts.append("List side effects")
                if additional_notes:
                    analysis_parts.append(f"Notes: {additional_notes}")
                
                analysis_msg = " | ".join(analysis_parts)
                
                if language != "English":
                    analysis_msg += f"\n\nIMPORTANT: Provide the complete analysis in {language} language only."
                
                # Get response in selected language
                result = api.explain_medicines(analysis_msg, uploaded_files)
                
                # Get English response if language is not English
                english_result = None
                if language != "English" and result.get("success"):
                    english_analysis_msg = " | ".join(analysis_parts)
                    english_result = api.explain_medicines(english_analysis_msg, uploaded_files)
                
                st.markdown("---")
                
                if result.get("success"):
                    st.success("✅ Analysis Complete!")
                    st.markdown("### 💊 Medicine Analysis")
                    
                    # Display bilingual response
                    if language == "English":
                        st.markdown(result["message"])
                    else:
                        display_bilingual_response(
                            language,
                            result["message"],
                            english_result["message"] if english_result and english_result.get("success") else None
                        )
                    
                    if include_generics and not result.get("demo_mode"):
                        with st.expander("💰 Generic Alternatives Information"):
                            st.markdown("""
                            **Common Generic Savings:**
                            
                            | Brand Name | Generic Alternative | Typical Savings |
                            |------------|---------------------|-----------------|
                            | Metformin | Metformin HCl | 85% |
                            | Atorvastatin | Atorvastatin Calcium | 78% |
                            | Losartan | Losartan Potassium | 82% |
                            
                            💡 Generic medicines contain the same active ingredients and are equally effective.
                            """)
                    
                    if result.get("demo_mode"):
                        st.markdown('<div class="demo-mode">⚠️ Demo Mode: Using sample response</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

# ========== BILL AUDITOR PAGE ==========
elif st.session_state.selected_tool == "💰 Bill Auditor":
    st.markdown("""
    <div class="glass-card">
        <h2 style="margin-top: 0;">💰 Medical Bill Auditor</h2>
        <p>Upload your medical bill and get cost analysis in your preferred language</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language Selection
    language = language_selector_component("bill")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "📤 Upload Medical Bill",
        type=['txt', 'pdf', 'docx', 'jpg', 'png', 'jpeg'],
        accept_multiple_files=True,
        help="Upload your medical bill for AI analysis"
    )
    
    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")
        for file in uploaded_files:
            st.markdown(f"""
            <div class="file-card">
                💰 {file.name} ({(len(file.getvalue()) / 1024):.1f} KB)
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔍 Check for:**")
        check_overcharges = st.checkbox("🚨 Overcharges", True)
        check_duplicates = st.checkbox("🔄 Duplicate Charges", True)
    
    with col2:
        analysis_depth = st.radio(
            "📊 Analysis Depth:",
            ["Quick Audit", "Detailed Analysis"],
            label_visibility="collapsed"
        )
    
    additional_notes = st.text_area(
        "Additional instructions (optional):",
        height=80,
        placeholder="E.g., Compare with insurance rates, Focus on medicine costs, etc."
    )
    
    if st.button("🔍 Analyze Bill", type="primary", use_container_width=True):
        if not uploaded_files and not additional_notes:
            st.warning("⚠️ Please upload a medical bill or enter instructions")
        else:
            with st.spinner(f"💰 Auditing bill in {language}..."):
                # Build analysis message with language
                analysis_parts = [f"{analysis_depth}"]
                if check_overcharges:
                    analysis_parts.append("Check overcharges")
                if check_duplicates:
                    analysis_parts.append("Check duplicates")
                if additional_notes:
                    analysis_parts.append(f"Notes: {additional_notes}")
                
                analysis_msg = " | ".join(analysis_parts)
                
                if language != "English":
                    analysis_msg += f"\n\nIMPORTANT: Provide the complete audit report in {language} language only."
                
                # Get response in selected language
                result = api.analyze_bill(analysis_msg, uploaded_files)
                
                # Get English response if language is not English
                english_result = None
                if language != "English" and result.get("success"):
                    english_analysis_msg = " | ".join(analysis_parts)
                    english_result = api.analyze_bill(english_analysis_msg, uploaded_files)
                
                st.markdown("---")
                
                if result.get("success"):
                    st.success("✅ Audit Complete!")
                    st.markdown("### 📊 Audit Results")
                    
                    # Display bilingual response
                    if language == "English":
                        st.markdown(result["message"])
                    else:
                        display_bilingual_response(
                            language,
                            result["message"],
                            english_result["message"] if english_result and english_result.get("success") else None
                        )
                    
                    if result.get("demo_mode"):
                        st.markdown('<div class="demo-mode">⚠️ Demo Mode: Using sample audit report</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Audit failed: {result.get('error', 'Unknown error')}")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; padding: 20px;">
    <p style="font-size: 1.1em;">🏥 <strong>CHRONOCHECK</strong> • CHECK • CARE • CLARITY</p>
    <p style="font-size: 0.9em;">
        Medical AI Assistant • Comprehensive Healthcare Tools
    </p>
    <p style="font-size: 0.8em; margin-top: 10px;">
        ⚠️ For informational purposes only. Always consult healthcare professionals.
    </p>
</div>
""", unsafe_allow_html=True)