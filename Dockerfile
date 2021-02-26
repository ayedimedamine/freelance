FROM python:3
WORKDIR /usr/src/app
COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt
COPY . .
#RUN chmod +x run.sh
EXPOSE 5000
CMD [ "gunicorn","-b","0.0.0.0:5000","--timeout=300","-w 2","--worker-class=gevent","--worker-connections=1000","app:app" ]   
