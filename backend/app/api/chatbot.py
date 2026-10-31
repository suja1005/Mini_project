import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.security import get_current_user
from app.database.connection import get_database
from app.services.career_roadmap_service import get_or_initialize_user_roadmap

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/chatbot", tags=["AI Career Assistant Chatbot (Gemini)"])

class ChatMessage(BaseModel):
    role: str  # "user" or "model" / "assistant"
    content: str = Field(..., min_length=1, max_length=2000)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    reply: str
    suggested_followups: Optional[List[str]] = []
    personalized_context_used: bool = True

def build_student_context_prompt(student_name: str, profile: Dict[str, Any], roadmap: Dict[str, Any]) -> str:
    target_career = roadmap.get("career_title", profile.get("target_role", "AI Engineer"))
    overall_progress = roadmap.get("overall_progress", 0)

    completed_topic_names = [t.get("title", "") for t in roadmap.get("completed_topics", [])]
    pending_topic_names = [t.get("title", "") for t in roadmap.get("pending_topics", [])]
    
    current_topic = roadmap.get("current_learning_topic", {})
    current_topic_name = current_topic.get("title", "Not Selected")
    current_phase_name = current_topic.get("phase_name", "Beginner Phase")

    # Assessment summary
    phases_info = []
    for p in roadmap.get("phases", []):
        p_name = p.get("name", "")
        p_status = p.get("status", "")
        b_score = p.get("best_score")
        score_str = f"Best Score: {b_score}%" if b_score is not None else "Not Attempted"
        phases_info.append(f"- {p_name}: Status={p_status}, {score_str}")

    return (
        f"You are the 'AI Career Assistant', a dedicated senior engineering mentor and career coach embedded in an "
        f"AI-Powered Career Guidance and Employability Enhancement Platform.\n\n"
        f"STUDENT PROFILE:\n"
        f"- Name: {student_name}\n"
        f"- Target Career: {target_career}\n"
        f"- Degree / Background: {profile.get('degree', 'B.Tech')} in {profile.get('department', 'Computer Science')}\n"
        f"- Overall Roadmap Progress: {overall_progress}%\n"
        f"- Current Active Phase: {current_phase_name}\n"
        f"- Current Topic to Study: {current_topic_name}\n"
        f"- Completed Topics: {', '.join(completed_topic_names) if completed_topic_names else 'None yet'}\n"
        f"- Pending Topics: {', '.join(pending_topic_names[:5]) if pending_topic_names else 'None'}\n"
        f"- Phase Statuses & Scores:\n" + "\n".join(phases_info) + "\n\n"
        f"MENTORSHIP INSTRUCTIONS:\n"
        f"1. Provide encouraging, technically rigorous, clear, and actionable answers.\n"
        f"2. When explaining programming or AI concepts, include clean, idiomatic code examples with explanations.\n"
        f"3. Tailor explanations to the student's current learning phase ({current_phase_name}) and target role ({target_career}).\n"
        f"4. If asked about what to study next or how to prepare for assessments, reference the 80% passing requirement and their current topic.\n"
        f"5. Answer general educational questions about computer science, software engineering, and interview preparation accurately.\n"
        f"6. Never reveal internal API keys, passwords, or mock scores."
    )

