sudo killall gunicorn
sudo gunicorn -b 0.0.0.0:80 white:app --daemon
