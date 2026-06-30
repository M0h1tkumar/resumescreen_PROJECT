import streamlit as st
import tempfile
import os
from langfuse.langchain import CallbackHandler
import sys
from dotenv import load_dotenv

load_dotenv()

# Add parent dir to path so we can import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.graph import screening_app
from agents.state import ScreeningState
from utils.parsers import extract_text

st.set_page_config(page_title="Resume Screening Agent", layout="wide")

st.title("Multi-Agent Resume Screening System")

# Init Langfuse Handler
langfuse_handler = CallbackHandler()

st.sidebar.header("Configuration")
job_description = st.sidebar.text_area("Job Description", height=300, placeholder="Paste job description here...")

uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=['pdf', 'docx'], accept_multiple_files=True)

if st.button("Run Screening"):
    if not job_description:
        st.error("Please provide a Job Description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        for uploaded_file in uploaded_files:
            st.subheader(f"Results for: {uploaded_file.name}")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
                
            raw_text = extract_text(tmp_path)
            os.remove(tmp_path)
            
            if not raw_text:
                st.error("Failed to extract text from document.")
                continue
                
            initial_state: ScreeningState = {
                "raw_text": raw_text,
                "job_description": job_description,
                "candidate_profile": None,
                "anomalies": [],
                "alignment_score": None,
                "interview_questions": [],
                "metadata": {}
            }
            
            with st.spinner(f"Agents are processing {uploaded_file.name}..."):
                # Pass Langfuse handler to LangGraph config
                config = {"callbacks": [langfuse_handler]}
                try:
                    final_state = screening_app.invoke(initial_state, config=config)
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    
                    score = final_state.get("alignment_score", 0)
                    with col1:
                        st.metric("Alignment Score", f"{score}/100")
                        
                    with col2:
                        profile = final_state.get("candidate_profile")
                        name = "Unknown"
                        if profile:
                            if hasattr(profile, "personal_info") and profile.personal_info:
                                name = getattr(profile.personal_info, "name", "Unknown")
                            elif isinstance(profile, dict) and isinstance(profile.get("personal_info"), dict):
                                name = profile["personal_info"].get("name", "Unknown")
                        st.metric("Candidate Name", str(name) if name else "Unknown")
                        
                    with col3:
                        anomalies = final_state.get("anomalies", [])
                        st.metric("Anomalies Flagged", len(anomalies))
                        
                    st.divider()
                    
                    if anomalies:
                        st.warning("⚠️ Anomalies Detected: " + "; ".join(anomalies))
                    else:
                        st.success("✅ No career anomalies detected.")
                        
                    st.markdown("### Targeted Interview Questions")
                    questions = final_state.get("interview_questions", [])
                    if questions:
                        for idx, q in enumerate(questions):
                            st.write(f"{idx+1}. {q}")
                    else:
                        st.write("No specific questions generated.")
                        
                    with st.expander("View Extracted Profile Details"):
                        if profile:
                            if hasattr(profile, "model_dump"):
                                st.json(profile.model_dump())
                            else:
                                st.json(profile)
                        else:
                            st.write("Profile parsing failed.")
                            
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")

