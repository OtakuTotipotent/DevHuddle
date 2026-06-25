import json
from .models import AIReport


class DevHuddleAIEngine:
    """
    Facade for all AI interactions.
    Swap the implementation inside _call_llm() to change AI providers.
    """

    @staticmethod
    def _call_llm(system_prompt, user_data):
        # -------------------------------------------------------------
        # 🔌 AI INTEGRATION POINT
        # Replace this logic with your free open-source AI package.
        # Example using g4f (GPT4Free) or Gemini Free Tier API:
        # response = g4f.ChatCompletion.create(model="gpt-3.5", messages=[...])
        # -------------------------------------------------------------

        # Simulated intelligent response for current testing phase:
        return f"""
### 🧠 DevHuddle AI Analysis

Based on the provided telemetry, here is the architectural breakdown.

**Strengths:**
* High density of backend logic.
* Demonstrated capability in `{user_data.get("role", "Development")}`.

**Areas for Improvement:**
* Expand Open-Source contributions.
* Increase cross-functional skill tagging.

**Market Viability:**
Highly competitive for Mid-to-Senior level enterprise roles. 
        """

    @classmethod
    def analyze_profile(cls, target_user, requester):
        # Check Cache
        recent_report = AIReport.objects.filter(
            report_type="profile", target_user=target_user
        ).first()

        if recent_report:
            return recent_report

        # Extract & Encapsulate Context
        context = {
            "username": target_user.username,
            "role": target_user.role,
            "bio": target_user.bio,
            "skills": list(target_user.skills.values_list("name", flat=True)),
            "projects_count": target_user.projects.count(),
            "experience_count": target_user.experiences.count(),
        }

        # Prompt Engineering
        sys_prompt = "You are DevHuddle's elite AI career coach. Analyze this developer's JSON profile and output a harsh but constructive Markdown report."

        raw_markdown = cls._call_llm(sys_prompt, context)

        return AIReport.objects.create(
            report_type="profile",
            requester=requester,
            target_user=target_user,
            content=raw_markdown,
        )

    @classmethod
    def analyze_post(cls, target_post, requester):
        # Check Cache
        recent_report = AIReport.objects.filter(
            report_type="post", target_post=target_post
        ).first()
        if recent_report:
            return recent_report

        # Encapsulate
        context = {
            "post_body": target_post.body,
            "post_type": target_post.post_type,
            "author": target_post.author.username,
            "likes": target_post.likes.count(),
        }

        # Generate
        sys_prompt = "You are DevHuddle's senior technical architect. Review this post/code snippet and provide technical feedback, security risks, or praise."
        raw_markdown = cls._call_llm(sys_prompt, context)

        return AIReport.objects.create(
            report_type="post",
            requester=requester,
            target_post=target_post,
            content=raw_markdown,
        )
