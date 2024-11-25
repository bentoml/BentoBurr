from pathlib import Path

import bentoml
from burr.integrations.opentelemetry import init_instruments

from application import build_application

init_instruments("openai")


@bentoml.service(
    workers=1,
    resources={"cpu": "2000m"},
    traffic={"concurrency": 16, "external_queue": True}
)
class EmailAssistantService:
    def __init__(self, project_name: str = "email-assistant-bentoml", app_id: str = None):
        self.application = build_application(project_name=project_name, app_id=app_id)

    @bentoml.task
    async def run(self, pdf_file_path: Path, query: str) -> str:
        action_name, results, state = await self.application.arun(
            halt_after=["generate_email"],
            inputs={"pdf_file_path": pdf_file_path, "query": query}
        )
        return state["llm_reply"]
        