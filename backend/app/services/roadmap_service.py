import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from app.database.connection import get_database
from app.ml.recommendation_engine import load_careers_data, calculate_career_fit
from app.services.evidence_service import get_or_create_user_evidence, add_project_evidence
from app.services.question_generation_service import question_gen_service

def build_default_tasks_for_career(roadmap_id: str, user_id: str) -> List[Dict[str, Any]]:
    """
    Creates standard structured learning tasks with topics, subtopics, and prerequisites.
    """
    t1_id = f"task_{uuid.uuid4().hex[:8]}"
    t2_id = f"task_{uuid.uuid4().hex[:8]}"
    t3_id = f"task_{uuid.uuid4().hex[:8]}"
    t4_id = f"task_{uuid.uuid4().hex[:8]}"
    t5_id = f"task_{uuid.uuid4().hex[:8]}"
    t6_id = f"task_{uuid.uuid4().hex[:8]}"

    tasks = [
        {
            "id": t1_id,
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 1,
            "phase_name": "Phase 1: Core Fundamentals",
            "title": "Learn Python Fundamentals",
            "description": "Build a strong foundation in Python programming language core syntax and mechanics.",
            "difficulty": "Beginner",
            "estimated_hours": "3 hours",
            "priority": "HIGH",
            "status": "NOT_STARTED",
            "order": 1,
            "prerequisites": [],
            "skill": "Python",
            "type": "Learning",
            "explanation": "Essential prerequisite for AI Engineering and Data Science workflows.",
            "passing_score": 70,
            "verification_status": "Not Started",
            "quiz_score": None,
            "attempts_count": 0,
            "learning_progress_percentage": 0,
            "learning_objectives": [
                "Understand basic Python syntax and variable assignment",
                "Write simple conditional programs using if/elif/else",
                "Use while and for loops to iterate over data",
                "Create reusable functions with parameters and return values",
                "Work with basic collections: lists, tuples, sets, and dictionaries"
            ],
            "topics": [
                {
                    "id": "top_py_1",
                    "title": "Python Basics",
                    "description": "Fundamental variables, data types, and I/O",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_py_1_1", "title": "Variables", "completed": False},
                        {"id": "sub_py_1_2", "title": "Data Types", "completed": False},
                        {"id": "sub_py_1_3", "title": "Input and Output", "completed": False},
                        {"id": "sub_py_1_4", "title": "Type Conversion", "completed": False}
                    ]
                },
                {
                    "id": "top_py_2",
                    "title": "Control Flow",
                    "description": "Conditional branching and iteration structures",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_py_2_1", "title": "if / elif / else", "completed": False},
                        {"id": "sub_py_2_2", "title": "for loop", "completed": False},
                        {"id": "sub_py_2_3", "title": "while loop", "completed": False},
                        {"id": "sub_py_2_4", "title": "break / continue", "completed": False}
                    ]
                },
                {
                    "id": "top_py_3",
                    "title": "Functions",
                    "description": "Function definition, parameter passing, and scope",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_py_3_1", "title": "Function definition", "completed": False},
                        {"id": "sub_py_3_2", "title": "Parameters", "completed": False},
                        {"id": "sub_py_3_3", "title": "Return values", "completed": False},
                        {"id": "sub_py_3_4", "title": "Scope", "completed": False}
                    ]
                },
                {
                    "id": "top_py_4",
                    "title": "Data Structures",
                    "description": "Built-in sequential and mapped data containers",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_py_4_1", "title": "List", "completed": False},
                        {"id": "sub_py_4_2", "title": "Tuple", "completed": False},
                        {"id": "sub_py_4_3", "title": "Set", "completed": False},
                        {"id": "sub_py_4_4", "title": "Dictionary", "completed": False}
                    ]
                }
            ],
            "resources": [
                {"title": "Official Python Tutorial", "type": "Documentation", "url": "https://docs.python.org/3/tutorial/", "provider": "Python.org"},
                {"title": "Python for Beginners Interactive Course", "type": "Interactive", "url": "https://python.org", "provider": "Open Access"}
            ]
        },

        {
            "id": t2_id,
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 2,
            "phase_name": "Phase 2: Data Structures & Advanced Control",
            "title": "Python Functions & Data Structure Optimization",
            "description": "Master list comprehensions, dictionary operations, lambda expressions, and scope mechanics.",
            "difficulty": "Intermediate",
            "estimated_hours": "4 hours",
            "priority": "HIGH",
            "status": "LOCKED",
            "order": 2,
            "prerequisites": [t1_id],
            "skill": "Python",
            "type": "Learning",
            "explanation": "Advanced data structure handling is required for building ML data pipelines.",
            "passing_score": 70,
            "verification_status": "Not Started",
            "quiz_score": None,
            "attempts_count": 0,
            "learning_progress_percentage": 0,
            "learning_objectives": [
                "Utilize list and dictionary comprehensions effectively",
                "Apply map, filter, and lambda functions to sequence transformations",
                "Manage positional and keyword argument unpacking (*args, **kwargs)"
            ],
            "topics": [
                {
                    "id": "top_py_func_1",
                    "title": "Advanced Functions",
                    "description": "Lambda functions, positional & keyword unpacking",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_func_1", "title": "Lambda Functions", "completed": False},
                        {"id": "sub_func_2", "title": "*args and **kwargs", "completed": False},
                        {"id": "sub_func_3", "title": "Higher-Order Functions", "completed": False}
                    ]
                },
                {
                    "id": "top_py_func_2",
                    "title": "Comprehensions",
                    "description": "Efficient set, list, and dict comprehensions",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_comp_1", "title": "List Comprehensions", "completed": False},
                        {"id": "sub_comp_2", "title": "Dict Comprehensions", "completed": False}
                    ]
                }
            ],
            "resources": []
        },

        {
            "id": t3_id,
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 3,
            "phase_name": "Phase 3: Relational Data & SQL",
            "title": "SQL Database Design & Data Querying",
            "description": "Master SQL SELECT queries, WHERE filtering, JOINs, aggregations, and schema normalization.",
            "difficulty": "Beginner",
            "estimated_hours": "4 hours",
            "priority": "MEDIUM",
            "status": "NOT_STARTED",
            "order": 3,
            "prerequisites": [],
            "skill": "SQL",
            "type": "Learning",
            "explanation": "Relational data extraction is crucial for data retrieval in AI pipelines.",
            "passing_score": 70,
            "verification_status": "Not Started",
            "quiz_score": None,
            "attempts_count": 0,
            "learning_progress_percentage": 0,
            "learning_objectives": [
                "Formulate SQL SELECT queries with WHERE and ORDER BY clauses",
                "Perform INNER, LEFT, and RIGHT JOINs across relational tables",
                "Aggregate records using GROUP BY and HAVING clauses"
            ],
            "topics": [
                {
                    "id": "top_sql_1",
                    "title": "SQL Fundamentals",
                    "description": "Data selection and conditional filtering",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_sql_1", "title": "SELECT Queries", "completed": False},
                        {"id": "sub_sql_2", "title": "WHERE Clause Filtering", "completed": False},
                        {"id": "sub_sql_3", "title": "ORDER BY and LIMIT", "completed": False}
                    ]
                },
                {
                    "id": "top_sql_2",
                    "title": "Joins and Aggregation",
                    "description": "Multi-table queries and group summary metrics",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_sql_4", "title": "INNER and LEFT JOINs", "completed": False},
                        {"id": "sub_sql_5", "title": "GROUP BY & HAVING", "completed": False}
                    ]
                }
            ],
            "resources": []
        },

        {
            "id": t4_id,
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 4,
            "phase_name": "Phase 4: Machine Learning Fundamentals",
            "title": "Machine Learning Core Concepts & Model Evaluation",
            "description": "Learn Supervised vs Unsupervised learning, train/test splitting, accuracy metrics, and overfitting.",
            "difficulty": "Intermediate",
            "estimated_hours": "6 hours",
            "priority": "HIGH",
            "status": "LOCKED",
            "order": 4,
            "prerequisites": [t1_id],
            "skill": "Machine Learning",
            "type": "Learning",
            "explanation": "Core algorithmic knowledge required for AI model selection.",
            "passing_score": 70,
            "verification_status": "Not Started",
            "quiz_score": None,
            "attempts_count": 0,
            "learning_progress_percentage": 0,
            "learning_objectives": [
                "Distinguish Supervised Learning from Unsupervised Learning",
                "Evaluate classification models using Accuracy, Precision, and Recall",
                "Diagnose model Overfitting vs Underfitting and apply scaling"
            ],
            "topics": [
                {
                    "id": "top_ml_1",
                    "title": "ML Paradigms",
                    "description": "Supervised, Unsupervised, and Reinforcement Learning",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_ml_1", "title": "Supervised vs Unsupervised", "completed": False},
                        {"id": "sub_ml_2", "title": "Regression vs Classification", "completed": False}
                    ]
                },
                {
                    "id": "top_ml_2",
                    "title": "Model Evaluation",
                    "description": "Validation strategies and metric selection",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_ml_3", "title": "Model Evaluation Metrics", "completed": False},
                        {"id": "sub_ml_4", "title": "Overfitting & Underfitting", "completed": False},
                        {"id": "sub_ml_5", "title": "Feature Scaling", "completed": False}
                    ]
                }
            ],
            "resources": []
        },

        {
            "id": t5_id,
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 5,
            "phase_name": "Phase 5: Capstone Applied Project",
            "title": "Build & Deploy Applied Machine Learning Pipeline",
            "description": "Implement an end-to-end Python ML pipeline, evaluate accuracy, and publish project evidence.",
            "difficulty": "Advanced",
            "estimated_hours": "10 hours",
            "priority": "HIGH",
            "status": "LOCKED",
            "order": 5,
            "prerequisites": [t4_id],
            "skill": "Machine Learning",
            "type": "Project",
            "explanation": "Provides practical evidence proving real-world AI implementation proficiency.",
            "passing_score": 70,
            "verification_status": "Not Started",
            "quiz_score": None,
            "attempts_count": 0,
            "learning_progress_percentage": 0,
            "learning_objectives": [
                "Preprocess raw datasets using Pandas and Scikit-Learn",
                "Train and hyperparameter tune a classification model",
                "Deploy model API and document GitHub evidence"
            ],
            "topics": [
                {
                    "id": "top_proj_1",
                    "title": "Pipeline Engineering",
                    "description": "Data loading, cleaning, feature engineering",
                    "completed": False,
                    "subtopics": [
                        {"id": "sub_proj_1", "title": "Data Preprocessing", "completed": False},
                        {"id": "sub_proj_2", "title": "Model Training", "completed": False},
                        {"id": "sub_proj_3", "title": "API Deployment", "completed": False}
                    ]
                }
            ],
            "resources": []
        }
    ]
    return tasks

