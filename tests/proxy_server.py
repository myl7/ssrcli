from twisted.web import proxy, http
from twisted.internet import reactor

PROXY_TEST_SERVER_PORT = 8002


class ProxyFactory(http.HTTPFactory):
    protocol = proxy.Proxy


if __name__ == '__main__':
    try:
        port = reactor.listenTCP(PROXY_TEST_SERVER_PORT, ProxyFactory())
        reactor.run()
    finally:
        reactor.disconnectAll()
