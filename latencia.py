import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import os

def main():
    # Verifica se o usuário passou o caminho do arquivo
    if len(sys.argv) != 2:
        print("Uso correto: python laten.py caminho/arquivo.csv")
        sys.exit(1)

    # Captura o caminho do arquivo CSV a partir dos argumentos
    caminho_arquivo = sys.argv[1]

    # Extrai o diretório onde o arquivo está localizado
    caminho_pasta = os.path.dirname(caminho_arquivo)

    # Extrai o nome do arquivo sem extensão
    nome_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    # Carregar o CSV
    df = pd.read_csv(caminho_arquivo)

    # Converter timeStamp para datetime
    df["timeStamp"] = pd.to_datetime(df["timeStamp"], unit="ms")

    # Criar uma coluna de tempo decorrido desde o primeiro registro
    df["tempo_decorrido"] = (df["timeStamp"] - df["timeStamp"].iloc[0]).dt.total_seconds()

    # Criar o gráfico de linha
    plt.figure(figsize=(10, 5))
    plt.plot(df["tempo_decorrido"], df["Latency"], marker="o", linestyle="-", color="b", label="Latência (ms)")

    # Configurar rótulos e título
    plt.xlabel("Tempo Decorrido (s)")
    plt.ylabel("Latência (ms)")
    plt.title("Gráfico de Latência ao Longo do Tempo")
    plt.legend()
    plt.grid(True)

    # Criar o nome do arquivo de saída no formato latencia_NOME.png
    nome_saida = f"latencia_{nome_arquivo}.png"
    caminho_grafico = os.path.join(caminho_pasta, nome_saida)

    # Salvar o gráfico na mesma pasta do CSV
    plt.savefig(caminho_grafico)
    print(f"Gráfico salvo em: {caminho_grafico}")

    # Exibir o gráfico
    # plt.show()

main()
