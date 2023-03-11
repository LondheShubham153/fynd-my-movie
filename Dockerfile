FROM python:3.9.5-buster
WORKDIR /usr/app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE $PORT
CMD ["python3", "app.py"]