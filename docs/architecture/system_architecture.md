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
3. **Evidence-Based Employability**: Distinguishes claimed skills, submitted certificates/projects, practically assessed skills, and skills verified through practical performance plus project evidence. Certificates alone never verify a skill.
4. **Adaptive Continuous Feedback**: Practical assessment results are saved per student and update skill performance, remediation priorities, and roadmap recommendations after every valid attempt.
5. **Sequential Student Workflow**: Student Profile → Career Recommendation → Career Selection → Career Decision & Risk Analysis → Employability Evidence Engine → Practical Skill Assessment → Weak Skill Identification → Personalized Adaptive Roadmap → Progress Tracking.

### Practical Assessment and Roadmap
- FastAPI generates randomized, skill-specific question sets from the authenticated student's profile, selected career requirements, and project/certificate evidence.
- Private answer keys remain in MongoDB; submission validation and per-skill scoring run on the backend. Attempts and question history are retained per student.
- The roadmap prioritizes skills below 70%, orders the weakest skills first, and supplies beginner, intermediate, and advanced learning phases. Strong skills are not assigned redundant beginner remediation.
- `/roadmap` APIs require at least one completed practical assessment. Existing career phases and progress tracking remain available after that prerequisite.
