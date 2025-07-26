from fastapi import FastAPI, BackgroundTasks
from observability.traces.trace import instrument, tracer
from observability.logs.log import logger
from opentelemetry import context
from opentelemetry.propagate import inject
# import requests

app = FastAPI()

@app.get("/ping")
@instrument
def ping():
    logger.info("Ping endpoint called!")
    return {"result": "pong"}

@app.get("/complex")
@instrument
def complex_op():
    logger.info("complex op started")
    with tracer.start_as_current_span("db_query"):
        logger.info("performing DB query in child span")
        # some db action query
    with tracer.start_as_current_span("external_api_call"):
        logger.info("making external API request")
        headers = {}
        inject(headers)
        # make downstream hTTP call (would carry trace context)
        # requests.get("http://external-service/endpoint", headers=headers)
    logger.info("Complex op completed")
    return {"result": "complex done"}

@app.get("/heavy")
@instrument
def heavy(background_tasks: BackgroundTasks):
    current_ctx = context.get_current()
    background_tasks.add_task(background_task, current_ctx)
    return {"result": "scheduled"}

def background_task(ctx):
    token = context.attach(ctx)
    with tracer.start_as_current_span("background_processing"):
        logger.info("Heavy background work being traced")
        # do some stuff here like agents calling and wait
        import time
        time.sleep(10)
    context.detach(token)
