FROM firesh/nginx-lua

# install mc for debug?
# RUN apt-get update &&  apt-get install --assume-yes apt-utils && apt-get install -yqq mc

RUN rm /etc/nginx/conf.d/*
COPY sites-enabled/project.conf /etc/nginx/conf.d/default.conf
RUN echo "env NGINX_SERVER;" >>  /etc/nginx/nginx.conf
RUN echo "env APP_PORT;" >>  /etc/nginx/nginx.conf
RUN echo "" >>  /etc/nginx/nginx.conf
