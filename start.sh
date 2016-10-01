cat > /etc/supervisor/conf.d/python-app.conf <<EOF
[program:pythonapp]
directory=/opt/app/
command=/opt/app/venv/bin/gunicorn main:app --bind :80
autostart=true
autorestart=true
user=root
# Environment variables ensure that the application runs inside of the
# configured virtualenv.
environment=VIRTUAL_ENV="/opt/app/venv",PATH="/opt/app/venv/bin",\
    HOME="/home/root",USER="root"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update
#supervisorctl restart pythonapp
