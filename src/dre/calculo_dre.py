import pandas as pd
from .estrutura_dre import MAPEAMENTO_DRE


def calcular_dre(caminho_csv):
    df = pd.read_csv(caminho_csv)

    df["categoria_dre"] = df["conta_contabil"].map(MAPEAMENTO_DRE)
    resumo = df.groupby("categoria_dre")["valor"].sum()

    receita_bruta = resumo.get("receita_bruta", 0)
    impostos = resumo.get("impostos", 0)
    cmv = resumo.get("cmv", 0)

    receita_liquida = receita_bruta + impostos
    lucro_bruto = receita_liquida + cmv

    despesas_op = resumo.get("despesas_operacionais", 0)
    depreciacao = resumo.get("depreciacao", 0)

    ebitda = lucro_bruto + despesas_op
    resultado_operacional = ebitda + depreciacao

    resultado_financeiro = (
        resumo.get("receitas_financeiras", 0) +
        resumo.get("despesas_financeiras", 0)
    )

    resultado_liquido = resultado_operacional + resultado_financeiro

    return {
        "Receita Bruta": receita_bruta,
        "Impostos": impostos,
        "Receita Líquida": receita_liquida,
        "CMV": cmv,
        "Lucro Bruto": lucro_bruto,
        "Despesas Operacionais": despesas_op,
        "EBITDA": ebitda,
        "Depreciação": depreciacao,
        "Resultado Operacional": resultado_operacional,
        "Resultado Financeiro": resultado_financeiro,
        "Resultado Líquido": resultado_liquido
    }


def calcular_kpis_avancados(dre):
    receita = dre["Receita Líquida"]

    if receita == 0:
        return {}

    custos_variaveis = abs(dre["CMV"] + dre["Impostos"])
    despesas_fixas = abs(dre["Despesas Operacionais"])

    margem_contribuicao_valor = receita - custos_variaveis
    margem_contribuicao_pct = (margem_contribuicao_valor / receita) * 100

    break_even = despesas_fixas / (margem_contribuicao_valor / receita) if margem_contribuicao_valor != 0 else 0

    ebit = dre["Resultado Operacional"]
    grau_alavancagem = margem_contribuicao_valor / ebit if ebit != 0 else 0

    return {
        "Margem Bruta (%)": (dre["Lucro Bruto"] / receita) * 100,
        "Margem EBITDA (%)": (dre["EBITDA"] / receita) * 100,
        "Margem Líquida (%)": (dre["Resultado Líquido"] / receita) * 100,
        "CMV (%)": (dre["CMV"] / receita) * 100,
        "Despesas Operacionais (%)": (dre["Despesas Operacionais"] / receita) * 100,
        "Margem de Contribuição (%)": margem_contribuicao_pct,
        "Margem de Contribuição (Valor)": margem_contribuicao_valor,
        "Break-even": break_even,
        "Alavancagem Operacional": grau_alavancagem
    }