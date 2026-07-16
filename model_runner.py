"""
Core functions for calling local models via Ollama, measuring performance,
and handling both plain and JSON-structured prompts.
"""

import time
import json
import subprocess
import re
from ollama import chat
from pydantic import ValidationError

from schemas import TicketAnalysisSchema


def get_model_memory_mb(model_name):
    """Return the model's current RAM/VRAM usage in MB, via `ollama ps`."""
    result = subprocess.run(["ollama", "ps"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if model_name in line:
            match = re.search(r'(\d+\.?\d*)\s*(GB|MB)', line)
            if match:
                size, unit = match.groups()
                size = float(size)
                return size * 1024 if unit == "GB" else size
    return None


def run_model(model_name, prompt, temperature=None):
    """Call a local model via Ollama and return timing + token metrics."""
    start_time = time.perf_counter()
    options = {"temperature": temperature} if temperature is not None else {}

    response = chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        options=options,
    )
    end_time = time.perf_counter()

    latency = end_time - start_time
    generation_time = response.eval_duration / 1_000_000_000
    tokens_per_second = response.eval_count / generation_time if generation_time > 0 else 0

    prompt_eval_time = response.prompt_eval_duration / 1_000_000_000
    prompt_eval_rate = response.prompt_eval_count / prompt_eval_time if prompt_eval_time > 0 else 0

    memory_mb = get_model_memory_mb(model_name)

    return {
        "model": model_name,
        "prompt": prompt,
        "response": response.message.content,
        "latency": latency,
        "generation_time": generation_time,
        "tokens_per_second": tokens_per_second,
        "output_tokens": response.eval_count,
        "prompt_tokens": response.prompt_eval_count,
        "prompt_tokens_per_second": prompt_eval_rate,
        "memory_mb": memory_mb,
        "temperature": temperature,
    }


def build_structured_prompt(user_text):
    """Wrap raw ticket text with JSON-schema instructions."""
    return f"""Analyze the following text and respond ONLY with valid JSON in this exact format:
{{
  "category": "billing" | "technical" | "account" | "other",
  "priority": "low" | "medium" | "high",
  "summary": "<one sentence>",
  "requires_escalation": true | false
}}

Text: {user_text}

Respond with JSON only. No explanation, no markdown formatting."""


def structured_prompt(model_name, user_text, max_retries=1):
    """Run a structured (schema-validated) prompt, with one retry on invalid JSON."""
    prompt = build_structured_prompt(user_text)
    attempt = 0
    result = None

    while attempt <= max_retries:
        result = run_model(model_name, prompt)
        raw_output = result["response"]

        try:
            cleaned = raw_output.strip().strip("```json").strip("```").strip()
            parsed = TicketAnalysisSchema.model_validate_json(cleaned)
            result["prompt_type"] = "structured"
            result["valid_json"] = True
            result["parsed"] = parsed.model_dump()
            return result
        except (ValidationError, json.JSONDecodeError) as e:
            attempt += 1
            if attempt > max_retries:
                result["prompt_type"] = "structured"
                result["valid_json"] = False
                result["parsed"] = None
                result["error"] = str(e)
                return result
            prompt = prompt + f"\n\nYour previous response was invalid: {e}. Please fix and respond with valid JSON only."

    return result


def general_prompt(model_name, prompt_text):
    """Run a plain prompt (Q&A, reasoning, summarization, creative) with no schema."""
    result = run_model(model_name, prompt_text)
    result["prompt_type"] = "general"
    result["valid_json"] = None
    result["parsed"] = None
    return result
