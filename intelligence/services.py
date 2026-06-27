import json
from google import genai
from django.conf import settings
from .models import AIReport

# Initialize the key from configs
client = genai.Client(api_key=settings.GEMINI_API_KEY)

if client:
    print("Genai client received")
else:
    print("Genai client not received")


class DevHuddleAIEngine:
    """
    Facade for Google Gemini interactions.
    """

    @staticmethod
    def _call_llm(system_prompt, user_data):
        try:
            # Combine the prompt and the JSON data
            combined_prompt = f"{system_prompt}\n\nHere is the data:\n{json.dumps(user_data, indent=2)}"

            # API Cal
            response = client.interactions.create(
                model="gemini-3.5-flash",
                input=combined_prompt,
            )

            if response:
                print("Genai response received")
            else:
                print("Genai response not received")

            return response.output_text

        except Exception as e:
            # Fallback in case API fails, internet drops, or quota runs out
            return f"**Error connecting to AI Provider:** {str(e)}\n\nPlease try again later."

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
