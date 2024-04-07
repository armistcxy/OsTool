def log(x) -> None:
    with open("log.txt", "a") as f:
        f.write(f"{x}\n")


def refresh(path: str) -> None:
    with open(path, "w") as f:
        f.truncate()
