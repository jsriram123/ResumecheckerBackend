import streamlit as st
import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Resume Relevance Check System", layout="wide")

st.title("Automated Resume Relevance Check System")
st.markdown("---")

# JD Upload
st.header("1. Upload Job Description")
jd_file = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], key="jd")

# Resume Upload
st.header("2. Upload Resumes")
resume_files = st.file_uploader("Upload Resumes (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], 
                               accept_multiple_files=True, key="resumes")

if st.button("Evaluate Resumes", type="primary") and jd_file and resume_files:
    progress_bar = st.progress(0)
    status_text = st.empty()
    results = []
    
    for i, resume_file in enumerate(resume_files):
        status_text.text(f"Processing {i+1}/{len(resume_files)}: {resume_file.name}")
        
        try:
            files = {
                "jd_file": (jd_file.name, jd_file.getvalue(), jd_file.type),
                "resume_file": (resume_file.name, resume_file.getvalue(), resume_file.type)
            }
            
            response = requests.post(f"{API_URL}/evaluate-resume/", files=files)
            if response.status_code == 200:
                results.append(response.json())
            else:
                st.error(f"Error processing {resume_file.name}: {response.text}")
        except Exception as e:
            st.error(f"Error processing {resume_file.name}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(resume_files))
    
    status_text.text("Processing complete!")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()
    
    if results:
        st.header("Evaluation Results")
        
        for result in results:
            with st.expander(f"{result['resume_name']} - Score: {result['relevance_score']}/100 - {result['verdict']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Scores")
                    st.metric("Overall Relevance", f"{result['relevance_score']}/100")
                    st.metric("Keyword Score", f"{result['keyword_score']}/100")
                    st.metric("Semantic Score", f"{result['semantic_score']}/100")
                    st.metric("Skill Match Score", f"{result['skill_score']}/100")
                    st.metric("Verdict", result['verdict'])
                
                with col2:
                    st.subheader("Missing Skills")
                    if result['missing_skills']:
                        for skill in result['missing_skills']:
                            st.write(f"❌ {skill}")
                    else:
                        st.success("No missing required skills!")
        
        st.download_button(
            label="Download Results as JSON",
            data=json.dumps(results, indent=2),
            file_name="evaluation_results.json",
            mime="application/json"
        )

st.header("View Previous Results")
if st.button("Load Previous Evaluations"):
    try:
        response = requests.get(f"{API_URL}/results/")
        if response.status_code == 200:
            previous_results = response.json()
            
            if previous_results:
                st.subheader("Previous Evaluation Results")
                for result in previous_results:
                    with st.expander(f"{result['resume_name']} for {result['jd_name']} - {result['relevance_score']}/100"):
                        st.write(f"Date: {result['created_at']}")
                        st.write(f"Verdict: {result['verdict']}")
                        st.write(f"Missing Skills: {', '.join(result['missing_skills'])}")
            else:
                st.info("No previous evaluations found.")
        else:
            st.error("Error loading previous results")
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")

st.markdown("---")
st.markdown("Built with ❤️ for Informatics Research Labs")