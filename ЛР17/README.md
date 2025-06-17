# Лабораторная работа № 17

## Задание

Вам необходимо настроить проект с помощью пакетного менеджера Poetry. Нужно будет настроить разные окружения (dev и prod), установить зависимости, запустить тесты и основную программу в разных средах. Выполнить анализ деревьев зависимостей и оформить отчет. Более подробная информация по заданию и отчету в методических рекомендациях.

Контакты для связи: @vishnya_chern (тг)

[Методичка по лабораторной работе «Настройка проекта калькулятора с помощью Poetry».pdf](https://moodle.herzen.spb.ru/pluginfile.php/1824203/mod_assign/introattachment/0/Методичка%20по%20лабораторной%20работе%20«Настройка%20проекта%20калькулятора%20с%20помощью%20Poetry».pdf?forcedownload=1)

## Решение

**1 шаг: Установки зависимостей**

![image_2025-06-17_20-20-03](https://github.com/user-attachments/assets/45fd8c8e-8390-4e11-bbcb-8c317816a77e)

Создаем вручную файл pyproject.toml и заполняем

![image_2025-06-17_22-53-22](https://github.com/user-attachments/assets/ff9410df-82b5-4f8f-bac8-f6e5298d81c3)

![image_2025-06-17_22-55-45](https://github.com/user-attachments/assets/180a158c-5376-4d86-be1b-e419d0e6218d)


**2 шаг: Запуск тестов и основной программы**

Запуск test/test_core.py

![image_2025-06-17_23-14-09](https://github.com/user-attachments/assets/bfa7f288-90fd-461d-8613-475184e0508f)

Запуск main.py

![image_2025-06-17_23-17-15](https://github.com/user-attachments/assets/c37b507d-0540-40ca-b4e1-2e367fb20574)

Генерация документации calc-history.log.txt

![image_2025-06-17_23-20-52](https://github.com/user-attachments/assets/ae179d71-ba65-4d3f-9db5-48115d27fe0f)

**3 шаг: Анализ деревьев зависимостей**

Общее дерево зависимостей

![image_2025-06-17_23-22-09](https://github.com/user-attachments/assets/83029a50-c73d-46eb-9725-8fbd05581463)

Только prod-зависимости

![image_2025-06-17_23-23-07](https://github.com/user-attachments/assets/fba8fcb1-8474-4fe8-9910-eef422cfceb5)

Только dev-зависимости

![image_2025-06-17_23-24-17](https://github.com/user-attachments/assets/5d7a8aa2-0e9d-49cd-892a-6743c30c9e36)