async def calculate_employability_metrics(user_id: str, career: Dict[str, Any], verified_skills: Dict[str, int]) -> Dict[str, int]:
    db = get_database()
    profile = None
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})

    if not profile:
        profile = {
            "degree": "B.Tech",
            "interests": ["Artificial Intelligence", "Data Science"],
            "aptitude_scores": {"logical_reasoning": 75, "numerical_ability": 70, "analytical_thinking": 80},
            "target_role": career.get("title", "AI Engineer")
        }

    temp_profile = {**profile, "technical_skills": verified_skills}
    fit_info = calculate_career_fit(temp_profile, career)
    fit_score = fit_info["fit_score"]

    tech_avg = sum(verified_skills.values()) / len(verified_skills) if verified_skills else 40
    apt_avg = sum(profile.get("aptitude_scores", {}).values()) / 3 if profile.get("aptitude_scores") else 70

    current_employability = int((fit_score * 0.50) + (tech_avg * 0.30) + (apt_avg * 0.20))
    current_employability = max(35, min(95, current_employability))
    required_employability = career.get("required_employability", 80)
    employability_gap = max(0, required_employability - current_employability)

    return {
        "fit_score": fit_score,
        "current_employability": current_employability,
        "required_employability": required_employability,
        "employability_gap": employability_gap
    }

