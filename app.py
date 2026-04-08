import pandas as pd
from sqlalchemy import create_engine
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent


# 1. CARREGAR DATASET

url = "https://gist.githubusercontent.com/denandreychuk/b9aa812f10e4b60368cff69c6384a210/raw/100%20Sales%20Records.csv"
df = pd.read_csv(url)
df.columns = [c.replace(" ", "_") for c in df.columns]

# 2. CRIAR BANCO DE DADOS (SQLite)
engine = create_engine("sqlite:///sales.db")
df.to_sql("sales", con=engine, if_exists="replace", index=False)

# 3. CONFIGURAR IA E FERRAMENTAS (LangChain + Ollama)
db = SQLDatabase.from_uri("sqlite:///sales.db") 
llm = ChatOllama(model="llama3", temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 4. INSTRUÇÕES DO AGENTE (prompt)
prefix = """
Você é um especialista em SQL que responde APENAS sobre a tabela 'sales'.
Colunas: Region, Country, Item_Type, Units_Sold, Total_Revenue, Total_Cost, Total_Profit, Order_Date.

REGRAS CRÍTICAS:
1. Se a pergunta NÃO for sobre vendas, países, regiões ou lucros, responda IMEDIATAMENTE: "Não foi possível encontrar essa informação na base de dados."
2. Não tente inventar tabelas. Se não souber, desista na primeira tentativa.
3. Responda sempre em Português.
4. Se o usuário pedir algo que não está nas colunas acima, diga que não encontrou.
"""

# 5. CRIAR O AGENTE
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False, 
    agent_type="zero-shot-react-description",
    max_iterations=3, 
    handle_parsing_errors=True,
    prefix=prefix
)

# 6. INTERAÇÃO COM O USUÁRIO

print("\n" + "=" * 50)
print("🤖 Agente SQL Otimizado Pronto!")
print("=" * 50 + "\n")

# Lista de palavras-chave para um filtro simples e ultra rápido
keywords = ['venda', 'lucro', 'país', 'região', 'custo', 'item', 'unidade', 'receita', 'data', 'quanto', 'qual', 'sales']

while True:
    question = input("📝 Sua pergunta: ").strip()

    if question.lower() == "sair":
        break

    # FILTRO RÁPIDO: Se não tiver palavras-chave, nem processa o SQL
    if not any(word in question.lower() for word in keywords):
        print("⚠️ Não foi possível encontrar essa informação na base de dados.\n")
        continue

    try:
        print("⏳ Analisando dados...")
        # Adicionei um limitador de tempo interno na chamada se necessário
        response = agent_executor.invoke({"input": question})
        output = response.get("output", "")

        if "Agent stopped" in output or not output:
             print("⚠️ Não foi possível encontrar essa informação na base de dados.\n")
        else:
            print(f"✅ Resultado: {output}\n")

    except Exception:
        print("⚠️ Não foi possível encontrar essa informação na base de dados.\n")