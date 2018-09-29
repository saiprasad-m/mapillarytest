 FROM python:3
  ENV PYTHONUNBUFFERED 1
   RUN mkdir /code
    WORKDIR /code
     ADD requirements.txt /code/
      RUN pip install -r requirements.txt
       ADD . /code/


CMD ["ls -a"]
CMD [ "python.exe", "api\app.py" ]
CMD [ "python.exe", "test\base_test.py" ]