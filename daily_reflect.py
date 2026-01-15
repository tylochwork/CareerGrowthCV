import os
import random
from openai import OpenAI

# ================= CONFIG =================
MODEL = "gpt-4o-mini"
# client will use OPENAI_API_KEY from environment automatically

PROMPT_TEMPLATE = """You are an expert résumé writer..."""  # your original prompt is fine

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_questions():
    path = os.path.join(SCRIPT_DIR, "question_bank.md")
    # ... your parsing logic or better yaml version ...
    # return categories dict

def get_random_question(categories):
    if not categories:
        return None, None
    cat = random.choice(list(categories.keys()))
    q = random.choice(categories[cat])
    return cat, q

def refine_answer(question, raw_answer):
    client = OpenAI()  # ← safe, uses env variable
    
    prompt = PROMPT_TEMPLATE.format(question=question, answer=raw_answer)
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300,
            temperature=0.45,           # ← more conservative
        )
        text = response.choices[0].message.content.strip()
        # Optional: clean up common LLM artifacts
        text = text.removeprefix("Here are").removeprefix("**").strip()
        return text
    except Exception as e:
        print(f"LLM API error: {e}")
        return None

def main():
    print("Welcome to CareerGrowthCV Daily Reflection! 🚀\n")
    
    categories = load_questions()
    if not categories:
        print("No questions loaded. Check question_bank.md")
        return

    cat, question = get_random_question(categories)
    print(f"Category: {cat}")
    print(f"Question: {question}\n")

    answer = input("Your reflection (1-3 min): ").strip()
    if len(answer) < 10:
        print("Answer too short. Try again tomorrow :)")
        return

    print("\nGenerating résumé bullets...\n")
    result = refine_answer(question, answer)
    
    if result:
        print("Suggested résumé bullets:\n")
        print(result)
    else:
        print("Failed to generate bullets :(")

if __name__ == "__main__":
    main()
