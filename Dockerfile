FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 5000

ENV PORT=5000
ENV SQLITE_DB_PATH=sqlite:///app.db

CMD ["./entrypoint.sh"]
