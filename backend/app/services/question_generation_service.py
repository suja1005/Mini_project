import os
import json
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple, Optional

PRIMARY_QUESTIONS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "level_assessment_questions.json"
)

LEGACY_QUESTIONS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "roadmap_questions.json"
)

class QuestionGenerator(ABC):
    @abstractmethod
    def generate_level_assessment(
        self,
        skill: str,
        level: int,
        topics: List[Dict[str, Any]] = None,
        exclude_ids: List[str] = None,
        mcq_count: int = 15,
        practical_count: int = 5
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Returns (client_questions, full_questions_with_answers)
        """
        pass

    @abstractmethod
    def evaluate_assessment(
        self,
        full_questions: List[Dict[str, Any]],
        student_answers: Dict[str, str],
        passing_score: int = 70
    ) -> Dict[str, Any]:
        pass

class RuleBasedQuestionGenerator(QuestionGenerator):
    def __init__(self, primary_path: str = PRIMARY_QUESTIONS_PATH, legacy_path: str = LEGACY_QUESTIONS_PATH):
        self.primary_path = primary_path
        self.legacy_path = legacy_path
        self.questions_bank = self._load_questions()

    def _load_questions(self) -> List[Dict[str, Any]]:
        bank = []
        if os.path.exists(self.primary_path):
            try:
                with open(self.primary_path, "r", encoding="utf-8") as f:
                    bank.extend(json.load(f))
            except Exception as e:
                print(f"[RuleBasedQuestionGenerator] Error loading primary questions json: {e}")
        
        # Also load legacy questions if primary is empty or for fallback
        if os.path.exists(self.legacy_path):
            try:
                with open(self.legacy_path, "r", encoding="utf-8") as f:
                    legacy = json.load(f)
                    # Convert task_type to skill if missing
                    for q in legacy:
                        if "skill" not in q:
                            q["skill"] = q.get("task_type", "General")
                        if "type" not in q:
                            q["type"] = "mcq"
                        if "level" not in q:
                            q["level"] = 1
                    bank.extend(legacy)
            except Exception as e:
                print(f"[RuleBasedQuestionGenerator] Error loading legacy questions json: {e}")

        return bank

    def generate_level_assessment(
        self,
        skill: str,
        level: int,
        topics: List[Dict[str, Any]] = None,
        exclude_ids: List[str] = None,
        mcq_count: int = 15,
        practical_count: int = 5
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        if exclude_ids is None:
            exclude_ids = []

        skill_norm = skill.lower().replace("-", " ").strip()

        # Filter candidates matching skill and level
        candidates = []
        for q in self.questions_bank:
            q_skill = str(q.get("skill", "")).lower().replace("-", " ").strip()
            q_level = int(q.get("level", 1))

            matches_skill = (skill_norm in q_skill or q_skill in skill_norm)
            matches_level = (q_level == level)

            if matches_skill and matches_level:
                candidates.append(q)

        # Fallback to skill match only if exact level has few questions
        if len(candidates) < (mcq_count + practical_count):
            for q in self.questions_bank:
                q_skill = str(q.get("skill", "")).lower().replace("-", " ").strip()
                if (skill_norm in q_skill or q_skill in skill_norm) and q not in candidates:
                    candidates.append(q)

        # Fallback to all questions if still empty
        if not candidates:
            candidates = list(self.questions_bank)

        # Separate into MCQs and Practicals
        mcq_candidates = [q for q in candidates if q.get("type", "mcq") == "mcq"]
        practical_candidates = [q for q in candidates if q.get("type") == "practical"]

        # Filter un-used questions where possible
        avail_mcqs = [q for q in mcq_candidates if q["id"] not in exclude_ids]
        if len(avail_mcqs) < mcq_count:
            avail_mcqs = list(mcq_candidates) if mcq_candidates else list(candidates)

        avail_practicals = [q for q in practical_candidates if q["id"] not in exclude_ids]
        if len(avail_practicals) < practical_count:
            avail_practicals = list(practical_candidates) if practical_candidates else list(candidates)

        # Sample MCQs and Practicals
        random.shuffle(avail_mcqs)
        random.shuffle(avail_practicals)

        selected_mcqs = avail_mcqs[:mcq_count]
        selected_practicals = avail_practicals[:practical_count]

        # In rare case where practicals or mcqs pool is short, fill from remaining
        combined = selected_mcqs + selected_practicals
        if len(combined) < (mcq_count + practical_count):
            remaining = [q for q in candidates if q not in combined]
            random.shuffle(remaining)
            combined.extend(remaining[: (mcq_count + practical_count) - len(combined)])

        # Randomize question presentation order
        random.shuffle(combined)
        selected_questions = combined[: (mcq_count + practical_count)]

        client_questions = []
        full_questions = []

        for idx, q in enumerate(selected_questions, 1):
            q_id = q["id"]
            options = list(q.get("options", []))
            if q.get("type", "mcq") == "mcq" and options:
                random.shuffle(options)

            client_q = {
                "question_id": q_id,
                "question_number": idx,
                "type": q.get("type", "mcq"),
                "question": q["question"],
                "topic": q.get("topic", "General"),
                "difficulty": q.get("difficulty", "Beginner"),
                "options": options,
                "starter_code": q.get("starter_code"),
                "practical_type": q.get("practical_type")
            }
            client_questions.append(client_q)

            full_q = dict(q)
            full_q["question_number"] = idx
            full_questions.append(full_q)

        return client_questions, full_questions

    def evaluate_assessment(
        self,
        full_questions: List[Dict[str, Any]],
        student_answers: Dict[str, str],
        passing_score: int = 70
    ) -> Dict[str, Any]:
        total_questions = len(full_questions)
        if total_questions == 0:
            return {
                "score": 0,
                "total_questions": 0,
                "percentage": 0,
                "passed": False,
                "status": "FAILED",
                "passing_score": passing_score,
                "attempts_count": 1,
                "topic_performance": {},
                "strengths": [],
                "weak_topics": [],
                "recommended_revisions": [],
                "suggested_practice": [],
                "reviews": []
            }

        correct_count = 0
        topic_stats: Dict[str, Dict[str, int]] = {}
        reviews = []

        for q in full_questions:
            q_id = q["id"]
            q_num = q.get("question_number", 1)
            q_type = q.get("type", "mcq")
            topic = q.get("topic", "General")
            correct_ans = str(q.get("correct_answer", "")).strip()
            acceptable_answers = [str(a).strip().lower() for a in q.get("acceptable_answers", [correct_ans])]
            
            student_ans_raw = student_answers.get(q_id, "")
            student_ans = str(student_ans_raw).strip() if student_ans_raw is not None else ""
            student_ans_clean = student_ans.lower()

            # Initialize topic stats
            topic_stats.setdefault(topic, {"correct": 0, "total": 0})
            topic_stats[topic]["total"] += 1

            is_correct = False

            if q_type == "mcq":
                # Direct match for MCQ option
                is_correct = (student_ans_clean == correct_ans.lower()) or (student_ans_clean in acceptable_answers)
            else:
                # Practical / Application evaluation
                # 1. Exact match against any acceptable answer
                if student_ans_clean in acceptable_answers:
                    is_correct = True
                # 2. Number normalization (e.g. 5.0 vs 5, 80% vs 0.8)
                elif any(self._numeric_match(student_ans_clean, acc) for acc in acceptable_answers):
                    is_correct = True
                # 3. Substring / normalized key term presence
                elif any(acc in student_ans_clean for acc in acceptable_answers if len(acc) >= 3):
                    is_correct = True

            if is_correct:
                correct_count += 1
                topic_stats[topic]["correct"] += 1

            reviews.append({
                "question_id": q_id,
                "question_number": q_num,
                "question": q["question"],
                "type": q_type,
                "topic": topic,
                "user_answer": student_ans if student_ans else "(No Answer)",
                "correct_answer": correct_ans,
                "is_correct": is_correct,
                "explanation": q.get("explanation", "Review the topic documentation to reinforce this concept.")
            })

        percentage = int(round((correct_count / total_questions) * 100))
        passed = (percentage >= passing_score)

        topic_performance: Dict[str, Dict[str, int]] = {}
        strengths = []
        weak_topics = []
        recommended_revisions = []
        suggested_practice = []

        for top, stat in topic_stats.items():
            top_pct = int(round((stat["correct"] / stat["total"]) * 100)) if stat["total"] > 0 else 0
            topic_performance[top] = {
                "total": stat["total"],
                "correct": stat["correct"],
                "percentage": top_pct
            }
            if top_pct >= 70:
                strengths.append(top)
            else:
                weak_topics.append(top)
                recommended_revisions.append({
                    "topic": top,
                    "score_percentage": top_pct,
                    "recommendation": f"Review core principles, syntax examples, and practice challenges for '{top}'."
                })
                suggested_practice.append(f"Complete extra code/exercise drills for: {top}")

        return {
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": percentage,
            "passed": passed,
            "status": "PASSED" if passed else "FAILED",
            "passing_score": passing_score,
            "topic_performance": topic_performance,
            "strengths": strengths,
            "weak_topics": weak_topics,
            "recommended_revisions": recommended_revisions,
            "suggested_practice": suggested_practice,
            "reviews": reviews
        }

    def _numeric_match(self, s1: str, s2: str) -> bool:
        s1_clean = s1.replace("%", "").strip()
        s2_clean = s2.replace("%", "").strip()
        try:
            return abs(float(s1_clean) - float(s2_clean)) < 1e-4
        except ValueError:
            return False

    # Legacy method compatibility
    def generate_questions(
        self,
        task_skill: str,
        task_title: str,
        difficulty: str,
        topics: List[Dict[str, Any]],
        exclude_ids: List[str],
        count: int = 5
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        level = 1
        diff_str = (difficulty or "beginner").lower()
        if "inter" in diff_str:
            level = 2
        elif "adv" in diff_str:
            level = 3

        client_qs, full_qs = self.generate_level_assessment(
            skill=task_skill,
            level=level,
            topics=topics,
            exclude_ids=exclude_ids,
            mcq_count=count,
            practical_count=0
        )
        return client_qs, full_qs

    def evaluate_quiz(
        self,
        full_questions: List[Dict[str, Any]],
        student_answers: Dict[str, str],
        passing_score: int = 70
    ) -> Dict[str, Any]:
        eval_res = self.evaluate_assessment(full_questions, student_answers, passing_score)
        # Add legacy format dictionary for topic performance
        legacy_topic_perf = {k: v["percentage"] for k, v in eval_res["topic_performance"].items()}
        return {
            **eval_res,
            "topic_performance": legacy_topic_perf
        }

# Global instance
question_gen_service = RuleBasedQuestionGenerator()
