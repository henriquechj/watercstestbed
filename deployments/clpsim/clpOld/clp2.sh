#!/bin/sh

while :
do
  # Simula a leitura do nível do tanque
  LEVEL=$((RANDOM % 100))
  echo "Nivel Tanque: $LEVEL"

  # Simula a ativação/desativação da bomba de captação
  if [ "$LEVEL" -lt 50 ]; then
    echo "Ativando bomba de captação"
  elif [ "$LEVEL" -ge 100 ]; then
    echo "Desativando bomba de captação"
  fi

  # Simula um delay
  sleep 5
done
