# Installation for development

### 1. Create python virtual environment

```sh
virtualenv -p `which python` env
source env/bin/activate
```

### 2. Install packages

```sh
pip install Django Pillow
```

### 3. Prepare database

```sh
cd shop
python manage.py migrate
python manage.py createsuperuser
python manage.py migrate accounts
python manage.py migrate sales
python manage.py collectstatic --noinput
```

### 4. Run develop server

```
pyton manager.py runserver
```

It uses address `http://127.0.0.1:8000/`.

### 5. Nginx

The application uses `HTTP <-> HTTPS` redirects, but Djano debug web-server doesn't support it. So **Ngix** can be used for this as proxy server.

The Nginx config example can be found in the file `nginx_example.conf`. It has some templates that are to be replaced by proper values: `SERVER_NAME, REPO_DIR, CERTS_DIR`.

SSL certificate for custom `SERVER_NAME` can be generated using **openssl** tool:

```sh
openssl req -newkey rsa:2048 -new -x509 \
	-days 365 -nodes -out cert.crt -keyout cert.key
cat cert.key cert.crt > cert.pem
```

After that the develop web server will be available as `http://SERVER_NAME/` or `http://SERVER_NAME/`.
