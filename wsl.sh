#!/bin/bash

# este arquivo é para o lado do servidor, onde foi usado docker numa windows com WSL, por isso o script tem chamados .exe

# se ja tiver os resultados

# rm 2/resultados.csv
# rm 5/resultados.csv

# # primeira parte, funciona o servidor docker

# cd server

# # deixa apenas 2 servidores
# for counter in $(seq 3 5); do
#     sed -i '/app'$counter'/s/^/#/' docker-compose.yml
#     sed -i '/app'$counter'/s/^/#/' nginx.conf
#     sed -i '/app'$counter':/,/[a-z]/s/^\(\s*build: .*\)/#\1/' docker-compose.yml
# done

# # roda
# docker-compose.exe up --build -d

# while [[ false ]]; do
#     echo "pressione "sim" para continuar..."
#     read -n 3 key
#     echo ''
#     if [[ $key == 'sim' ]]; then
#         break
#     fi
# done

# docker-compose.exe down

# # desliga o docker e muda para 5 servidores

# sed -i '/#/s/#//g' docker-compose.yml
# sed -i '/^#/s/^#//g' nginx.conf

# # liga o docker com 5 maquina

# echo '5 maquinas'
# docker-compose.exe up --build -d

# # desliga o docker e faz os teste

# while [[ false ]]; do
#     echo "pressione "sim" para continuar..."
#     read -n 3 key
#     echo ''
#     if [[ $key == 'sim' ]]; then
#         break
#     fi
# done

# docker-compose.exe down

# cd .. # sai da pasta so quando desligar tudo, pois o docker precisa saber o que vai ser desligado

# while [[ false ]]; do
#     echo 'traga os arquivos para esse computador para realizar análises e gráficos'
#     echo "pressione "sim" para iniciar análise..."
#     read -n 3 key
#     echo ''
#     if [[ $key == 'sim' ]]; then
#         break
#     fi
# done

# # parte 2, automatizar os testes

# # funcao FOR de acordo com a pasta, de 2 ou 5 servidores
# fazgraf() {
#     for counter in $(seq 1 4); do
#         python.exe ccsv.py "$1/$counter.csv"
#     done
# }

# echo 'gerar resultados baseados na tabela JMeter'

# fazgraf "5"
# fazgraf "2"

# # gerar grafico do 2 e 5
# intconf() {
#     python.exe media.py $1
# }

# echo 'gerar graficos baseados nos resultados'

# intconf 2
# intconf 5

# echo ''

# gerar grafico de latencia
fazlate() {
    for counter in $(seq 1 4); do
        python.exe latencia.py "$1/$counter.csv"
    done
}

fazlate 2
fazlate 5