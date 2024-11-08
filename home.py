import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


class AnalysisApp:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Приложение дляанализа данных")
        self.main_window.geometry("800x600")

        self.dataframe = None
        self.original_dataframe = None  # Хранение исходных данных для сброса

        # Инициализация элементов интерфейса
        self.init_ui()

    def init_ui(self):
        # Кнопка для загрузки файла
        self.load_file_button = tk.Button(self.main_window,
                                          text="Загрузить файл",
                                          command=self.open_file)
        self.load_file_button.pack(pady=10)

        # Рамка для таблицы данных и скроллбаров
        self.table_frame = tk.Frame(self.main_window)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Горизонтальный скроллбар
        self.horizontal_scroll = ttk.Scrollbar(self.table_frame,
                                               orient="horizontal")
        self.horizontal_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Таблица данных с поддержкой горизонтальной прокрутки
        self.data_table =\
            ttk.Treeview(
                self.table_frame, xscrollcommand=self.horizontal_scroll.set)
        self.data_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.horizontal_scroll.config(command=self.data_table.xview)

        # Панель для кнопок анализа данных и поля для фильтрации
        self.control_panel = tk.Frame(self.main_window)
        self.control_panel.pack(pady=10)

        tk.Button(self.control_panel, text="Среднее",
                  command=self.calculate_average).grid(row=0, column=0, padx=5)
        tk.Button(self.control_panel, text="Минимум",
                  command=self.calculate_minimum).grid(row=0, column=1, padx=5)
        tk.Button(self.control_panel, text="Максимум",
                  command=self.calculate_maximum).grid(row=0, column=2, padx=5)

        # Поле для ввода номера столбца
        tk.Label(self.control_panel,
                 text="Введите номер столбца:").grid(row=1, column=0, pady=5)
        self.column_number_input = tk.StringVar()
        tk.Entry(self.control_panel,
                 textvariable=self.column_number_input,
                 width=10).grid(row=1, column=1, padx=5)

        # Поле для ввода значения фильтра и кнопка для сброса фильтрации
        self.filter_input = tk.StringVar()
        tk.Entry(self.control_panel,
                 textvariable=self.filter_input, width=20).grid(
            row=2, column=0, padx=5)
        tk.Button(self.control_panel, text="Фильтровать",
                  command=self.apply_filter).grid(row=2, column=1, padx=5)
        tk.Button(self.control_panel, text="Сбросить фильтр",
                  command=self.reset_filter).grid(row=2, column=2, padx=5)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("CSV files", "*.csv")])
        if file_path:
            try:
                # Загружаем данные с разделителем ";"
                self.dataframe = pd.read_csv(file_path, sep=';')
                self.original_dataframe = self.dataframe.copy()
                # Сохраняю оригинальные данные
                self.display_data()
            except Exception as e:
                messagebox.showerror("Ошибка",
                                     f"Не удалось загрузить файл: {e}")

    def display_data(self):
        # Очистка предыдущих данных
        self.data_table.delete(*self.data_table.get_children())
        self.data_table["column"] = [f"{i+1}: {col}" for i, col
                                     in enumerate(self.dataframe.columns)]
        self.data_table["show"] = "headings"

        # Установка заголовков столбцов с номерами
        for column in self.data_table["columns"]:
            self.data_table.heading(column, text=column)

        # Вставка данных в таблицу
        for _, row in self.dataframe.iterrows():
            self.data_table.insert("", "end",
                                   values=list(row))

    def get_selected_column(self):
        """Получаю индекс выбранного столбца на основе номера,
        введенного пользователем."""
        column_number = self.column_number_input.get()
        try:
            column_index = int(column_number) - 1
            if 0 <= column_index < len(self.dataframe.columns):
                return self.dataframe.columns[column_index]
            else:
                messagebox.showerror("Ошибка",
                                     "Номер столбца выходит "
                                     "за пределы диапазона.")
                return None
        except ValueError:
            messagebox.showerror("Ошибка",
                                 "Введите корректный номер столбца.")
            return None

    def calculate_average(self):
        column = self.get_selected_column()
        if column:
            numeric_column = pd.to_numeric(self.dataframe[column],
                                           errors='coerce')
            if pd.api.types.is_numeric_dtype(numeric_column):
                avg_value = numeric_column.mean()
                messagebox.showinfo("Среднее значение",
                                    f"Среднее значение для "
                                    f"столбца {column}: {avg_value}")
            else:
                messagebox.showerror("Ошибка",
                                     f"Столбец {column} не является числовым.")

    def calculate_minimum(self):
        column = self.get_selected_column()
        if column:
            numeric_column = pd.to_numeric(self.dataframe[column],
                                           errors='coerce')
            if pd.api.types.is_numeric_dtype(numeric_column):
                min_value = numeric_column.min()
                messagebox.showinfo("Минимальное значение",
                                    f"Минимальное значение "
                                    f"для столбца {column}: {min_value}")
            else:
                messagebox.showerror("Ошибка",
                                     f"Столбец {column} не является числовым.")

    def calculate_maximum(self):
        column = self.get_selected_column()
        if column:
            numeric_column = pd.to_numeric(self.dataframe[column],
                                           errors='coerce')
            if pd.api.types.is_numeric_dtype(numeric_column):
                max_value = numeric_column.max()
                messagebox.showinfo("Максимальное значение",
                                    f"Максимальное значение "
                                    f"для столбца {column}: {max_value}")
            else:
                messagebox.showerror("Ошибка",
                                     f"Столбец {column} не является числовым.")

    def apply_filter(self):
        if self.dataframe is None:
            messagebox.showerror("Ошибка",
                                 "Сначала загрузите данные.")
            return

        filter_text = self.filter_input.get()
        if not filter_text:
            messagebox.showwarning("Предупреждение",
                                   "Введите значение для фильтрации.")
            return

        filtered_df = self.dataframe[self.dataframe.apply(
            lambda row: row.astype(str).str.contains(filter_text).any(),
            axis=1)]
        if not filtered_df.empty:
            self.dataframe = filtered_df
            self.display_data()
        else:
            messagebox.showinfo("Результат фильтрации", "Нет строк, "
                                                        "удовлетворяющих "
                                                        "фильтру.")

    def reset_filter(self):
        """Сброс фильтра и восстановление исходных данных."""
        if self.original_dataframe is not None:
            self.dataframe = self.original_dataframe.copy()
            self.display_data()
            self.filter_input.set("")  # Очистка поля фильтра


if __name__ == "__main__":

    main_window = tk.Tk()
    app = AnalysisApp(main_window)
    main_window.mainloop()
