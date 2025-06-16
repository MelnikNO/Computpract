# Лабораторная работа № 16

## Задание

Цель работы

Показать, как при недостаточно строгом уровне изоляции транзакций в базе данных возможно возникновение аномалии «Потерянное обновление», привести пример её проявления и предложить способы предотвращения.

[полный текст задания](https://drive.google.com/file/d/1itv97nkbvWf4nla12wF9Yy_rjsPnvpW0/view?usp=sharing)

---

## Решение

Postgres использовался через сервис Supabase.

Для создания таблиц были написаны SQL-запросы:

```
-- Таблица книг
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Таблица филиалов
CREATE TABLE branches (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Таблица запасов
CREATE TABLE stock (
  book_id INT REFERENCES books(id),
  branch_id INT REFERENCES branches(id),
  quantity INT NOT NULL CHECK (quantity >= 0),
  PRIMARY KEY (book_id, branch_id)
);

-- Таблица перемещений
CREATE TABLE movements (
  id SERIAL PRIMARY KEY,
  book_id INT REFERENCES books(id),
  quantity INT NOT NULL,
  from_branch_id INT REFERENCES branches(id),
  to_branch_id INT REFERENCES branches(id),
  movement_time TIMESTAMP DEFAULT NOW()
);
```

```
-- Функция для проверки и блокировки запасов
CREATE OR REPLACE FUNCTION check_and_lock_stock(
  p_book_id INT,
  p_branch_id INT
) RETURNS TABLE(book_id INT, branch_id INT, quantity INT) AS $$
BEGIN
  RETURN QUERY 
  SELECT s.book_id, s.branch_id, s.quantity 
  FROM stock s
  WHERE s.book_id = p_book_id AND s.branch_id = p_branch_id
  FOR UPDATE;
END;
$$ LANGUAGE plpgsql;

-- Функция для обновления запасов
CREATE OR REPLACE FUNCTION update_stock(
  p_book_id INT,
  p_branch_id INT,
  p_quantity INT
) RETURNS VOID AS $$
BEGIN
  INSERT INTO stock (book_id, branch_id, quantity)
  VALUES (p_book_id, p_branch_id, GREATEST(p_quantity, 0))
  ON CONFLICT (book_id, branch_id)
  DO UPDATE SET quantity = GREATEST(stock.quantity + EXCLUDED.quantity, 0);
END;
$$ LANGUAGE plpgsql;

-- Упрощённая функция для перемещения книг
CREATE OR REPLACE FUNCTION move_books_safe(
  p_book_id INT,
  p_from_branch_id INT,
  p_to_branch_id INT,
  p_quantity INT
) RETURNS JSON AS $$
DECLARE
  current_quantity INT;
BEGIN
  -- Проверка и блокировка
  SELECT quantity INTO current_quantity
  FROM stock 
  WHERE book_id = p_book_id AND branch_id = p_from_branch_id
  FOR UPDATE;
  
  IF NOT FOUND OR current_quantity < p_quantity THEN
    RETURN json_build_object('error', 'Недостаточно книг в филиале-отправителе');
  END IF;
  
  -- Обновление запасов
  UPDATE stock SET quantity = quantity - p_quantity
  WHERE book_id = p_book_id AND branch_id = p_from_branch_id;
  
  INSERT INTO stock (book_id, branch_id, quantity)
  VALUES (p_book_id, p_to_branch_id, p_quantity)
  ON CONFLICT (book_id, branch_id)
  DO UPDATE SET quantity = stock.quantity + EXCLUDED.quantity;
  
  -- Логирование
  INSERT INTO movements (book_id, quantity, from_branch_id, to_branch_id)
  VALUES (p_book_id, p_quantity, p_from_branch_id, p_to_branch_id);
  
  RETURN json_build_object('success', true);
EXCEPTION WHEN OTHERS THEN
  RETURN json_build_object('error', SQLERRM);
END;
$$ LANGUAGE plpgsql;
```

Для переменных окружений, которые используются в программе, создан файл .env.

Программа в файле [main.py](https://github.com/MelnikNO/Computpract/blob/main/ЛР16/main.py).

**Результат программы:**

![image](https://github.com/user-attachments/assets/b81a8410-b6b9-402b-92e0-196c0b523878)

![image](https://github.com/user-attachments/assets/af7404d3-e03e-4cb0-b4a0-8fc1387c00cd)

![image](https://github.com/user-attachments/assets/b95e2cfd-76fa-4b2b-869c-4a1dc7f1a3c6)

![image](https://github.com/user-attachments/assets/5c5316c7-117e-499c-91aa-1988371cb8df)

![image](https://github.com/user-attachments/assets/c74de395-e0b2-49fb-9bc4-50953cd022a2)


**Способы предотвращения:**

- Явные блокировки (FOR UPDATE)
- Оптимистичные блокировки
- Использование строгих уровней изоляции
- Атомарные операции
- Очередь операций (для высоконагруженных систем)


