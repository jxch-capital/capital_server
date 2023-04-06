FROM python

ADD . /code
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_ENV='production'
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_NEED_PROXY=false
ENV FLASK_PROXY_HOST=''
ENV FLASK_PROXY_PORT=''
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]