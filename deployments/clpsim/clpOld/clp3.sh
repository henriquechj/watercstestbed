#!/bin/sh

while :
do
  # Simula a leitura da pressão da rede
  PRESSURE=$((RANDOM % 100))
  echo "Pressao Rede: $PRESSURE"

  # Simula a ativação/desativação da bomba de distribuição
  if [ "$PRESSURE" -lt 40 ]; then
    echo "Ativando bomba de distribuição"
  elif [ "$PRESSURE" -ge 80 ]; then
    echo "Desativando bomba de distribuição"
  fi

  # Simula um delay
  sleep 5
done
