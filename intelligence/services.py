from .models import AIReport
from .providers.gemini import gemini_response


class DevHuddleAIEngine:
    """
    Facade for Intelligent System interactions.
    """

    @staticmethod
    def _call_llm(system_prompt, user_data):
        return gemini_response(system_prompt, user_data)

    @classmethod
    def analyze_profile(cls, target_user, requester):
        # Check Cache if report already exists
        recent_report = AIReport.objects.filter(
            report_type="profile", target_user=target_user
        ).first()
        if recent_report:
            return recent_report

        # User data
        context = {
            "username": target_user.username,
            "role": target_user.role,
            "bio": target_user.bio,
            "skills": list(target_user.skills.values_list("name", flat=True)),
            "projects_count": target_user.projects.count(),
            "experience_count": target_user.experiences.count(),
            "follower_count": target_user.followers.count(),
        }

        # Prompt Engineering
        sys_prompt = """
        You are an elite Technical Recruiter and Career Coach for an app called DevHuddle. 
        Analyze the provided JSON profile of this developer.
        Write a professional, formatted Markdown report with three sections:
        1. 🌟 Core Strengths (Based on their skills/projects)
        2. 📈 Areas for Growth (What are they missing?)
        3. 💼 Market Viability (How employable are they?)
        Keep it concise, highly technical, and use markdown bullet points. Do not wrap the response in ```markdown tags.
        """

        raw_markdown = cls._call_llm(sys_prompt, context)
        return AIReport.objects.create(
            report_type="profile",
            requester=requester,
            target_user=target_user,
            content=raw_markdown,
        )

    @classmethod
    def analyze_post(cls, target_post, requester):
        # Check Cache if post already exists
        recent_report = AIReport.objects.filter(
            report_type="post", target_post=target_post
        ).first()
        if recent_report:
            return recent_report

        # Encapsulate
        context = {
            "post_body": target_post.body,
            "post_type": target_post.post_type,
            "author_role": target_post.author.role,
            "likes_count": target_post.likes.count(),
        }

        sys_prompt = """
        You are a Senior Software Architect reviewing a post from a developer community called DevHuddle.
        Analyze the post content. Provide a Markdown report containing:
        1. Technical Breakdown (What is the core subject?)
        2. Sentiment & Tone
        3. Potential follow-up questions to ask the author to spark discussion.
        Keep it concise and technical.
        """
        raw_markdown = cls._call_llm(sys_prompt, context)
        return AIReport.objects.create(
            report_type="post",
            requester=requester,
            target_post=target_post,
            content=raw_markdown,
        )
