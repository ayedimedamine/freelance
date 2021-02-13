#python3 flushMaster.py
sudo killall gunicorn 
sudo gunicorn -b 0.0.0.0:80 app:app --timeout 300 -w 8 --worker-class gevent  --worker-connections=1000 --daemon
