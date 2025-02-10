# Usar a imagem base do Alpine Linux com curl
FROM alpine:latest

# Instalar curl e utilitários necessários
RUN apk --no-cache add curl bash coreutils

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o script para o contêiner
COPY send_medicoes.sh .

# Dar permissão de execução ao script
RUN chmod +x send_medicoes.sh

# Comando para executar o script
CMD ["./send_medicoes.sh"]
