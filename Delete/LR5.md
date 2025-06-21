# Лабораторная работа №5

## Задание

Задание - доделать проект по WebAssembly - budget_planner_project.zip

1. Изучить файл README.md внутри проекта и сделать первичное изучение кода самого проекта, понять общих принцип работы кода.
2. Скачать и установить компилятор для WebAssembly с сайта https://emscripten.org (см. README.md).
3. Добиться компиляции и работы самого приложения.
4. Самостоятельно придумать какое-либо улучшение (improvment) для проекта, основываясь на исходных примерах кода в проекте.
5. Сделать отчёт о проделано работе в формате Markdown.
6. Закомитить всё в один репозиторий на GitHub и прислать ответ в виде ссылке на него.

## Решение 

Выполнить через https://emscripten.org не удалось из-за ошибки

![image](https://github.com/user-attachments/assets/54a7e424-eba3-49ce-9ada-98c4c0fdf774)

Поэтому был рассмотрен вариант решения через Docker-образ:

* Запуск контейнера с Emscripten

```
docker pull emscripten/emsdk
```

```
docker run -it --rm -v ${PWD}:/src emscripten/emsdk bash
```

* Работа внутри контейнера

Переходим в директорию с проектом

```
cd /src
```

Проверяем файлы

```
ls -la
```

* Компиляция проекта

Выполняем команду из README.md, адаптированную для Docker

```
emcc main.c -o index.js -s WASM=1 -O2 \
-s EXPORTED_RUNTIME_METHODS='["stringToUTF8","UTF8ToString"]' \
-s EXPORTED_FUNCTIONS='["_main","_jsAddExpense","_jsDeleteExpense","_jsClearAllExpenses","_jsGetTotalExpenses","_jsGetExpenseCount","_jsGetCategoryCount","_getExpenseJSON","_getCategoryTotalJSON","_freeMemory","_malloc","_free"]' \
--shell-file index.html -s ALLOW_MEMORY_GROWTH=1
```

* Запуск приложения

Выходим из контейнера

```
exit
```

Запускаем веб-сервер для тестирования

```
python -m http.server 8000
```

Открываем в браузере адрес

```
http://localhost:8000
```

![image](https://github.com/user-attachments/assets/34224a82-2532-481c-a4b6-28956731e83b)

![image](https://github.com/user-attachments/assets/543890bb-2d0b-412d-8ac3-b89dfb238554)


**Веб-приложение**

![image](https://github.com/user-attachments/assets/8a3ab9e2-cb24-4a05-ac22-21aff6a37496)


