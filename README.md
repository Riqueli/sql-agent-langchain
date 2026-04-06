# 🤖 SQL Agent com LangChain

Projeto de estudo que implementa um agente capaz de responder perguntas em linguagem natural a partir de uma base de dados SQL.

---

## 🚀 Funcionalidades

- Recebe perguntas em linguagem natural  
- Converte automaticamente para consultas SQL  
- Executa queries em um banco SQLite  
- Retorna respostas em português de forma objetiva  

---

## 🧠 Tecnologias Utilizadas

- **Python** — linguagem principal  
- **Pandas** — leitura e manipulação do dataset (CSV)  
- **SQLite** — banco de dados leve e local  
- **SQLAlchemy** — conexão e gerenciamento do banco  
- **LangChain** — orquestração do agente e uso de ferramentas  
- **Ollama (Llama3)** — modelo de linguagem rodando localmente  
- **SQLDatabaseToolkit** — toolkit do LangChain para interação com SQL  

---

## ⚙️ Como funciona

1. O dataset em CSV é carregado com Pandas  
2. Os dados são armazenados em um banco SQLite  
3. O LangChain conecta o banco ao agente  
4. O usuário faz uma pergunta em linguagem natural  
5. O agente gera uma query SQL automaticamente  
6. A query é executada e o resultado é retornado em texto  

---

## 📚 Referências e Estudos

Para o desenvolvimento deste projeto, foram utilizadas as seguintes fontes:

- **LangChain Documentation**: https://python.langchain.com/docs/tutorials/sql_qa/  
- **Ollama (Llama 3)**: https://ollama.com/library/llama3  
- **YouTube**: Conteúdos sobre agentes ReAct e integração de LLMs com bancos de dados SQL  
