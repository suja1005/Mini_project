# MongoDB Schema Design

## Database Name: `career_guidance_db`

### Collections Overview

1. **`users`**:
   - `_id`: ObjectId
   - `email`: string (unique)
   - `hashed_password`: string
   - `full_name`: string
   - `created_at`: datetime

2. **`student_profiles`**:
   - `_id`: ObjectId
   - `user_id`: string
   - `degree`: string
   - `department`: string
   - `year_of_study`: int
   - `cgpa`: float
   - `technical_skills`: array of `{ skill_name: string, proficiency: string, score: float }`
   - `soft_skills`: array of `{ skill_name: string, rating: float }`
   - `interests`: array of string
   - `career_goals`: object

3. **`careers` & `career_requirements`**:
   - `_id`: ObjectId
   - `career_id`: string (unique identifier)
   - `title`: string
   - `description`: string
   - `required_skills`: map / array of `{ skill: string, required_score: float, weight: float }`
   - `required_soft_skills`: map / array
   - `aptitude_requirements`: map / array
   - `opportunity_indicator`: float
   - `learning_difficulty`: string ("Low" | "Medium" | "High")

4. **`assessments` & `assessment_questions`**:
   - Question bank across logical reasoning, numerical ability, verbal ability, and technical domains.
   - User assessment submissions and evaluated results.

5. **`skill_evidence`**:
   - Verified project submissions, GitHub links, test results, certifications, and interviews.

6. **`roadmaps` & `roadmap_tasks`**:
   - Adaptive skill remediation milestones customized to gap size and career urgency.

7. **`progress` & `employability_scores`**:
   - Historical snapshots of employability score trajectory (recalculated over time).
