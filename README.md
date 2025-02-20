# adrc-2024.2
Códigos da matéria de Análise de Desempenho em Redes de Computadores

### Arquivos

As pastas `2` e `5` são respectivamente onde está os dados de coleta e resultado das análises onde tinham `2 servidores` e `5 servidores` docker, mais a máquina `nginx`, totalizando 3 ou 6 servidores.

Os arquivos enumerados de `1-4.csv` provém da coleta realizada do *APache JMeter*, que usei para requisiçoes. O arquivo `resultados.csv` corresponde ao resultado processado dos arquivos anteriores, usando 50 amostras, que foram coletadas apenas entre os que resultados que deram certo (status 200 HTTP). Por fim a imagem `intervalo.png` é onde encontra-se o intervalo de confiança e as médias de cada teste.

#### ccsv.py

Pega os dados vindos de um CSV do JMeter e exporta para o arquivo `resultados.csv` para cada pasta de servidores.

#### media.py

Pega os dados vindos do arquivo `resultados.csv` e transforma na imagem com intervalo de confiança.

#### israel.jmx

Arquivo de configuração do JMeter, importa-lo, e lá terá todas as tabelas usadas. e últimas configurações.

#### Arquivos CSV

Exportados do JMeter, trás informações que utilizo ao longo do trabalho.

### Testes

Os testes são requisições HTTP ao servidor, realizadas quase instantaneamente, sendo o tempo decorrido pela conexão é do próprio protocolo HTTP. Os valores dos testes foram:
 - 100 x 3
 - 500 x 6
 - 1000 x 4
 - 2500 x 4

### Configurações

Foi usado um computador Windows 10, e Ubuntu no WSL, pois prefiro o Bash para scripts.

### Como funciona

Ele irá rodar primeiro o docker com 2 servidores, certifique-se de tudo estar ligado, depois após sua confirmação digitando `sim` ele irá mudar para 5 servidores, depois, confirme de novo para começar a fazer os testes. 

### Pacotes Python

```pip install pandas numpy scipy matplotlib```


