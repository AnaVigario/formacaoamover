#Dockerfile
# Use uma imagem base do Python
FROM python:3-alpine3.19

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 80

# Comando para executar o aplicativo
CMD ["python", "../formacao.py"]