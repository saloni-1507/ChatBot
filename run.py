import gradio as gr
import uvicorn

from api.chat import app
from core.config import settings
from ui.chat import interface

app = gr.mount_gradio_app(
    app,
    interface,
    path="/",
    run_history=False,
    pwa=True,
    footer_links=[],
    css='button[aria-label="Clear"] { display: none !important; }',
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)