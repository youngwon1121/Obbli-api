FROM python:latest

WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "./manage.py", "migrate" ]

EXPOSE 8000