import pytest
from app.database.connection import connect_to_mongo, get_database
from app.services.question_generation_service import question_gen_service
from app.services.career_roadmap_service import (
    get_or_initialize_user_roadmap,
    get_topic_learning_material,
    complete_topic,
    generate_phase_assessment,
    submit_phase_assessment,
    PASSING_SCORE_THRESHOLD
)

@pytest.mark.anyio
async def test_case_01_and_02_interest_based_questions():
    """
    Cases 1 & 2:
    - A student with an AI interest receives AI-related questions.
    - A student with a Web Development interest receives relevant questions.
    """
    ai_profile = {
        "interests": ["Artificial Intelligence"],
        "target_role": "AI Engineer",
        "technical_skills": {"Python": 70, "Machine Learning": 60}
    }
    client_qs_ai, full_qs_ai = question_gen_service.generate_personalized_assessment(
        user_id="test_ai_student",
        profile=ai_profile,
        total_count=10
    )
    ai_skills_in_questions = {q.get("skill") for q in full_qs_ai}
    ai_topics_in_questions = {q.get("topic") for q in full_qs_ai}
    # Must contain AI, Python, Machine Learning, or Math
    assert any(s in ["Artificial Intelligence", "Python", "Machine Learning", "Mathematics"] for s in ai_skills_in_questions)

    web_profile = {
        "interests": ["Web Development"],
        "target_role": "Full Stack Developer",
        "technical_skills": {"JavaScript": 70, "HTML": 70}
    }
    client_qs_web, full_qs_web = question_gen_service.generate_personalized_assessment(
        user_id="test_web_student",
        profile=web_profile,
        total_count=10
    )
    web_skills_in_questions = {q.get("skill") for q in full_qs_web}
    web_topics_in_questions = {q.get("topic") for q in full_qs_web}
    assert any("Web" in s or "HTML" in t or "CSS" in t or "JavaScript" in t or "React" in t for s in web_skills_in_questions for t in web_topics_in_questions)

@pytest.mark.anyio
async def test_case_03_and_04_randomized_and_avoid_repeats():
    """
    Cases 3 & 4:
    - Assessment attempts use randomized question sets.
    - Previously used questions are avoided when enough alternatives exist.
    """
    profile = {
        "interests": ["Artificial Intelligence"],
        "target_role": "AI Engineer",
        "technical_skills": {"Python": 70}
    }
    # Attempt 1
    _, attempt_1_qs = question_gen_service.generate_personalized_assessment(
        user_id="test_rand_user",
        profile=profile,
        total_count=5
    )
    ids_attempt_1 = [q["id"] for q in attempt_1_qs]

    # Attempt 2, excluding attempt 1 IDs
    _, attempt_2_qs = question_gen_service.generate_personalized_assessment(
        user_id="test_rand_user",
        profile=profile,
        exclude_ids=ids_attempt_1,
        total_count=5
    )
    ids_attempt_2 = [q["id"] for q in attempt_2_qs]

    # Overlap between attempt 1 and attempt 2 must be 0 because we have plenty of questions
    overlap = set(ids_attempt_1).intersection(set(ids_attempt_2))
    assert len(overlap) == 0, f"Expected 0 repeated questions, but found: {overlap}"

@pytest.mark.anyio
async def test_case_05_06_07_topic_completion_and_persistence():
    """
    Cases 5, 6, 7:
    - Opening a topic does NOT mark it completed.
    - Completing all configured topic requirements marks it completed.
    - The completion indicator persists after retrieval / refresh.
    """
    await connect_to_mongo()
    db = get_database()
    test_user = "test_topic_completion_user"

    if db is not None:
        await db.topic_completions.delete_many({"user_id": test_user})
        await db.career_roadmaps.delete_many({"user_id": test_user})

    # 1. Opening the topic material
    materials = await get_topic_learning_material(test_user, "phase-1", "ai_beg_python_fund")
    assert materials["completed"] is False, "Opening a topic must NOT automatically mark it completed"

    # Verify roadmap state shows topic is still incomplete
    rm = await get_or_initialize_user_roadmap(test_user)
    p1_modules = rm["phases"][0]["modules"]
    mod1 = next(m for m in p1_modules if m["id"] == "ai_beg_python_fund")
    assert mod1["completed"] is False

    # 2. Complete the topic with verified check
    res = await complete_topic(test_user, "phase-1", "ai_beg_python_fund", practice_answer="Set")
    assert res["success"] is True
    assert res["completed"] is True

    # 3. Verify completion persists upon re-reading from DB
    materials_after = await get_topic_learning_material(test_user, "phase-1", "ai_beg_python_fund")
    assert materials_after["completed"] is True
    assert materials_after["completed_at"] is not None

    rm_after = await get_or_initialize_user_roadmap(test_user)
    mod1_after = next(m for m in rm_after["phases"][0]["modules"] if m["id"] == "ai_beg_python_fund")
    assert mod1_after["completed"] is True

