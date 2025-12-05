import os
import shutil
import uuid
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="CodeMap Backend")

# CORS Setup
origins = os.environ.get("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Models
class ProjectResponse(BaseModel):
    project_id: str
    message: str

class AnalysisResult(BaseModel):
    project_id: str
    language: str
    nodes: List[dict]
    edges: List[dict]
    complexity: Optional[dict] = None

# Routes
@app.get("/")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/upload", response_model=ProjectResponse)
async def upload_code(file: UploadFile = File(...)):
    project_id = str(uuid.uuid4())
    project_path = os.path.join(UPLOAD_DIR, project_id)
    os.makedirs(project_path)
    
    file_path = os.path.join(project_path, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # If zip, unzip (Basic implementation)
    if file.filename.endswith(".zip"):
        import zipfile
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(project_path)
        os.remove(file_path) # cleanup zip

    return {"project_id": project_id, "message": "Upload successful"}

# Placeholder for Analyzers
@app.get("/api/analyze/{language}/{project_id}", response_model=AnalysisResult)
def analyze_project(language: str, project_id: str):
    project_path = os.path.join(UPLOAD_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")

    from analyzers import get_analyzer
    analyzer = get_analyzer(language, project_path)
    
    if not analyzer:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    result = analyzer.analyze()
    
    if "error" in result:
         # In a real app we might return 400 or just partial result. 
         # For now, let's wrap it in the response model structure or raise
         if "nodes" not in result: # distinct error
             raise HTTPException(status_code=500, detail=result["error"])

    return {
        "project_id": project_id,
        "language": language,
        "nodes": result.get("nodes", []),
        "edges": result.get("edges", []),
        "complexity": result.get("complexity", {})
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
