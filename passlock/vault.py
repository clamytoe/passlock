from dataclasses import dataclass
from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from .entry import Entry
from .log_init import setup_logging

logger = setup_logging()


@dataclass
class Vault:
    loc: str = ".passlock"
    key_name: str = "plock"
    documents: str = "Documents"
    extension: str = ".bin"

    def __post_init__(self):
        self.home: Path = Path.home()
        logger.debug(f"Home: {self.home}")
        self.base: Path = self.home / self.loc
        logger.debug(f"Base: {self.base}")
        self.docs: Path = self.home / self.documents
        logger.debug(f"Documents: {self.docs}")
        self.store: Path = self.docs / self.loc
        logger.debug(f"Store: {self.store}")

        if not self.base.is_dir():
            logger.info(f"Creating {self.base}")
            self.base.mkdir(mode=0o700)
            logger.info(f"Created {self.base} with 700 permissions")

        if not self.store.is_dir():
            logger.info(f"Creating {self.store}")
            self.store.mkdir(mode=0o700)
            logger.info(f"Created {self.store} with 700 permissions")

        self.plock: Path = self.base.joinpath(self.key_name)
        self.pub: Path = self.base.joinpath(f"{self.key_name}.pub")

        if not self.plock.exists():
            logger.info("Creating private/public key pairs")
            self.key = RSA.generate(4096)
            private_key = self.key.export_key()
            with self.plock.open("wb") as private:
                private.write(private_key)
            logger.info(f"Created private key:{self.plock}")
            self.plock.chmod(mode=0o600)
            logger.info(f"Changed permissions of private key to 600")

            public_key = self.key.publickey().export_key()
            with self.pub.open("wb") as pub:
                pub.write(public_key)
            logger.info(f"Created public key:{self.pub}")

    @property
    def private_key(self):
        logger.info(f"Private key accessed: {self.plock}")
        return self.plock.read_text()

    @property
    def public_key(self):
        logger.info(f"Public key accessed: {self.pub}")
        return self.pub.read_text()

    def encrypt_file(self, data):
        logger.debug(f"Encrypting data for {data.name}")
        name = data.name + self.extension
        target = self.store.joinpath(name)
        logger.info(f"Creating vault: {target}")

        logger.info(f"Importing public key: {self.pub.name}")
        pub_key = RSA.import_key(self.public_key)

        logger.info("Generating random byte for session key")
        session_key = get_random_bytes(16)
        logger.debug(f"session_key: {session_key}")

        logger.debug(f"Generating RSA key from: {self.pub.name}")
        cipher_rsa = PKCS1_OAEP.new(pub_key)
        logger.info("Generating encrypted session key")
        enc_session_key = cipher_rsa.encrypt(session_key)
        logger.debug(f"enc_session_key: {enc_session_key}")

        logger.info("Generating AES cipher")
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        logger.debug(f"cipher_aes: {cipher_aes}")

        logger.info("Encrypting data to create cipher text")
        cipher_text, tag = cipher_aes.encrypt_and_digest(repr(data).encode())
        logger.debug(f"cipher_text: {cipher_text}")
        logger.debug(f"tag: {tag}")

        logger.info(f"Writing cipher text to: {target.name}")
        self.write(target, enc_session_key, cipher_aes.nonce, tag, cipher_text)

    def decrypt_file(self, data):
        file = self.store.joinpath(f"{data}{self.extension}")
        logger.info(f"Opening file for reading: {file}")
        file_in = open(f"{file.absolute()}", "rb")
        logger.info(f"Importing private key: {self.plock.name}")
        _key = RSA.import_key(self.private_key)

        logger.info("Extracting encrypted session key")
        enc_session_key, nonce, tag, cipher_text = [
            file_in.read(x)
            for x in (_key.size_in_bytes(), 16, 16, -1)
        ]
        logger.debug(f"enc_session_key: {enc_session_key}")
        logger.debug(f"nonce: {nonce}")
        logger.debug(f"tag: {tag}")
        logger.debug(f"cipher_text: {cipher_text}")

        logger.info(f"Generating RSA cipher key from imported private key")
        cipher_rsa = PKCS1_OAEP.new(_key)
        logger.info("Decrypting extracted session key")
        session_key = cipher_rsa.decrypt(enc_session_key)
        logger.info("Session key was successfully restored")
        logger.debug(f"session_key: {session_key}")

        logger.info("Generating AES cipher from session key")
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        logger.debug(f"cipher_aes: {cipher_aes}")

        logger.info("Decrypting and verifying cipher text")
        decoded_data = cipher_aes.decrypt_and_verify(cipher_text, tag)

        logger.info(f"Closing: {file.name} ")
        file_in.close()

        logger.info("Generating new Entry object from decrypted data")
        name, url, user, passwd = decoded_data.decode("utf-8").split(",")
        d = Entry(name, url, user, passwd)
        logger.debug(f"Decrypted data: {repr(d)}")

        logger.info(f"Returning decrypted text for: {data}")
        print(d)

    @staticmethod
    def write(target, session, aes, tag, cipher):
        if target.exists():
            logger.warn(f"{target.name} already exists!")
        with target.open("wb") as t:
            [
                t.write(x)
                for x in (session, aes, tag, cipher)
            ]
        logger.info(f"Successfully wrote to: {target}")
        print(f"Successfully created: {target}")
