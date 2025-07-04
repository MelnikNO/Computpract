# Лабораторная работа № 20

## Задание

Необходимо придумать и написать код с собственной реализацией паттерна Singleton, где присутствует многопоточность. В комментарии к коду требуется обосновать актуальность использования данного паттерна для этой задачи.

## Решение

Код содержится в файле [main.py](https://github.com/MelnikNO/Computpract/blob/main/ЛР20/main.py)

Актуальность использования паттерна Singleton для данной задачи:

1. Ресурсоемкая инициализация:
   - Долгая инициализация (time.sleep(1)) имитирует создание подключения к БД
   - Singleton гарантирует, что эта операция выполнится только один раз

2. Многопоточная среда:
   - Без Singleton каждый поток создавал бы свой экземпляр, что привело бы к:
     * Избыточному расходу ресурсов
     * Конфликтам при работе с общими ресурсами
   - Двойная проверка блокировки предотвращает race condition

3. Согласованность состояния:
   - Все потоки работают с единым экземпляром
   - Изменения состояния (set_value) видны всем потокам

4. Практические применения:
   - Подключения к базе данных
   - Логгеры системы
   - Кеширование данных
   - Конфигурация приложения

5. Экономия ресурсов:
   - Исключается дублирование функциональности
   - Оптимизируется использование памяти

**Результат**

![image](https://github.com/user-attachments/assets/5c998f66-da2c-477c-9701-1d6bc53795dd)

