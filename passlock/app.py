#!/usr/bin/env python3
"""
app.py

Password Locker
"""
from .entry import Entry
from .vault import Vault, logger


def main():
    logger.debug("Entering main.")
    ip = Entry("ip", "http://192.168.2.1", "admin", "admin")
    # local = Entry("local", "http://localhost:8080", "user", "password1")

    v = Vault()
    v.encrypt_file(ip)
    # v.encrypt_file(local)
    v.decrypt_file(ip.name)
    # v.decrypt_file(local.name)


if __name__ == "__main__":
    logger.debug("Running as a module.")
    main()
