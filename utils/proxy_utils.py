import socket
import socks
import logging


def proxy(proxy_host, proxy_port):
    logging.log(logging.INFO, f'开启网络代理: socks5 {proxy_host}:{proxy_port}')
    socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
    socket.socket = socks.socksocket
