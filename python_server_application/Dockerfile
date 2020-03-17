FROM python:3.7
COPY .. /app
WORKDIR /app
RUN sh lilypond-2.20.0-1.linux-64.sh
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]