import json
from google import genai
from config import settings
from .models import AIReport
from django.utils import timezone
from feed.models import Notification

# Initialize the key from configs
client = genai.Client(api_key=settings.GEMINI_API_KEY)


class DevHuddleAIEngine:
    """
    Facade for Intelligent System interactions.
    """

    @staticmethod
    def _call_llm(system_prompt, user_data):
        try:
            combined_prompt = f"{system_prompt}\n\nHere is the exact data:\n{json.dumps(user_data, indent=2)}"

            # API Cal
            response = client.interactions.create(
                model="gemini-2.5-flash",
                input=combined_prompt,
            )
            return response.output_text

        except Exception as e:
            print(f"GenAI Exception: {str(e)}")
            return "⚠️ **AI Generation Failed**\n\nThe intelligence engine is currently overloaded or configuring. Please try again in a few moments."

    @classmethod
    def analyze_profile(cls, target_user, requester):
        recent_report = AIReport.objects.filter(
            report_type="profile", target_user=target_user
        ).first()

        # If a report is already generated this week
        print(recent_report)
        if recent_report and (timezone.now() - recent_report.created_at).days < 7:
            return recent_report

        context = {
            "role": target_user.role,
            "bio": target_user.bio,
            "skills": list(target_user.skills.values_list("name", flat=True)),
            "projects_count": target_user.projects.count(),
            "experience_count": target_user.experiences.count(),
        }

        sys_prompt = """
        You are DevHuddle's Elite Technical Analyzer.
        Analyze the JSON data and output a highly concise, professional Markdown report.
        STRICT RULES:
        - NO conversational intros (e.g., "Here is the report").
        - MUST output exactly three sections: 🌟 Core Strengths, 📈 Areas for Growth, 💼 Market Viability.
        - STRICT LIMIT: Maximum 2 short bullet points per section.
        - Tone must be direct, technical, and objective.
        """

        # API Call
        raw_markdown = cls._call_llm(sys_prompt, context)
        report = AIReport.objects.create(
            report_type="profile",
            requester=requester,
            target_user=target_user,
            content=raw_markdown,
        )

        # DUAL NOTIFICATIONS
        if requester != target_user:
            Notification.objects.create(
                recipient=target_user, actor=requester, verb="ai_profile"
            )
            Notification.objects.create(
                recipient=requester, actor=target_user, verb="ai_ready"
            )

        return report

    @classmethod
    def analyze_post(cls, target_post, requester):
        recent_report = AIReport.objects.filter(
            report_type="post", target_post=target_post
        ).first()
        if recent_report and (timezone.now() - recent_report.created_at).days < 7:
            return recent_report

        context = {
            "post_body": target_post.body,
            "post_type": target_post.post_type,
            "author_role": target_post.author.role,
        }

        sys_prompt = """
        You are DevHuddle's Code Review AI.
        Analyze the post content. Provide a highly concise Markdown report.
        STRICT RULES:
        - NO conversational intros.
        - MUST output exactly three sections: 🔬 Technical Breakdown, 📊 Sentiment & Tone, 🗣️ Suggested Follow-up.
        - STRICT LIMIT: Maximum 2 short bullet points per section.
        - Keep it strictly relevant to Software Development & Engineering.
        """

        raw_markdown = cls._call_llm(sys_prompt, context)
        report = AIReport.objects.create(
            report_type="post",
            requester=requester,
            target_post=target_post,
            content=raw_markdown,
        )

        # DUAL NOTIFICATIONS
        if requester != target_post.author:
            Notification.objects.create(
                recipient=target_post.author,
                actor=requester,
                verb="ai_post",
                post=target_post,
            )
            Notification.objects.create(
                recipient=requester,
                actor=target_post.author,
                verb="ai_ready",
                post=target_post,
            )

        return report
