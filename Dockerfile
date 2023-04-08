FROM python:3.10
RUN pip install django==3.2
COPY . .
COPY requirements.txt .
RUN pip install -r requirements.txt 
EXPOSE 9090
CMD ["python","app.py"]