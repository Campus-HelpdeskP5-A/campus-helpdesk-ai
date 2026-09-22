import subprocess
import threading
import time

import gradio as gr
import httpx


def start_fastapi():
    subprocess.run([
        "uvicorn", "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
    ])


threading.Thread(target=start_fastapi, daemon=True).start()
time.sleep(3)


def call_predict_category(title, description):
    try:
        response = httpx.post(
            "http://127.0.0.1:8000/predict/category",
            json={"title": title, "description": description},
            timeout=10.0,
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


with gr.Blocks(title="Campus Helpdesk AI") as demo:
    gr.Markdown("# Campus Helpdesk AI Service")
    gr.Markdown(
        "This Space runs the FastAPI backend internally. "
        "Use the API directly at `/predict/category`, `/predict/priority`, "
        "`/predict/sla-risk`, `/predict/duplicate` (see `/docs` for the full "
        "OpenAPI spec once the Space is running)."
    )

    with gr.Row():
        title_input = gr.Textbox(label="Ticket Title")
        description_input = gr.Textbox(label="Ticket Description")

    output = gr.JSON(label="Prediction")
    submit_btn = gr.Button("Predict Category")

    submit_btn.click(
        fn=call_predict_category,
        inputs=[title_input, description_input],
        outputs=output,
    )


demo.launch(server_name="0.0.0.0", server_port=7860)