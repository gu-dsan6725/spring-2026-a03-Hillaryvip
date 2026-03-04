from dotenv import load_dotenv
import os

load_dotenv()

import subprocess
from groq import Groq

REPO_PATH = "../mcp-gateway-registry"


def run_bash(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout[:4000]


def classify_query(question):
    q = question.lower()

    if "dependencies" in q:
        return "dependencies"
    if "entry point" in q:
        return "entry"
    if "languages" in q or "file types" in q:
        return "structure"
    if "authentication" in q:
        return "auth"
    if "api endpoints" in q:
        return "api"
    if "oauth" in q:
        return "oauth"

    return "general"


def retrieve_context(question_type):

    if question_type == "dependencies":
        return run_bash(f"cat {REPO_PATH}/pyproject.toml")

    if question_type == "entry":
        return run_bash(f"grep -r 'FastAPI' {REPO_PATH}/registry")

    if question_type == "structure":
        return run_bash(f"tree -L 2 {REPO_PATH}")

    if question_type == "auth":
        return run_bash(f"grep -r 'auth' {REPO_PATH}/auth_server")

    if question_type == "api":
        return run_bash(f"grep -r '@router' {REPO_PATH}/registry")

    if question_type == "oauth":
        return run_bash(f"grep -r 'oauth' {REPO_PATH}")

    return run_bash(f"grep -r '{question_type}' {REPO_PATH}")


def ask_llm(question, context):

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are a software architecture assistant.

Answer the question using the repository context below.

Context:
{context}

Question:
{question}

Provide a clear explanation and reference files when possible.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def answer_question(question):

    qtype = classify_query(question)

    context = retrieve_context(qtype)

    answer = ask_llm(question, context)

    return answer


if __name__ == "__main__":

    questions = [
        "What Python dependencies does this project use?",
        "What is the main entry point file for the registry service?",
        "What programming languages and file types are used in this repository?",
        "How does the authentication flow work?",
        "What API endpoints exist in the registry service?",
        "How would you add support for a new OAuth provider?"
    ]

    with open("part1_results.txt", "w") as f:

        for q in questions:

            print("\nQUESTION:", q)

            ans = answer_question(q)

            print(ans)

            f.write("QUESTION: " + q + "\n")
            f.write(ans + "\n\n")