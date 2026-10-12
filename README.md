# AI-Powered Career Guidance and Employability Enhancement Platform

A full-stack, evidence-based career intelligence platform that provides continuous feedback, risk-aware career recommendations, transparent skill verification, and adaptive employability roadmaps.

---

## 🌟 Core Philosophy

The platform addresses critical student questions through explainable AI models:
1. **Which career suits me?** (Multi-Career Recommendation based on technical skills, interests, aptitude, and academics)
2. **Why is it suitable?** (Explainable breakdown of strong areas and missing competencies)
3. **How achievable is it from my current position?** (Career risk, learning effort, and model-based achievability estimates)
4. **How employable am I currently?** (Current readiness vs. target career benchmark)
5. **What skills/evidence am I missing?** (Transparent gap analysis)
6. **What should I do next to become more job-ready?** (Personalized high-impact action recommendations)
7. **Am I actually improving?** (Continuous tracking with recalculation upon task completion and evidence submission)

> ⚠️ **Responsible AI Notice:** All scores, readiness percentages, and achievability ratings are **model-based algorithmic estimates** intended for guidance and decision support—they are not employment guarantees.

---

## 🏗️ System Architecture

```text
                 React Frontend (Vite, Tailwind CSS, Recharts)
                                      │
                                      ▼
                 FastAPI Backend (REST API, Python 3.12)
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
 Recommendation Engine        Employability Engine           Evidence Engine
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      ▼
                            MongoDB Database Layer
                                      │
                                      ▼
                             AI/ML Layer & Models
                                      │
                                      ▼
                            LLM Explanations Service
```

---

## 💻 Tech Stack

### Frontend
- **Framework:** React 19 + Vite
- **Styling:** Tailwind CSS + PostCSS
- **Routing:** React Router DOM (v7)
- **Data Visualization:** Recharts
- **Icons & UI:** Lucide React
- **HTTP Client:** Axios (configured with JWT interceptors)

### Backend
- **Framework:** FastAPI (Python 3.12)
- **Server:** Uvicorn ASGI
- **Validation:** Pydantic v2 & Pydantic Settings
- **Database Driver:** Motor (Async MongoDB) & PyMongo
- **Authentication:** JWT (python-jose) & bcrypt (passlib)
- **Data & ML:** Pandas, NumPy, Scikit-learn

### Database
- **Primary Database:** MongoDB (Local or MongoDB Atlas)

---

## 📁 Project Structure

```text
career-intelligence-platform/
│
├── frontend/                     # React + Vite application
│   ├── src/
│   │   ├── components/           # Reusable UI components (Navbar, Sidebar, MetricCard)
│   │   ├── pages/                # Application routes (Dashboard, Onboarding, etc.)
│   │   ├── layouts/              # Main layout wrapper
│   │   ├── services/             # Axios API integration modules
│   │   ├── hooks/                # Custom React hooks (useMetrics, etc.)
│   │   ├── utils/                # Formatting and scoring helpers
│   │   ├── context/              # Authentication context provider
│   │   ├── App.jsx               # Main router and view mounts
│   │   └── main.jsx              # React entry point
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.example
│
├── backend/                      # FastAPI Python application
│   ├── app/
│   │   ├── api/                  # API route controllers (health, auth, profile, etc.)
│   │   ├── core/                 # App configurations and security settings
│   │   ├── database/             # MongoDB connection lifecycle
│   │   ├── models/               # Database document structures
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── services/             # Business logic & scoring engines
│   │   ├── ml/                   # ML models and recommendation logic
│   │   └── main.py               # FastAPI application entry point
│   ├── data/                     # Seeds and reference data (careers, skills, questions)
│   │   ├── careers.json / .csv
│   │   ├── skills.json / .csv
│   │   └── assessment_questions.json / .csv
│   ├── requirements.txt
│   └── .env.example
│
├── docs/                         # Engineering & Academic Documentation
│   ├── architecture/             # System diagrams and data flow
│   ├── database/                 # MongoDB schemas and collections
│   └── research/                 # Mathematical formulas and evaluation metrics
│
├── .gitignore
├── .env.example
└── README.md
```

---

## ⚙️ Environment Configuration

### 1. Root Configuration (`.env`)
```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=career_guidance_db
JWT_SECRET=your-super-secret-jwt-key
LLM_API_KEY=
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 2. Backend Configuration (`backend/.env`)
```env
PROJECT_NAME="AI-Powered Career Guidance & Employability Platform"
API_V1_STR="/api/v1"
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=career_guidance_db
JWT_SECRET=your-super-secret-jwt-key
LLM_API_KEY=
ENV=development
```

### 3. Frontend Configuration (`frontend/.env`)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
- **Python:** 3.10+ (Recommended: Python 3.12)
- **Node.js:** v18+ (Recommended: v20 or v22) & npm
- **MongoDB:** Community Edition running locally or MongoDB Atlas connection string

---

### Step 1: Backend Setup

1. Open a terminal in the project root:
   ```bash
   # Create and activate Python virtual environment
   python -m venv .venv

   # On Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Configure environment:
   ```bash
   cp backend/.env.example backend/.env
   ```

4. Launch the FastAPI server:
   ```bash
   python backend/app/main.py
   # Or using uvicorn:
   uvicorn app.main:app --reload --app-dir backend
   ```
   - API will be accessible at: `http://localhost:8000`
   - Interactive Swagger Docs: `http://localhost:8000/docs`
   - Health Check Endpoint: `http://localhost:8000/api/v1/health`

---

### Step 2: Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   ```

4. Start the Vite development server:
   ```bash
   npm run dev
   ```
   - Web application will be available at: `http://localhost:5173`

---

## 🩺 System Health Check

You can verify that the system foundation is operating correctly by testing the health check endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

Expected JSON response:
```json
{
  "status": "healthy",
  "version": "2.0.0-phase1",
  "service": "AI-Powered Career Guidance & Employability Enhancement Platform API",
  "database_connected": true,
  "phase": "Phase 1 - Project Foundation"
}
```

---

## 🔄 Development Roadmap

- [x] **Phase 1: Project Foundation & Architecture Setup**
- [ ] **Phase 2: Career & Skill Data Intelligence**
- [ ] **Phase 3: Secure JWT Authentication**
- [ ] **Phase 4: AI Student Profile & Onboarding**
- [ ] **Phase 5: Multi-Career Recommendation Algorithm**
- [ ] **Phase 6: Career Decision & Risk Intelligence**
- [ ] **Phase 7: Employability Measurement Engine**
- [ ] **Phase 8: Multi-Modal Evidence Engine**
- [ ] **Phase 9: Adaptive Remediation Roadmap**
- [ ] **Phase 10: Employability Progress Tracker & Feedback Loop**
- [ ] **Phase 11: LLM Explanations & Natural Language Feedback**
- [ ] **Phase 12: Comprehensive Integration Testing & Quality Assurance**
- [ ] **Phase 13: Production Deployment**
