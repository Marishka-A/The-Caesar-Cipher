import tkinter as tk
from tkinter import scrolledtext
import re

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифр Цезаря")
        self.root.geometry("800x600")

        # Цвета
        self.error_color = "#ffcccc"
        self.normal_color = "white"

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Ввод текста
        tk.Label(self.root, text="Исходный текст:").pack(pady=(10, 0))
        self.text_input = scrolledtext.ScrolledText(self.root, height=5, wrap=tk.WORD)
        self.text_input.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Ключ
        tk.Label(self.root, text="Ключ:").pack()
        self.key_entry = tk.Entry(self.root)
        self.key_entry.pack(fill=tk.X, padx=10)

        # Кнопки действий
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Зашифровать", command=self.encrypt).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Расшифровать", command=self.decrypt).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Взломать", command=self.crack).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=5)

        # Результат
        tk.Label(self.root, text="Результат:").pack()
        self.result_text = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state='disabled')
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Статус
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_var, fg="red")
        self.status_label.pack()

    def show_error(self, message):
        self.status_var.set(message)
        self.status_label.config(fg="red")

    def clear_error(self):
        self.status_var.set("")

    def clear(self):
        self.text_input.delete(1.0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')
        self.clear_error()

    def preprocess_text(self, text):
        # Замена ё на е
        text = text.replace('ё', 'е').replace('Ё', 'е')

        # Удаление всех небуквенных символов и приведение к нижнему регистру
        text = re.sub(r'[^a-zA-Zа-яА-Я]', '', text.lower())

        return text

    def format_output(self, text):
        # Разбиение на группы по 5 символов
        grouped = ' '.join(text[i:i + 5] for i in range(0, len(text), 5))
        return grouped

    def validate_key(self, key_str, alphabet_type):
        try:
            key = int(key_str)
        except ValueError:
            self.show_error("Ключ должен быть целым числом")
            return None

        if alphabet_type == 'cyrillic':
            key = key % 32
        elif alphabet_type == 'latin':
            key = key % 26

        return key

    def detect_alphabet(self, text):
        has_cyrillic = bool(re.search('[а-я]', text))
        has_latin = bool(re.search('[a-z]', text))

        if has_cyrillic and has_latin:
            self.show_error("Текст должен содержать только кириллицу или только латиницу")
            return None
        elif has_cyrillic:
            return 'cyrillic'
        elif has_latin:
            return 'latin'
        else:
            self.show_error("Текст должен содержать буквы (кириллицу или латиницу)")
            return None

    def caesar_cipher(self, text, key, mode='encrypt'):
        # Определение алфавита
        alphabet_type = self.detect_alphabet(text)
        if not alphabet_type:
            return None

        # Обработка ключа
        processed_key = self.validate_key(key, alphabet_type)
        if processed_key is None:
            return None

        if mode == 'decrypt':
            processed_key = -processed_key

        result = []

        for char in text:
            if alphabet_type == 'cyrillic' and 'а' <= char <= 'я':
                # Кириллица
                shifted = ord(char) - ord('а')
                shifted = (shifted + processed_key) % 32
                result.append(chr(shifted + ord('а')))
            elif alphabet_type == 'latin' and 'a' <= char <= 'z':
                # Латиница
                shifted = ord(char) - ord('a')
                shifted = (shifted + processed_key) % 26
                result.append(chr(shifted + ord('a')))
            else:
                # Пропускаем символы, не входящие в алфавит
                continue

        return ''.join(result)

    def encrypt(self):
        self.clear_error()
        text = self.text_input.get(1.0, tk.END).strip()
        key = self.key_entry.get().strip()

        if not text:
            self.show_error("Введите текст для зашифрования")
            return

        if not key:
            self.show_error("Введите ключ")
            return

        # Предварительная обработка текста
        processed_text = self.preprocess_text(text)

        # Шифрование
        encrypted = self.caesar_cipher(processed_text, key, 'encrypt')
        if encrypted is None:
            return

        # Форматирование вывода
        formatted = self.format_output(encrypted)

        # Вывод результата
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, formatted)
        self.result_text.config(state='disabled')

    def decrypt(self):
        self.clear_error()
        text = self.text_input.get(1.0, tk.END).strip()
        key = self.key_entry.get().strip()

        if not text:
            self.show_error("Введите текст для расшифрования")
            return

        if not key:
            self.show_error("Введите ключ")
            return

        # Предварительная обработка текста
        processed_text = self.preprocess_text(text)

        # Расшифрование
        decrypted = self.caesar_cipher(processed_text, key, 'decrypt')
        if decrypted is None:
            return

        # Форматирование вывода
        formatted = self.format_output(decrypted)

        # Вывод результата
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, formatted)
        self.result_text.config(state='disabled')

    def crack(self):
        self.clear_error()
        text = self.text_input.get(1.0, tk.END).strip()

        if not text:
            self.show_error("Введите текст для взлома")
            return

        # Предварительная обработка текста
        processed_text = self.preprocess_text(text)

        # Определение языка текста
        alphabet_type = self.detect_alphabet(processed_text)
        if not alphabet_type:
            return

        if alphabet_type == 'cyrillic':
            # Частоты букв в русском языке (порядок: а-я)
            freq_table = [
                0.062, 0.014, 0.038, 0.013, 0.025, 0.072, 0.007, 0.016,
                0.062, 0.010, 0.028, 0.035, 0.026, 0.053, 0.090, 0.023,
                0.040, 0.045, 0.053, 0.021, 0.002, 0.009, 0.003, 0.012,
                0.006, 0.003, 0.014, 0.016, 0.014, 0.003, 0.006, 0.018
            ]
            alphabet_size = 32
        elif alphabet_type == 'latin':
            # Частоты букв в английском языке (порядок: a-z)
            freq_table = [
                0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                0.00978, 0.02360, 0.00150, 0.01974, 0.00074
            ]
            alphabet_size = 26

        # Подсчет частот в зашифрованном тексте
        text_len = len(processed_text)
        text_freq = [0] * alphabet_size

        for char in processed_text:
            if alphabet_type == 'cyrillic' and 'а' <= char <= 'я':
                idx = ord(char) - ord('а')
                text_freq[idx] += 1
            elif alphabet_type == 'latin' and 'a' <= char <= 'z':
                idx = ord(char) - ord('a')
                text_freq[idx] += 1

        text_freq = [f / text_len for f in text_freq]

        # Метод наименьших квадратов для поиска ключа
        min_error = float('inf')
        best_key = 0

        for shift in range(alphabet_size):
            error = 0.0
            for i in range(alphabet_size):
                shifted_i = (i - shift) % alphabet_size
                error += (text_freq[i] - freq_table[shifted_i]) ** 2

            if error < min_error:
                min_error = error
                best_key = shift

        # Расшифровка с найденным ключом
        decrypted = self.caesar_cipher(processed_text, str(best_key), 'decrypt')

        # Форматирование вывода
        formatted = self.format_output(decrypted)

        # Вывод результата
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END,
                                f"Найденный ключ: {best_key}\nЯзык: {'русский' if alphabet_type == 'cyrillic' else 'английский'}\n\n")
        self.result_text.insert(tk.END, formatted)
        self.result_text.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherApp(root)
    root.mainloop()