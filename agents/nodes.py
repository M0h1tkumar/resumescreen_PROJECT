from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import ScreeningState
from agents.schemas import CandidateProfile
import json

def get_llm():
    # Assumes GOOGLE_API_KEY is in env
    return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.2)

from langchain_core.runnables import RunnableConfig

def parser_node(state: ScreeningState, config: RunnableConfig) -> dict:
    """Extracts structured JSON from raw resume text."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(CandidateProfile)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert HR parsing system. Extract candidate information strictly into the requested format."),
        ("human", "Parse the following resume text:\n\n{raw_text}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"raw_text": state["raw_text"]}, config=config)
    
    return {"candidate_profile": result}

def scoring_node(state: ScreeningState, config: RunnableConfig) -> dict:
    """Matches candidate profile against Job Description and calculates alignment score."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical recruiter. Compare the candidate profile to the job description. Output ONLY a JSON object with a single key 'score' containing an integer from 0 to 100 representing the alignment score."),
        ("human", "Candidate Profile:\n{profile}\n\nJob Description:\n{jd}")
    ])
    
    chain = prompt | llm
    profile_json = state["candidate_profile"].model_dump_json() if state.get("candidate_profile") else "{}"
    response = chain.invoke({"profile": profile_json, "jd": state["job_description"]}, config=config)
    
    try:
        # Strip markdown json block if present
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        score_data = json.loads(content)
        score = int(score_data.get("score", 0))
    except Exception as e:
        print(f"Error parsing score: {e}")
        score = 0
        
    return {"alignment_score": score}

def ranking_node(state: ScreeningState, config: RunnableConfig) -> dict:
    """Calculates employment gaps and anomalies."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze the candidate's experience for any employment gaps, overlapping roles, or anomalies. Output a JSON array of strings, where each string is a flagged anomaly. If none, output []."),
        ("human", "Candidate Profile:\n{profile}")
    ])
    
    chain = prompt | llm
    profile_json = state["candidate_profile"].model_dump_json() if state.get("candidate_profile") else "{}"
    response = chain.invoke({"profile": profile_json}, config=config)
    
    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        anomalies = json.loads(content)
        if not isinstance(anomalies, list):
            anomalies = []
    except:
        anomalies = []
        
    return {"anomalies": anomalies}

def interview_question_node(state: ScreeningState, config: RunnableConfig) -> dict:
    """Generates targeted interview questions based on anomalies and skills."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate 3-5 specific interview questions based on the candidate's skills and any flagged anomalies. Output ONLY a JSON array of strings."),
        ("human", "Skills: {skills}\nAnomalies: {anomalies}")
    ])
    
    skills = state["candidate_profile"].skills if state.get("candidate_profile") else []
    anomalies = state.get("anomalies", [])
    
    chain = prompt | llm
    response = chain.invoke({"skills": skills, "anomalies": anomalies}, config=config)
    
    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        questions = json.loads(content)
        if not isinstance(questions, list):
            questions = []
    except:
        questions = []
        
    return {"interview_questions": questions}
