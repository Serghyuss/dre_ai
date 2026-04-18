from dotenv import load_dotenv
import os

load_dotenv()

print("DEBUG API KEY:", os.getenv("GEMINI_API_KEY"))

import streamlit as st
import pandas as pd

from dre.calculo_dre import calcular_dre, calcular_kpis_avancados
from ia.analise_gemini import gerar_analise

st.set_page_config(page_title="DRE com IA", layout="wide")

st.title("📊 Dashboard Financeiro com IA")

uploaded_file = st.file_uploader("Upload do CSV financeiro", type=["csv"])

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_pct(valor):
    return f"{valor:.2f}".replace(".", ",") + "%"

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Converter coluna de data
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)
        df = df.sort_values("data")

    st.subheader("📄 Dados")
    st.dataframe(df.head())

    temp_path = "temp.csv"
    df.to_csv(temp_path, index=False)

    dre = calcular_dre(temp_path)
    kpis = calcular_kpis_avancados(dre)

    # 📊 DRE estruturada
    st.subheader("📊 DRE")

    st.markdown(f"""
    **Receita Bruta:**  {formatar_moeda(dre['Receita Bruta'])}  
    
    **(-) Impostos:**  {formatar_moeda(dre['Impostos'])}  
    
    **= Receita Líquida:**  {formatar_moeda(dre['Receita Líquida'])}  

    **(-) CMV:**  {formatar_moeda(dre['CMV'])}  
    
    **= Lucro Bruto:**  {formatar_moeda(dre['Lucro Bruto'])}  

    **(-) Despesas Operacionais:**  {formatar_moeda(dre['Despesas Operacionais'])}  
    
    **= EBITDA:**  {formatar_moeda(dre['EBITDA'])}  

    **(-) Depreciação:**  {formatar_moeda(dre['Depreciação'])}  
    
    **= Resultado Operacional:**  {formatar_moeda(dre['Resultado Operacional'])}  

    **(+/-) Resultado Financeiro:**  {formatar_moeda(dre['Resultado Financeiro'])}  

    **= Resultado Líquido:**  {formatar_moeda(dre['Resultado Líquido'])}  
    """)

    # 📈 KPIs
    st.subheader("📈 KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Margem EBITDA", formatar_pct(kpis["Margem EBITDA (%)"]))
    col2.metric("Margem Líquida", formatar_pct(kpis["Margem Líquida (%)"]))
    col3.metric("Break-even", formatar_moeda(kpis["Break-even"]))

    st.write("**Margem de Contribuição:**", formatar_pct(kpis["Margem de Contribuição (%)"]))
    st.write("**Alavancagem Operacional:**", f"{kpis['Alavancagem Operacional']:.2f}")

    # 📊 Gráfico simples
    st.subheader("📊 Receita vs Custos")

    grafico_df = pd.DataFrame({
        "Categoria": ["Receita Líquida", "CMV", "Despesas"],
        "Valor": [
            dre["Receita Líquida"],
            abs(dre["CMV"]),
            abs(dre["Despesas Operacionais"])
        ]
    })

    st.bar_chart(grafico_df.set_index("Categoria"))

    # 🤖 IA
    if st.button("Gerar análise com IA"):
        with st.spinner("Analisando..."):
            analise = gerar_analise(kpis, dre, df)

        st.subheader("🤖 Análise Executiva")
        st.write(analise)