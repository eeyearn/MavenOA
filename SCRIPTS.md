# Startup Scripts Documentation

This project includes automated scripts to simplify setup and running the application.

## Available Scripts

### 1. `dev.sh` - Development Mode (Recommended)

**Best for active development and debugging.**

```bash
./dev.sh
```

**What it does:**
- ✅ Checks for Node.js and Python installation
- ✅ Creates Python virtual environment (if needed)
- ✅ Installs all backend dependencies
- ✅ Installs all frontend dependencies
- ✅ Starts backend on port 8000
- ✅ Starts frontend on port 3000
- ✅ Shows **combined live logs** from both services with color-coded prefixes

**Features:**
- **Live logs** - See both backend and frontend output in one terminal
- **Color-coded** - `[BACKEND]` in cyan, `[FRONTEND]` in magenta
- **Clean shutdown** - Press `Ctrl+C` to stop both services
- **Error visibility** - Immediately see errors from either service

**When to use:**
- During development
- When debugging issues
- When you want to see all logs in one place

**Example output:**
```
[BACKEND]  INFO:     Uvicorn running on http://0.0.0.0:8000
[FRONTEND] VITE v5.0.11  ready in 432 ms
[BACKEND]  INFO:     Started server process
[FRONTEND] ➜  Local:   http://localhost:3000/
```

---

### 2. `start.sh` - Background Mode

**Best for running services in the background.**

```bash
./start.sh
```

**What it does:**
- ✅ Everything `dev.sh` does, plus:
- ✅ Runs services in **background**
- ✅ Creates log files in `logs/` directory
- ✅ Saves process IDs for clean shutdown
- ✅ Checks if ports 3000 and 8000 are available
- ✅ Validates services started successfully

**Features:**
- **Background processes** - Services run independently
- **Log files** - Output saved to `logs/backend.log` and `logs/frontend.log`
- **Process management** - PIDs saved for easy stopping
- **Port validation** - Ensures ports are free before starting

**When to use:**
- When you want services running while doing other work
- For longer testing sessions
- When you don't need to watch logs constantly

**Log files:**
```
logs/
├── backend.log     # Backend service logs
├── frontend.log    # Frontend service logs
├── backend.pid     # Backend process ID
└── frontend.pid    # Frontend process ID
```

**View logs in real-time:**
```bash
# Watch backend logs
tail -f logs/backend.log

# Watch frontend logs
tail -f logs/frontend.log

# Watch both
tail -f logs/backend.log logs/frontend.log
```

---

### 3. `stop.sh` - Stop All Services

**Cleanly stops all services started by `start.sh`.**

```bash
./stop.sh
```

**What it does:**
- ✅ Reads process IDs from log files
- ✅ Gracefully stops backend process
- ✅ Gracefully stops frontend process
- ✅ Force-kills if necessary
- ✅ Cleans up any processes on ports 3000 and 8000
- ✅ Removes PID files

**When to use:**
- After running `start.sh` to stop background services
- When services are stuck
- To clean up any orphaned processes

**Note:** If you used `dev.sh`, just press `Ctrl+C` to stop. This script is for `start.sh`.

---

## Quick Reference

| Task | Command |
|------|---------|
| Start for development | `./dev.sh` |
| Start in background | `./start.sh` |
| Stop background services | `./stop.sh` |
| View backend logs | `tail -f logs/backend.log` |
| View frontend logs | `tail -f logs/frontend.log` |
| Check if running | `lsof -i :3000,8000` |

---

## First Time Setup

### Before Running Any Script

1. **Configure Google OAuth** (required):
   ```bash
   cd backend
   cp .env.example .env
   nano .env  # Add your Google OAuth credentials
   ```

2. **Make scripts executable** (if not already):
   ```bash
   chmod +x dev.sh start.sh stop.sh
   ```

3. **Run the script:**
   ```bash
   ./dev.sh
   ```

---

## What Each Script Checks

### Prerequisites Validation

All scripts verify:
- ✅ Node.js is installed (v18+)
- ✅ npm is available
- ✅ Python 3 is installed (v3.9+)

If any are missing, the script exits with an error message.

### Environment Setup

1. **Backend:**
   - Creates `venv/` if it doesn't exist
   - Activates virtual environment
   - Upgrades pip
   - Installs dependencies from `requirements.txt`
   - Validates `.env` file exists

