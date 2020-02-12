#!/usr/bin/env python3
"""
app.py

Password Locker
"""
from dataclasses import dataclass
from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from .log_init import setup_logging

logger = setup_logging()


@dataclass
class Vault:
    loc: str = ".passlock"
    key_name: str = "plock"
    documents: str = "Documents"

    def __post_init__(self):
        self.home: Path = Path.home()
        self.base: Path = self.home / self.loc
        self.docs: Path = self.home / self.documents

        if not self.base.is_dir():
            logger.info(f"Creating BASE_DIR: {self.base}")
            self.base.mkdir(mode=0o700, exist_ok=True)

        self.plock: Path = self.base.joinpath(self.key_name)
        self.pub: Path = self.base.joinpath(f"{self.key_name}.pub")

        if not self.plock.exists():
            self.key = RSA.generate(4096)
            private_key = self.key.export_key()
            with self.plock.open("wb") as private:
                private.write(private_key)
            self.plock.chmod(mode=0o600)

            public_key = self.key.publickey().export_key()
            with self.pub.open("wb") as pub:
                pub.write(public_key)

    @property
    def private_key(self):
        return self.plock.read_bytes()

    @property
    def public_key(self):
        return self.pub.read_bytes()

    def encrypt_file(self, data, save_to="pwds.toe"):
        source = self.docs.joinpath(data)
        target = self.docs.joinpath(save_to)
        if source.exists():
            source_data = source.read_bytes()
            pub_key = RSA.import_key(self.public_key)
            session_key = get_random_bytes(16)

            cipher_rsa = PKCS1_OAEP.new(pub_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            cipher_text, tag = cipher_aes.encrypt_and_digest(source_data)
            [target.write_bytes(x) for x in (enc_session_key, cipher_aes.nonce, tag, cipher_text)]
            if source.exists():
                print(f"Successfully created: {target}")
            else:
                print("Something went wrong...")
        else:
            print(f"{source}, does not exist!")


def main():
    logger.debug("Entering main.")
    v = Vault()
    if v.plock.is_file():
        print(f"Private Key [{v.plock}]: {v.private_key}")
    else:
        print(f"Private key, {v.plock}, not found!")

    if v.pub.is_file():
        print(f" Public Key [{v.pub}]: {v.public_key}")
    else:
        print(f"Public key, {v.pub}, not found!")

    v.encrypt_file("newtek.txt")


if __name__ == "__main__":
    logger.debug("Running as a module.")
    main()
