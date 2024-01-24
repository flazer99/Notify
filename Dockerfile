FROM python:3.8

EXPOSE 8080
WORKDIR /app

COPY . .

ENV PROJECT_ID=<PROJECT_ID>
ENV BUCKET_NAME=<BUCKET_NAME>

RUN pip install -r requirements.txt

CMD ["python", "main.py"]