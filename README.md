# Local Offline AI Assistant — Model Comparison Benchmark

Compares small local LLMs (via Ollama) on speed, memory usage, and structured-output
reliability, across a standardized set of prompts spanning multiple task types.

## Project Structure

```
local-llm-benchmark/
├── config.py            # models list + file paths — edit this to add/remove models
├── schemas.py            # Pydantic schema(s) for structured output validation
├── model_runner.py        # run_model, memory tracking, structured/general prompt handling
├── prompts.py              # standardized 30+ prompt test set (structured + general)
├── storage.py               # save_to_csv / save_to_json
├── benchmark.py              # MAIN SCRIPT — runs all models x all prompts
├── temperature_test.py       # runs temperature=0 vs 0.7 variance test
├── analyze.py                  # aggregates results.csv into comparison tables
├── requirements.txt
├── results/                    # output data (created automatically)
│   ├── results.csv
│   ├── results.json
│   ├── temperature_results.csv
│   └── temperature_results.json
└── notebooks/                  # optional: exploratory analysis / report drafting
```

## Setup

```bash
pip install -r requirements.txt
```

Make sure Ollama is installed and the models listed in `config.py` are pulled:

```bash
ollama pull llama3.2:3b
ollama pull phi4-mini
ollama pull mistral:7b
```

## How to Run (in order)

1. **Main benchmark** (Phase 1 + 2 — speed, memory, structured output validity)
   ```bash
   python benchmark.py
   ```

2. **Temperature variance test** (Phase 2, step 6)
   ```bash
   python temperature_test.py
   ```

3. **Analyze results**
   ```bash
   python analyze.py
   ```

4. **(Optional, stretch goal)** Pull quantized versions (e.g. `mistral:7b-instruct-q4_0`),
   add them to `config.py` under a separate list, and rerun `benchmark.py` against them
   to compare quality-vs-speed trade-offs.

## Notes

- `results.csv` excludes the full `response` text and `prompt` text to stay readable —
  the complete text for every run is preserved in `results.json`.
- Each prompt has a stable `id` (see `prompts.py`) so you can join/compare the same
  prompt across different models during analysis.
- `prompt_type` is `"structured"` for ticket-style prompts (routed through JSON schema
  validation + one retry) and `"general"` for everything else (Q&A, reasoning,
  summarization, creative, edge cases — run directly, judged manually for quality).
