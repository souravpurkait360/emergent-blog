import logging
import os

from asgiref.sync import async_to_sync
from emergentintegrations.llm.chat import LlmChat, StreamDone, TextDelta, UserMessage

logger = logging.getLogger(__name__)
LLM_API_KEY = os.environ.get("EMERGENT_LLM_KEY", "")
LLM_PROVIDER = "openai"
LLM_MODEL = "gpt-5.4"


class AIService:
    """Singleton service for AI-powered blog writing features."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "AIService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _run_llm(self, session_id: str, system_message: str, user_text: str) -> str:
        """Execute a streaming LLM call and return the full response text."""
        async def _execute():
            chat = LlmChat(
                api_key=LLM_API_KEY,
                session_id=session_id,
                system_message=system_message,
            ).with_model(LLM_PROVIDER, LLM_MODEL)

            collected_text = []
            async for event in chat.stream_message(UserMessage(text=user_text)):
                if isinstance(event, TextDelta):
                    collected_text.append(event.content)
                elif isinstance(event, StreamDone):
                    break
            return "".join(collected_text)

        return async_to_sync(_execute)()

    def generate_writing_assistance(self, title: str, existing_content: str) -> str:
        """Return a content continuation for the given blog post."""
        user_text = (
            f"Continue writing the blog post titled '{title}'.\n\n"
            f"Existing content:\n{existing_content[:3000]}\n\n"
            "Return only the continuation HTML, no explanations."
        )
        return self._run_llm(
            session_id=f"assist-{hash(title)}",
            system_message=(
                "You are an expert blog writer. Write engaging, informative content. "
                "Return only the text continuation with basic HTML formatting."
            ),
            user_text=user_text,
        )

    def generate_summary(self, title: str, content: str) -> str:
        """Generate a concise 2-3 sentence summary for the post."""
        user_text = f"Write a concise 2-3 sentence summary for this blog post titled '{title}':\n\n{content[:3000]}"
        return self._run_llm(
            session_id=f"summarize-{hash(title)}",
            system_message="You are an expert content summarizer. Create concise, engaging summaries.",
            user_text=user_text,
        )