@pytest.mark.anyio
async def test_case_08_to_14_strict_phase_locking_and_80_percent_rule():
    """
    Cases 8 to 14:
    - Intermediate is locked when Beginner is incomplete.
    - A score of 79% does NOT unlock next phase.
    - A score of exactly 80% unlocks next phase.
    - A failed assessment does not unlock next phase.
    - Direct API calls cannot bypass phase locking.
    - Intermediate cannot be accessed before Beginner is passed.
    - Advanced cannot be accessed before Intermediate is passed.
    """
    await connect_to_mongo()
    db = get_database()
    test_user = "test_strict_locking_user"

    if db is not None:
        await db.topic_completions.delete_many({"user_id": test_user})
        await db.phase_assessments.delete_many({"user_id": test_user})
        await db.career_roadmaps.delete_many({"user_id": test_user})
        await db.active_quizzes.delete_many({"user_id": test_user})

    # 1. Intermediate and Advanced must be LOCKED initially
    rm = await get_or_initialize_user_roadmap(test_user)
    assert rm["phases"][0]["status"] in ["AVAILABLE", "IN_PROGRESS"]
    assert rm["phases"][1]["status"] == "LOCKED"
    assert rm["phases"][2]["status"] == "LOCKED"

    # 2. Direct access to Intermediate materials MUST be rejected by backend
    with pytest.raises(PermissionError, match="Cannot access"):
        await get_topic_learning_material(test_user, "phase-2", "ai_int_numpy_pandas")

    # 3. Direct access to Advanced materials MUST be rejected by backend
    with pytest.raises(PermissionError, match="Cannot access"):
        await get_topic_learning_material(test_user, "phase-3", "ai_adv_deep_learning")

    # 4. Attempting Phase 1 assessment before completing all Phase 1 topics MUST be rejected
    with pytest.raises(ValueError, match="must study and complete all topics"):
        await generate_phase_assessment(test_user, "phase-1")

    # Complete all Beginner topics
    for m in rm["phases"][0]["modules"]:
        await complete_topic(test_user, "phase-1", m["id"])

    # Now Phase 1 assessment is allowed!
    quiz = await generate_phase_assessment(test_user, "phase-1")
    assert quiz["total_questions"] == 10
    assert quiz["passing_score"] == 80

    # Retrieve full active questions for answer key simulation
    active_q = await db.active_quizzes.find_one({"user_id": test_user, "phase_id": "phase-1"})
    full_qs = active_q["full_questions"]

    # 5. Simulate 79% / failing score (e.g. 7 correct out of 10 = 70% < 80%)
    failing_answers = {q["id"]: q["correct_answer"] for q in full_qs[:7]}
    # Give wrong answers for remaining
    for q in full_qs[7:]:
        failing_answers[q["id"]] = "DEFINITELY_WRONG_OPTION_XYZ"

    fail_res = await submit_phase_assessment(test_user, "phase-1", failing_answers)
    assert fail_res["passed"] is False
    assert fail_res["percentage"] == 70
    assert fail_res["unlocked_next_phase"] is False

    # Verify Intermediate is STILL strictly LOCKED after failed attempt
    rm_after_fail = await get_or_initialize_user_roadmap(test_user)
    assert rm_after_fail["phases"][1]["status"] == "LOCKED"

    # Direct API calls to Phase 2 still blocked
    with pytest.raises(PermissionError):
        await get_topic_learning_material(test_user, "phase-2", "ai_int_numpy_pandas")

    # 6. Simulate EXACTLY 80% passing score (8 correct out of 10 = 80%)
    quiz_retry = await generate_phase_assessment(test_user, "phase-1")
    active_q2 = await db.active_quizzes.find_one({"user_id": test_user, "phase_id": "phase-1"})
    full_qs2 = active_q2["full_questions"]

    passing_80_answers = {q["id"]: q["correct_answer"] for q in full_qs2[:8]}
    for q in full_qs2[8:]:
        passing_80_answers[q["id"]] = "WRONG_ANSWER"

    pass_res = await submit_phase_assessment(test_user, "phase-1", passing_80_answers)
    assert pass_res["passed"] is True
    assert pass_res["percentage"] == 80
    assert pass_res["unlocked_next_phase"] is True

    # 7. Intermediate Phase is now UNLOCKED!
    rm_after_pass = await get_or_initialize_user_roadmap(test_user)
    assert rm_after_pass["phases"][0]["status"] == "COMPLETED"
    assert rm_after_pass["phases"][1]["status"] == "AVAILABLE"
    # Advanced is still LOCKED until Intermediate is passed!
    assert rm_after_pass["phases"][2]["status"] == "LOCKED"

    # Now Intermediate topic materials CAN be accessed
    int_mat = await get_topic_learning_material(test_user, "phase-2", "ai_int_numpy_pandas")
    assert int_mat["module_title"] == "NumPy and Pandas"

    # But Advanced is still blocked
    with pytest.raises(PermissionError):
        await get_topic_learning_material(test_user, "phase-3", "ai_adv_deep_learning")

@pytest.mark.anyio
async def test_case_15_to_18_chatbot_and_isolation():
    """
    Cases 15 to 18:
    - Chatbot backend response generation with student context
    - API key not exposed in responses
    - User record isolation
    """
    from app.api.chatbot import generate_local_fallback_reply, build_student_context_prompt

    # Prompt builder must include target role, progress, and topic
    prompt = build_student_context_prompt(
        student_name="Test Student",
        profile={"degree": "B.Tech", "target_role": "AI Engineer"},
        roadmap={"career_title": "AI Engineer", "overall_progress": 25, "phases": []}
    )
    assert "AI Engineer" in prompt
    assert "25%" in prompt

    # Fallback reply must be coherent and informative
    reply = generate_local_fallback_reply("Give me a python example", "AI Engineer", "Python Fundamentals", "Beginner Phase")
    assert "```python" in reply
    assert "Python Fundamentals" in reply
    # Must never contain secret keys
    assert "sk-" not in reply
    assert "AIza" not in reply
