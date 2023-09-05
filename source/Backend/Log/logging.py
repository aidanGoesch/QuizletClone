import pathlib

def reset_log() -> None:
    file_path = pathlib.Path("source/Backend/Log/log.txt")
    with open(file_path, "w") as file:
        file.write("### EVENT LOG ###")


def log(text: str) -> None:
    file_path = pathlib.Path("source/Backend/Log/log.txt")
    with file_path.open(mode = "a") as file:
        file.write(f"\n{text}")



if __name__ == '__main__':
    reset_log()
    log('this is bad')
    log('ss')