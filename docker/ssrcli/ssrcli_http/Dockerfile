FROM alpine:3.10
RUN echo "http://mirrors.ustc.edu.cn/alpine/v3.10/main/" >/etc/apk/repositories
RUN apk --no-cache add privoxy
COPY privoxy.conf /etc/

EXPOSE 10800
CMD [ "privoxy", "--no-daemon", "/etc/privoxy.conf" ]
LABEL maintainer="myl7 <myl.ustc@gmail.com>" version="1.0.0"