async def generate_adaptive_roadmap(user_id: str, career_id: str = "ai-engineer") -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    careers = load_careers_data()
    career = next((c for c in careers if c["id"] == career_id), None) or careers[0]
    roadmap_id = f"rm_{user_id}_{career['id']}"

    evidence_data = await get_or_create_user_evidence(user_id)
    verified_map = {item["skill"]: item["verified_score"] for item in evidence_data.get("skills", [])}

    emp_metrics = await calculate_employability_metrics(user_id, career, verified_map)

    tasks = build_default_tasks_for_career(roadmap_id, user_id)
    phases = [
        "Phase 1: Core Fundamentals",
        "Phase 2: Data Structures & Advanced Control",
        "Phase 3: Relational Data & SQL",
        "Phase 4: Machine Learning Fundamentals",
        "Phase 5: Capstone Applied Project"
    ]

    roadmap_doc = {
        "id": roadmap_id,
        "user_id": user_id,
        "career_id": career["id"],
        "career_title": career["title"],
        "target_employability": emp_metrics["required_employability"],
        "current_employability": emp_metrics["current_employability"],
        "employability_gap": emp_metrics["employability_gap"],
        "total_tasks": len(tasks),
        "verified_tasks": 0,
        "completed_tasks": 0,
        "progress_percentage": 0,
        "phases": phases,
        "last_updated": now_str
    }

    if db is not None:
        await db.roadmaps.update_one(
            {"user_id": user_id},
            {"$set": roadmap_doc},
            upsert=True
        )
        await db.roadmap_tasks.delete_many({"user_id": user_id})
        if tasks:
            insert_tasks = [{**t} for t in tasks]
            await db.roadmap_tasks.insert_many(insert_tasks)

    return await get_user_roadmap(user_id)

