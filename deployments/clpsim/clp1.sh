#!/bin/sh

while :
do
  # Simula a leitura do nível da barragem
  LEVEL=$((RANDOM % 100))
  echo "Nivel Barragem: $LEVEL"

  # Simula um delay
  sleep 5
done
