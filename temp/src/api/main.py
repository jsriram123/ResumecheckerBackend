from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List
import uuid

from src.data_processing.text_extractor import TextExtractor
from src.data_processing.resume_parser import ResumeParser
from src.data_processing.jd_parser import JDParser
from src.scoring.scoring_orchestrator import ScoringOrchestrator
from src.database.db_manager import DatabaseManager

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

text_extractor = TextExtractor()
resume_parser = ResumeParser()
jd_parser = JDParser()
scoring_orchestrator = ScoringOrchestrator()
db_manager = DatabaseManager()

@app.post("/evaluate-resume/")
async def evaluate_resume(jd_file: UploadFile, resume_file: UploadFile):
    try:
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        # Save uploaded files temporarily
        jd_path = f"temp/jd_{uuid.uuid4().hex}.txt"
        resume_path = f"temp/resume_{uuid.uuid4().hex}.txt"
        
        with open(jd_path, "wb") as jd_buffer:
            jd_buffer.write(await jd_file.read())
        
        with open(resume_path, "wb") as resume_buffer:
            resume_buffer.write(await resume_file.read())
        
        # Extract text
        jd_text = text_extractor.extract_text(jd_path)
        resume_text = text_extractor.extract_text(resume_path)
        
        # Parse content
        jd_data = jd_parser.parse_jd(jd_text)
        resume_data = resume_parser.parse_resume(resume_text)
        
        # Calculate scores
        result = scoring_orchestrator.calculate_relevance_score(
            {"text": resume_text, **resume_data},
            {"text": jd_text, **jd_data}
        )
        
        # Save to database
        evaluation_id = db_manager.save_evaluation_result(
            resume_file.filename, jd_file.filename, result
        )
        
        # Clean up temporary files
        os.remove(jd_path)
        os.remove(resume_path)
        
        return JSONResponse(content={
            "evaluation_id": evaluation_id, 
            "resume_name": resume_file.filename,
            "jd_name": jd_file.filename,
            **result
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/")
async def get_results(jd_name: str = None, min_score: float = None):
    results = db_manager.get_evaluation_results({
        "jd_name": jd_name,
        "min_score": min_score
    })
    return JSONResponse(content=results)

@app.get("/")
async def root():
    return {"message": "Resume Evaluation API is running!"}