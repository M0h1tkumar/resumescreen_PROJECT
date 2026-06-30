from typing import TypedDict, Optional, List, Dict, Any
from agents.schemas import CandidateProfile

class ScreeningState(TypedDict):
    raw_text: str
    job_description: str
    candidate_profile: Optional[CandidateProfile]
    anomalies: List[str]
    alignment_score: Optional[int]
    interview_questions: List[str]
    metadata: Dict[str, Any]
