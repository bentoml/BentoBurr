# Burr Serving with BentoML

This repository shows how to deploy Burr `Application` with BentoML.


## Overview

[Burr](https://github.com/dagworks-inc/burr) and [BentoML](https://github.com/bentoml/BentoML) help you build the **application** and **serving** layers of your system. 

### Application layer

Burr creates easy to understand and debug applications with a clear path to production. It supports [synchronous, asynchronous](https://burr.dagworks.io/concepts/state-machine/), and [streaming](https://burr.dagworks.io/concepts/streaming-actions/) actions. [Persistence](https://burr.dagworks.io/concepts/state-persistence/), [hooks](https://burr.dagworks.io/concepts/hooks/), and [telemetry](https://burr.dagworks.io/concepts/additional-visibility/) features are built-in.

### Serving layer

BentoML is a specialized tool to [package, deploy, and manage AI services](https://docs.bentoml.com/en/latest/scale-with-bentocloud/deployment/index.html). Get the most performance from your system by specifying resource requirements (CPU, GPU, RAM, concurrency, workers, etc.), [autoscaling](https://docs.bentoml.com/en/latest/scale-with-bentocloud/scaling/autoscaling.html), and [adaptive batching](https://docs.bentoml.com/en/latest/get-started/adaptive-batching.html) for requests. It also automatically generates synchronous and asynchronous clients for your service. 

## Directory Content

- `web_page_qna/` is an introductory example to deploy with BentoML a Burr `Application` that uses LLMs to answer questions about a web page.

## Community

Join the [BentoML developer community](https://l.bentoml.com/join-slack) on Slack for more support and discussions!

Join the [Burr Discord server](https://discord.gg/6Zy2DwP4f3) for help, questions, and feature requests.