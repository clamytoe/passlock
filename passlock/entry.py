from dataclasses import dataclass


@dataclass
class Entry:
    name: str
    url: str
    username: str
    password: str

    def __repr__(self):
        return f"{self.name},{self.url},{self.username},{self.password}"

    def __str__(self):
        out = f"\n[{self.name}]\n"
        out += f"INFO: {self.url}\n"
        out += f"USER: {self.username}\n"
        out += f"PASS: {self.password}\n"
        return out
