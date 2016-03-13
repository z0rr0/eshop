# eShop - https://github.com/z0rr0/eshop
#
# Run example
# docker run --rm --name eshop -v /data:/data -p 9090:9090 eshop
#
# Files should be prepared manually:
# /data/local_settings.py
# /data/settings.py
# /data/eshop.ini
#
# Also database initialization should be done separately.

FROM ubuntu:latest
MAINTAINER Alexander Zaytsev "thebestzorro@yandex.ru"

RUN apt-get update && \
    apt-get -y upgrade
RUN apt-get install -y python3-dev uwsgi uwsgi-core \
	uwsgi-plugin-python3 python3-pip libjpeg-dev zlib1g-dev \
	libtiff-dev libfreetype6-dev libwebp-dev libopenjpeg-dev
RUN pip3 install django pillow

EXPOSE 9090
VOLUME ["/data/"]
ADD shop /shop

RUN rm -rf /shop/shop/settings.py /shop/shop/local_settings.py && \
	rm -rf /shop/media/images /shop/db.sqlite3 && \
	ln -s /data/settings.py /shop/shop/settings.py && \
	ln -s /data/local_settings.py /shop/shop/local_settings.py && \
	ln -s /data/images /shop/media/images

WORKDIR /shop
ENTRYPOINT ["/usr/bin/uwsgi"]
CMD ["--ini", "/data/eshop.ini"]
