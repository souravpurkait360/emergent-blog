import os

from asgiref.sync import async_to_sync
from emergentintegrations.llm.chat import LlmChat, StreamDone, TextDelta, UserMessage
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')


def run_llm(session_id, system_msg, user_text):
    async def _run():
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=system_msg
        ).with_model("openai", "gpt-5.4")
        result = []
        async for event in chat.stream_message(UserMessage(text=user_text)):
            if isinstance(event, TextDelta):
                result.append(event.content)
            elif isinstance(event, StreamDone):
                break
        return ''.join(result)
    return async_to_sync(_run)()


class AIAssistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content', '')
        prompt = request.data.get('prompt', 'Continue writing this blog post. Return only the continuation:')
        user_text = f"{prompt}\n\nExisting content:\n{content[:3000]}"
        suggestion = run_llm(
            f"assist-{request.user.id}",
            "You are an expert blog writer. Write engaging, informative content. Return only the text continuation, no explanations or meta-commentary.",
            user_text
        )
        return Response({'suggestion': suggestion})


class AISummarizeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content', '')
        title = request.data.get('title', '')
        user_text = f"Write a concise 2-3 sentence summary for a blog post titled '{title}':\n\n{content[:3000]}"
        summary = run_llm(
            f"summarize-{request.user.id}",
            "You are an expert content summarizer. Create concise, engaging summaries for blog posts.",
            user_text
        )
        return Response({'summary': summary})
