import os
import uvicorn
from server import app

# Hugging Face Gradio compatibility wrapper
try:
    import gradio as gr
    # Mount FastAPI directly into Gradio
    demo = gr.mount_gradio_app(app, gr.Blocks(title="رادار السوق"), path="/gradio")
except Exception as e:
    print(f"Gradio mount notice: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
