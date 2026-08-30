# LLM Benchmarking: Local Small Language Model Performance & Reliability Analysis

A comprehensive benchmarking framework for evaluating small language models (SLMs) running locally via **Ollama**. This project measures performance metrics, memory usage, and structured output reliability across multiple models and task types.

---

## 🎯 What We're Building

This project runs a suite of **standardized test prompts** against multiple small language models and collects:

- **Performance Metrics**: latency, generation time, tokens-per-second
- **Memory Usage**: actual RAM consumed by each model
- **Structured Output Reliability**: how well models handle JSON schema validation tasks
- **General Task Quality**: reasoning, Q&A, summarization across varied prompts

The goal: **identify which SLM offers the best balance of speed, accuracy, and resource efficiency** for real-world applications.

---

## 🤔 Why We Built This

### The Problem
- **Too many SLM options**: llama3.2, mistral, gemma, phi — which one to use?
- **No standardized comparison**: Different sources test models differently
- **Trade-offs are unclear**: Does a faster model sacrifice quality? How much memory does it actually need?
- **Structured output matters**: For real applications (ticket routing, JSON APIs), can the model reliably output valid JSON?

### The Solution
A **repeatable, data-driven benchmark** that:
1. Tests **multiple models** against the same prompts under identical conditions
2. Captures both **quantitative metrics** (speed, memory) and **qualitative validation** (JSON correctness)
3. Produces **CSV + JSON reports** for further analysis
4. Enables side-by-side comparison of performance vs. resource usage

---

## 🏗️ Architecture & How It Works

### Project Structure

```
LLM_Benchmarking/
├── notebooks/
│   └── main.ipynb                 # Exploratory analysis & iterative testing
├── pyproject.toml                 # Project metadata & dependencies
├── schemas.py                     # Pydantic models for structured output validation
└── (future files as you develop)
    ├── config.py                  # Model list & output paths
    ├── model_runner.py            # Core: run_model() function + memory tracking
    ├── prompts.py                 # Standardized prompt test suite
    ├── benchmark.py               # MAIN: orchestrates full benchmark run
    ├── storage.py                 # CSV/JSON saving utilities
    ├── analyze.py                 # Aggregates & visualizes results
    └── results/                   # Auto-generated output directory
        ├── results.csv            # All runs (metrics only, no text)
        ├── results.json           # Full results (includes responses)
        ├── temperature_results.csv
        └── temperature_results.json
```

### Core Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. Define Models & Prompts (config.py, prompts.py)     │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 2. For Each (Model, Prompt) Pair:                       │
│    a. Send prompt to Ollama                            │
│    b. Measure latency & generation time                │
│    c. Extract tokens & memory usage                    │
│    d. For structured tasks: validate JSON schema       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Collect Results:                                     │
│    • CSV: metrics only (compact, easy to analyze)      │
│    • JSON: full responses (preserves everything)       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Analyze & Compare:                                   │
│    • Calculate avg tokens/sec per model                │
│    • Track JSON validation success rate                │
│    • Identify speed vs. quality trade-offs             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Key Components Explained

### 1. **Schemas** (`schemas.py`)
Defines the **structure we expect** from models on JSON tasks.

```python
class TicketAnalysisSchema(BaseModel):
    category: Literal["billing", "technical", "account", "other"]
    priority: Literal["low", "medium", "high"]
    summary: str
    requires_escalation: bool
```

**Why?** For real applications, we can't accept free-form text — we need valid, predictable JSON. This schema validates if a model's output can be parsed and used programmatically.

### 2. **Model Runner** (`model_runner.py`)
The heart of the benchmark. For each prompt, it:

```python
def run_model(model_name, prompt):
    start_time = time.perf_counter()
    
    # 1. Send to Ollama
    response = chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    
    end_time = time.perf_counter()
    latency = end_time - start_time
    
    # 2. Extract metrics from response
    generation_time = response.eval_duration / 1_000_000_000  # nanoseconds → seconds
    tokens_per_second = response.eval_count / generation_time
    
    # 3. Capture memory usage
    memory_mb = get_model_memory_mb(model_name)  # via `ollama ps`
    
    return {
        "response": response.message.content,
        "latency": latency,
        "generation_time": generation_time,
        "tokens_per_second": tokens_per_second,
        "output_tokens": response.eval_count,
        "prompt_tokens": response.prompt_eval_count,
        "prompt_tokens_per_second": prompt_eval_rate,
        "memory_mb": memory_mb,
    }
```

**Key metrics captured:**
- **Latency**: End-to-end time (includes model load time, inference)
- **Generation Time**: Pure inference time (excludes I/O overhead)
- **Tokens/Second**: Model throughput (higher = faster)
- **Memory**: Actual RAM in use (important for resource-constrained environments)

### 3. **Structured vs. General Prompts**

