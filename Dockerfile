# Используем официальный образ Python в качестве базового
FROM python:3.12-slim

COPY req.txt req.txt
RUN pip install -r req.txt

COPY . .

# Указываем команду по умолчанию (будет переопределена в docker-compose)
CMD ["python", "main.py"]