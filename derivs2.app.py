import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# --- Funções Monte Carlo e Parâmetros ---
def capturar_parametros(ticker: str, periodo: str) -> tuple:
    """
    Baixa históricos via yfinance e retorna (S0, mu, sigma_hist, dados).
    """
    dados = yf.download(ticker, period=periodo)
    dados['Return'] = dados['Close'].pct_change()
    dados = dados.dropna()
    S0 = dados['Close'].iloc[-1]
    mu = dados['Return'].mean()
    sigma_hist = dados['Return'].std()
    return S0, mu, sigma_hist, dados


def monte_carlo_opcao_europeia(S0, K, T, r, sigma, n_sim):
    Z = np.random.standard_normal(n_sim)
    ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    payoff = np.maximum(ST - K, 0)
    return np.exp(-r*T) * payoff.mean()


def monte_carlo_opcao_asiatica(S0, K, T, r, sigma, n_sim, m=50):
    dt = T/m
    payoffs = []
    for _ in range(n_sim):
        Z = np.random.standard_normal(m)
        path = S0 * np.exp(np.cumsum((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z))
        payoffs.append(max(path.mean() - K, 0))
    return np.exp(-r*T) * np.mean(payoffs)


def plot_trajetorias(S0, T, r, sigma, n_sim, m=50):
    dt = T/m
    paths = np.zeros((m+1, n_sim))
    paths[0] = S0
    for t in range(1, m+1):
        Z = np.random.standard_normal(n_sim)
        paths[t] = paths[t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)
    fig, ax = plt.subplots()
    ax.plot(paths[:, :min(10, n_sim)], alpha=0.6)
    ax.set_title('Trajetórias Monte Carlo')
    ax.set_xlabel('Passo')
    ax.set_ylabel('Preço do Ativo')
    return fig

# --- Geração do app.py ---

# Salva o código acima em 'app.py'
output_path = Path('app.py')
output_path.write_text(app_code)
print(f"Arquivo 'app.py' criado com sucesso em {output_path.resolve()}")
