
import streamlit as st
import pandas as pd
import numpy as np
from monte_carlo import (
    capturar_parametros,
    monte_carlo_opcao_europeia,
    monte_carlo_opcao_asiatica,
    plot_trajetorias
)

st.set_page_config(page_title="Calculadora de Volatilidade e Opções", layout="centered")

st.title("Calculadora de Volatilidade e Opções")

# Sidebar: parâmetros do ativo
st.sidebar.header("Dados do Ativo")
ticker = st.sidebar.text_input("Ticker (ex: AAPL)", value="AAPL")
periodo = st.sidebar.selectbox("Período Histórico", ["1mo", "3mo", "6mo", "1y"], index=3)

if st.sidebar.button("Carregar Dados"):
    try:
        S0, mu, sigma_hist, dados = capturar_parametros(ticker, periodo)
        st.sidebar.write(f"Preço Atual (S0): {S0:.2f}")
        st.sidebar.write(f"Retorno Esperado (μ): {mu:.2%}")
        st.sidebar.write(f"Vol. Histórica (σ): {sigma_hist:.2%}")
        st.line_chart(dados['Close'], use_container_width=True)
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar dados: {e}")

# Main: precificação de opções
st.header("Precificação de Opções")
col1, col2 = st.columns(2)
with col1:
    option_type = st.selectbox("Tipo de Opção", ["Europeia", "Asiática"])
    S0_input = st.number_input("Preço Atual (S0)", value=S0 if 'S0' in locals() else 100.0)
    K = st.number_input("Strike (K)", value=S0_input * 1.05)
with col2:
    T = st.number_input("Tempo até Vencimento (anos)", value=1.0, min_value=0.01, step=0.01)
    r = st.number_input("Taxa Livre de Risco (r)", value=0.04, format="%.4f")
    sigma_input = st.number_input("Volatilidade (σ)", value=sigma_hist if 'sigma_hist' in locals() else 0.2, format="%.4f")

n_sim = st.slider("Número de Simulações", min_value=1000, max_value=100000, value=20000, step=1000)

if st.button("Calcular"):
    try:
        if option_type == "Europeia":
            preco = monte_carlo_opcao_europeia(S0_input, K, T, r, sigma_input, n_sim)
        else:
            preco = monte_carlo_opcao_asiatica(S0_input, K, T, r, sigma_input, n_sim)
        st.write(f"Preço da Opção {option_type}: {preco:.4f}")
        # plot_trajetorias deve retornar uma figura matplotlib
        fig = plot_trajetorias(S0_input, T, r, sigma_input, n_sim)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao calcular: {e}")

# Dica: Para volatilidade implícita, implemente uma função de root-finding que busca σ
# tal que monte_carlo_opcao_europeia(...) == preço_de_mercado e exiba em outro bloco.
