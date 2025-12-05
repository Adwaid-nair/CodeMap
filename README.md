# CodeMap: Intelligent Codebase Visualization & Analysis Tool

CodeMap is a full-stack tool aimed at developers to visualize and analyze source code structure. It supports Python, Java, and C++ (experimental).

## Features
- **Upload & Parse**: Upload your project source code.
- **Visualizations**:
    - Flowcharts (Mermaid.js)
    - Call Graphs (React Flow)
    - Dependency Maps
    - Complexity Heatmaps
- **Git Integration**: View commit history and diffs.
- **Metrics**: Cyclomatic complexity analysis.

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + TailwindCSS

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
