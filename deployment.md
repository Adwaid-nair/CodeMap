# Deploying CodeMap for Free

This guide explains how to deploy CodeMap (both Backend and Frontend) for free using [Render](https://render.com).

## Prerequisites
1.  Push your code to a GitHub repository.

## Step 1: Deploy Backend (Python/FastAPI)
1.  Log in to **Render** and click **New +** -> **Web Service**.
2.  Connect your GitHub repository.
3.  Choose the **backend** directory as the Root Directory (if asked, or set manually in settings).
    *   **Root Directory**: `backend`
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4.  **Environment Variables**:
    *   Add `PYTHON_VERSION` = `3.9.0` (optional)
    *   Add `CORS_ORIGINS` = `https://your-frontend-app.onrender.com` (After you deploy frontend, come back and update this. For now, you can leave it empty to allow all or set `*`).
5.  Click **Create Web Service**.
6.  Copy the **URL** (e.g., `https://codemap-backend.onrender.com`).

## Step 2: Deploy Frontend (React/Vite)
1.  Click **New +** -> **Static Site**.
2.  Connect the same GitHub repository.
3.  Settings:
    *   **Root Directory**: `frontend`
    *   **Build Command**: `npm run build`
    *   **Publish Directory**: `dist`
4.  **Environment Variables**:
    *   Add `VITE_API_URL` = `https://codemap-backend.onrender.com` (The URL from Step 1).
5.  Click **Create Static Site**.

## Conclusion
Your app should now be live!
-   Open the Frontend URL.
-   The frontend will communicate with the backend using the configuring URL.
