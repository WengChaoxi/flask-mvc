#! /bin/bash

if [ "$1" = "start" ]; then
    echo -e "[runserver] starting server...\c"
    nohup uwsgi uwsgi/uwsgi.ini &>>logs/web_server.log &
    echo "success"
elif [ "$1" = reload ]; then
    echo -e "[runserver] reloading server...\c"
    uwsgi --reload uwsgi/uwsgi.pid
    echo "success"
elif [ "$1" = "stop" ]; then
    echo -e "[runserver] stoping server...\c"
    uwsgi --stop uwsgi/uwsgi.pid
    echo "success"
else
    echo "[runserver] need an argument: [start | reload | stop]"
fi
    

