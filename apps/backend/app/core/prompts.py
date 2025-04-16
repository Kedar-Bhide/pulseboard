def generate_and_log_question():
    from app.core.gpt import ask_openai
    prompt = (
        "Generate one thought-provoking check-in question for a startup team "
        "related to product, growth, or team alignment."
    )
    question = ask_openai(prompt)
    print(f"Daily Question: {question}")