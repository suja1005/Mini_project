import os
import json
import random
import logging
import uuid
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple, Optional

from app.core.config import settings

logger = logging.getLogger("uvicorn")

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
        passing_score: int = 80
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
                logger.error(f"[QuestionGenerator] Error loading primary questions: {e}")
        
        if os.path.exists(self.legacy_path):
            try:
                with open(self.legacy_path, "r", encoding="utf-8") as f:
                    legacy = json.load(f)
                    for q in legacy:
                        if "skill" not in q:
                            q["skill"] = q.get("task_type", "General")
                        if "type" not in q:
                            q["type"] = "mcq"
                        if "level" not in q:
                            q["level"] = 1
                    bank.extend(legacy)
            except Exception as e:
                logger.error(f"[QuestionGenerator] Error loading legacy questions: {e}")

        return bank

    def reload_bank(self):
        self.questions_bank = self._load_questions()

    def get_personalized_skills(self, profile: Dict[str, Any]) -> List[str]:
        """
        Extract personalized target skills and topics matching the student's profile:
        - Interests (e.g. AI, Web Development, Data Science)
        - Target role / selected career
        - Technical skills and academic background
        """
        interests = profile.get("interests", [])
        if isinstance(interests, str):
            interests = [interests]
        target_role = profile.get("target_role", "") or profile.get("career", "") or profile.get("career_title", "")
        tech_skills = list(profile.get("technical_skills", {}).keys()) if isinstance(profile.get("technical_skills"), dict) else []
        preferred_domain = profile.get("preferred_domain", "")

        all_tokens = (
            [str(i).lower() for i in interests] +
            [str(target_role).lower(), str(preferred_domain).lower()] +
            [str(s).lower() for s in tech_skills]
        )
        combined_text = " ".join(all_tokens)

        # 1. Artificial Intelligence
        if any(k in combined_text for k in ["artificial intelligence", "ai engineer", "machine learning", "deep learning", "neural"]):
            return ["Artificial Intelligence", "Python", "Machine Learning", "Mathematics", "Problem Solving"]

        # 2. Web Development
        if any(k in combined_text for k in ["web development", "web developer", "frontend", "front-end", "backend", "back-end", "full stack", "react", "html"]):
            return ["Web Development", "Python", "SQL", "Git and GitHub", "Problem Solving"]

        # 3. Data Science
        if any(k in combined_text for k in ["data science", "data scientist", "data analyst", "statistics", "data engineering"]):
            return ["Data Science", "Python", "SQL", "Mathematics", "Machine Learning"]

        # Fallback to general technical skills
        return ["Python", "Problem Solving", "Mathematics", "SQL", "Git and GitHub"]

    def generate_personalized_assessment(
        self,
        user_id: str,
        profile: Dict[str, Any],
        exclude_ids: Optional[List[str]] = None,
        total_count: int = 15,
        phase: str = "Beginner"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Generates personalized, non-repeating questions according to student's profile.
        - Matches interests, skills, career
        - Excludes questions already attempted by this student when alternatives exist
        - Avoids repeating questions within the same assessment
        - Randomizes answer options
        - Hides correct answers from client payload
        """
        if exclude_ids is None:
            exclude_ids = []

        relevant_skills = self.get_personalized_skills(profile)
        level = 1
        phase_lower = phase.lower()
        if "inter" in phase_lower or phase_lower == "2":
            level = 2
        elif "adv" in phase_lower or phase_lower == "3":
            level = 3

        # Filter candidate questions matching personalized skills and level
        candidates = []
        for q in self.questions_bank:
            q_skill = str(q.get("skill", "")).strip()
            q_topic = str(q.get("topic", "")).strip()
            q_level = int(q.get("level", 1))

            matches_skill = any(
                rs.lower() in q_skill.lower() or
                q_skill.lower() in rs.lower() or
                rs.lower() in q_topic.lower()
                for rs in relevant_skills
            )
            matches_level = (q_level == level)

            if matches_skill and matches_level:
                candidates.append(q)

        # If matching level has fewer questions, widen level filter within matching skills
        if len(candidates) < total_count:
            for q in self.questions_bank:
                q_skill = str(q.get("skill", "")).strip()
                q_topic = str(q.get("topic", "")).strip()
                matches_skill = any(
                    rs.lower() in q_skill.lower() or
                    q_skill.lower() in rs.lower() or
                    rs.lower() in q_topic.lower()
                    for rs in relevant_skills
                )
                if matches_skill and q not in candidates:
                    candidates.append(q)

        # Fallback to full question bank if still insufficient
        if len(candidates) < total_count:
            candidates = list(self.questions_bank)

        # Prioritize primary interest skill to ensure relevant representation
        primary_skill = relevant_skills[0] if relevant_skills else "General"
        primary_candidates = [
            q for q in candidates
            if primary_skill.lower() in q.get("skill", "").lower()
            or q.get("skill", "").lower() in primary_skill.lower()
            or primary_skill.lower() in q.get("topic", "").lower()
        ]
        other_candidates = [q for q in candidates if q not in primary_candidates]

        # Allocate at least 40-50% to primary interest
        primary_target = min(len(primary_candidates), max(1, total_count // 2))
        other_target = total_count - primary_target

        # Filter unused for primary
        avail_prim = [q for q in primary_candidates if q["id"] not in exclude_ids]
        random.shuffle(avail_prim)
        chosen_prim = avail_prim[:primary_target]

        # Filter unused for other relevant skills
        needed_from_others = total_count - len(chosen_prim)
        avail_other = [q for q in other_candidates if q["id"] not in exclude_ids]
        random.shuffle(avail_other)
        chosen_other = avail_other[:needed_from_others]

        combined = chosen_prim + chosen_other

        # If still short of total_count, take any other unused questions from full relevant candidates
        if len(combined) < total_count:
            rem_unused = [q for q in candidates if q["id"] not in exclude_ids and q not in combined]
            random.shuffle(rem_unused)
            combined.extend(rem_unused[: total_count - len(combined)])

        # If still short, try any unused question in the entire question bank
        if len(combined) < total_count:
            all_bank_unused = [q for q in self.questions_bank if q["id"] not in exclude_ids and q not in combined]
            random.shuffle(all_bank_unused)
            combined.extend(all_bank_unused[: total_count - len(combined)])

        # Only when the student has exhausted all available unused questions, fill remaining from candidates
        if len(combined) < total_count:
            rem_any = [q for q in candidates if q not in combined]
            random.shuffle(rem_any)
            combined.extend(rem_any[: total_count - len(combined)])

        random.shuffle(combined)
        selected_questions = combined[:total_count]

        # Prepare client-facing questions (WITHOUT correct_answer or explanation)
        client_questions = []
        full_questions = []

        for idx, q in enumerate(selected_questions, 1):
            q_id = q["id"]
            options = list(q.get("options", []))
            if options:
                # Randomize option order
                random.shuffle(options)

            client_q = {
                "question_id": q_id,
                "question_number": idx,
                "type": q.get("type", "mcq"),
                "question": q["question"],
                "skill": q.get("skill", "Technical"),
                "topic": q.get("topic", "General"),
                "difficulty": q.get("difficulty", phase),
                "options": options
            }
            client_questions.append(client_q)

            full_q = dict(q)
            full_q["question_number"] = idx
            full_questions.append(full_q)

        return client_questions, full_questions

    def _try_gemini_generate_questions(
        self,
        relevant_skills: List[str],
        level: int,
        phase: str,
        needed: int,
        exclude_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Attempts to generate structured questions via Google Gemini API if configured.
        Validates output strictly on backend.
        """
        if not settings.GEMINI_API_KEY or needed <= 0:
            return []

        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            skill_focus = ", ".join(relevant_skills[:3])
            prompt = (
                f"Generate {needed} multiple choice questions for a university computer science student.\n"
                f"Skills/Topics focus: {skill_focus}.\n"
                f"Learning phase: {phase} (Level {level}).\n"
                f"Difficulty: {phase}.\n\n"
                "You must return ONLY a JSON array with no markdown code fences, matching this schema:\n"
                "[\n"
                "  {\n"
                "    \"id\": \"gemini_<unique_id>\",\n"
                "    \"skill\": \"<Skill Name>\",\n"
                "    \"topic\": \"<Specific Topic>\",\n"
                "    \"level\": " + str(level) + ",\n"
                "    \"difficulty\": \"" + phase + "\",\n"
                "    \"type\": \"mcq\",\n"
                "    \"question\": \"<Question text>\",\n"
                "    \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
                "    \"correct_answer\": \"<Exact match of one of the options>\",\n"
                "    \"explanation\": \"<Why this answer is correct>\"\n"
                "  }\n"
                "]"
            )

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )

            text = response.text.strip()
            # Clean possible markdown formatting
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            parsed = json.loads(text)
            validated = []
            for item in parsed:
                # Backend validation
                if not isinstance(item, dict):
                    continue
                q_id = str(item.get("id", f"gen_{uuid.uuid4().hex[:8]}"))
                q_text = str(item.get("question", "")).strip()
                options = item.get("options", [])
                correct_ans = str(item.get("correct_answer", "")).strip()

                if not q_text or len(options) < 2 or not correct_ans:
                    continue
                if correct_ans not in options:
                    # Invalid question - correct answer not in options
                    continue
                if q_id in exclude_ids:
                    continue

                item["id"] = q_id
                item["skill_slug"] = str(item.get("skill", "general")).lower().replace(" ", "-")
                item["acceptable_answers"] = [correct_ans]
                validated.append(item)

            logger.info(f"Successfully generated {len(validated)} validated questions via Gemini API.")
            return validated
        except Exception as e:
            logger.warning(f"Gemini question generation fallback: {e}")
            return []

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

        combined = selected_mcqs + selected_practicals
        if len(combined) < (mcq_count + practical_count):
            remaining = [q for q in candidates if q not in combined]
            random.shuffle(remaining)
            combined.extend(remaining[: (mcq_count + practical_count) - len(combined)])

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
        passing_score: int = 80
    ) -> Dict[str, Any]:
        """
        Backend-evaluated assessment scoring using strict formula:
        Score Percentage = (Correct Answers / Total Questions) * 100
        Pass condition: Score Percentage >= 80% (or specified passing_score)
        """
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

            topic_stats.setdefault(topic, {"correct": 0, "total": 0})
            topic_stats[topic]["total"] += 1

            is_correct = False
            if q_type == "mcq":
                is_correct = (student_ans_clean == correct_ans.lower()) or (student_ans_clean in acceptable_answers)
            else:
                if student_ans_clean in acceptable_answers:
                    is_correct = True
                elif any(self._numeric_match(student_ans_clean, acc) for acc in acceptable_answers):
                    is_correct = True
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
                "explanation": q.get("explanation", "Review the lesson materials and practical examples for this topic.")
            })

        # Strict percentage formula
        percentage = int(round((correct_count / float(total_questions)) * 100))
        passed = (percentage >= passing_score)

        topic_performance: Dict[str, Dict[str, Any]] = {}
        strengths = []
        weak_topics = []
        recommended_revisions = []
        suggested_practice = []

        for top, stat in topic_stats.items():
            top_pct = int(round((stat["correct"] / float(stat["total"])) * 100)) if stat["total"] > 0 else 0
            topic_performance[top] = {
                "total": stat["total"],
                "correct": stat["correct"],
                "percentage": top_pct
            }
            if top_pct >= passing_score:
                strengths.append(top)
            else:
                weak_topics.append(top)
                recommended_revisions.append({
                    "topic": top,
                    "score_percentage": top_pct,
                    "recommendation": f"Review core concepts, code walkthroughs, and practice problems for '{top}'."
                })
                suggested_practice.append(f"Complete focused practice exercises for: {top}")

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

    # Legacy compatibility methods
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
        passing_score: int = 80
    ) -> Dict[str, Any]:
        eval_res = self.evaluate_assessment(full_questions, student_answers, passing_score)
        legacy_topic_perf = {k: v["percentage"] for k, v in eval_res["topic_performance"].items()}
        return {
            **eval_res,
            "topic_performance": legacy_topic_perf
        }

# Global instance
question_gen_service = RuleBasedQuestionGenerator()
