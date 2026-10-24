import pytest
from app.services.roadmap_curriculum import (
    get_all_skills,
    get_skill_curriculum,
    get_level_curriculum,
    get_all_curriculum_levels
)
from app.services.question_generation_service import question_gen_service

def test_seven_skills_and_three_levels_exist():
    """Verify all 7 skills exist and each has exactly 3 levels."""
    skills = get_all_skills()
    assert len(skills) == 7
    expected_slugs = {
        "python",
        "machine-learning",
        "mathematics",
        "problem-solving",
        "git-and-github",
        "sql",
        "communication"
    }
    actual_slugs = {s["skill_slug"] for s in skills}
    assert expected_slugs == actual_slugs

    all_levels = get_all_curriculum_levels()
    assert len(all_levels) == 21  # 7 skills * 3 levels = 21

    for slug in expected_slugs:
        curric = get_skill_curriculum(slug)
        assert curric is not None
        assert len(curric["levels"]) == 3
        levels = [lvl["level"] for lvl in curric["levels"]]
        assert levels == [1, 2, 3]

def test_python_topics_match_specification():
    """Verify Python curriculum has exact requested topics."""
    l1 = get_level_curriculum("python", 1)
    l1_titles = [t[0] for t in l1["topics"]]
    assert "Variables and naming rules" in l1_titles
    assert "Conditional statements" in l1_titles
    assert "For and while loops" in l1_titles
    assert "Lists, tuples, sets, and dictionaries" in l1_titles
    assert len(l1_titles) == 13

    l2 = get_level_curriculum("python", 2)
    l2_titles = [t[0] for t in l2["topics"]]
    assert "Lambda, map, filter, and comprehensions" in l2_titles
    assert "Classes, objects, inheritance, and polymorphism" in l2_titles
    assert len(l2_titles) == 13

    l3 = get_level_curriculum("python", 3)
    l3_titles = [t[0] for t in l3["topics"]]
    assert "Decorators and closures" in l3_titles
    assert "Threading, multiprocessing, and asynchronous programming" in l3_titles
    assert len(l3_titles) == 13

def test_machine_learning_topics_match_specification():
    """Verify Machine Learning curriculum topics."""
    l1 = get_level_curriculum("machine-learning", 1)
    assert len(l1["topics"]) == 14
    l2 = get_level_curriculum("machine-learning", 2)
    assert len(l2["topics"]) == 17
    l3 = get_level_curriculum("machine-learning", 3)
    assert len(l3["topics"]) == 14

def test_level_assessment_generation_structure():
    """Verify assessment delivers 20 questions: 15 MCQs and 5 practical questions."""
    for slug in ["python", "machine-learning", "sql", "git-and-github", "communication"]:
        client_qs, full_qs = question_gen_service.generate_level_assessment(
            skill=slug,
            level=1,
            mcq_count=15,
            practical_count=5
        )
        assert len(client_qs) == 20
        assert len(full_qs) == 20

        # Verify no answer keys leaked to client
        for q in client_qs:
            assert "correct_answer" not in q
            assert "acceptable_answers" not in q
            assert "question_id" in q
            assert "type" in q
            assert q["type"] in ["mcq", "practical"]

        mcq_count = sum(1 for q in client_qs if q["type"] == "mcq")
        practical_count = sum(1 for q in client_qs if q["type"] == "practical")
        assert mcq_count == 15
        assert practical_count == 5

def test_assessment_scoring_and_pass_criteria():
    """Verify scoring logic requires 70% to pass and provides detailed feedback."""
    _, full_qs = question_gen_service.generate_level_assessment("python", 1)
    
    # 1. Failing submission (10/20 = 50% < 70%)
    partial_answers = {q["id"]: q["correct_answer"] for q in full_qs[:10]}
    fail_res = question_gen_service.evaluate_assessment(full_qs, partial_answers, passing_score=70)
    assert fail_res["score"] == 10
    assert fail_res["percentage"] == 50
    assert fail_res["passed"] is False
    assert fail_res["status"] == "FAILED"
    assert len(fail_res["weak_topics"]) > 0

    # 2. Passing submission (14/20 = 70% >= 70%)
    passing_answers = {q["id"]: q["correct_answer"] for q in full_qs[:14]}
    pass_res = question_gen_service.evaluate_assessment(full_qs, passing_answers, passing_score=70)
    assert pass_res["score"] == 14
    assert pass_res["percentage"] == 70
    assert pass_res["passed"] is True
    assert pass_res["status"] == "PASSED"
    assert len(pass_res["reviews"]) == 20
