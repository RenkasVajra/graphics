import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображения")

        # Компоненты для отображения изображений
        self.original_image_label = tk.Label(root)
        self.original_image_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.modified_image_label = tk.Label(root)
        self.modified_image_label.pack(side=tk.RIGHT, padx=10, pady=10)

        # Компоненты для отображения данных о пикселях
        self.data_grid = ttk.Treeview(root, columns=("X", "Y", "Цвет", "Яркость"), show="headings")
        self.data_grid.pack(pady=10)
        self.data_grid.heading("X", text="X")
        self.data_grid.heading("Y", text="Y")
        self.data_grid.heading("Цвет", text="Цвет")
        self.data_grid.heading("Яркость", text="Яркость")

        # Компоненты для выбора диапазона пикселей
        self.x_start_label = tk.Label(root, text="X начало:")
        self.x_start_label.pack()
        self.x_start_entry = tk.Entry(root)
        self.x_start_entry.pack()

        self.x_end_label = tk.Label(root, text="X конец:")
        self.x_end_label.pack()
        self.x_end_entry = tk.Entry(root)
        self.x_end_entry.pack()

        self.y_start_label = tk.Label(root, text="Y начало:")
        self.y_start_label.pack()
        self.y_start_entry = tk.Entry(root)
        self.y_start_entry.pack()

        self.y_end_label = tk.Label(root, text="Y конец:")
        self.y_end_label.pack()
        self.y_end_entry = tk.Entry(root)
        self.y_end_entry.pack()

        # Кнопка для загрузки изображения
        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack(pady=10)

        # Кнопка для обработки изображения
        self.process_button = tk.Button(root, text="Обработать изображение", command=self.process_image)
        self.process_button.pack(pady=10)

        # Кнопка для очистки данных
        self.clear_button = tk.Button(root, text="Очистить данные", command=self.clear_data)
        self.clear_button.pack(pady=10)

        # Переменные для хранения изображений
        self.original_image = None
        self.modified_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.bmp *.jpg *.jpeg *.png")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.original_image.thumbnail((300, 300))  # Уменьшаем изображение для отображения
            photo = ImageTk.PhotoImage(self.original_image)
            self.original_image_label.config(image=photo)
            self.original_image_label.image = photo  # Сохраняем ссылку на изображение

    def process_image(self):
        if self.original_image:
            x_start = int(self.x_start_entry.get())
            x_end = int(self.x_end_entry.get())
            y_start = int(self.y_start_entry.get())
            y_end = int(self.y_end_entry.get())

            # Очистка данных в таблице
            self.data_grid.delete(*self.data_grid.get_children())

            # Обработка изображения
            modified_image = self.original_image.copy()
            pixels = modified_image.load()

            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    r, g, b = pixels[x, y]
                    brightness = (r + g + b) / 3
                    # Изменение цвета пикселя
                    pixels[x, y] = (255 - r, 255 - g, 255 - b)
                    # Добавление данных в таблицу
                    self.data_grid.insert("", "end", values=(x, y, f"({r}, {g}, {b})", brightness))

            # Отображение модифицированного изображения
            photo = ImageTk.PhotoImage(modified_image)
            self.modified_image_label.config(image=photo)
            self.modified_image_label.image = photo  # Сохраняем ссылку на изображение

    def clear_data(self):
        self.data_grid.delete(*self.data_grid.get_children())


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()