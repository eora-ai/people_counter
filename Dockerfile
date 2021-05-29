FROM python:3.9

RUN pip install -U pip

WORKDIR app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]
