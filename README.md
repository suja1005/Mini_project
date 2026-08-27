# AI-Powered Career Guidance and Employability Enhancement Platform

> **Final-Year Academic Project Prototype — Phase 1 Implementation**  
> *An integrated career decision and employability framework that combines explainable career fit scoring, risk & achievability analysis, evidence-supported skill verification, and adaptive career roadmaps.*

---

## 🌟 Executive Summary

Traditional career guidance systems act as static recommenders, suggesting job titles based solely on superficial interest surveys or simple skill tags. They fail to answer critical practical questions for students:
- *How realistically achievable is this target career from my current position?*
- *What specific skill gaps must I bridge first?*
- *How will my verified employability evolve over time?*

This platform introduces **Career Decision Intelligence + Employability Enhancement**, providing a deterministic, transparent, and explainable guidance pipeline.

---

## 🎯 System Architecture & Data Flow

```
Student Profile Onboarding (Academic, Technical, Soft Skills, Aptitude, Goals)
                        │
                        ▼
           Skill & Aptitude Assessment
                        │
                        ▼
   Explainable Multi-Career Recommendation Scoring
 (Technical 40%, Interest 20%, Aptitude 15%, Academic 10%, Pref 15%)
                        │
                        ▼
      Career Decision & Risk Analysis Dashboard
  (Fit Score, Current Employability, Gap, Learning Effort, Achievability)
                        │
                        ▼
    ┌───────────────────┴───────────────────┐
    │     Upcoming Future Phase Engine      │
    │  - Evidence Engine (Claimed vs Verified)
    │  - Adaptive Employability Roadmap     │
    │  - Employability Progress Tracker     │
    └───────────────────────────────────────┘
```

---

## 🚀 Phase 1 Implementation Scope

This repository represents **Phase 1 (30% Baseline Prototype)** built specifically for the initial project review.

### ✅ Completed in Phase 1
1. **Base Project Infrastructure**: Modular React + Vite frontend and FastAPI backend setup with MongoDB database connection setup.
2. **UI Design System**: Sleek glassmorphism theme using Tailwind CSS, responsive layouts, sidebar navigation, custom card widgets, and Recharts visualization components.
3. **Frontend Client Router**: Complete client-side routing covering:
   - `/login` — Auth Login Shell
   - `/register` — Auth Registration Shell
   - `/onboarding` — AI Student Profile Onboarding Shell (Module B)
   - `/assessment` — Skill & Aptitude Assessment Shell (Module C)
   - `/recommendations` — Multi-Career Recommendation Shell (Module D)
   - `/career/:careerId` — Basic Decision & Risk Analysis Shell (Module E)
   - `/dashboard` — Central Student Overview Dashboard
4. **Backend Health & System API**: `GET /api/v1/health` verifying system lifespan, CORS policies, database connection, and module statuses.
5. **Seed Datasets**: Pre-structured dataset templates for 20 tech careers, 30+ skills (with 30/60/85 mapping), and 15 assessment questions.

### 🔮 Reserved for Subsequent Phases
- Phase 2: Full recommendation scoring logic execution, MongoDB collection persistence, JWT auth endpoints, live assessment score persistence.
- Phase 3: Evidence Engine (Claimed Skill ≠ Verified Skill), Adaptive Employability Roadmap, and Progress Tracker.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | React.js, Vite, Tailwind CSS, React Router, Axios, Recharts, Lucide Icons |
| **Backend** | Python 3.13, FastAPI, Uvicorn, Pydantic v2, PyJWT, Passlib (bcrypt) |
| **Database** | MongoDB / Async Motor Client (Atlas compatible) |
| **AI / Data Science** | NumPy, Pandas, Scikit-Learn |

---

## 📁 Repository Folder Structure

