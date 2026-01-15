import random
import re
import os
from openai import OpenAI  # Change to anthropic if preferred

# === CONFIG ===
API_KEY = os.getenv("OPENAI_API_KEY")  # or ANTHROPIC_API_KEY, etc.
MODEL = "gpt-4o-mini"  # cheap/fast; or "claude-3-5-sonnet-20241022", "grok-beta"
PROMPT_TEMPLATE = """
You are an expert résumé writer specializing in concise, highly quantifiable, impact-focused bullet points that recruiters love.

Transform the user's raw daily work answer into 2-3 professional résumé bullet points.

Strict Rules:
- ALWAYS start with a strong action verb (e.g., Streamlined, Developed, Optimized, Automated, Standardized, Implemented, Created, Reduced)
- ALWAYS include plausible, conservative quantification — invent realistic estimates if none provided (e.g., time saved: 2–5 hours/week; efficiency gain: 30–50%; impacted: 5–15 team members/users)
- Emphasize measurable business impact (time/money saved, productivity increased, errors reduced, better decisions enabled, revenue/user growth)
- Include relevant context (what/who/where)
- Keep each bullet 1 line (15–35 words max)
- ATS-friendly: plain text, no fancy formatting
- Sound senior, results-oriented, and proactive

Original question: {question}
User's raw answer: {answer}

Output only the 2-3 bullet points, numbered, nothing else.
"""

# === Load questions from markdown ===
def load_questions(file_path="question_bank.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    categories = {}
    current_cat = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("## "):
            current_cat = line[3:].strip()
            categories[current_cat] = []
        elif line.startswith("- ") and current_cat:
            question = line[2:].strip()
            if question:
                categories[current_cat].append(question)
    return categories

# === Pick random question ===
def get_random_question(categories):
    if not categories:
        return None, None
    cat = random.choice(list(categories.keys()))
    question = random.choice(categories[cat])
    return cat, question

# === Call LLM ===
def refine_answer(question, raw_answer):
    client = OpenAI(api_key=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)  # For Grok: OpenAI(base_url="https://api.x.ai/v1", api_key=...)
    # For Anthropic: use anthropic.Anthropic() + different format

    filled_prompt = PROMPT_TEMPLATE.format(question=question, answer=raw_answer)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": filled_prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# === Main CLI loop ===
if __name__ == "__main__":
    print("Welcome to CareerGrowthCV Daily Reflection! 🚀\n")

    categories = load_questions()
    if not categories:
        print("No questions found in question_bank.md!")
        exit(1)

    cat, question = get_random_question(categories)
    print(f"Today's category: {cat}")
    print(f"Question: {question}\n")

    raw_answer = input("Your answer (1-3 min reflection): ").strip()
    if not raw_answer:
        print("No answer provided. Exiting.")
        exit(0)

    print("\nRefining your achievement... (calling LLM)\n")
    try:
        bullets = refine_answer(question, raw_answer)
        print("Generated Résumé Bullets:\n")
        print(bullets)
    except Exception as e:
        print(f"Error calling LLM: {e}")
        print("Check your API key and internet connection.")
