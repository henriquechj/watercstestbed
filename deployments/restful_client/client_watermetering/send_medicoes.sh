#!/bin/bash

# URL da API
API_URL="http://localhost:8080/api/medicoes"

# Matrícula fictícia
MATRICULA="123456"

# Função para enviar medição
send_medicao() {
  # Data e hora atual
  DATA_HORA=$(date +"%Y-%m-%dT%H:%M:%S")

  # Medição fictícia
  MEDICAO_ATUAL=$(awk -v min=1 -v max=5 'BEGIN{srand(); print min+rand()*(max-min+1)}')
  MEDICAO=$MEDICAO+$MEDICAO_ATUAL
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

  echo "Enviada medição: $JSON_DATA"
}

# Loop infinito para enviar medições a cada 60 segundos
while true; do
  send_medicao
  sleep 60
done
