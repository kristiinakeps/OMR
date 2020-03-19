FROM python:3.7
COPY . /app
WORKDIR /app
RUN  date && apt-get update && apt-get install -y lilypond
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]