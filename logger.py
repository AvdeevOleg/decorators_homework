import datetime

# Декоратор, который логгирует вызовы функций в файл main.log
def logger(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        log_entry = f"{datetime.datetime.now()} - {old_function.__name__} called with args: {args}, kwargs: {kwargs}. Returned: {result}\n"
        with open("main.log", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
        return result
    return new_function

# Параметризованный декоратор, который логгирует вызовы функций в указанный файл
def logger_with_path(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            log_entry = f"{datetime.datetime.now()} - {old_function.__name__} called with args: {args}, kwargs: {kwargs}. Returned: {result}\n"
            with open(path, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
            return result
        return new_function
    return __logger
