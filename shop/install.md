# Installation for development

### 1. Create python virtual environment

```sh
virtualenv -p `which python3` env
source env/bin/activate
```

### 2. Install packages

```sh
pip install Django Pillow
```

### 3. Security issues

Create the file `local_settings.py` and redefine security variables: `SECRET_KEY, COOKIE_SALT, ALLOWED_HOSTS, DATABASES`.

```sh
touch shop/shop/local_settings.py
```

### 4. Prepare database

```sh
cd shop
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py migrate accounts
python3 manage.py migrate sales
python3 manage.py collectstatic --noinput
```

### 5. Run develop server

```
python3 manager.py runserver
```

It uses address `http://127.0.0.1:8000/`.

### 6. Nginx

The application uses `HTTP <-> HTTPS` redirects, but Djano debug web-server doesn't support it. So **Ngix** can be used for this as a proxy server.

The Nginx config example can be found in the file `nginx_example.conf`. It has some templates that are to be replaced by proper values: `SERVER_NAME, REPO_DIR, CERTS_DIR`.

A self-signed SSL certificate for custom `SERVER_NAME` domain can be generated using **openssl** tool:

```sh
openssl req -newkey rsa:2048 -new -x509 \
	-days 365 -nodes -out cert.crt -keyout cert.key
cat cert.key cert.crt > cert.pem
```

After that the develop web server will be available as `http(s)://SERVER_NAME/`.

### 7. Docker

Another way to install eShop is an using of Docker container [z0rr0/eshop](https://hub.docker.com/r/z0rr0/eshop). It is easier, but you should know that you do :)
