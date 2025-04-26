#Efetuar o build da maquina atacante
docker build -t attacker .
#Executar a máquina atacante
docker run -d \
  --name attacker \
  -m 1g \
  --memory-reservation 512m \
  --cpus="0.75" \
  --pids-limit=200 \
  attacker:latest
