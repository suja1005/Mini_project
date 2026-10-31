import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import connect_to_mongo, get_database

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.mark.anyio
async def test_full_student_journey_end_to_end():
    await connect_to_mongo()
    db = get_database()
    
    with TestClient(app) as client:
        # 1. Register a fresh student
        email = f"journey_student_{id(app)}@test.com"
        reg_payload = {
            "full_name": "Journey Student",
            "email": email,
            "password": "Password123!",
            "degree": "B.Tech",
            "department": "Computer Science"
        }
        reg_res = client.post("/api/v1/auth/register", json=reg_payload)
        assert reg_res.status_code == 200, reg_res.text
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Complete onboarding profile with AI interest
        profile_payload = {
            "full_name": "Journey Student",
            "degree": "B.Tech",
            "department": "Computer Science",
            "year_of_study": "Final Year",
            "cgpa": "8.5",
            "technical_skills": {"Python": 75, "Machine Learning": 70},
            "soft_skills": ["Problem Solving", "Communication"],
            "interests": ["Artificial Intelligence"],
            "aptitude_scores": {"logical_reasoning": 80, "numerical_ability": 75, "analytical_thinking": 85},
            "target_role": "AI Engineer",
            "preferred_domain": "Artificial Intelligence"
        }
        prof_res = client.put("/api/v1/profile", json=profile_payload, headers=headers)
        assert prof_res.status_code == 200

        # 3. Request personalized assessment questions
        q_res = client.get("/api/v1/assessment/questions", headers=headers)
        assert q_res.status_code == 200
        questions = q_res.json()
        assert len(questions) > 0
        # Verify correct_answer is not exposed
        for q in questions:
            assert "correct_answer" not in q

        # Verify AI relevant content
        skills_in_q = [q.get("skill") for q in questions]
        assert any(s in ["Artificial Intelligence", "Python", "Machine Learning", "Mathematics"] for s in skills_in_q)

        # 4. Fetch Roadmap: Beginner is AVAILABLE, Intermediate and Advanced are LOCKED
        rm_res = client.get("/api/v1/roadmap", headers=headers)
        assert rm_res.status_code == 200
        rm = rm_res.json()
        assert rm["career_title"] == "AI Engineer"
        assert rm["phases"][0]["status"] in ["AVAILABLE", "IN_PROGRESS"]
        assert rm["phases"][1]["status"] == "LOCKED"
        assert rm["phases"][2]["status"] == "LOCKED"

        # 5. Direct API call to access locked Phase 2 topic MUST be rejected (403 Forbidden)
        p2_blocked = client.get("/api/v1/roadmap/topics/phase-2/ai_int_numpy_pandas", headers=headers)
        assert p2_blocked.status_code == 403

        # 6. Direct API call to complete locked Phase 2 topic MUST be rejected (403 Forbidden)
        p2_comp_blocked = client.post("/api/v1/roadmap/topics/phase-2/ai_int_numpy_pandas/complete", json={}, headers=headers)
        assert p2_comp_blocked.status_code == 403

        # 7. Opening a Beginner topic does NOT mark it complete
        t1_id = rm["phases"][0]["modules"][0]["id"]
        t1_mat = client.get(f"/api/v1/roadmap/topics/phase-1/{t1_id}", headers=headers).json()
        assert t1_mat["completed"] is False

        # 8. Complete all Beginner topics with verified practice answer
        for mod in rm["phases"][0]["modules"]:
            comp_res = client.post(
                f"/api/v1/roadmap/topics/phase-1/{mod['id']}/complete",
                json={"practice_answer": None},
                headers=headers
            )
            assert comp_res.status_code == 200
            assert comp_res.json()["completed"] is True

        # Verify completion persisted upon re-fetching roadmap
        rm_recheck = client.get("/api/v1/roadmap", headers=headers).json()
        assert rm_recheck["phases"][0]["all_topics_completed"] is True

        # 9. Generate Phase 1 Assessment
        phase_q_res = client.post("/api/v1/roadmap/phases/phase-1/assessment/generate", headers=headers)
        assert phase_q_res.status_code == 200
        phase_quiz = phase_q_res.json()
        assert phase_quiz["total_questions"] == 10
        assert phase_quiz["passing_score"] == 80

        # Retrieve active quiz answers from test database
        user_doc = await db.users.find_one({"email": email})
        user_id = str(user_doc["_id"])
        active_q = await db.active_quizzes.find_one({"user_id": user_id, "phase_id": "phase-1"})
        full_qs = active_q["full_questions"]

        # 10. Simulate 70% failing score (7/10 correct < 80%)
        fail_sub = {q["id"]: q["correct_answer"] for q in full_qs[:7]}
        for q in full_qs[7:]:
            fail_sub[q["id"]] = "DEFINITELY_WRONG"

        fail_res = client.post("/api/v1/roadmap/phases/phase-1/assessment/submit", json={"answers": fail_sub}, headers=headers)
        assert fail_res.status_code == 200
        fail_data = fail_res.json()
        assert fail_data["passed"] is False
        assert fail_data["percentage"] == 70
        assert fail_data["unlocked_next_phase"] is False

        # Phase 2 remains strictly LOCKED
        rm_fail = client.get("/api/v1/roadmap", headers=headers).json()
        assert rm_fail["phases"][1]["status"] == "LOCKED"

        # 11. Simulate 80% passing score (8/10 correct = 80%)
        pass_sub = {q["id"]: q["correct_answer"] for q in full_qs[:8]}
        for q in full_qs[8:]:
            pass_sub[q["id"]] = "WRONG_ANSWER"

        pass_res = client.post("/api/v1/roadmap/phases/phase-1/assessment/submit", json={"answers": pass_sub}, headers=headers)
        assert pass_res.status_code == 200
        pass_data = pass_res.json()
        assert pass_data["passed"] is True
        assert pass_data["percentage"] == 80
        assert pass_data["unlocked_next_phase"] is True

        # Phase 1 is now COMPLETED and Phase 2 is UNLOCKED!
        rm_pass = client.get("/api/v1/roadmap", headers=headers).json()
        assert rm_pass["phases"][0]["status"] == "COMPLETED"
        assert rm_pass["phases"][1]["status"] == "AVAILABLE"
        assert rm_pass["phases"][2]["status"] == "LOCKED"

        # Phase 2 topics can now be accessed
        p2_now_allowed = client.get("/api/v1/roadmap/topics/phase-2/ai_int_numpy_pandas", headers=headers)
        assert p2_now_allowed.status_code == 200
        assert p2_now_allowed.json()["module_title"] == "NumPy and Pandas"

        # 12. Chatbot Endpoint verification
        chat_res = client.post(
            "/api/v1/chatbot/message",
            json={"message": "What should I study next?", "history": []},
            headers=headers
        )
        assert chat_res.status_code == 200
        chat_data = chat_res.json()
        assert "reply" in chat_data
        assert len(chat_data["reply"]) > 10
        # Verify no secret keys leaked
        assert "sk-" not in chat_data["reply"]
        assert "AIza" not in chat_data["reply"]
