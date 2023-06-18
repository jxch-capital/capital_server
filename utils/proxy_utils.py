import socket
import socks
import logging


def proxy(host='localhost', port=10808):
    logging.info(f'开启网络代理: socks5 {host}:{port}')
    socks.setdefaultproxy(socks.SOCKS5, host, port)
    socket.socket = socks.socksocket
