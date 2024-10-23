FROM python:3.13

ADD hangman.py .
ADD data.json .

RUN pip install wonderwords pyfiglet

CMD ["python", "./hangman.py"]