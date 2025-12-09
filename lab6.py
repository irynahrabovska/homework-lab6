import logging
import os
import yaml

class FileCorrupted(Exception):
    """Raised when YAML file cannot be read or written."""
    pass

def logged(exception_type, mode="console"):
    logger = logging.getLogger(f"{mode}_{exception_type.__name__}")
    logger.setLevel(logging.ERROR)
    
    if not logger.handlers:
        handler = (logging.StreamHandler()
                   if mode == "console"
                   else logging.FileHandler("logs.txt", encoding="utf-8"))

        formatter = logging.Formatter(
            "Time: %(asctime)s\n"
            "Level: %(levelname)s\n"
            "Message: %(message)s\n"
            "---"
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

    def __init__(self, path: str):
        if not path.endswith(".yaml"):
            path += ".yaml"
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as file:
                yaml.safe_dump({"data": []}, file, allow_unicode=True)

    @logged(FileCorrupted, mode="file")
    def append(self, item: str):
        """
        Append new item into YAML data list.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                content = yaml.safe_load(file) or {}
            if "data" not in content or not isinstance(content["data"], list):
                content["data"] = []
            content["data"].append(item)

            with open(self.path, "w", encoding="utf-8") as file:
                yaml.safe_dump(content, file, allow_unicode=True)

        except Exception as e:
            raise FileCorrupted(f"Failed to append item: {e}")
    @logged(FileCorrupted, mode="file")
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return f.read()
        except Exception as e:
            raise FileCorrupted(f"Failed to read file: {e}")

def main():
    manager = FileManager("test.yaml")

    print("Enter items (empty line = finish):")
    while True:
        text = input("-> ").strip()
        if not text:
            break
        manager.append(text)

    print("\nFile content:")
    print(manager.read())
    
if __name__ == "__main__":
    main()

    
