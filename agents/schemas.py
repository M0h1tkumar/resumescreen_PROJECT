from pydantic import BaseModel, Field
from typing import List, Optional

class PersonalInfo(BaseModel):
    name: Optional[str] = Field(None, description="Full name of the candidate")
    email: Optional[str] = Field(None, description="Email address of the candidate")
    phone: Optional[str] = Field(None, description="Phone number of the candidate")

class Education(BaseModel):
    degree: str = Field(..., description="Name of the degree")
    institution: str = Field(..., description="Name of the university or institution")
    graduation_year: Optional[int] = Field(None, description="Year of graduation")

class Experience(BaseModel):
    job_title: str = Field(..., description="Job title or role")
    company: str = Field(..., description="Company name")
    duration: Optional[str] = Field(None, description="Duration of employment")
    description: Optional[str] = Field(None, description="Description of responsibilities and achievements")

class CandidateProfile(BaseModel):
    personal_info: PersonalInfo = Field(..., description="Personal information")
    summary: Optional[str] = Field(None, description="Professional summary")
    skills: List[str] = Field(default_factory=list, description="List of technical and soft skills")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    experience: List[Experience] = Field(default_factory=list, description="Professional experience")

class ScoreOutput(BaseModel):
    score: int = Field(description="Alignment score from 0 to 100")

class AnomaliesOutput(BaseModel):
    anomalies: List[str] = Field(description="List of flagged anomalies")

class QuestionsOutput(BaseModel):
    questions: List[str] = Field(description="List of interview questions")
