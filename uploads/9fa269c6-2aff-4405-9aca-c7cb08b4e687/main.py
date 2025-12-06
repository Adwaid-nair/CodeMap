from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
# Import analyzers
from analyzers import get_analyzer

app = FastAPI(title="CodeMap Backend")

# In-memory store for demo purposes
PROJECTS = {"demo_deps": {"language": "python", "original_filename": "demo_deps.py"}}
ANALYSIS_RESULTS = {
    "demo_deps": {
        "nodes": [
            {"id": "func1", "label": "main_func", "type": "function", "file": "main.py"},
            {"id": "func2", "label": "helper", "type": "function", "file": "utils.py"},
            {"id": "func3", "label": "core_logic", "type": "function", "file": "core.py"}
        ],
        "edges": [
            {"source": "func1", "target": "func2"},
            {"source": "func1", "target": "func3"}
        ],
        "complexity": {
            "file_metrics": {
                "core.py": 10,
                "utils.py": 2,
                "main.py": 5
            },
            "average_complexity": 5.6
        }
    }
}

# Create uploads folder if missing
os.makedirs("uploads", exist_ok=True)

# Allowed frontend origins (Vercel URL added after deployment)
FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    # "https://your-vercel-url.vercel.app"  ← we will update this later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "CodeMap backend running!"}


@app.post("/upload")
async def upload_code(file: UploadFile = File(...)):
    project_id = str(uuid.uuid4())
    project_dir = f"uploads/{project_id}"
    os.makedirs(project_dir, exist_ok=True)
    
    save_path = f"{project_dir}/{file.filename}"
    
    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)
        
    # Run analysis
    # Detect language - simplified for MVP
    language = "python" # Default
    if file.filename.endswith(".java"):
        language = "java"
    elif file.filename.endswith((".cpp", ".h", ".hpp")):
        language = "cpp"
        
    analyzer = get_analyzer(language, project_dir)
    if analyzer:
        try:
            results = analyzer.analyze()
            ANALYSIS_RESULTS[project_id] = results
            PROJECTS[project_id] = {"language": language, "original_filename": file.filename}
        except Exception as e:
            print(f"Analysis failed: {e}")
            ANALYSIS_RESULTS[project_id] = {"nodes": [], "edges": [], "complexity": {}, "error": str(e)}
    else:
        ANALYSIS_RESULTS[project_id] = {"nodes": [], "edges": [], "complexity": {}}

    return {
        "project_id": project_id,
        "filename": file.filename,
        "size": len(contents),
        "saved_to": save_path,
        "message": "Analysis complete" 
    }

@app.get("/api/analyze/{language}/{project_id}")
def get_analysis_result(language: str, project_id: str):
    if project_id not in ANALYSIS_RESULTS:
        # For dev/test resilience, verify if we can re-analyze or just return 404
        raise HTTPException(status_code=404, detail="Project not found")
    return ANALYSIS_RESULTS[project_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
