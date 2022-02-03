FROM python:3.8-slim-buster
COPY . /run
WORKDIR /run
RUN pip3 install -r requirements.txt
ENV FLASK_APP=run.py
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["run.py"]