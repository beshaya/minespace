cd ~/minespace
gunicorn index:app :80 --daemon --pid gunicorn-minespace