**Structured Prompts** (e.g., ticket analysis):
- Input: A customer complaint
- Expected output: Valid JSON matching `TicketAnalysisSchema`
- Handling: If JSON is invalid, retry up to 5 times with feedback

```python
def get_structured_response(model_name, user_text, max_retries=5):
    prompt = build_structured_prompt(user_text)  # Instruct model to output JSON
    
    for attempt in range(max_retries):
        result = run_model(model_name, prompt)
        try:
            parsed = TicketAnalysisSchema.model_validate_json(result["response"])
            result["valid_json"] = True
            result["parsed"] = parsed.model_dump()
            return result
        except (ValidationError, JSONDecodeError):
            if attempt < max_retries:
                # Reprompt with feedback
                prompt += "\n\nYour previous response was invalid. Please fix and respond with valid JSON only."
            else:
                result["valid_json"] = False
    return result
```

**General Prompts** (Q&A, reasoning, creative):
- Input: "What is machine learning?"
- Expected output: Free-form text (judged manually)
- Handling: No validation, just measure speed & quality

### 4. **Storage** (`storage.py`)
Saves results in two formats:

```python
def save_to_csv(result, filepath="results.csv"):
    # Excludes "response" & "prompt" to keep file readable
    filtered_result = {k: v for k, v in result.items() 
                      if k not in ("response", "prompt")}
    # Append to CSV row-by-row (safer if interrupted)
    
def save_to_json(results_list, filepath="results.json"):
    # Preserves everything: full responses, all metrics
    json.dump(results_list, f, indent=2)
```

**Why two formats?**
- **CSV**: Easy to load into pandas, Excel, or visualization tools; compact
- **JSON**: Complete record; allows joining response text back to metrics later

---

## 📊 Example Workflow from `main.ipynb`

The notebook demonstrates the full pipeline:

### Step 1: Define Models & Prompts
```python
models = [
    "llama3.2:3b",
    "mistral:7b",
    "gemma3:4b"
]

prompts = [
    {"text": "My internet has been down for 3 days...", "type": "structured"},
    {"text": "What is the capital of Australia?", "type": "general"},
]
```

### Step 2: Run Benchmark
```python
for model in models:
    for prompt in prompts:
        if prompt["type"] == "structured":
            response = structured_prompt(model, prompt["text"])
        else:
            response = general_prompt(model, prompt["text"])
        
        # Save to both CSV and JSON
        save_to_csv(response)
        all_results.append(response)

save_to_json(all_results)
```

### Step 3: Collect Sample Output
For a structured prompt on `mistral:7b`:
```json
{
    "response": "{\"category\": \"technical\", \"priority\": \"high\", ...}",
    "latency": 2.513,
    "generation_time": 2.393,
    "tokens_per_second": 22.15,
    "output_tokens": 53,
    "prompt_tokens": 127,
    "prompt_tokens_per_second": 1895.1,
    "memory_mb": 5017.6,
    "valid_json": true,
    "parsed": {
        "category": "technical",
        "priority": "high",
        "summary": "Internet down for 3 days, no response from support via email.",
        "requires_escalation": true
    }
}
```

### Step 4: Analyze Results
```python
import pandas as pd
df = pd.read_csv("results.csv")
# Group by model, calculate mean tokens/sec, JSON success rate, memory usage
# Identify fastest, most reliable, most efficient models
```

---

## 📈 Metrics Explained

| Metric | Unit | What It Means | Why It Matters |
|--------|------|---------------|----------------|
| **Latency** | seconds | Total time from request to response | User-facing: how fast does the app feel? |
| **Generation Time** | seconds | Pure inference (excludes I/O) | Model speed independent of system overhead |
| **Tokens/Second** | tokens/sec | Throughput | Throughput for batch processing; cost of inference |
| **Output Tokens** | count | Number of tokens generated | Affects latency & cost; longer = more compute |
| **Prompt Tokens** | count | Input size (after tokenization) | Longer prompts = more latency |
| **Prompt Tokens/Second** | tokens/sec | Speed of reading input | Affects latency for long prompts |
| **Memory** | MB | RAM consumed by model in VRAM | Resource constraint: fits on your hardware? |
| **Valid JSON** | bool | Did structured output pass validation? | Reliability for real applications |

---

## 🚀 How to Use

### 1. **Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt  # or: pip install ollama>=0.6.2 openai>=2.45.0 requests>=2.34.2

