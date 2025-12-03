import logging
import os

class FileCorrupted(Exception):
    pass

def logged(exception_type, mode="console"):
    logger = logging.getLogger(f"{mode}_{exception_type.__name__}")
    logger.setLevel(logging.ERROR)
    if not logger.handlers:
        handler = logging.StreamHandler() if mode=="console" else logging.FileHandler("logs.yaml", encoding="utf-8")
        formatter = logging.Formatter(
            "Час: %(asctime)s\nРівень: %(levelname)s\nПовідомлення: %(message)s\n---"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as e:
                logger.error(e)
                raise
        return wrapper
    return decorator

class FileManager:

    def __init__(self, path):
        if not path.endswith(".yaml"):
            path += ".yaml"
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                f.write("data:\n")

    @logged(FileCorrupted)
    def append(self, item):
        try:
            with open(self.path, "r+", encoding="utf-8") as f:
                content = f.read()
                if not content.startswith("data:"):
                    f.seek(0, 0)
                    f.write("data:\n" + content)
                f.seek(0, 2)
                f.write(f"- {item}\n")
        except Exception:
            raise FileCorrupted("не вдалося дописати у файл")

    @logged(FileCorrupted)
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            raise FileCorrupted("не вдалося прочитати файл")

if __name__ == "__main__":
    fm = FileManager("test.yaml")

    print("dедіть елементи (порожній рядок = завершити):")
    while True:
        item = input("-> ")
        if not item:
            break
        fm.append(item)

    print("\ndміст файлу:")
    print(fm.read())
