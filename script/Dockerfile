FROM netping/python:3.8-slim
ADD main.py /script/
ADD requirements.txt /script/
WORKDIR /script/
RUN pip install --require-hashes -r requirements.txt