2. **Frontend:**
   - Installs dependencies from `package.json`
   - Creates `node_modules/` if needed

---

## Troubleshooting

### Script won't run

**Issue:** `Permission denied`

**Solution:**
```bash
chmod +x dev.sh start.sh stop.sh
```

---

### Port already in use

**Issue:** Port 3000 or 8000 is already in use

**Solution:**
```bash
# Find what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use the stop script
./stop.sh
```

---

### Virtual environment activation fails

**Issue:** `Could not activate virtual environment`

**Solution:**
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Dependencies not installing

**Issue:** pip or npm fails to install dependencies

**Solution for backend:**
```bash
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --verbose
```

**Solution for frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

### Services start but crash immediately

**Issue:** Backend or frontend crashes after starting

**Check backend logs:**
```bash
cat logs/backend.log
```

Common causes:
- Missing `.env` file
- Invalid Google OAuth credentials
- Missing API keys for vector DB/embeddings

**Check frontend logs:**
```bash
cat logs/frontend.log
```

Common causes:
- Backend not running
- Port conflict
- Missing dependencies

---

### Can't stop services

**Issue:** `./stop.sh` doesn't work

**Nuclear option:**
```bash
# Kill everything on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

---

## Windows Users

These scripts are written for **Bash** and work best on:
- ✅ macOS
- ✅ Linux
- ✅ Windows with Git Bash
- ✅ Windows with WSL (Windows Subsystem for Linux)

### Using Git Bash on Windows

1. Install [Git for Windows](https://git-scm.com/download/win)
2. Open **Git Bash** terminal
3. Navigate to project directory
4. Run scripts: `./dev.sh`

### Alternative: Manual Setup on Windows

If the scripts don't work, use manual commands:

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm run dev
```

---

## Advanced Usage

### Running with custom ports

Edit the scripts or set environment variables:

```bash
# In start.sh or dev.sh, modify these lines:
PORT=8000  # Backend port
# Frontend port is in frontend/vite.config.ts
```

### Installing additional dependencies

The scripts don't install vector DB or embedding libraries. You need to add:

```bash
cd backend
source venv/bin/activate

# Choose your stack:
pip install chromadb openai              # ChromaDB + OpenAI
# OR
pip install pinecone-client cohere       # Pinecone + Cohere
# OR
pip install qdrant-client sentence-transformers  # Qdrant + Local embeddings
```

---

## Script Comparison

| Feature | `dev.sh` | `start.sh` |
|---------|----------|------------|
| Live logs in terminal | ✅ | ❌ |
| Background processes | ❌ | ✅ |
| Log files | ❌ | ✅ |
| Easy to stop | ✅ (Ctrl+C) | ⚠️ (need stop.sh) |
| Best for development | ✅ | ❌ |
| Best for background running | ❌ | ✅ |
| Color-coded output | ✅ | ⚠️ (in log files) |

**Recommendation:** Use `dev.sh` for active development, `start.sh` for background testing.

---

## Files Created by Scripts

```
project/
├── logs/                    # Created by start.sh
│   ├── backend.log         # Backend output
│   ├── frontend.log        # Frontend output
│   ├── backend.pid         # Backend process ID
│   └── frontend.pid        # Frontend process ID
├── .pids                   # Combined PIDs (start.sh)
└── backend/
    └── venv/               # Python virtual environment
```

**Safe to delete:**
- `logs/` directory
- `.pids` file
- `backend/venv/` (will be recreated)

**Don't delete:**
- `backend/.env` (your credentials!)

---

## Next Steps

After running the scripts successfully:

1. ✅ Services are running at:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

2. ✅ Start implementing the backend services:
   - `backend/src/services/ingestion_service.py`
   - `backend/src/services/retrieval_service.py`
   - `backend/src/services/chat_service.py` (optional)

3. ✅ Test your implementation:
   - Create test files in Google Drive
   - Click "Start Ingestion"
   - Try searching

---

## Support

If you encounter issues with the scripts:

1. Check this documentation
2. Read error messages carefully
3. Try manual setup as fallback
4. Email: yuv2bindal@gmail.com or sultan.shayaan@gmail.com

Happy coding! 🚀
