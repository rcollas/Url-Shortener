FROM python:3.11

COPY requirements.txt requierements.txt

RUN pip install -r requierements.txt

COPY . .

CMD ["python3", "-m", "flask", "--app", "core", "run"]

EXPOSE 5000