async def get_user_roadmap(user_id: str) -> Dict[str, Any]:
    db = get_database()
    if db is not None:
        roadmap = await db.roadmaps.find_one({"user_id": user_id})
        if roadmap:
            cursor = db.roadmap_tasks.find({"user_id": user_id}).sort("order", 1)
            raw_tasks = await cursor.to_list(length=100)
            if not raw_tasks:
                return await generate_adaptive_roadmap(user_id, roadmap.get("career_id", "ai-engineer"))

            # Determine verified tasks map for unlocking logic
            verified_task_ids = set()
            for t in raw_tasks:
                if t.get("status") in ["VERIFIED", "COMPLETED"]:
                    verified_task_ids.add(t.get("id"))

            formatted_tasks = []
            verified_count = 0
            completed_count = 0

            for t in raw_tasks:
                t_id = t.get("id", str(t.get("_id")))
                status = t.get("status", "NOT_STARTED")
                prereqs = t.get("prerequisites", [])

                # Sequential Lock evaluation
                if prereqs and not all(p_id in verified_task_ids for p_id in prereqs):
                    if status != "VERIFIED":
                        status = "LOCKED"
                else:
                    if status == "LOCKED":
                        status = "NOT_STARTED"

                if status in ["VERIFIED", "COMPLETED"]:
                    verified_count += 1
                    completed_count += 1

                t_dict = {
                    "id": t_id,
                    "roadmap_id": t.get("roadmap_id", roadmap["id"]),
                    "phase": t.get("phase", 1),
                    "phase_name": t.get("phase_name", "Phase 1"),
                    "title": t.get("title", ""),
                    "description": t.get("description", ""),
                    "difficulty": t.get("difficulty", "Beginner"),
                    "estimated_hours": t.get("estimated_hours", "3 hours"),
                    "priority": t.get("priority", "HIGH"),
                    "status": status,
                    "order": t.get("order", 1),
                    "prerequisites": prereqs,
                    "skill": t.get("skill", "General"),
                    "type": t.get("type", "Learning"),
                    "explanation": t.get("explanation", ""),
                    "passing_score": t.get("passing_score", 70),
                    "verification_status": t.get("verification_status", "Not Started"),
                    "quiz_score": t.get("quiz_score"),
                    "attempts_count": t.get("attempts_count", 0),
                    "learning_progress_percentage": t.get("learning_progress_percentage", 0),
                    "learning_objectives": t.get("learning_objectives", []),
                    "topics": t.get("topics", []),
                    "resources": t.get("resources", []),
                    "completed_at": t.get("completed_at")
                }
                formatted_tasks.append(t_dict)

            total = len(formatted_tasks)
            pct = int((verified_count / total * 100)) if total > 0 else 0

            # Update document progress
            await db.roadmaps.update_one(
                {"user_id": user_id},
                {"$set": {
                    "verified_tasks": verified_count,
                    "completed_tasks": completed_count,
                    "progress_percentage": pct
                }}
            )

            return {
                "id": roadmap.get("id", f"rm_{user_id}"),
                "user_id": user_id,
                "career_id": roadmap.get("career_id", "ai-engineer"),
                "career_title": roadmap.get("career_title", "AI Engineer"),
                "target_employability": roadmap.get("target_employability", 80),
                "current_employability": roadmap.get("current_employability", 58),
                "employability_gap": roadmap.get("employability_gap", 22),
                "total_tasks": total,
                "verified_tasks": verified_count,
                "completed_tasks": completed_count,
                "progress_percentage": pct,
                "phases": roadmap.get("phases", []),
                "tasks": formatted_tasks,
                "last_updated": roadmap.get("last_updated", "")
            }

    return await generate_adaptive_roadmap(user_id, "ai-engineer")

