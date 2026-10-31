import pytest
from app.services.roadmap_service import (
    init_user_skill_levels,
    get_skills_overview,
    get_skill_level_detail,
    start_skill_level,
    toggle_level_topic,
    generate_level_assessment,
    submit_level_assessment,
    get_progress_dashboard
)

from app.database.connection import connect_to_mongo, get_database

@pytest.mark.anyio
async def test_level_progression_locking_rules():
    """Verify backend enforces progression locking: Level 2 cannot start until Level 1 passes."""
    await connect_to_mongo()
    test_user_id = "test_progression_user_001"
    
    # Clean up test user state for test idempotency
    db = get_database()
    if db is not None:
        await db.user_skill_levels.delete_many({"user_id": test_user_id})
        await db.roadmap_verifications.delete_many({"user_id": test_user_id})
        await db.active_quizzes.delete_many({"user_id": test_user_id})

    # Initialize
    await init_user_skill_levels(test_user_id)
    
    # 1. Level 1 must be AVAILABLE initially
    lvl1 = await get_skill_level_detail(test_user_id, "python", 1)
    assert lvl1["status"] in ["AVAILABLE", "IN_PROGRESS"]

    # 2. Level 2 must be LOCKED initially
    lvl2 = await get_skill_level_detail(test_user_id, "python", 2)
    assert lvl2["status"] == "LOCKED"

    # 3. Attempting to start Level 2 directly MUST raise ValueError
    with pytest.raises(ValueError, match="Level 1"):
        await start_skill_level(test_user_id, "python", 2)

    # 4. Start Level 1 and complete a topic
    started_l1 = await start_skill_level(test_user_id, "python", 1)
    assert started_l1["status"] == "IN_PROGRESS"

    top_id = started_l1["topics"][0]["id"]
    toggled = await toggle_level_topic(test_user_id, "python", 1, top_id, completed=True, practice_completed=True)
    assert toggled["topics"][0]["completed"] is True
    assert toggled["topics"][0]["practice_completed"] is True

    # 5. Take Level 1 Assessment and simulate passing (100% score)
    quiz_data = await generate_level_assessment(test_user_id, "python", 1)
    assert len(quiz_data["questions"]) == 20
    
    # Query database active quiz for answer key simulation
    active_quiz = await db.active_quizzes.find_one({"user_id": test_user_id, "level_id": "python_lvl_1"})
    full_qs = active_quiz["full_questions"]
    
    answers = {q["id"]: q["correct_answer"] for q in full_qs}
    res = await submit_level_assessment(test_user_id, "python", 1, answers)
    assert res["passed"] is True
    assert res["status"] == "PASSED"
    assert res["unlocked_next_level"] is True
    assert res["next_level_id"] == "python_lvl_2"

    # 6. Now Level 2 MUST be AVAILABLE!
    lvl2_now = await get_skill_level_detail(test_user_id, "python", 2)
    assert lvl2_now["status"] == "AVAILABLE"

    # 7. Level 2 can now be started successfully!
    started_l2 = await start_skill_level(test_user_id, "python", 2)
    assert started_l2["status"] == "IN_PROGRESS"

    # 8. Level 3 is still LOCKED until Level 2 passes
    lvl3 = await get_skill_level_detail(test_user_id, "python", 3)
    assert lvl3["status"] == "LOCKED"

    # 9. Progress Dashboard reflects progress
    dash = await get_progress_dashboard(test_user_id)
    assert dash["passed_levels_count"] >= 1
    assert dash["overall_completion_percentage"] > 0
