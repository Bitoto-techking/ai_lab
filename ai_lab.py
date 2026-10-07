"""A simple private, offline chat interface for a local Ollama model."""

import ollama


MODEL = "llama3.2:3b"
SYSTEM_PROMPT = (
    "You are Ayungo Bitoto AI Lab, a helpful local AI assistant. "
    "Be honest when you are unsure and do not claim to have live internet access."
)


def chat() -> None:
    """Run a local conversation until the user chooses to exit."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("=== AYUNGO BITOTO AI LAB — OFFLINE ===")
    print(f"Local model: {MODEL}")
    print("Type a question, or use /help. Type /exit to close.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not question:
            continue
        if question.lower() in {"/exit", "/quit", "exit", "quit"}:
            print("Goodbye.")
            break
        if question.lower() == "/help":
            print("Commands: /help, /clear, /exit\n")
            continue
        if question.lower() == "/clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Conversation cleared.\n")
            continue

        messages.append({"role": "user", "content": question})
        try:
            response = ollama.chat(model=MODEL, messages=messages)
            answer = response["message"]["content"]
        except ollama.ResponseError as error:
            messages.pop()
            print(f"\nOllama could not answer: {error.error}\n")
            continue
        except Exception as error:
            messages.pop()
            print(
                "\nCould not reach your local Ollama service. Make sure Ollama is running "
                f"and the '{MODEL}' model is installed.\nDetails: {error}\n"
            )
            continue

        messages.append({"role": "assistant", "content": answer})
        print(f"\nAI: {answer}\n")


if __name__ == "__main__":
    chat()