async def get_task_by_id(user_id: str, task_id: str) -> Optional[Dict[str, Any]]:
    roadmap = await get_user_roadmap(user_id)
    tasks = roadmap.get("tasks", [])
    return next((t for t in tasks if t["id"] == task_id), None)

async def start_task(user_id: str, task_id: str) -> Dict[str, Any]:
    db = get_database()
    task = await get_task_by_id(user_id, task_id)
    if not task:
        raise ValueError("Task not found.")
    if task["status"] == "LOCKED":
        raise ValueError("Cannot start locked task. Complete prerequisite tasks first.")

    if db is not None:
        await db.roadmap_tasks.update_one(
            {"user_id": user_id, "id": task_id},
            {"$set": {"status": "IN_PROGRESS"}}
        )
    return await get_user_roadmap(user_id)

async def toggle_subtopic(user_id: str, task_id: str, topic_id: str, subtopic_id: str, completed: bool) -> Dict[str, Any]:
    db = get_database()
    if db is None:
        return await get_user_roadmap(user_id)

    raw_task = await db.roadmap_tasks.find_one({"user_id": user_id, "id": task_id})
    if not raw_task:
        raise ValueError("Task not found.")

    topics = raw_task.get("topics", [])
    total_subtopics = 0
    completed_subtopics = 0

    for top in topics:
        if top.get("id") == topic_id:
            for sub in top.get("subtopics", []):
                if sub.get("id") == subtopic_id:
                    sub["completed"] = completed
            # Check if all subtopics in topic completed
            top["completed"] = all(s.get("completed", False) for s in top.get("subtopics", [])) if top.get("subtopics") else completed

        # Tally total vs completed across task
        for sub in top.get("subtopics", []):
            total_subtopics += 1
            if sub.get("completed"):
                completed_subtopics += 1

    pct = int(round((completed_subtopics / total_subtopics) * 100)) if total_subtopics > 0 else 0

    await db.roadmap_tasks.update_one(
        {"user_id": user_id, "id": task_id},
        {"$set": {
            "topics": topics,
            "learning_progress_percentage": pct
        }}
    )
    return await get_user_roadmap(user_id)

