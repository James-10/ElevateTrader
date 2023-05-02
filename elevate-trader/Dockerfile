FROM python:3.10-windowsservercore-ltsc2022

RUN mkdir /elevate-trader

WORKDIR /elevate-trader

COPY Pipfile Pipfile.lock /elevate-trader/

RUN python.exe -m pip install --upgrade pip
RUN python.exe -m pip install --upgrade pipenv
RUN pipenv install --verbose --system --deploy ;

ADD . /elevate-trader

CMD ["python", "app/main.py"] 