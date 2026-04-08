import pandas as pd
from sqlalchemy import create_engine

from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent


# 1. Load dataset
url = "https://gist.githubusercontent.com/denandreychuk/b9aa812f10e4b60368cff69c6384a210/raw/100%20Sales%20Records.csv"
df = pd.read_csv(url)
df.columns = [c.replace(" ", "_") for c in df.columns]


# 2. Create SQLite database
engine = create_engine("sqlite:///sales.db")
df.to_sql("sales", con=engine, if_exists="replace", index=False)


# 3. Connect LangChain to database
db = SQLDatabase.from_uri("sqlite:///sales.db")

llm = ChatOllama(
    model="llama3",
    temperature=0
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)


# 4. Agent instructions
prefix = """
You are an agent that queries a SQLite database.

Rules:
- Understand tables and columns before answering
- Generate valid SQL queries
- Limit results to 5 rows unless specified otherwise
- Do not hallucinate data
- Answer clearly in Portuguese
"""


# 5. Create SQL agent
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False,
    agent_type="zero-shot-react-description",
    max_iterations=10,
    handle_parsing_errors=True,
    prefix=prefix
)


# 6. User interaction loop
print("\n" + "=" * 50)
print("🤖 SQL Agent ready!")
print("Ask your question about the database")
print("Type 'exit' to quit")
print("=" * 50 + "\n")

while True:
    question = input("📝 Your question: ").strip()

    if question.lower() == "exit":
        print("\n👋 Exiting the SQL Agent...\n")
        break

    if not question:
        print("⚠️ Please enter a valid question.\n")
        continue

    try:
        print("\n⏳ Thinking...\n")
        response = agent_executor.invoke({"input": question})

        output = response.get("output", "").strip()

        if output:
            print("✅ Result:")
            print(output)
            print()
        else:
            print("⚠️ Could not generate a response.\n")

    except Exception:
        print("❌ An error occurred while processing your question.")
        print("Please try rephrasing it.\n")