async def complete_learning(user_id: str, task_id: str) -> Dict[str, Any]:
    db = get_database()
    raw_task = await db.roadmap_tasks.find_one({"user_id": user_id, "id": task_id}) if db is not None else None
    if not raw_task:
        raise ValueError("Task not found.")

    topics = raw_task.get("topics", [])
    incomplete_topics = []
    for top in topics:
        subtopics = top.get("subtopics", [])
        if subtopics:
            incomp_subs = [s["title"] for s in subtopics if not s.get("completed")]
            if incomp_subs:
                incomplete_topics.append(f"{top['title']}: ({', '.join(incomp_subs)})")
        elif not top.get("completed"):
            incomplete_topics.append(top['title'])

    if incomplete_topics:
        raise ValueError("Please complete all required learning topics before verifying this task.")

    if db is not None:
        await db.roadmap_tasks.update_one(
            {"user_id": user_id, "id": task_id},
            {"$set": {
                "status": "LEARNING_COMPLETED",
                "learning_progress_percentage": 100
            }}
        )

    return await get_user_roadmap(user_id)

async def generate_task_questions(user_id: str, task_id: str) -> List[Dict[str, Any]]:
    db = get_database()
    raw_task = await db.roadmap_tasks.find_one({"user_id": user_id, "id": task_id}) if db is not None else None
    if not raw_task:
        raise ValueError("Task not found.")

    # Fetch previously used question IDs for this student + task to ensure non-repeating retries
    used_ids = []
    if db is not None:
        cursor = db.roadmap_verifications.find({"student_id": user_id, "task_id": task_id})
        past_attempts = await cursor.to_list(length=100)
        for att in past_attempts:
            used_ids.extend(att.get("question_ids", []))

    task_skill = raw_task.get("skill", "Python")
    task_title = raw_task.get("title", "")
    difficulty = raw_task.get("difficulty", "Beginner")
    topics = raw_task.get("topics", [])

    frontend_qs, full_qs = question_gen_service.generate_questions(
        task_skill=task_skill,
        task_title=task_title,
        difficulty=difficulty,
        topics=topics,
        exclude_ids=used_ids,
        count=5
    )

    # Store full quiz metadata in db.active_quizzes for evaluation during submission
    if db is not None:
        await db.active_quizzes.update_one(
            {"user_id": user_id, "task_id": task_id},
            {"$set": {
                "user_id": user_id,
                "task_id": task_id,
                "full_questions": full_qs,
                "created_at": datetime.now(timezone.utc).isoformat()
            }},
            upsert=True
        )

    return frontend_qs

