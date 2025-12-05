from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="CodeMap Backend")

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
    contents = await file.read()
    
    save_path = f"uploads/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(contents)

    # Here you will later call your analyzer functions
    return {
        "filename": file.filename,
        "size": len(contents),
        "saved_to": save_path
    }
