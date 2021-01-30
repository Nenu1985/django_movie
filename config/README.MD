Конфиг Гуникорна:
gunicorn.conf.py

    ```
    bind = '127.0.0.1:8000'
    workers = 2
    user = "nenu"
    timeout = 30  # After timeout sec server will return 5xx error
    ```

Супервизор
Автоматически поднимает gunicorn:
movie.conf

```
[program:movie]
command=/home/ubuntu/code/env/bin/gunicorn django_movie.wsgi:application -c /home/ubuntu/django_movie/config/gunicorn.conf.py
directory=/home/john/django_movie
user=nenu
autorestart=true
redirect_stderr=true
stdout_logfile = /home/nenu/django_movie/logs/debug.log
```