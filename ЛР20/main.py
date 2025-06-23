import threading
import time


class SingletonMeta(type):
    """
    Метакласс для реализации потокобезопасного Singleton.
    Использует двойную проверку блокировки (double-checked locking) для
    оптимальной работы в многопоточной среде.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    Класс Singleton с имитацией ресурсоемкой инициализации.
    Демонстрирует актуальность паттерна в многопоточной среде.
    """
    def __init__(self):
        time.sleep(1)
        self.value = "Initial Value"

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


def test_singleton(thread_id):
    """
    Функция для тестирования Singleton в разных потоках.
    Демонстрирует, как потоки работают с единым экземпляром.
    """
    singleton = Singleton()
    print(f"Thread {thread_id}: Singleton instance ID: {id(singleton)}")
    print(f"Thread {thread_id}: Initial value: {singleton.get_value()}")

    new_value = f"Value from thread {thread_id}"
    singleton.set_value(new_value)
    print(f"Thread {thread_id}: New value set: {new_value}")

    time.sleep(0.5)
    print(f"Thread {thread_id}: Final value: {singleton.get_value()}")


if __name__ == "__main__":
    print("Testing Singleton in multi-threaded environment...")

    threads = []
    for i in range(5):
        thread = threading.Thread(target=test_singleton, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All threads completed.")

    final_singleton = Singleton()
    print(f"Final singleton value: {final_singleton.get_value()}")