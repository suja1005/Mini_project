# System Architecture

## AI-Powered Career Guidance & Employability Enhancement Platform

### High-Level Architecture Overview

```text
                 React Frontend (Vite, Tailwind, Recharts)
                                  │
                                  ▼
                 FastAPI Backend (REST API, Python 3.12)
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
 Recommendation Engine    Employability Engine       Evidence Engine
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  ▼
                        MongoDB Database Layer
                                  │
                                  ▼
                             AI/ML Layer
                                  │
                                  ▼
                             LLM Service
```

### Core Architecture Principles
1. **Separation of Concerns**: Frontend never communicates directly with MongoDB. All data access occurs through FastAPI REST endpoints.
2. **Deterministic Scoring First**: The scoring engines (employability, career fit, risk, confidence) use strict mathematical models. LLMs are never allowed to arbitrarily calculate or invent numerical scores.
3. **Evidence-Based Employability**: Distinguishes between self-claimed skills and evidence-supported skills (assessments, repositories, projects, certifications).
4. **Adaptive Continuous Feedback**: The platform serves as a closed-loop system where completed roadmap tasks and submitted evidence directly update student skill confidence and recalculate career readiness.
