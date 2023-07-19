import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
import csv

# Список доменов почтовых сервисов, которые мы хотим исключить
excluded_domains = ["mail.ru", "gmail.com", "yandex.ru", "outlook.com", "bk.ru", "ya.ru", "k-syndicate.school",
                    "ukr.net", "tut.by", "hotmail.com", "i.ua", "list.ru", "icloud.com", "inbox.ru",
                    "googlemail.com", "crona.studio", "yandex.by", "yandex.com", "rambler.ru", "live.ru",
                    "narod.ru", "mail.ua", "gmai.com", "meta.ua", "iziink.tattoo", "inbox.lv"]

def extract_campaigns(email_file, output_file):
    emails = []
    with open(email_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row or not row[0].strip():
                continue
            email = row[0]
            emails.append(email)

    # Словарь для хранения кампаний и их соответствующих адресов электронной почты
    campaigns = {}

    # Регулярное выражение для извлечения названия кампании после "@"
    pattern = re.compile(r"@([a-zA-Z0-9.-]+)")

    for email in emails:
        match = pattern.search(email)
        if match:
            domain = match.group(1).lower()
            if domain not in excluded_domains:
                campaign_name = domain
                if campaign_name not in campaigns:
                    campaigns[campaign_name] = []
                campaigns[campaign_name].append(email)

    # Записываем результаты в другой CSV файл
    with open(output_file, "w", newline="") as output_csv_file:
        writer = csv.writer(output_csv_file)
        writer.writerow(["Кампания", "Адреса электронной почты"])
        for campaign, email_list in campaigns.items():
            unique_emails = set(email_list)
            writer.writerow([campaign, ", ".join(unique_emails)])

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def process():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()

    if not input_file or not output_file:
        messagebox.showwarning("Ошибка", "Пожалуйста, укажите файлы ввода и вывода.")
        return

    try:
        extract_campaigns(input_file, output_file)
        messagebox.showinfo("Успех", "Извлечение кампаний завершено успешно!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

app = tk.Tk()
app.title("K-Syndicate extractor")

input_file_label = tk.Label(app, text="Файл с имейлами(CSV):")
input_file_label.pack()

input_file_entry = tk.Entry(app, width=50)
input_file_entry.pack()

input_file_browse_btn = tk.Button(app, text="Обзор", command=browse_input_file)
input_file_browse_btn.pack()

output_file_label = tk.Label(app, text="Файл для сохранения (CSV):")
output_file_label.pack()

output_file_entry = tk.Entry(app, width=50)
output_file_entry.pack()

output_file_browse_btn = tk.Button(app, text="Обзор", command=browse_output_file)
output_file_browse_btn.pack()

process_btn = tk.Button(app, text="Извлечь кампании", command=process)
process_btn.pack()

app.mainloop()
