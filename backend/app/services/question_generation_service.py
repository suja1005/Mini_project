import os
import json
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

QUESTIONS_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "roadmap_questions.json"
)

class QuestionGenerator(ABC):
    @abstractmethod
    def generate_questions(
        self,
        task_skill: str,
        task_title: str,
        difficulty: str,
        topics: List[Dict[str, Any]],
        exclude_ids: List[str],
        count: int = 5
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Returns (frontend_questions, full_questions_with_answers)
        """
        pass

    @abstractmethod
    def evaluate_quiz(
        self,
        full_questions: List[Dict[str, Any]],
        student_answers: Dict[str, str],
        passing_score: int = 70
    ) -> Dict[str, Any]:
        pass

class RuleBasedQuestionGenerator(QuestionGenerator):
    def __init__(self, questions_path: str = QUESTIONS_FILE_PATH):
        self.questions_path = questions_path
        self.questions_bank = self._load_questions()

    def _load_questions(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.questions_path):
            try:
                with open(self.questions_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[RuleBasedQuestionGenerator] Error loading questions json: {e}")
        return []

    def generate_questions(
        self,
        task_skill: str,
        task_title: str,
        difficulty: str,
        topics: List[Dict[str, Any]],
        exclude_ids: List[str],
        count: int = 5
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        diff_str = (difficulty or "beginner").lower()
        topic_titles = [t.get("title", "") for t in topics] if topics else []

        # Filter candidates matching task skill or topics
        candidates = []
        for q in self.questions_bank:
            q_skill = q.get("task_type", "").lower()
            q_topic = q.get("topic", "")
            
            # Match skill or matching topic
            matches_skill = task_skill.lower() in q_skill or q_skill in task_skill.lower() or q_skill == "general"
            matches_topic = any(tt.lower() in q_topic.lower() or q_topic.lower() in tt.lower() for tt in topic_titles)

            if matches_skill or matches_topic:
                candidates.append(q)

        if not candidates:
            # Fallback to all questions if no match
            candidates = list(self.questions_bank)

        # Exclude recently used questions if possible
        available_candidates = [q for q in candidates if q["id"] not in exclude_ids]
        if len(available_candidates) < count:
            # Pool exhausted or small -> reset exclusion constraint
            available_candidates = list(candidates)

        # Group by topic/subtopic to maximize diversity across questions
        topic_buckets: Dict[str, List[Dict[str, Any]]] = {}
        for q in available_candidates:
            top_key = q.get("topic", "General")
            topic_buckets.setdefault(top_key, []).append(q)

        selected: List[Dict[str, Any]] = []
        bucket_keys = list(topic_buckets.keys())
        random.shuffle(bucket_keys)

        # Round-robin selection across topics
        while len(selected) < count and available_candidates:
            added_in_round = False
            for key in bucket_keys:
                if len(selected) >= count:
                    break
                if topic_buckets[key]:
                    item = random.choice(topic_buckets[key])
                    topic_buckets[key].remove(item)
                    if item not in selected:
                        selected.append(item)
                        added_in_round = True

            if not added_in_round:
                # Fill remaining from available pool randomly
                remaining = [q for q in available_candidates if q not in selected]
                if remaining:
                    needed = count - len(selected)
                    selected.extend(random.sample(remaining, min(needed, len(remaining))))
                break

        # If still less than count, duplicate/sample from candidate bank with shuffled options
        if len(selected) < count and self.questions_bank:
            needed = count - len(selected)
            extra = random.sample(self.questions_bank, min(needed, len(self.questions_bank)))
            selected.extend(extra)

        selected = selected[:count]

        # Prepare frontend version (DO NOT send correct_answer or explanation)
        frontend_questions = []
        full_questions = []

        for q in selected:
            options = list(q.get("options", []))
            # Shuffle options for randomness while maintaining correct_answer reference
            shuffled_options = list(options)
            random.shuffle(shuffled_options)

            full_questions.append({
                "id": q["id"],
                "question": q["question"],
                "options": shuffled_options,
                "correct_answer": q["correct_answer"],
                "explanation": q.get("explanation", ""),
                "topic": q.get("topic", "General"),
                "subtopic": q.get("subtopic", ""),
                "difficulty": q.get("difficulty", difficulty)
            })

            frontend_questions.append({
                "question_id": q["id"],
                "question": q["question"],
                "options": shuffled_options,
                "topic": q.get("topic", "General"),
                "difficulty": q.get("difficulty", difficulty)
            })

        return frontend_questions, full_questions

    def evaluate_quiz(
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
                "topic_performance": {},
                "weak_topics": [],
                "explanations": {}
            }

        correct_count = 0
        topic_stats: Dict[str, Dict[str, int]] = {}
        explanations = {}

        for q in full_questions:
            q_id = q["id"]
            correct_ans = str(q.get("correct_answer", "")).strip()
            student_ans = str(student_answers.get(q_id, "")).strip()
            topic = q.get("topic", "General")

            topic_stats.setdefault(topic, {"correct": 0, "total": 0})
            topic_stats[topic]["total"] += 1

            is_correct = (student_ans.lower() == correct_ans.lower())
            if is_correct:
                correct_count += 1
                topic_stats[topic]["correct"] += 1

            explanations[q_id] = {
                "is_correct": is_correct,
                "student_answer": student_ans,
                "correct_answer": correct_ans,
                "explanation": q.get("explanation", "")
            }

        pct = int(round((correct_count / total_questions) * 100))
        passed = (pct >= passing_score)

        topic_performance: Dict[str, int] = {}
        weak_topics = []
        for top, stat in topic_stats.items():
            top_pct = int(round((stat["correct"] / stat["total"]) * 100)) if stat["total"] > 0 else 0
            topic_performance[top] = top_pct
            if top_pct < 70:
                weak_topics.append(top)

        return {
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": pct,
            "passed": passed,
            "status": "VERIFIED" if passed else "FAILED",
            "topic_performance": topic_performance,
            "weak_topics": weak_topics,
            "explanations": explanations
        }

class LLMQuestionGenerator(QuestionGenerator):
    """
    Optional LLM Question Generator Stub.
    Maintains clean interface for future AI model expansion.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def generate_questions(
        self,
        task_skill: str,
        task_title: str,
        difficulty: str,
        topics: List[Dict[str, Any]],
        exclude_ids: List[str],
        count: int = 5
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        # Fallback to rule based generator if LLM key absent
        fallback = RuleBasedQuestionGenerator()
        return fallback.generate_questions(task_skill, task_title, difficulty, topics, exclude_ids, count)

    def evaluate_quiz(
        self,
        full_questions: List[Dict[str, Any]],
        student_answers: Dict[str, str],
        passing_score: int = 70
    ) -> Dict[str, Any]:
        fallback = RuleBasedQuestionGenerator()
        return fallback.evaluate_quiz(full_questions, student_answers, passing_score)

# Default global service instance
question_gen_service = RuleBasedQuestionGenerator()
