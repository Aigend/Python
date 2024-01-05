"""
    ssl cert function
    path: /etc/ssl/cgw
"""


def get_trust_chain():
    return "/etc/ssl/cgw/trust_chain.pem"


def get_cert():
    return "/etc/ssl/cgw/tls_lion_cert.pem"


def get_private_key():
    return "/etc/ssl/cgw/tls_lion_priv_key.pem"