```
AI-Career Guidance/
├── frontend/                  # React + Vite Client Application
│   ├── src/
│   │   ├── components/        # Reusable UI components (Navbar, Sidebar, MetricCard)
│   │   ├── pages/             # Page views (Dashboard, Login, Register, Onboarding, etc.)
│   │   ├── layouts/           # MainLayout & Auth wrappers
│   │   ├── services/          # Axios API communication services
│   │   ├── App.jsx            # React Router table
│   │   ├── index.css          # Tailwind directives & glassmorphism CSS
│   │   └── main.jsx           # React app entry point
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── .env.example
├── backend/                   # FastAPI Backend Server
│   ├── app/
│   │   ├── api/               # API endpoint routers (health, auth, profile, etc.)
│   │   ├── core/              # Config, settings, security tokens
│   │   ├── database/          # Async Motor MongoDB connection setup
│   │   ├── models/            # Database collection schema definitions
│   │   ├── schemas/           # Pydantic validation models
│   │   ├── services/          # Core business services
│   │   ├── ml/                # Scoring models (explainable match & risk math)
│   │   └── main.py            # FastAPI entry point
│   ├── data/                  # Prototype seed datasets (careers, skills, questions)
│   ├── requirements.txt       # Python dependencies
│   └── .env.example
├── docs/                      # Architecture & research documentation
├── .env.example               # Root configuration template
└── README.md                  # System documentation
```

---

## ⚡ Quick Start Guide

### Prerequisites
- **Node.js**: v18+ or v22+
- **Python**: v3.10+
- **MongoDB**: Local MongoDB server or MongoDB Atlas connection URI

---

### Step 1: Backend Setup & Execution

1. Navigate to the project root:
   ```bash
   cd "d:\AI-Career Guidance"
   ```

2. Activate virtual environment (if available) or create one:
   ```bash
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Run the FastAPI dev server:
   ```bash
   python -m uvicorn app.main:app --app-dir backend --reload --port 8000
   ```

5. Verify backend health endpoint:
   - OpenAPI Docs: `http://127.0.0.1:8000/docs`
   - Health Endpoint: `http://127.0.0.1:8000/api/v1/health`

---

### Step 2: Frontend Setup & Execution

1. Open a second terminal and navigate to `frontend`:
   ```bash
   cd "d:\AI-Career Guidance\frontend"
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Launch Vite local development server:
   ```bash
   npm run dev
   ```

4. Open browser at: `http://localhost:5173`

---

## 📊 Explainable Scoring & Risk Methodology

The system deliberately avoids opaque "black-box" LLM scoring for numerical decisions. Recommendation scores follow an explicit multi-factor weighted formula:

$$\text{Career Fit Score} = (S \times 0.40) + (I \times 0.20) + (A \times 0.15) + (Ac \times 0.10) + (P \times 0.15)$$

Where:
- $S$: Technical Skill Match Score
- $I$: Domain Interest Match
- $A$: Aptitude Score (Logical, Numerical, Analytical)
- $Ac$: Academic Relevance Score
- $P$: Career Goal Preference Match

### Employability & Achievability Metrics
- **Skill Gap**: $\text{Required Level} - \text{Current Verified Level}$
- **Employability Gap**: $\text{Required Employability Target} - \text{Current Readiness Score}$
- **Achievability Estimate**: Model-based calculation integrating Fit Score, Employability Gap, Learning Effort (LOW/MEDIUM/HIGH), and Risk (LOW/MEDIUM/HIGH).

---

## 📌 Phase 1 Review Demo Flow

1. **Dashboard Home** (`/dashboard`): Overview of current employability, top match, target gap, and future phase architecture status.
2. **Student Profile Onboarding** (`/profile` or `/onboarding`): 3-step profile builder collecting academic background, technical skill proficiency (30/60/85), soft skills, and interest domains.
3. **Assessment Shell** (`/assessment`): 15-question aptitude preview across Logical Reasoning, Numerical Ability, and Technical Aptitude.
4. **Career Recommendations** (`/recommendations`): Top 3–5 matched career cards displaying Fit Score (e.g. AI Engineer 87%), "Why Recommended", and "Needs Improvement".
5. **Career Decision & Risk Analysis** (`/career/ai-engineer`): Detailed analysis view featuring metrics, Recharts bar graph comparing Current vs Required skills, priority gap table, and future phase placeholders.
