import bentoml

from application import build_application


@bentoml.service(
    workers=2,
    resources={"cpu": "2000m"},
    traffic={"concurrency": 16, "external_queue": True}
)
class WebPageQAService:
    def __init__(self):
        # a new `app_id` will be assigned each time the service is deployed
        # on a worker node
        self.application = build_application(project_name="webpage-qa-bentoml")
        
    @bentoml.task
    def run(self, web_page_url: str, query: str) -> str:
        action_name, results, state = self.application.run(
            halt_after=["answer_question"],
            inputs={"web_page_url": web_page_url, "query": query}
        )
        return state["llm_reply"]