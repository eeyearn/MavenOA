# Setup Guide - Maven Drive Copilot Assessment

This guide will walk you through setting up the project step-by-step.

## Prerequisites

Before you begin, ensure you have:
- **Node.js 18+** and npm installed
- **Python 3.9+** installed
- A **Google account** for Drive access
- **Git** installed

## Step 1: Google Cloud Setup (15 minutes)

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Maven Drive Copilot" or similar
4. Click "Create"

### 1.2 Enable Google Drive API

1. In the Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on it and press "Enable"

### 1.3 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: Maven Drive Copilot
   - User support email: your email
   - Developer contact: your email
   - Scopes: Add `../auth/drive.readonly`
   - Test users: Add your Gmail address
   - Save and continue
4. Back to creating OAuth client ID:
   - Application type: **Web application**
   - Name: Drive Copilot Client
   - Authorized redirect URIs: `http://localhost:8000/api/auth/callback`
   - Click "Create"
5. **Copy the Client ID and Client Secret** - you'll need these!

### 1.4 Add Test Users

1. Go to "OAuth consent screen"
2. Scroll to "Test users"
3. Add your Gmail address
4. Save

## Step 2: Clone and Setup Project

```bash
# Clone or download the project
cd maven-drive-copilot

# Verify structure
ls
# Should see: frontend/ backend/ README.md
```

## Step 3: Backend Setup

### 3.1 Create Virtual Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### 3.2 Install Base Dependencies

```bash
pip install -r requirements.txt
```

### 3.3 Choose and Install Vector Database

**Option A: ChromaDB (Recommended - Easiest)**
```bash
pip install chromadb
```

**Option B: Pinecone**
```bash
pip install pinecone-client
```

**Option C: Qdrant**
```bash
pip install qdrant-client
```

### 3.4 Choose and Install Embedding Provider

**Option A: OpenAI (Recommended - Best Quality)**
```bash
pip install openai
```

**Option B: Sentence Transformers (Free, Local)**
```bash
pip install sentence-transformers
```

**Option C: Cohere**
```bash
pip install cohere
```

### 3.5 (Optional) Install LLM for Chat

If implementing the chat service:

```bash
# For OpenAI GPT
pip install openai  # Already installed if using OpenAI embeddings

# For Anthropic Claude
pip install anthropic

# For Cohere
pip install cohere
```

### 3.6 Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

Add your credentials:
```env
# Google OAuth (Required)
GOOGLE_CLIENT_ID=your_client_id_from_step_1.3
GOOGLE_CLIENT_SECRET=your_client_secret_from_step_1.3
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/callback

# Vector Database (choose one)
# If using Pinecone:
# PINECONE_API_KEY=your_pinecone_key
# PINECONE_ENVIRONMENT=your_environment

# Embedding Provider (choose one)
# If using OpenAI:
OPENAI_API_KEY=your_openai_key

# If using Cohere:
# COHERE_API_KEY=your_cohere_key

# Application
PORT=8000
ENVIRONMENT=development
```

### 3.7 Verify Backend Setup

```bash
# Test imports
python -c "from src.main import app; print('Backend setup successful!')"
```

## Step 4: Frontend Setup

Open a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# This should install all dependencies including:
# - React & React DOM
# - React Query
# - Axios
# - Tailwind CSS
# - Vite
# - TypeScript
```

## Step 5: Start the Application

### 5.1 Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # Activate venv if not already active

# Start server
python -m src.main

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5.2 Start Frontend (Terminal 2)

```bash
cd frontend

# Start dev server
npm run dev

# You should see:
# VITE v5.x.x  ready in xxx ms
# ➜  Local:   http://localhost:3000/
```

### 5.3 Verify Everything Works

1. Open browser to http://localhost:3000
2. You should see the Maven Drive Copilot UI
3. Click "Connect Google Drive"
4. You should be redirected to Google OAuth
5. Sign in with your test account
6. Grant permissions
7. You should be redirected back to the app

## Step 6: Create Test Data in Google Drive

Before implementing, create some test files:

1. Go to [Google Drive](https://drive.google.com)
2. Create a folder called "Test Project"
3. Create a Google Doc called "Project Overview" with content:
   ```
   Project Overview

   This is our new initiative to build a drive copilot.
   We're using vector databases for semantic search.
   The project will be completed in Q1 2024.
   ```
4. Create another Google Doc "Meeting Notes":
   ```
   Meeting Notes - Jan 15, 2024

   Attendees: Team members

   Discussion:
   - Reviewed project timeline
   - Discussed architecture choices
   - Decided on using ChromaDB for vector storage
   ```

## Step 7: Implement Services

Now you're ready to implement! See [ASSESSMENT.md](ASSESSMENT.md) for details.

Start with:
1. [backend/src/services/ingestion_service.py](backend/src/services/ingestion_service.py)
2. [backend/src/services/retrieval_service.py](backend/src/services/retrieval_service.py)

## Troubleshooting

### Google OAuth Issues

**Error: "Access blocked: Maven Drive Copilot has not completed the Google verification process"**
- Solution: Make sure you added yourself as a test user in the OAuth consent screen

**Error: "redirect_uri_mismatch"**
- Solution: Ensure redirect URI in Google Cloud Console exactly matches: `http://localhost:8000/api/auth/callback`

### Backend Issues

**ImportError: No module named 'src'**
- Solution: Make sure you're running `python -m src.main` from the `backend` directory

**Connection refused on port 8000**
- Solution: Check if backend is running, check for port conflicts

### Frontend Issues

**Network Error when calling API**
- Solution: Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify proxy is configured in vite.config.ts

**npm install fails**
- Solution: Try deleting `node_modules` and `package-lock.json`, then run `npm install` again

### Vector Database Issues

**ChromaDB: "Cannot connect to database"**
- Solution: ChromaDB runs in-memory by default, no setup needed. Check if library is installed.

**Pinecone: "Invalid API key"**
- Solution: Verify your Pinecone API key in .env file

## Getting Help

If you're stuck on setup:
1. Check the error message carefully
2. Review this guide again
3. Email us: yuv2bindal@gmail.com, sultan.shayaan@gmail.com

## Next Steps

Once setup is complete:
1. Read [ASSESSMENT.md](ASSESSMENT.md) for implementation details
2. Review the code structure in [README.md](README.md)
3. Start implementing the services
4. Test as you go

Good luck!
