import json
from google import genai
from config import settings
from .models import AIReport
from django.utils import timezone
from feed.models import Notification

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class DevHuddleAIEngine:
    """
    Facade for Intelligent System interactions with Fallback Cascade.
    """

    @staticmethod
    def _call_llm(system_prompt, user_data):
        combined_prompt = f"{system_prompt}\n\nHere is the exact data:\n{json.dumps(user_data, indent=2)}"

        # Primary Attempt (Latest Model)
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=combined_prompt,
            )
            return response.text
        except Exception as e1:
            print(f"Primary AI Failed: {str(e1)}")

            # 2. Fallback Attempt (Stable Free-Tier Model)
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=combined_prompt,
                )
                return response.text
            except Exception as e2:
                print(f"Fallback AI Failed: {str(e2)}")

                # 3. Graceful UI Error (Markdown Formatted)
                return """
### ⚠️ Intelligence Engine Overloaded
The DevHuddle AI network is currently experiencing extremely high traffic or API rate limits.
**Diagnostics:**
* Primary Model (`2.5-flash`): Connection Refused.
* Fallback Model (`1.5-flash`): Connection Refused.

**Action Required:**
Please delete this report from your dashboard and try again in 60 seconds.
                """

    @classmethod
    def analyze_profile(cls, target_user, requester):
        recent_report = AIReport.objects.filter(
            report_type="profile", target_user=target_user
        ).first()

        # Check Cache (Valid for 7 days to save API quota)
        if recent_report and (timezone.now() - recent_report.created_at).days < 7:
            return recent_report

        # 🧠 DEEP DATA EXTRACTION (The Context Payload)
        context = {
            "identity": {
                "username": target_user.username,
                "role": target_user.get_role_display(),
                "bio": target_user.bio or "No bio provided.",
            },
            "network": {
                "followers": target_user.followers.count(),
                "following": target_user.following.count(),
                "is_premium": target_user.is_premium,
            },
            "expertise": {
                "skills": list(target_user.skills.values_list("name", flat=True)),
                "projects": [
                    {"title": p.title, "tech_details": p.description[:100]}
                    for p in target_user.projects.all()[:3]
                ],
                "experiences": [
                    {"role": e.role, "company": e.company}
                    for e in target_user.experiences.all()[:3]
                ],
            },
        }

        # 🛑 STRICT PROMPT ENGINEERING
        sys_prompt = """
        You are DevHuddle's Elite Technical Recruiter & Architect. Analyze this developer's JSON profile.
        Output a highly professional, beautifully formatted Markdown report.
        
        REQUIRED SECTIONS:
        ### 🌟 Core Identity & Strengths
        (2-3 bullet points analyzing their stack and experience)
        
        ### 📈 Areas for Growth
        (2-3 actionable bullet points on what skills/projects they are missing)
        
        ### 💼 Market Viability
        (A short, punchy paragraph on how employable they are for enterprise roles)

        Do NOT use conversational intros. Go straight into the markdown headers.
        """

        raw_markdown = cls._call_llm(sys_prompt, context)

        report = AIReport.objects.create(
            report_type="profile",
            requester=requester,
            target_user=target_user,
            content=raw_markdown,
        )

        # Notify Target
        if requester != target_user:
            Notification.objects.create(
                recipient=target_user, actor=requester, verb="ai"
            )
            Notification.objects.create(
                recipient=requester, actor=target_user, verb="ai"
            )

        return report

    @classmethod
    def analyze_post(cls, target_post, requester):
        recent_report = AIReport.objects.filter(
            report_type="post", target_post=target_post
        ).first()

        if recent_report and (timezone.now() - recent_report.created_at).days < 7:
            return recent_report

        # 🧠 DEEP DATA EXTRACTION
        context = {
            "post": {
                "body": target_post.body,
                "type": target_post.get_post_type_display(),
                "age_in_days": (timezone.now() - target_post.created_at).days,
                "has_media": bool(target_post.image),
            },
            "author": {
                "username": target_post.author.username,
                "role": target_post.author.get_role_display(),
                "premium_status": target_post.author.is_premium,
            },
            "engagement": {
                "likes": target_post.likes.count(),
                "comments": target_post.comments.count(),
            },
        }

        sys_prompt = """
        You are DevHuddle's Code Review AI. Analyze the post content and its engagement metrics.
        Output a highly professional Markdown report.
        
        REQUIRED SECTIONS:
        ### 🔬 Technical Breakdown
        (Analyze the subject matter and intent of the post)
        
        ### 📊 Engagement Analysis
        (Analyze the likes/comments ratio based on the author's role and post age)
        
        ### 🗣️ Suggested Follow-up
        (Provide 1 highly technical, intelligent question the user can comment on this post to spark discussion)
        
        Do NOT use conversational intros.
        """

        raw_markdown = cls._call_llm(sys_prompt, context)

        report = AIReport.objects.create(
            report_type="post",
            requester=requester,
            target_post=target_post,
            content=raw_markdown,
        )

        if requester != target_post.author:
            Notification.objects.create(
                recipient=target_post.author,
                actor=requester,
                verb="ai",
                post=target_post,
            )
            Notification.objects.create(
                recipient=requester,
                actor=target_post.author,
                verb="ai",
                post=target_post,
            )

        return report
