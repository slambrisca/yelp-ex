FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "app.py", "/mnt2/yelp_dataset.tar"]