async def submit_task_verification(user_id: str, task_id: str, answers: Dict[str, str]) -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    # 1. Fetch task and active quiz
    raw_task = await db.roadmap_tasks.find_one({"user_id": user_id, "id": task_id}) if db is not None else None
    if not raw_task:
        raise ValueError("Task not found.")

    active_quiz = await db.active_quizzes.find_one({"user_id": user_id, "task_id": task_id}) if db is not None else None
    full_questions = active_quiz.get("full_questions", []) if active_quiz else []

    if not full_questions:
        # Fallback question generation if active quiz missing
        _, full_questions = question_gen_service.generate_questions(
            task_skill=raw_task.get("skill", "Python"),
            task_title=raw_task.get("title", ""),
            difficulty=raw_task.get("difficulty", "Beginner"),
            topics=raw_task.get("topics", []),
            exclude_ids=[]
        )

    # 2. Evaluate quiz answers
    passing_score = raw_task.get("passing_score", 70)
    eval_result = question_gen_service.evaluate_quiz(full_questions, answers, passing_score=passing_score)

    # 3. Count attempt number
    attempts_count = 1
    if db is not None:
        past_count = await db.roadmap_verifications.count_documents({"student_id": user_id, "task_id": task_id})
        attempts_count = past_count + 1

    question_ids = [q["id"] for q in full_questions]

    verification_doc = {
        "id": f"verif_{uuid.uuid4().hex[:8]}",
        "task_id": task_id,
        "student_id": user_id,
        "attempt_number": attempts_count,
        "score": eval_result["score"],
        "total_questions": eval_result["total_questions"],
        "percentage": eval_result["percentage"],
        "passed": eval_result["passed"],
        "topic_performance": eval_result["topic_performance"],
        "question_ids": question_ids,
        "created_at": now_str
    }

    if db is not None:
        await db.roadmap_verifications.insert_one(verification_doc)

    unlocked_next = False
    new_status = "VERIFIED" if eval_result["passed"] else "FAILED"
    verif_status_label = "Verified" if eval_result["passed"] else "Failed"

    if db is not None:
        await db.roadmap_tasks.update_one(
            {"user_id": user_id, "id": task_id},
            {"$set": {
                "status": new_status,
                "verification_status": verif_status_label,
                "quiz_score": eval_result["score"],
                "attempts_count": attempts_count,
                "completed_at": now_str if eval_result["passed"] else None
            }}
        )

    # 4. If passed, apply empirical skill improvement & unlock dependent tasks
    if eval_result["passed"]:
        unlocked_next = True
        skill_name = raw_task.get("skill")
        if skill_name and skill_name != "General":
            # Add project evidence if task is a project
            if raw_task.get("type") == "Project":
                await add_project_evidence(user_id, {
                    "title": f"{skill_name} Milestone Project",
                    "description": f"Verified implementation project for {skill_name}.",
                    "skills_used": [skill_name],
                    "project_type": "Academic",
                    "completion_status": "Completed"
                })

        # Recalculate employability
        roadmap_info = await db.roadmaps.find_one({"user_id": user_id}) if db is not None else None
        career_id = roadmap_info.get("career_id", "ai-engineer") if roadmap_info else "ai-engineer"
        careers = load_careers_data()
        career = next((c for c in careers if c["id"] == career_id), None) or careers[0]

        evidence_res = await get_or_create_user_evidence(user_id)
        verified_map = {item["skill"]: item["verified_score"] for item in evidence_res.get("skills", [])}
        emp_metrics = await calculate_employability_metrics(user_id, career, verified_map)

        if db is not None:
            await db.roadmaps.update_one(
                {"user_id": user_id},
                {"$set": {
                    "current_employability": emp_metrics["current_employability"],
                    "employability_gap": emp_metrics["employability_gap"],
                    "last_updated": now_str
                }}
            )

    return {
        "task_id": task_id,
        "score": eval_result["score"],
        "total_questions": eval_result["total_questions"],
        "percentage": eval_result["percentage"],
        "passed": eval_result["passed"],
        "status": new_status,
        "topic_performance": eval_result["topic_performance"],
        "weak_topics": eval_result["weak_topics"],
        "message": "Learning verified successfully! Next task unlocked." if eval_result["passed"] else "Your score is below the required level (70%). Review weak topics and retry.",
        "unlocked_next_task": unlocked_next,
        "attempts_count": attempts_count
    }

async def get_verification_history(user_id: str, task_id: str) -> List[Dict[str, Any]]:
    db = get_database()
    history = []
    if db is not None:
        cursor = db.roadmap_verifications.find({"student_id": user_id, "task_id": task_id}).sort("attempt_number", 1)
        records = await cursor.to_list(length=100)
        for r in records:
            history.append({
                "id": str(r.get("_id", r.get("id"))),
                "task_id": r.get("task_id"),
                "student_id": r.get("student_id"),
                "attempt_number": r.get("attempt_number", 1),
                "score": r.get("score", 0),
                "total_questions": r.get("total_questions", 5),
                "percentage": r.get("percentage", 0),
                "passed": r.get("passed", False),
                "topic_performance": r.get("topic_performance", {}),
                "created_at": r.get("created_at", "")
            })
    return history
