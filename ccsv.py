import pandas as pd
import numpy as np
from scipy import stats
import os
import argparse

parser = argparse.ArgumentParser(description="Processamento de dados CSV com status 200 e latency")
parser.add_argument('input_csv', type=str, help="Caminho para o arquivo CSV de entrada")
args = parser.parse_args()  # pega os argumentos da linha de comando

def obter_caminho(arquivo):
    partes = arquivo.split("/")  # separa a string usando '/'
    return "/".join(partes[:-1])  # junta tudo, exceto o último elemento

caminho = obter_caminho(args.input_csv)

no_mostra = 50

# arquivo CSV de entrada; arquivo do JMeter
df = pd.read_csv(args.input_csv, delimiter=",")

# tira espaços 
df.columns = df.columns.str.strip()

df.columns = [col.lower() for col in df.columns] # tudo em minusculo

# remove espaços e nao numeros
df['responsecode'] = df['responsecode'].astype(str).str.strip()  # tira espaços extras ao redor
df['responsecode'] = pd.to_numeric(df['responsecode'], errors='coerce')  # conversao para numero, transformando erros em NaN

# quantos tiveram status 200 (sucesso) e quantas falhas
total_amostras = len(df)

sucessos_df = df[df['responsecode'] == 200]
falhas_df = df[df['responsecode'] != 200]

num_sucessos = len(sucessos_df)
num_falhas = len(falhas_df)

perc_sucessos = num_sucessos / total_amostras * 100
perc_falhas = num_falhas / total_amostras * 100

print(f"Total de amostras: {total_amostras}")
print(f"Sucessos (status == 200): {num_sucessos} ({perc_sucessos:.2f}%)")
print(f"Falhas (status != 200): {num_falhas} ({perc_falhas:.2f}%)\n")

# calculo para 'latency' nas linhas com status 200
latencies = sucessos_df['latency']
n_total = len(latencies)
media_latency = latencies.mean()
desvio_latency = latencies.std(ddof=1)

# intervalo de confiança de 90%
conf = 0.90
z = stats.norm.ppf(1 - (1 - conf) / 2)
margem = z * desvio_latency / np.sqrt(n_total)
ic_inferior = media_latency - margem
ic_superior = media_latency + margem

print("Estatísticas total para status com sucesso")
print(f"Média: {media_latency:.2f}")
print(f"Desvio Padrão: {desvio_latency:.2f}")
print(f"Intervalo de Confiança de 90%: [{ic_inferior:.2f}, {ic_superior:.2f}]\n")

# 3. Selecionar aleatoriamente 50 amostras entre as linhas com status 200
if n_total < no_mostra:
    print(f"Atenção: Menos de {no_mostra} amostras com status 200 disponíveis. Usando todas as amostras.")
    amostras = sucessos_df.copy()
else:
    amostras = sucessos_df.sample(n=no_mostra, random_state=42)  # random_state para reprodutibilidade

latencies_amostra = amostras['latency']
n_amostra = len(latencies_amostra)
media_amostra = latencies_amostra.mean()
desvio_amostra = latencies_amostra.std(ddof=1)
margem_amostra = z * desvio_amostra / np.sqrt(n_amostra)
ic_inferior_amostra = media_amostra - margem_amostra
ic_superior_amostra = media_amostra + margem_amostra

print(f"Estatísticas para amostra aleatória de {no_mostra} sucessos (status == 200):")
print(f"Média: {media_amostra:.2f}")
print(f"Desvio Padrão: {desvio_amostra:.2f}")
print(f"Intervalo de Confiança de 90%: [{ic_inferior_amostra:.2f}, {ic_superior_amostra:.2f}]")

# Definindo o nome do arquivo CSV de saída
output_csv = caminho + '/resultados.csv'

# Tentando carregar o CSV e adicionando a nova linha se o arquivo já existir
try:
    # Tenta carregar o arquivo CSV
    resultados_df = pd.read_csv(output_csv)
except FileNotFoundError:
    # Se o arquivo não existir, cria um novo DataFrame com os cabeçalhos
    resultados_df = pd.DataFrame(columns=['requisicoes', 'media', 'desviopadrao', 'amostras'])

# Adiciona a nova linha com os resultados, garantindo que todas as colunas estão presentes
nova_linha = {
    'requisicoes': total_amostras, # Número de requisições com status 200
    'media': f"{media_amostra:.2f}", # Média da amostra
    'desviopadrao': f"{desvio_amostra:.2f}", # Desvio padrão da amostra
    'amostras': no_mostra # Número de amostras
}

# Converte nova_linha para um DataFrame e garante que as colunas estão corretas
nova_linha_df = pd.DataFrame([nova_linha], columns=resultados_df.columns)

# Adiciona a nova linha ao DataFrame original usando pd.concat
resultados_df = pd.concat([resultados_df, nova_linha_df], ignore_index=True)

# Salva o DataFrame no CSV
resultados_df.to_csv(output_csv, index=False)

print(f"\nResultados adicionados ao arquivo '{output_csv}'")
