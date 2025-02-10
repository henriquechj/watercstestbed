#!/bin/bash

# URL da API
API_URL="http://restful:8080/api/medicoes"

# Matrícula fictícia
MATRICULA="123456"
MEDICAO=0

# Função para enviar medição
send_medicao() {
  # Data e hora atual
  DATA_HORA=$(date +"%Y-%m-%dT%H:%M:%S")

  # Medição fictícia
  MEDICAO_ATUAL=$(awk -v min=1 -v max=5 'BEGIN{srand(); print min+rand()*(max-min+1)}')
  #MEDICAO=$(($MEDICAO + $MEDICAO_ATUAL))
  MEDICAO=`awk -v y1=$MEDICAO -v y2=$MEDICAO_ATUAL 'BEGIN {print y1+y2}'`
  # JSON com os dados da medição
  JSON_DATA=$(cat <<EOF
{
  "matricula": "$MATRICULA",
  "dataHora": "$DATA_HORA",
  "medicaoAtual": $MEDICAO
}
EOF
  )

  # Enviar medição usando curl
  curl -X POST "$API_URL" \
       -H "Content-Type: application/json" \
       -d "$JSON_DATA"

  #echo "Enviada medição: $JSON_DATA"
}

# Loop infinito para enviar medições a cada 20 segundos
while true; do
  send_medicao
  sleep 20
done
