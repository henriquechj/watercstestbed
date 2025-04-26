# Preparando o Ambiente Atacante

Este documento descreve os passos para construir e executar uma máquina atacante utilizando Docker.

## 1. Construção da Imagem Docker

O primeiro passo é construir a imagem Docker que conterá as ferramentas e configurações necessárias para a máquina atacante. Certifique-se de que você possui um arquivo `Dockerfile` no diretório atual que define o ambiente da sua máquina atacante.

Para construir a imagem, execute o seguinte comando no seu terminal, dentro do diretório que contém o `Dockerfile`:

```bash
docker build -t attacker .
```

## 2.  Execução do Container do Atacante

Com a imagem construída, o próximo passo é executar um container a partir dessa imagem. O container é uma instância em execução da imagem Docker.

Utilize o seguinte comando para executar a máquina atacante como um container em segundo plano:

```bash
docker run -d \
  --name attacker \
  -m 1g \
  --memory-reservation 512m \
  --cpus="0.75" \
  --pids-limit=200 \
  attacker:latest
```


