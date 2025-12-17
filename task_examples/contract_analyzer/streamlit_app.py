import os
import uuid

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Contract Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .analysis-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #2d5a87;
    }
    
    .risk-high {
        border-left-color: #dc3545;
        background: #fff5f5;
    }
    
    .risk-medium {
        border-left-color: #ffc107;
        background: #fffdf5;
    }
    
    .risk-low {
        border-left-color: #28a745;
        background: #f5fff5;
    }
    
    /* Metric styling */
    .metric-container {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        flex: 1;
        min-width: 120px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d5a87;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
    }
    
    /* Chat styling */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        max-width: 85%;
    }
    
    .user-message {
        background: #e3f2fd;
        margin-left: auto;
        margin-right: 0;
    }
    
    .assistant-message {
        background: #f5f5f5;
        margin-left: 0;
        margin-right: auto;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2d5a87 0%, #1e3a5f 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(45, 90, 135, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2d5a87;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        from PyPDF2 import PdfReader
        from io import BytesIO
        
        reader = PdfReader(BytesIO(file_content))
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n\n".join(text_parts)
    except ImportError:
        st.error("PyPDF2 is required for PDF support. Install with: pip install PyPDF2")
        return ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        from io import BytesIO
        
        doc = Document(BytesIO(file_content))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except ImportError:
        st.error("python-docx is required for DOCX support. Install with: pip install python-docx")
        return ""
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if "contract_text" not in st.session_state:
        st.session_state.contract_text = ""
    
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None


def get_or_create_agent():
    """Get existing agent or create a new one."""
    if st.session_state.agent is None:
        from contract_analyzer.agent import create_contract_analyzer_agent
        st.session_state.agent = create_contract_analyzer_agent(
            session_id=st.session_state.session_id
        )
    return st.session_state.agent


def render_header():
    """Render the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>📄 Contract Analyzer</h1>
        <p>AI-powered contract analysis for legal and business insights</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with upload and settings."""
    with st.sidebar:
        st.markdown("### 📁 Upload Contract")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "txt"],
            help="Upload a contract in PDF, Word, or text format"
        )
        
        if uploaded_file is not None:
            file_content = uploaded_file.read()
            file_type = uploaded_file.name.split(".")[-1].lower()
            
            if file_type == "pdf":
                text = extract_text_from_pdf(file_content)
            elif file_type == "docx":
                text = extract_text_from_docx(file_content)
            else:
                text = file_content.decode("utf-8")
            
            if text:
                st.session_state.contract_text = text
                st.success(f"✅ Loaded: {uploaded_file.name}")
                st.info(f"📝 {len(text):,} characters extracted")
        
        st.divider()
        
        st.markdown("### ✍️ Or Paste Contract")
        
        pasted_text = st.text_area(
            "Paste contract text",
            height=150,
            placeholder="Paste your contract text here..."
        )
        
        if pasted_text and pasted_text != st.session_state.contract_text:
            if st.button("Use Pasted Text", use_container_width=True):
                st.session_state.contract_text = pasted_text
                st.rerun()
        
        st.divider()
        
        st.markdown("### ⚙️ Settings")
        
        analysis_type = st.selectbox(
            "Analysis Type",
            options=["full", "summary", "risk", "extraction"],
            format_func=lambda x: {
                "full": "📊 Full Analysis",
                "summary": "📝 Executive Summary",
                "risk": "⚠️ Risk Assessment",
                "extraction": "🔍 Data Extraction"
            }.get(x, x)
        )
        
        st.divider()
        
        if st.button("🗑️ Clear Session", use_container_width=True):
            st.session_state.contract_text = ""
            st.session_state.analysis_result = None
            st.session_state.chat_history = []
            st.session_state.agent = None
            st.session_state.session_id = str(uuid.uuid4())[:8]
            st.rerun()
        
        return analysis_type


def render_analysis_tab(analysis_type: str):
    """Render the main analysis tab."""
    if not st.session_state.contract_text:
        st.info("👈 Upload a contract or paste text to begin analysis")
        
        if st.button("📄 Load Sample Contract"):
            st.session_state.contract_text = get_sample_contract()
            st.rerun()
        return
    
    with st.expander("📄 Contract Preview", expanded=False):
        st.text_area(
            "Contract Text",
            value=st.session_state.contract_text[:5000] + ("..." if len(st.session_state.contract_text) > 5000 else ""),
            height=200,
            disabled=True
        )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🔍 Analyze Contract",
            use_container_width=True,
            type="primary"
        )
    
    if analyze_button:
        with st.spinner("Analyzing contract... This may take a moment."):
            try:
                from contract_analyzer.agent import create_analysis_task
                from upsonic import Task
                
                agent = get_or_create_agent()
                task = create_analysis_task(
                    st.session_state.contract_text,
                    analysis_type
                )
                
                result = agent.do(task)
                st.session_state.analysis_result = str(result)
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.session_state.analysis_result = None
    
    if st.session_state.analysis_result:
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        st.markdown(st.session_state.analysis_result)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "📥 Download as Text",
                data=st.session_state.analysis_result,
                file_name="contract_analysis.txt",
                mime="text/plain"
            )
        
        with col2:
            md_content = f"""# Contract Analysis Report

Generated by Contract Analyzer

---

{st.session_state.analysis_result}
"""
            st.download_button(
                "📥 Download as Markdown",
                data=md_content,
                file_name="contract_analysis.md",
                mime="text/markdown"
            )


