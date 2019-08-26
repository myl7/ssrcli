FROM alpine/git:1.0.7 AS builder
RUN git clone https://github.com/shadowsocksr-backup/shadowsocksr -b manyuser /home/ssr \
 && rm -rf /home/ssr/.git*

FROM alpine:3.10
WORKDIR /home
RUN echo "http://mirrors.ustc.edu.cn/alpine/v3.10/main/" >/etc/apk/repositories
RUN apk --no-cache add python libsodium
COPY --from=builder /home/ssr ssr
COPY config.example.json /etc/ssr/config.json

EXPOSE 1080
VOLUME [ "/etc/ssr" ]
CMD [ "python", "/home/ssr/shadowsocks/local.py", "-c", "/etc/ssr/config.json", "start" ]
LABEL maintainer="myl7 <myl.ustc@gmail.com>" version="1.0.1"
