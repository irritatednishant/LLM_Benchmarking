# PROJECT SYNOPSIS

## SLM Benchmark
### A Local Small Language Model Performance & Reliability Analysis Web Platform

---

### 1. Project Definition and Introduction

With the rapid emergence and adoption of open-source Small Language Models (SLMs) such as Llama 3.2, Mistral, and Phi-4 Mini, developers and organizations increasingly seek to run AI models locally for strict data privacy, zero API costs, and offline availability. However, selecting the optimal model for production systems is challenging because empirical trade-offs between execution speed, memory footprint, and generation reliability are often undocumented across consumer hardware setups. Furthermore, downstream applications—such as automated customer ticket routing, data extraction, and internal microservices—demand strict adherence to structured outputs (e.g., valid JSON schemas), which lightweight models can frequently fail to generate accurately without a unified evaluation interface.

**SLM Benchmark** is a proposed full-stack web application and diagnostic framework designed to evaluate, profile, and compare local small language models executed via Ollama through an intuitive, interactive web interface. Built with a React.js single-page application and a high-performance Python FastAPI backend, the platform enables users to configure benchmark test suites, execute prompts across multiple model architectures, and monitor inference metrics in real time. By establishing an automated, data-driven testing pipeline, the project bridges the gap between raw parameter counts and real-world deployment viability, helping developers select the ideal model for resource-constrained environments.

---

### 2. What the System Will Do

The web application provides an interactive control dashboard where users can select candidate models, choose from standardized prompt suites, or craft custom test inputs. The FastAPI backend orchestrates asynchronous inference runs with the local Ollama runtime, continuously streaming live telemetry—including end-to-end latency, tokens generated per second, prompt evaluation velocity, and active RAM consumption—directly to the React frontend. For structured tasks, the system passes domain-specific prompts and utilizes Pydantic validation to inspect JSON syntax and field integrity, computing empirical schema compliance rates visualized through dynamic charts.

For example, a user can navigate to the benchmark dashboard, select models like Llama 3.2 3B, Mistral 7B, and Phi-4 Mini, and trigger a customer support ticket evaluation suite. The backend dispatches requests, measures hardware resource allocation, parses model outputs against target Pydantic contracts, and persists metrics to SQLite and dual CSV/JSON datastores. The React interface dynamically renders real-time latency gauges, token velocity bar charts, and JSON validation success rates side-by-side, allowing users to visually inspect generation quality and export comprehensive comparative reports for architectural decision-making.

---

### Language :

- **Frontend:** React.js, HTML5, CSS3 and JavaScript (with Chart.js for data visualization)
- **Backend:** Python with the FastAPI framework, Ollama API, and Pydantic
- **Database:** SQLite (with structured CSV and JSON logging datastores)
- **Core functionality:** Interactive web dashboard, multi-model benchmarking, latency & throughput profiling, and JSON schema validation

---

### Conclusion

SLM Benchmark aims to make local AI adoption practical, transparent, and dependable by providing an accessible, full-stack web platform for evaluating small language models before production deployment. By integrating a responsive React.js frontend, an asynchronous FastAPI backend, live hardware telemetry, and Pydantic schema validation, the project represents a comprehensive application of modern web development, API engineering, and AI performance evaluation. Its focus on speed, memory economy, and output validity empowers developers to make informed architectural choices while ensuring complete data privacy in a local, offline environment.

---

<br style="page-break-before: always;" />

### Student Details

- **Student Name:** Nishant
- **Enrollment Number:** 10517704426
- **Course:** Master of Computer Applications (MCA 1-B)
- **Project Mentor:** Dr. Cosmena
