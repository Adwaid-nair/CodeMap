# Deploying CodeMap for Free

This guide explains the **best free hosting stack** for CodeMap:
- **Backend (Python)**: [Render](https://render.com) (Free Web Service)
- **Frontend (React)**: [Vercel](https://vercel.com) (Free Static Hosting)

## Prerequisites
1.  Push your code to a GitHub repository.

## Step 1: Deploy Backend (Render)
1.  Log in to **Render** and click **New +** -> **Web Service**.
2.  Connect your GitHub repository.
3.  **Settings**:
    *   **Root Directory**: `backend`
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4.  **Environment Variables**:
    *   `PYTHON_VERSION`: `3.9.0` (Recommended)
    *   `CORS_ORIGINS`: `https://your-frontend-project.vercel.app` (You will update this *after* deploying the frontend).
5.  Click **Create Web Service**.
6.  **Copy the Backend URL** (e.g., `https://codemap-backend.onrender.com`).

## Step 2: Deploy Frontend (Vercel)
1.  Log in to **Vercel** and click **Add New** -> **Project**.
2.  Import your GitHub repository.
3.  **Framework Preset**: Select **Vite** (It should detect it automatically).
4.  **Root Directory**: Click "Edit" and select `frontend`.
5.  **Environment Variables**:
    *   Key: `VITE_API_URL`
    *   Value: `https://codemap-backend.onrender.com` (The URL from Step 1)
6.  Click **Deploy**.

## Step 3: Final Connection
1.  Once Vercel finishes, copy your **Frontend Domain** (e.g., `https://codemap.vercel.app`).
2.  Go back to **Render** -> Dashboard -> Settings -> Environment Variables.
3.  Update (or Add) `CORS_ORIGINS` with your actual Vercel domain.
4.  **Redeploy** the backend (Manual Deploy -> Deploy latest commit) to apply the CORS change.

## Conclusion
Your CodeMap app is now live!
- **Frontend**: Hosted on Vercel (Fast, Global CDN)
- **Backend**: Hosted on Render (Free container)
