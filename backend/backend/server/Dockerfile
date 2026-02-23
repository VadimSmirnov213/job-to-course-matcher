from python:3.10
RUN mkdir /server
RUN python3 -m pip install --upgrade pip
WORKDIR /server
COPY  . .
RUN pip install -r requirements.txt
CMD ["uvicorn","main:app","--host","0.0.0.0", "--port","9000"]