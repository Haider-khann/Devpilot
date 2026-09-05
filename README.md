# 🚀 DevPilot — AI-Powered Code Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-orange)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-purple)
![License](https://img.shields.io/badge/License-MIT-red)

**An AI/ML platform that analyzes GitHub repositories for code quality, security vulnerabilities, and documentation coverage.**

</div>

---

## 📊 Platform Statistics

| Metric | Score |
|--------|-------|
| Code Quality | **99.27%** 🏆 |
| Security Score | **71%** 🛡️ |
| Documentation | **36.52%** 📚 |
| ML Accuracy | **100%** 🤖 |
| Files Analyzed | **8** |
| Lines Analyzed | **2,287** |

---

## ✨ Features

### 🔍 Repository Analysis
- Fetches and analyzes GitHub repositories
- Supports 26+ file types (Python, JavaScript, HTML, CSS, Markdown, etc.)
- Calculates: files, lines, functions, classes
- Background processing with real-time status

### 🤖 ML-Powered Intelligence
- **Language Classifier**: Custom RandomForest model (100% accuracy)
- **Quality Predictor**: Scores code quality 0-100
- **Similarity Detection**: TF-IDF + Cosine similarity for duplicates
- 26-feature extraction pipeline

### 🔒 Security Scanner
- 14 vulnerability patterns
- Detects: Hardcoded secrets, SQL injection, XSS, Command injection
- Severity classification (critical/high/medium/low)
- Recommendations for each issue

### 💬 AI Features (Google Gemini)
- Code summarization
- Code improvement suggestions
- Code generation from natural language
- Two-mode chatbot (Support + AI Assistant)

### 📊 Reports
- PDF reports (ReportLab)
- Word documents (python-docx)
- JSON export
- Report preview page

### ⚖️ Repository Comparison
- Side-by-side metrics comparison
- Winner detection per metric

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| ML | scikit-learn, RandomForest, TF-IDF |
| AI | Google Gemini API |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Reports | ReportLab, python-docx |

---

## 📋 Prerequisites

- **Python 3.11+**
- **Gemini API Key** (Free: https://aistudio.google.com/app/apikey)
- **GitHub Token** (Optional: https://github.com/settings/tokens)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Haider-Khann/Devpilot
cd Devpilot
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create `.env` file in `backend/` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

### 4. Run Backend

```bash
python main.py
```

Backend runs at: `http://localhost:8000`

### 5. Run Frontend

Open a **new terminal**:

```bash
cd frontend
python -m http.server 8080
```

Frontend opens at: `http://localhost:8080`

---

## 📡 API Endpoints

### Repository Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/repositories` | Add repo for analysis |
| GET | `/api/repositories` | List all repos |
| GET | `/api/repositories/{id}` | Get repo details |
| DELETE | `/api/repositories/{id}` | Delete repo |
| GET | `/api/repositories/{id}/security` | Get security issues |
| GET | `/api/repositories/{id}/files` | List repo files |
| POST | `/api/repositories/{id}/reanalyze` | Re-run analysis |

### ML Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ml/train` | Train language classifier |
| POST | `/api/ml/train-quality` | Train quality predictor |
| POST | `/api/ml/predict-language` | Predict code language |
| POST | `/api/ml/predict-quality` | Predict quality score |
| POST | `/api/ml/similarity` | Check code similarity |
| GET | `/api/ml/status` | ML model status |

### AI Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat` | Chat with AI |
| POST | `/api/ai/chat-smart` | Smart chat (2 modes) |
| POST | `/api/ai/improve-code` | Improve code |
| POST | `/api/ai/generate-code` | Generate code |
| POST | `/api/ai/summarize-code` | Summarize code |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports/analysis/{id}` | Analysis report |
| GET | `/api/reports/analysis/{id}/pdf` | PDF download |
| GET | `/api/reports/analysis/{id}/word` | Word download |
| GET | `/api/reports/statistics` | Platform stats |
| GET | `/api/reports/comparison/{id1}/{id2}` | Comparison report |

### Other
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze-code` | Security scan |
| POST | `/api/compare` | Compare repos |
| GET | `/api/stats` | Platform stats |
| GET | `/health` | Health check |

---

## 📁 Project Structure

```
Devpilot/
├── backend/
│   ├── main.py              # FastAPI backend (all endpoints)
│   ├── gemini_service.py    # AI service (Gemini)
│   ├── ml_service.py        # ML models (RandomForest, TF-IDF)
│   ├── ml_models/           # Trained model files
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Main dashboard
│   └── report.html          # Report preview page
└── README.md
```

---

## 🎯 Use Cases

- **Recruiters**: Quick assessment of candidate's code
- **Developers**: Evaluate libraries before using
- **Teams**: Monitor code quality
- **Students**: Learn what "good code" looks like

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Gemini API not working | Check `.env` file has `GEMINI_API_KEY` |
| GitHub rate limit | Add `GITHUB_TOKEN` to `.env` |
| Port 8000 busy | Change port in `main.py` |

---

## 📚 What I Learned

- **ML Pipeline**: Feature engineering → Training → Evaluation → Deployment
- **Security Analysis**: Pattern-based vulnerability detection
- **Full-Stack**: FastAPI backend + modern frontend
- **AI Integration**: Google Gemini API, prompt engineering
- **Problem Solving**: Debugging, optimization, false positive reduction

---

## 📄 License

MIT License - feel free to use and modify!

---

<div align="center">

### 💡 Built with ❤️ by Haider Khan

[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/Haider-Khann)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/haiderkhan-rk/)

</div>
