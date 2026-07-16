"""
Standardized prompt set used to compare models across different situations.
Each prompt has a stable 'id' (for cross-model comparison later) and a 'type':
  - "structured": routed through the JSON schema + validation + retry path
  - "general":     run directly, no schema (Q&A, reasoning, summarization, creative, edge cases)
"""

PROMPTS = [
    # --- structured / ticket-style (8) ---
    {"id": "tic_01", "type": "structured", "text": "My internet has been down for 3 days and no one from support has responded to my emails."},
    {"id": "tic_02", "type": "structured", "text": "I was charged twice for my subscription this month, can someone look into this?"},
    {"id": "tic_03", "type": "structured", "text": "How do I change my billing address on my account?"},
    {"id": "tic_04", "type": "structured", "text": "The app crashes every time I try to upload a photo, this is really frustrating."},
    {"id": "tic_05", "type": "structured", "text": "I forgot my password and the reset email never arrived."},
    {"id": "tic_06", "type": "structured", "text": "Can you explain what the premium plan includes?"},
    {"id": "tic_07", "type": "structured", "text": "Our production server is down and customers cannot check out, this needs urgent attention."},
    {"id": "tic_08", "type": "structured", "text": "I'd like to close my account permanently, please confirm the process."},

    # --- factual Q&A (8) ---
    {"id": "qa_01", "type": "general", "text": "What is the capital of Australia?"},
    {"id": "qa_02", "type": "general", "text": "What is machine learning?"},
    {"id": "qa_03", "type": "general", "text": "Who wrote 'Pride and Prejudice'?"},
    {"id": "qa_04", "type": "general", "text": "What is the boiling point of water in Celsius?"},
    {"id": "qa_05", "type": "general", "text": "Explain photosynthesis in simple terms."},
    {"id": "qa_06", "type": "general", "text": "What year did World War II end?"},
    {"id": "qa_07", "type": "general", "text": "What is the difference between RAM and storage?"},
    {"id": "qa_08", "type": "general", "text": "What causes seasons on Earth?"},

    # --- reasoning / logic (6) ---
    {"id": "rs_01", "type": "general", "text": "If a train leaves at 3pm going 60mph and travels for 2.5 hours, how far does it go?"},
    {"id": "rs_02", "type": "general", "text": "A farmer has 17 sheep, all but 9 die. How many are left?"},
    {"id": "rs_03", "type": "general", "text": "If all cats are animals, and some animals are pets, can we conclude all cats are pets? Explain."},
    {"id": "rs_04", "type": "general", "text": "I have 3 apples and buy 2 more boxes of 4 apples each. How many apples do I have?"},
    {"id": "rs_05", "type": "general", "text": "What comes next in the sequence: 2, 4, 8, 16, ?"},
    {"id": "rs_06", "type": "general", "text": "Why can't you fold a piece of paper in half more than about 7-8 times?"},

    # --- summarization (6) ---
    {"id": "sm_01", "type": "general", "text": "Summarize in one sentence: The company reported strong quarterly earnings driven by growth in its cloud division, though overall revenue growth slowed compared to last year due to weaker hardware sales."},
    {"id": "sm_02", "type": "general", "text": "Summarize in one sentence: Researchers found that regular exercise improves not only physical health but also cognitive function, with participants showing better memory retention after a 6-month walking program."},
    {"id": "sm_03", "type": "general", "text": "Summarize in one sentence: The city council voted to approve a new public transit line after years of debate, citing traffic congestion and environmental concerns as key motivating factors."},
    {"id": "sm_04", "type": "general", "text": "Summarize in one sentence: The novel follows a young detective investigating a series of mysterious disappearances in a small coastal town, uncovering a decades-old secret along the way."},
    {"id": "sm_05", "type": "general", "text": "Summarize in one sentence: A new study suggests that intermittent fasting may have similar cardiovascular benefits to calorie restriction, though researchers caution more long-term data is needed."},
    {"id": "sm_06", "type": "general", "text": "Summarize in one sentence: The startup raised $20 million in Series A funding to expand its AI-powered logistics platform into new international markets."},

    # --- creative / open-ended (6) ---
    {"id": "cr_01", "type": "general", "text": "Write a short product description for a reusable water bottle."},
    {"id": "cr_02", "type": "general", "text": "Write a two-sentence bedtime story about a curious fox."},
    {"id": "cr_03", "type": "general", "text": "Write a catchy tagline for a local coffee shop."},
    {"id": "cr_04", "type": "general", "text": "Give me three name ideas for a fitness app."},
    {"id": "cr_05", "type": "general", "text": "Write a short LinkedIn post announcing a job promotion."},
    {"id": "cr_06", "type": "general", "text": "Write a one-paragraph birthday message for a close friend."},

    # --- edge cases (5) ---
    {"id": "ec_01", "type": "general", "text": "asdkj what is teh capitol of frnace"},
    {"id": "ec_02", "type": "general", "text": "?"},
    {"id": "ec_03", "type": "general", "text": "Tell me something."},
    {"id": "ec_04", "type": "general", "text": "Translate 'good morning' into French, Spanish, and Japanese."},
    {"id": "ec_05", "type": "general", "text": "List the planets in our solar system in order from the sun."},
]

# Subset used for the temperature variance test (Phase 2, step 6).
# Kept small (~6-8 prompts) since each one runs multiple times per temperature.
TEMPERATURE_TEST_PROMPTS = [p for p in PROMPTS if p["id"] in (
    "tic_01", "tic_03", "qa_02", "qa_05", "rs_01", "sm_01", "cr_01", "ec_05"
)]
