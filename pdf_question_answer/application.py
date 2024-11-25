import openai
from burr.core import action, ApplicationBuilder, Application, State
from pypdf import PdfReader


@action(reads=[], writes=["pdf_text"])
def process_pdf(state: State, pdf_file_path: str) -> State:
    """Extract text from a PDF and return it as a string."""
    reader = PdfReader(pdf_file_path)
    text = " ".join([page.extract_text() for page in reader.pages])
    return state.update(pdf_text=text)


@action(reads=["pdf_text"], writes=["llm_reply"])
def generate_email(state: State, query: str) -> State:
    """Generate answer based on the PDF's text using an LLM following the query"""
    text = state["pdf_text"]
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": query},
            {"role": "user", "content": text},
        ],
    )
    return state.update(llm_reply=response.choices[0].message.content)


def build_application(project_name: str, app_id: str) -> Application:
    return (
        ApplicationBuilder()
        .with_actions(process_pdf, generate_email)
        .with_transitions(("process_pdf", "generate_email"))
        .with_entrypoint("process_pdf")
        .with_identifiers(app_id=app_id)
        .with_tracker(project=project_name, use_otel_tracing=True)
        .build()
    )


if __name__ == "__main__":
    from burr.integrations.opentelemetry import init_instruments

    init_instruments("openai")

    app = build_application("pdf-qa-bentoml", app_id="test-app")
    app.visualize("application.png", include_state=True)

    _, _, state = app.run(
        halt_after=["generate_email"],
        inputs={"pdf_file_path": "/home/tjean/downloads/2210.13393v1.pdf", "query": "what's the title?"}
    )
    print(state["llm_reply"])