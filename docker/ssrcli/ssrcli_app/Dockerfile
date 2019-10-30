FROM alpine/git:1.0.7 AS builder
WORKDIR /app
RUN git clone https://github.com/shadowsocksr-backup/shadowsocksr -b manyuser /app \
 && rm -rf /app/.git*

FROM alpine:3.10
WORKDIR /app
RUN echo "http://mirrors.ustc.edu.cn/alpine/v3.10/main/" >/etc/apk/repositories
RUN apk --no-cache add python2 libsodium
COPY --from=builder /app /app
COPY config.example.json /etc/ssr/config.json
EXPOSE 1080
VOLUME [ "/etc/ssr" ]
CMD [ "python2", "/app/shadowsocks/local.py", "-c", "/etc/ssr/config.json", "start" ]
LABEL maintainer="myl7 <myl.ustc@gmail.com>" version="1.1.0"
