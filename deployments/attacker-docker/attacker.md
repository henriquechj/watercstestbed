# Preparando o Ambiente Atacante

Este documento descreve os passos para construir e executar uma máquina atacante utilizando Docker.

## 1. Construção da Imagem Docker

Execute o comando abaixo dentro do diretório que contém o `Dockerfile`:

```bash
docker build -t attacker .
```

## 2.  Execução do Container do Atacante


```bash
docker run -d \
  --name attacker \
  -m 1g \
  --memory-reservation 512m \
  --cpus="0.75" \
  --pids-limit=200 \
  attacker:latest
```

## Acessando o Bash do Container em Execução

Para acessar o Bash do attacker, utilize o seguinte comando no seu terminal:

```bash
docker exec -it attacker bash
```