# Install Ollama (if not already installed)
# Visit https://ollama.com and download
```

### 2. **Pull Models**
```bash
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull gemma3:4b
```

### 3. **Run the Notebook** (interactive exploration)
```bash
jupyter notebook notebooks/main.ipynb
```
- Modify models/prompts in the notebook
- Run cells one at a time to explore
- Output saved to `results.csv` and `results.json`

### 4. **Run Full Benchmark** (once structure is finalized)
```bash
python benchmark.py
```

### 5. **Analyze Results**
```bash
python analyze.py
# Generates comparison tables, visualizations, summary statistics
```

---

## 🎓 What Each Model Tells Us

**llama3.2:3b**
- Smaller, faster, lower memory
- Good for quick responses; may sacrifice nuance

**mistral:7b**
- Larger, more capable
- Better at complex reasoning, structured output
- Higher memory footprint

**gemma3:4b** (or other models you test)
- Position on the spectrum: speed vs. quality

---

## 💡 Key Insights We're Looking For

After running the benchmark, answers we expect:

1. **"Which model is fastest?"** → Lowest `generation_time`, highest `tokens_per_second`
2. **"Which model is most reliable for JSON?"** → Highest `valid_json` success rate
3. **"Which model uses least memory?"** → Lowest `memory_mb`
4. **"Is there a clear winner?"** → Or must we trade off speed vs. quality?
5. **"How does temperature affect output?"** → Temperature variance test (future phase)

---

## 🛠️ Development Roadmap

✅ **Phase 1: Current**
- Core model runner with latency & memory tracking
- Structured output validation (JSON schema)
- CSV/JSON export
- Exploratory notebook

🚧 **Phase 2: Next**
- `benchmark.py`: Automated full-suite runner
- `analyze.py`: Aggregated reports & visualizations
- Temperature variance test (`temperature_test.py`)
- Quantized model comparison

📋 **Phase 3: Future**
- Fine-tuned model comparison
- Cost analysis (inference cost per 1M tokens)
- Multi-turn conversation tracking
- Web dashboard for results

---

## 📝 File-by-File Breakdown

### `main.ipynb`
**Purpose**: Exploratory, iterative testing. This is where ideas are tested before being moved to production scripts.

**Contains**:
- Helper functions for structured/general prompts
- Example runs demonstrating the full workflow
- Data analysis using pandas & matplotlib
- Comments showing experimental thinking

**Key functions**:
- `run_model(model_name, prompt)`: Core benchmark runner
- `get_structured_response(...)`: JSON validation with retries
- `general_prompt(...)`, `structured_prompt(...)`: Task routers

### `schemas.py`
**Purpose**: Define expected output structure for structured tasks.

**Contains**:
- `TicketAnalysisSchema`: Validates ticket classification output

**Extensibility**: Add new schemas here as you test new structured tasks (e.g., `SentimentAnalysisSchema`, `EntityExtractionSchema`).

### `pyproject.toml`
**Purpose**: Project metadata & dependency management.

**Key dependencies**:
- `ollama`: Python client for Ollama
- `openai`: Needed for compatibility (OpenAI-compatible API calls via Ollama)
- `requests`: HTTP library for API calls

---

## 🎯 How to Extend This Project

### Add a New Model
1. Pull the model: `ollama pull model_name`
2. Add to `config.py` model list
3. Rerun `benchmark.py`

### Add a New Structured Task
1. Define a new Pydantic schema in `schemas.py`
2. Create a `build_structured_prompt_for_task()` function
3. Extend `get_structured_response()` to route to the new task
4. Add test prompts to `prompts.py`

### Add a New Metric
1. Extract from the Ollama response object
2. Add to the returned dictionary in `run_model()`
3. Update CSV headers in `storage.py`
4. Update analysis logic in `analyze.py`

---

## 📚 Dependencies & Why

- **ollama** (0.6.2+): Native Python client for Ollama; queries local models
- **openai** (2.45.0+): OpenAI-compatible API; Ollama supports this interface
- **requests** (2.34.2+): HTTP library for API calls & system commands
- **pydantic** (included in project): Runtime JSON schema validation
- **pandas** (for analysis): Data wrangling & aggregation

---

## 📖 Notes

- **Results location**: `results/` directory (auto-created)
- **CSV vs JSON trade-off**: CSV is lightweight; JSON preserves full responses
- **Reproducibility**: Same models + same prompts = same results (determinism depends on model, temperature setting)
- **Prompt IDs**: Each prompt has a stable ID for tracking across runs
- **Memory tracking**: Via `ollama ps` system call; most reliable on Linux/macOS

---

## 🤝 Contributing

To extend this benchmark:
1. Add new schemas to `schemas.py`
2. Add new test prompts to `prompts.py` (with unique IDs)
3. Test in the notebook first
4. Move to production scripts once stable
5. Update `README.md` with findings

---

## 📄 License

[Add your license here if needed]

---

## 🙋 Questions?

For issues, refer to:
- **Ollama setup**: https://ollama.com
- **Pydantic schemas**: https://docs.pydantic.dev
- **Performance bottlenecks**: Check `results.json` for full response times

Happy benchmarking! 🚀
