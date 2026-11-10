# LOCAL SMALL LANGUAGE MODEL (SLM) BENCHMARK REPORT
## Empirical Performance, Schema Compliance & Reliability Analysis

**Generated On:** 2026-11-10 11:41:07  
**Host Hardware:** Darwin (arm64) | Total RAM: 16.0 GB | CPU Threads: 10  
**Runtime Engine:** Ollama Local Daemon (Active)  
**Total Benchmark Runs:** 351 evaluations across 3 models

---

### 1. Executive Summary & Diagnostic Verdict

For enterprise customer-support automation with strict JSON schemas, **llama3.2:3b** is recommended as the primary candidate, achieving an overall benchmark score of 100.0/100 with 100.0% schema compliance. If throughput is paramount, **llama3.2:3b** delivers peak inference velocity (45.93 tokens/s). For strictly resource-constrained edge devices (e.g., 8GB SBCs), **llama3.2:3b** is the most viable tier (2628.3 MB RAM footprint).

---

### 2. Comprehensive Model Performance Leaderboard

| Rank | Model | Composite Score | Generation Speed | P95 Latency | Memory Footprint | JSON Schema Pass | Deployment Tier |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 🥇 | **llama3.2:3b** | **100.0 / 100** | 45.93 tok/s | 9.61s | 2628.3 MB | 100.0% | Edge SBC (Pi 5 / 8GB RAM) |
| 🥈 | **phi4-mini** | **78.1 / 100** | 32.36 tok/s | 10.46s | 3174.4 MB | 100.0% | Laptop / 16GB Unified RAM |
| 🥉 | **mistral:7b** | **30.0 / 100** | 16.83 tok/s | 20.76s | 5085.9 MB | 100.0% | Laptop / 16GB Unified RAM |

---

### 3. Detailed Inference Latency & Throughput Distribution

| Model | Min Latency | Median (P50) | P95 Latency | Max Latency | Prompt Eval Speed | Tokens / GB RAM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **llama3.2:3b** | 0.23s | 1.4s | 9.61s | 14.22s | 578.2 tok/s | **17.9 tok/s/GB** |
| **phi4-mini** | 0.3s | 1.58s | 10.46s | 18.54s | 301.5 tok/s | **10.44 tok/s/GB** |
| **mistral:7b** | 0.58s | 4.78s | 20.76s | 33.69s | 112.8 tok/s | **3.39 tok/s/GB** |

---

### 4. Structured JSON Output & Schema Validation Telemetry

Models were evaluated against the production customer ticket Pydantic contract (`TicketAnalysisSchema`):
```json
{
  "category": "billing | technical | account | other",
  "priority": "low | medium | high",
  "summary": "<one sentence>",
  "requires_escalation": true | false
}
```

| Model | Structured Prompts | Valid Schema Outputs | Schema Compliance Rate | Status |
| :--- | :---: | :---: | :---: | :--- |
| **llama3.2:3b** | 24 | 24 | **100.0%** | ✅ Production Ready |
| **phi4-mini** | 24 | 24 | **100.0%** | ✅ Production Ready |
| **mistral:7b** | 24 | 24 | **100.0%** | ✅ Production Ready |

---

### 5. Temperature Variance & Output Stability Analysis

| Model | Temperature | Sample Runs | Mean Output Tokens | Token Std Dev (Variance) | Generation Behavior |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **llama3.2:3b** | 0.0 | 24 | 174.3 tok | ±146.75 | Deterministic (Minimal token divergence) |
| **llama3.2:3b** | 0.7 | 24 | 205.0 tok | ±182.19 | Balanced Exploration (Controlled variation) |
| **mistral:7b** | 0.0 | 24 | 202.5 tok | ±113.56 | Deterministic (Minimal token divergence) |
| **mistral:7b** | 0.7 | 24 | 215.6 tok | ±120.24 | Balanced Exploration (Controlled variation) |
| **phi4-mini** | 0.0 | 24 | 169.2 tok | ±142.38 | Deterministic (Minimal token divergence) |
| **phi4-mini** | 0.7 | 24 | 166.0 tok | ±156.18 | Balanced Exploration (Controlled variation) |

---

### 6. Edge Hardware & Resource Feasibility Guidelines

- **Raspberry Pi 5 / 8GB SBC:** Models under 3 GB RAM footprint (e.g. `llama3.2:3b`, `phi4-mini`) leave sufficient headroom for operating system and network buffers.
- **Consumer Laptop (16GB Unified RAM):** All tested models run without swapping, though models > 4.5 GB RAM footprint (e.g. `mistral:7b`) impact concurrent application responsiveness.
- **Throughput Efficiency Factor:** Calculated as `Tokens Generated per Second / GB VRAM`. Higher values signify superior memory economy for local deployments.

```
Report compiled automatically by SLM Benchmark Application Diagnostics Engine.
```