def render_chat_tab():
    """Render the interactive chat tab."""
    st.markdown("### 💬 Ask Questions About Your Contract")
    
    if not st.session_state.contract_text:
        st.info("👈 Upload a contract first to start asking questions")
        return
    
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            with st.chat_message("user"):
                st.write(content)
        else:
            with st.chat_message("assistant"):
                st.write(content)
    
    user_question = st.chat_input("Ask a question about your contract...")
    
    if user_question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })
        
        with st.chat_message("user"):
            st.write(user_question)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    from upsonic import Task
                    
                    agent = get_or_create_agent()
                    
                    task = Task(
                        description=f"""Based on the following contract, please answer this question:

Question: {user_question}

<contract>
{st.session_state.contract_text}
</contract>

Provide a helpful, accurate answer based on the contract content."""
                    )
                    
                    result = agent.do(task)
                    response = str(result)
                    
                    st.write(response)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {e}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_msg
                    })


def get_sample_contract() -> str:
    """Return a sample contract for testing."""
    return """SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of January 15, 2024 ("Effective Date") by and between:

ABC Technology Solutions Inc., a Delaware corporation ("Provider"), and 
XYZ Enterprises LLC, a California limited liability company ("Client").

RECITALS

WHEREAS, Provider is in the business of providing software development and IT consulting services; and
WHEREAS, Client desires to engage Provider to provide certain services as described herein;

NOW, THEREFORE, in consideration of the mutual covenants and agreements hereinafter set forth, the parties agree as follows:

1. SERVICES
Provider agrees to provide the following services to Client:
- Custom software development
- System integration consulting
- Technical support and maintenance
- Training and documentation

2. TERM
This Agreement shall commence on the Effective Date and continue for a period of two (2) years ("Initial Term"), unless earlier terminated in accordance with Section 8. This Agreement shall automatically renew for successive one (1) year periods unless either party provides written notice of non-renewal at least sixty (60) days prior to the end of the then-current term.

3. COMPENSATION
3.1 Fees. Client shall pay Provider the following fees:
- Monthly retainer: $15,000
- Additional development work: $175 per hour
- Emergency support: $250 per hour

3.2 Payment Terms. All invoices are due within thirty (30) days of receipt. Late payments shall accrue interest at 1.5% per month.

4. CONFIDENTIALITY
Each party agrees to maintain the confidentiality of all Confidential Information disclosed by the other party. This obligation shall survive for a period of five (5) years following termination of this Agreement.

5. INTELLECTUAL PROPERTY
5.1 Pre-existing IP. Each party retains ownership of its pre-existing intellectual property.
5.2 Work Product. All work product created by Provider specifically for Client shall be owned by Client upon full payment.

6. WARRANTIES
Provider warrants that all services will be performed in a professional and workmanlike manner. Provider makes no other warranties, express or implied, including any implied warranty of merchantability or fitness for a particular purpose.

7. LIMITATION OF LIABILITY
IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES. PROVIDER'S TOTAL LIABILITY SHALL NOT EXCEED THE FEES PAID BY CLIENT IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.

8. TERMINATION
8.1 For Cause. Either party may terminate this Agreement upon thirty (30) days written notice if the other party materially breaches this Agreement and fails to cure such breach within the notice period.
8.2 For Convenience. Either party may terminate this Agreement without cause upon ninety (90) days written notice.

9. INDEMNIFICATION
Client shall indemnify and hold harmless Provider from any claims arising from Client's use of the services or Client's breach of this Agreement.

10. GOVERNING LAW
This Agreement shall be governed by the laws of the State of Delaware, without regard to its conflict of laws principles. Any disputes shall be resolved through binding arbitration in Wilmington, Delaware.

11. ENTIRE AGREEMENT
This Agreement constitutes the entire agreement between the parties and supersedes all prior negotiations, representations, and agreements.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

ABC TECHNOLOGY SOLUTIONS INC.
By: ________________________
Name: John Smith
Title: Chief Executive Officer
Date: January 15, 2024

XYZ ENTERPRISES LLC
By: ________________________
Name: Jane Doe
Title: Managing Director
Date: January 15, 2024
"""


def main():
    """Main application entry point."""
    if not os.getenv("OPENAI_API_KEY"):
        st.error("""
        ⚠️ **OpenAI API Key Required**
        
        Please set your `OPENAI_API_KEY` environment variable or create a `.env` file.
        
        See `.env.example` for reference.
        """)
        st.stop()
    
    initialize_session_state()
    
    render_header()
    
    analysis_type = render_sidebar()
    
    tab1, tab2 = st.tabs([
        "📊 Analysis",
        "💬 Chat"
    ])
    
    with tab1:
        render_analysis_tab(analysis_type)
    
    with tab2:
        render_chat_tab()
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Built with <a href='https://github.com/Upsonic/Upsonic'>Upsonic AI Agent Framework</a> | "
        f"Session: {st.session_state.session_id}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
