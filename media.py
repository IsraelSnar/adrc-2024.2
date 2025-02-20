import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import sys

# Caminho do CSV
caminho = sys.argv[1]
df = pd.read_csv(caminho + "/resultados.csv", delimiter=",")

# Ajusta nomes das colunas
df.columns = df.columns.str.strip()
df.columns = [col.lower() for col in df.columns]

# Converte para numérico (caso haja texto)
for col in ["requisicoes", "media", "desviopadrao", "amostras"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df.dropna(subset=["requisicoes", "media", "desviopadrao", "amostras"], inplace=True)

# Intervalo de confiança 90%
conf = 0.90
z_score = stats.norm.ppf((1 + conf) / 2)
df["erropadrao"] = df["desviopadrao"] / np.sqrt(df["amostras"])
df["intervalo"] = z_score * df["erropadrao"]

# Monta as barras de erro superior e inferior
erro_inferior = df["intervalo"]
erro_superior = df["intervalo"]

plt.figure(figsize=(10, 6))

# 'fmt="o"' = só marca os pontos (sem linha), 'ecolor' = cor das barras
plt.errorbar(
    x=df["requisicoes"],
    y=df["media"],
    yerr=[erro_inferior, erro_superior],
    fmt='o',         # só marcador
    ecolor='blue',   # cor do “erro”
    alpha=0.9,       # transparência
    capsize=4,       # "chapeuzinho" da barra
    label="Intervalo de 90%"
)

# Adiciona texto com valor da média
for x, y in zip(df["requisicoes"], df["media"]):
    plt.text(x, y, f'{y:.2f}', fontsize=9, va='bottom')

plt.xlabel("Quantidade de Requisições")
plt.ylabel("Média (ms)")
plt.title("Média com Intervalo de Confiança de 90%")
plt.grid(True)
plt.legend()

plt.savefig(caminho + "/intervalo.png")
# plt.show() # mostra o grafico, n precisa pq é script
print("Gráfico salvo em:", caminho + "/intervalo.png")