def generate_local_fallback_reply(user_message: str, target_career: str, current_topic: str, phase_name: str) -> str:
    """
    Intelligent context-aware fallback response when live Gemini API key is absent or offline.
    """
    msg_lower = user_message.lower()
    
    if "python" in msg_lower or "code" in msg_lower:
        return (
            f"Here is a foundational Python example relevant to your {target_career} roadmap:\n\n"
            "```python\n"
            "# Computing normalized feature weights\n"
            "def calculate_readiness(skills: dict[str, int]) -> float:\n"
            "    weights = {'Python': 0.35, 'Machine Learning': 0.35, 'Math': 0.30}\n"
            "    total = sum(skills.get(k, 0) * w for k, w in weights.items())\n"
            "    return round(total, 2)\n\n"
            "my_skills = {'Python': 85, 'Machine Learning': 75, 'Math': 90}\n"
            "print('Employability Score:', calculate_readiness(my_skills))\n"
            "```\n\n"
            f"This aligns directly with your current topic **{current_topic}** in the **{phase_name}**. "
            "Mastering vectorized operations and defensive functional programming is key for AI and ML engineering!"
        )
    elif "next" in msg_lower or "study" in msg_lower or "what should i" in msg_lower:
        return (
            f"Based on your current roadmap progress for **{target_career}**, your next recommended action is to focus on "
            f"**{current_topic}** in the **{phase_name}**.\n\n"
            "1. Read the step-by-step lesson materials on the module page.\n"
            "2. Complete the hands-on practical exercise and test your code.\n"
            "3. Answer the mandatory knowledge check question to earn your green completion tick.\n"
            "4. Once all phase topics are complete, take the Phase Assessment (Score >= 80% to unlock the next phase)!"
        )
    elif "assessment" in msg_lower or "score" in msg_lower or "pass" in msg_lower:
        return (
            f"To excel in the Phase Assessment for {phase_name}:\n\n"
            "• **Passing Requirement:** You need at least **80%** to pass the phase and unlock the next tier.\n"
            "• **Question Types:** Questions are randomized from your completed topics to test deep comprehension.\n"
            "• **Tips:** Review weak topics highlighted in your results review and test yourself with the knowledge checks."
        )
    elif "project" in msg_lower or "portfolio" in msg_lower:
        return (
            f"Great question! For a student at your current stage ({phase_name}) targeting **{target_career}**, "
            "here is a high-impact project suggestion:\n\n"
            "• **Project Title:** End-to-End Career Intelligence & Employability Scorer\n"
            "• **Tech Stack:** Python, Pandas, Scikit-Learn, FastAPI\n"
            "• **Key Deliverable:** Ingest candidate skill metrics, train an explainable ensemble model, and serve predictions via a RESTful API.\n"
            "This directly showcases your full-stack AI and software engineering capabilities!"
        )
    else:
        return (
            f"Hello! I am your **AI Career Assistant** tailored to your **{target_career}** path. "
            f"You are currently working in the **{phase_name}**, studying **{current_topic}**.\n\n"
            "Feel free to ask me:\n"
            "• 'Explain this topic in simple English'\n"
            "• 'Give me a Python example'\n"
            "• 'What should I study next?'\n"
            "• 'How can I improve my assessment score?'\n"
            "• 'Suggest a project for my current learning phase'\n\n"
            "How can I assist your learning today?"
        )

@router.post("/message", response_model=ChatResponse)
async def chat_message_route(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Processes chat messages with the Google Gemini API, enriched with authenticated
    student profile and roadmap context.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    student_name = current_user.get("full_name", "Student")
    db = get_database()

    # 1. Fetch student profile and roadmap context
    profile = {}
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id}) or {}

    roadmap = await get_or_initialize_user_roadmap(user_id)

    system_instruction = build_student_context_prompt(student_name, profile, roadmap)
    target_career = roadmap.get("career_title", "AI Engineer")
    curr_topic = roadmap.get("current_learning_topic", {}).get("title", "Foundations")
    curr_phase = roadmap.get("current_learning_topic", {}).get("phase_name", "Beginner Phase")

    # 2. Try Calling Live Google Gemini API if key is configured
    if settings.GEMINI_API_KEY:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            # Build multi-turn contents
            contents = []
            
            # Add past turns
            for h in request.history[-6:]:  # Keep recent 6 turns for context
                role_tag = "user" if h.role == "user" else "model"
                contents.append(
                    types.Content(
                        role=role_tag,
                        parts=[types.Part.from_text(text=h.content)]
                    )
                )

            # Add current user prompt
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=request.message)]
                )
            )

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=1000
            )

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents,
                config=config
            )

            ai_text = response.text.strip() if response.text else "I am here to help you advance your career roadmap. What questions do you have?"
            
            return ChatResponse(
                reply=ai_text,
                suggested_followups=[
                    "What should I study next?",
                    "Give me a code example for this topic",
                    "How do I prepare for the phase assessment?",
                    "Suggest a practical mini-project"
                ],
                personalized_context_used=True
            )

        except Exception as e:
            logger.warning(f"Live Gemini API invocation note: {e}. Falling back to domain career intelligence.")
            # Gracefully degrade to domain-specific mentorship response

    # 3. Fallback response engine using student context
    fallback_text = generate_local_fallback_reply(request.message, target_career, curr_topic, curr_phase)
    return ChatResponse(
        reply=fallback_text,
        suggested_followups=[
            "What should I study next?",
            "Give me a code example for this topic",
            "How do I prepare for the phase assessment?",
            "Suggest a practical mini-project"
        ],
        personalized_context_used=True
    )
