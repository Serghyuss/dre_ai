from google import genai
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # lê o .env automaticamente

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def gerar_analise(kpis, dre, produtos):
    if isinstance(produtos, dict):
        produtos = pd.DataFrame(produtos)

    prompt = f"""
    Você é um analista financeiro sênior.

    Analise os dados abaixo:

    KPIs:
    {kpis}

    DRE:
    {dre}

    Produtos (Amostra):
    {produtos.head(10).to_string()}

    Gere:
    - Diagnóstico do negócio
    - Principais riscos
    - Oportunidades
    - Recomendações práticas
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",  # ✅ corrigido
        contents=prompt
    )

    return response.text