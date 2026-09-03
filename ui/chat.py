import base64

import gradio as gr
import httpx

from core.config import settings

API_URL = f"http://127.0.0.1:{settings.port}/chat"


async def respond(payload: dict, history: list, token: str | None) -> tuple[dict, list, str | None]:
    message = payload["text"].strip()
    if not message:
        history = history + [{"role": "assistant", "content": "Could you add a short description along with that?"}]
        return payload, history, token

    image_b64 = None
    if payload["files"]:
        with open(payload["files"][0], "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            API_URL, json={"message": message, "image_b64": image_b64}, headers=headers
        )
    data = response.json()
    history = history + [{"role": "user", "content": message}]
    if payload["files"]:
        history.append({"role": "user", "content": gr.Image(payload["files"][0])})
    history.append({"role": "assistant", "content": data["reply"]})
    return {"text": "", "files": []}, history, data["token"]


with gr.Blocks(title="Aurora Assistant", fill_height=True, fill_width=True) as interface:
    gr.Markdown("## ✨ Aurora Assistant")
    gr.Markdown("Product questions, sales, and support — one chat.")
    chatbot = gr.Chatbot(
        buttons=[],
        avatar_images=("public/avatar/user.png", "public/avatar/assistant.png"),
        scale=1,
    )
    msg = gr.MultimodalTextbox(
        placeholder="Message Aurora... (attach a screenshot for support issues)",
        show_label=False,
        sources=["upload"],
        file_types=["image"],
        file_count="single",
    )
    token_state = gr.State(None)

    msg.submit(respond, [msg, chatbot, token_state], [msg, chatbot, token_state])