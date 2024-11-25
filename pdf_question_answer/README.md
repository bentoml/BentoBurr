# PDF Question and Answer with Burr and BentoML

Deploy with BentoML a Burr `Application` that takes in a PDF + a query and returns an LLM-generated answer

## Overview

Burr and BentoML help you build the application and the serving layer of your system. 

- **Application**: Burr lets you define your application as a graph. It supports synchronous, asynchronous, and streaming operations. Persistence and telemetry features are built-in to meet your production requirements.
- **Serving**: BentoML is a specialized tool to package and deploy AI services. It automatically generate synchronous and asynchronous client APIs. BentoML makes it easy to specify resource requirements (CPU, GPU, RAM, concurrency, workers, etc.) and manage deployed models. 

## Getting Started

Download the example directory

```sh
git clone https://github.com/bentoml/BentoBurr.git
cd BentoBurr/
``` 

### Run locally

Install dependencies

```sh
pip install -r requirements.txt
```

Serve the application (replace `$YOUR_KEY` with your OpenAI API key)

```sh
OPENAI_API_KEY=$YOUR_KEY bentoml serve .
```

#### Synchronous API

Generate a client and call the `.run()` method, which corresponds to the one defined in `PDFQAService` in `service.py`

```python
import bentoml

client = bentoml.SyncHTTPClient("http://localhost:3000")
response = client.run(
    pdf_file_path=...,  # the PDF file path on your machine
    instructions=...,  # your query 
)
```

#### Asynchronous API

Generate a client and call the `.run.submit()` method. This will start an async task.

```python
import bentoml

client = bentoml.SyncHTTPClient("http://localhost:3000")
task = client.run.submit(
    pdf_file_path=...,  # the PDF file path on your machine
    instructions=...,  # your query 
)
```

Then, you can query the status of the task until it's equal to `"success"`

```python
# wait until task is completed; check status every 5 second
while task.get_status().value == "in_progress":
    print("Waiting for task to complete...")
    time.sleep(5)

# handle completed task
if task.get_status().value == "success":
    print("Result: ", task.get())
else:
    print("Task failed")
```

#### Inspect results

Launch the Burr UI locally to view the tracked execution. Then, navigate to http://localhost:7423 (default)

```sh
burr
```

From a notebook or Google Colab environment, you can do

```python
%load_ext burr.integrations.notebook

%burr_ui
```

## Remote deployment

You can deploy yourself or use BentoCloud. To track and persist your Burr application, you will need to setup a destination. See [this guide](https://github.com/DAGWorks-Inc/burr/tree/main/burr/tracking/server/s3) for an S3-backed Burr server.

