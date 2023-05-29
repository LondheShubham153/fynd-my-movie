FROM python:3.9.5-buster
WORKDIR /APP
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python3","app.py"]
