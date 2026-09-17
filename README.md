# MicroPython на ESP32 — курс лекцій та лабораторних робіт

Матеріали університетського курсу з програмування мікроконтролерів ESP32 мовою MicroPython: конспект лекцій та чотири лабораторні роботи.

## Вміст репозиторію

- `Lecture_Course_MicroPython_ESP32.ipynb` — конспект лекцій (16 розділів): цифрові GPIO, ADC/PWM, таймери й переривання, UART, I2C/SPI та інша периферія, з питаннями для самоперевірки після кожного розділу.
- `Lab_work_1.ipynb` — Лабораторна робота №1. Цифрові GPIO.
- `Lab_work_2.ipynb` — Лабораторна робота №2. ADC та PWM.
- `Lab_work_3.ipynb` — Лабораторна робота №3. Таймери, переривання та UART.
- `Lab_work_4.ipynb` — Лабораторна робота №4. I2C/SPI периферія.
- `regenerate_pdfs.py` — скрипт для самостійної генерації PDF з `.ipynb` (налаштовує підтримку кирилиці в nbconvert/xelatex і експортує всі ноутбуки).

## Завантажити PDF

Готові PDF-версії не зберігаються в репозиторії — вони публікуються як файли [релізу](../../releases/latest):

- 📘 [Конспект лекцій (PDF)](../../releases/latest/download/Lecture_Course_MicroPython_ESP32.pdf)
- 📝 [Лабораторна робота №1 (PDF)](../../releases/latest/download/Lab_work_1.pdf)
- 📝 [Лабораторна робота №2 (PDF)](../../releases/latest/download/Lab_work_2.pdf)
- 📝 [Лабораторна робота №3 (PDF)](../../releases/latest/download/Lab_work_3.pdf)
- 📝 [Лабораторна робота №4 (PDF)](../../releases/latest/download/Lab_work_4.pdf)

Посилання завжди ведуть на файли з останнього релізу.

## Як згенерувати PDF самостійно

```bash
pip install jupyter nbconvert
python3 regenerate_pdfs.py
```

Потрібен встановлений `xelatex` (повний дистрибутив TeX) — скрипт перевіряє наявність усіх залежностей і виводить інструкції з встановлення під поточну ОС, якщо чогось бракує.

## Автор

Пахалюк Богдан
