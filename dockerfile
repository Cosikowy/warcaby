FROM python:slim

COPY ./ /home/server

WORKDIR /home/server

EXPOSE 5000

CMD ["python", "async_server.py"]