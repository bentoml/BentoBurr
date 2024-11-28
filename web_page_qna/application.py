import openai
import requests
from bs4 import BeautifulSoup
from burr.core import action, ApplicationBuilder, Application, State


# @action define actions the application can take
@action(reads=[], writes=["web_page_text"])
def load_web_page(state: State, web_page_url: str) -> State:
    """Extract text from the HTML of a web page and return it as a string."""
    response = requests.get(web_page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return state.update(web_page_text=soup.get_text())


@action(reads=["web_page_text"], writes=["llm_reply"])
def answer_question(state: State, query: str) -> State:
    """Generate answer based on the web page's content using an LLM"""
    text = state["web_page_text"]
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query + "\n\n" + text},
        ],
    )
    return state.update(llm_reply=response.choices[0].message.content)


def build_application(project_name: str, app_id: str = None) -> Application:
    """Build the Q&A application and add tracking for the Burr UI"""
    return (
        ApplicationBuilder()
        .with_actions(load_web_page, answer_question)
        .with_transitions(
            ("load_web_page", "answer_question"),
            ("answer_question", "load_web_page")
        )
        .with_entrypoint("load_web_page")
        .with_identifiers(app_id=app_id)  # if None, generate a UUID
        .with_tracker(project=project_name, use_otel_tracing=True)
        .build()
    )


if __name__ == "__main__":
    # instrument OpenAI with OpenTelemetry
    from opentelemetry.instrumentation.openai import OpenAIInstrumentor
    OpenAIInstrumentor().instrument()
    
    # build and visualize the application
    app = build_application("webpage-qa-bentoml", app_id="test-app")
    app.visualize("application.png", include_state=True)

    # run the application and inspect results
    _, _, state = app.run(
        halt_after=["answer_question"],
        inputs={
            "web_page_url": "https://docs.bentoml.com/en/latest/build-with-bentoml/services.html",
            "query": "What's BentoML main feature?"
        }
    )
    print(state["llm_reply"])
