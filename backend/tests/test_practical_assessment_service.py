from app.services.practical_assessment_service import (
    QUESTION_BANK,
    build_adaptive_roadmap,
    create_question_set,
    evaluate_answers,
    get_career_and_skills,
    score_category,
)
from app.schemas.practical_assessment import PracticalQuestionResponse
from app.services.evidence_service import compute_evidence_for_skill


def test_score_categories_use_requested_thresholds():
    assert [score_category(score) for score in (0, 49, 50, 69, 70, 84, 85, 100)] == [
        "Weak",
        "Weak",
        "Needs Improvement",
        "Needs Improvement",
        "Good",
        "Good",
        "Strong",
        "Strong",
    ]


def test_question_generation_is_skill_specific_with_private_answer_keys():
    generated = create_question_set(["Python", "SQL"], [])
    assert generated
    assert {question["skill"] for question in generated} == {"Python", "SQL"}
    assert len({question["question_id"] for question in generated}) == len(generated)
    for question in generated:
        bank_ids = {item["question_id"] for item in QUESTION_BANK[question["skill"]]}
        assert question["question_id"] in bank_ids
    assert all("correct_answer" in question for question in generated)
    public_questions = [PracticalQuestionResponse(**question).model_dump() for question in generated]
    assert all("correct_answer" not in question for question in public_questions)


def test_backend_evaluation_calculates_each_skill_independently():
    questions = create_question_set(["Python"], [])
    answer_by_id = {question["question_id"]: question["correct_answer"] for question in questions}
    overall, skill_results, review = evaluate_answers(questions, answer_by_id)
    assert overall == 100
    assert skill_results[0]["score"] == 100
    assert skill_results[0]["category"] == "Strong"
    assert all(item["is_correct"] for item in review)


def test_every_question_accepts_its_own_answer_key():
    for skill_questions in QUESTION_BANK.values():
        for question in skill_questions:
            score, _, review = evaluate_answers(
                [question],
                {question["question_id"]: question["correct_answer"]},
            )
            assert score == 100, question["question_id"]
            assert review[0]["is_correct"], question["question_id"]


def test_evaluation_rejects_missing_or_unrecognized_question_ids():
    questions = create_question_set(["SQL"], [])
    try:
        evaluate_answers(questions, {})
    except ValueError as error:
        assert "every question" in str(error)
    else:
        raise AssertionError("Missing answers were accepted")

def test_written_workplace_response_uses_backend_rubric():
    question = next(
        item for item in QUESTION_BANK["Communication"]
        if item["topic"] == "Written status update"
    )
    score, results, _ = evaluate_answers(
        [question],
        {question["question_id"]: "Blocker: the endpoint issue. Impact: testing is delayed. Next step: deploy a fix."},
    )
    assert score == 100
    assert results[0]["skill"] == "Communication"


def test_adaptive_roadmap_prioritizes_weak_skills_and_skips_strong_skills():
    roadmap = build_adaptive_roadmap([
        {"skill": "Python", "score": 45, "category": "Weak"},
        {"skill": "SQL", "score": 60, "category": "Needs Improvement"},
        {"skill": "Java", "score": 85, "category": "Strong"},
    ], "Python Developer")
    assert [item["skill"] for item in roadmap] == ["Python", "SQL"]
    assert all(len(item["phases"]) == 3 for item in roadmap)
    assert all(topic["resources"] and topic["completion_requirements"] for item in roadmap for phase in item["phases"] for topic in phase["topics"])


def test_career_assessment_skills_include_claims_and_career_requirements():
    career, claimed, required = get_career_and_skills({
        "target_role": "Python Developer",
        "technical_skills": {"Python": 80},
        "soft_skills": ["Communication"],
        "aptitude_scores": {"logical_reasoning": 75},
    })
    assert career == "Python Developer"
    assert "Python" in claimed
    assert "Communication" in claimed
    assert "Problem Solving" in required
    assert "Aptitude" in required


def test_self_claim_and_project_only_cannot_verify_without_practical_assessment():
    self_claim = compute_evidence_for_skill("Python", 95, None, None)
    project_only = compute_evidence_for_skill("Python", 95, None, 90)
    passing_evidence = compute_evidence_for_skill("Python", 95, 70, 90)
    assert self_claim["status"] == "INSUFFICIENT EVIDENCE"
    assert project_only["status"] == "PARTIALLY VERIFIED"
    assert passing_evidence["status"] == "VERIFIED"
