from dotenv import load_dotenv
import os
import pandas as pd
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CSV_PATH = "data/structured/daily_sales.csv"
TEXT_PATH = "data/unstructured"


def classify_query(question):
    q = question.lower()

    if "revenue" in q or "sales" in q or "region" in q:
        return "csv"

    if "features" in q or "reviews" in q or "customers say" in q:
        return "text"

    if "best product" in q or "recommend" in q:
        return "both"

    return "text"


def query_csv(question):

    df = pd.read_csv(CSV_PATH)

    if "electronics" in question.lower():
        df = df[df["category"] == "Electronics"]

    if "december" in question.lower():
        df["date"] = pd.to_datetime(df["date"])
        df = df[df["date"].dt.month == 12]

    if "revenue" in question.lower():
        return str(df["total_revenue"].sum())

    if "region" in question.lower():
        return str(df.groupby("region")["units_sold"].sum())

    return df.head().to_string()


def query_text(question):

    context = ""

    for file in os.listdir(TEXT_PATH):
        path = os.path.join(TEXT_PATH, file)

        with open(path) as f:
            text = f.read()

        if any(word in text.lower() for word in question.lower().split()):
            context += text[:1000]

    return context[:4000]


def ask_llm(question, context):

    prompt = f"""
Answer the question using the provided context.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def answer_question(question):

    source = classify_query(question)

    if source == "csv":
        context = query_csv(question)

    elif source == "text":
        context = query_text(question)

    else:
        context = query_csv(question) + "\n" + query_text(question)

    return ask_llm(question, context)


if __name__ == "__main__":

    questions = [
        "What was the total revenue for Electronics category in December 2024?",
        "Which region had the highest sales volume?",
        "What are the key features of the Wireless Bluetooth Headphones?",
        "What do customers say about the Air Fryer's ease of cleaning?",
        "Which product has the best customer reviews and how well is it selling?",
        "I want a product for fitness that is highly rated and sells well in the West region. What do you recommend?"
    ]

    with open("part2_results.txt", "w") as f:

        for q in questions:

            print("\nQUESTION:", q)

            ans = answer_question(q)

            print(ans)

            f.write("QUESTION: " + q + "\n")
            f.write(ans + "\n\n")