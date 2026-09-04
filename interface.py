import tkinter as tk
from tkinter import ttk, messagebox
from library import Library, Book, Student, Teacher, Guest
from parser import load_books

def run():
    library = Library()

    for book in load_books("books.txt"):
        library.add_book(book)

    student = Student(1, "Иван")
    teacher = Teacher(2, "Алексей")
    guest = Guest(3, "Пётр")

    library.add_user(student)
    library.add_user(teacher)
    library.add_user(guest)

    window = tk.Tk()
    window.title("Библиотека")
    window.geometry("900x600")

    ttk.Label(window, text="Библиотека", font=("Arial", 20)).pack(pady=15)

    search_frame = ttk.Frame(window)
    search_frame.pack(pady=5)

    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=5)

    search_type = ttk.Combobox(search_frame, values=["Название", "Автор", "ISBN"], state="readonly", width=12)
    search_type.set("Название")
    search_type.pack(side="left", padx=5)

    search_button = ttk.Button(search_frame, text="Найти")
    search_button.pack(side="left", padx=5)

    columns = ("title", "author", "isbn", "status")

    books_table = ttk.Treeview(window, columns=columns, show="headings")


    books_table.heading("title", text="Название")
    books_table.heading("author", text="Автор")
    books_table.heading("isbn", text="ISBN")
    books_table.heading("status", text="Статус")

    books_table.column("title", width=230)
    books_table.column("author", width=180)
    books_table.column("isbn", width=200)
    books_table.column("status", width=100)

    books_table.pack(fill="both", expand=True, padx=20, pady=10)

    user_frame = ttk.Frame(window)
    user_frame.pack(pady=5)

    ttk.Label(user_frame, text="Пользователь:").pack(side="left", padx=5)

    user_select = ttk.Combobox(user_frame, values=[user.name for user in library.get_users().values()], state="readonly", width=20)
    user_select.set(student.name)
    user_select.pack(side="left")

    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)

    issue_button = ttk.Button(button_frame, text="Выдать")
    issue_button.pack(side="left", padx=4)

    return_button = ttk.Button(button_frame, text="Вернуть")
    return_button.pack(side="left", padx=4)

    update_button = ttk.Button(button_frame, text="Все книги")
    update_button.pack(side="left", padx=4)

    overdue_button = ttk.Button(button_frame, text="Просроченные")
    overdue_button.pack(side="left", padx=4)

    user_books_button = ttk.Button(button_frame, text="Книги пользователя")
    user_books_button.pack(side="left", padx=4)

    button_frame2 = ttk.Frame(window)
    button_frame2.pack(pady=5)

    add_button = ttk.Button(button_frame2, text="Добавить книгу")
    add_button.pack(side="left", padx=5)

    delete_button = ttk.Button(button_frame2, text="Удалить книгу")
    delete_button.pack(side="left", padx=5)

    add_user_button = ttk.Button(button_frame2, text="Добавить пользователя")
    add_user_button.pack(side="left", padx=5)

    def update_table(books=None):
        for item in books_table.get_children():
            books_table.delete(item)
        if books is None:
            books = library.get_books().values()
        for book in books:
            status = "+" if book.status == "Available" else f"Выдана до {book.return_date.strftime('%d.%m.%Y')}"
            books_table.insert("", "end", values=(book.title, book.author, book.isbn, status))

    def search_books():
        text = search_entry.get()
        if not text:
            update_table()
            return
        if search_type.get() == "Название":
            books = library.find_by_title(text)
        elif search_type.get() == "Автор":
            books = library.find_by_author(text)
        else:
            book = library.find_by_isbn(text)
            books = [] if book is None else [book]
        update_table(books)

    def get_selected_book():
        selected = books_table.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите книгу")
            return None
        values = books_table.item(selected[0], "values")
        return library.get_book(values[2])

    def get_selected_user():
        name = user_select.get()
        for user in library.get_users().values():
            if user.name == name:
                return user
        return None

    def issue_book():
        book = get_selected_book()
        if book is None:
            return
        user = get_selected_user()
        if user is None:
            messagebox.showwarning("Ошибка", "Выберите пользователя")
            return
        if user.take_book(book, library):
            messagebox.showinfo("Библиотека", f"Книга выдана пользователю {user.name}")
        else:
            messagebox.showwarning("Ошибка", "Книгу невозможно выдать")
        update_table()

    def return_book():
        book = get_selected_book()
        if book is None:
            return
        if book.status == "Available":
            messagebox.showwarning("Ошибка", "Книга не выдана")
            return
        user = book.user
        user.return_book(book, library)
        messagebox.showinfo("Библиотека", f"Книга возвращена пользователем {user.name}")
        update_table()

    def show_overdue_books():
        update_table(library.overdue_books())

    def show_user_books():
        user = get_selected_user()
        if user is None:
            return
        update_table(user.get_books())

    def add_book():
        add_window = tk.Toplevel(window)
        add_window.title("Добавить книгу")
        add_window.geometry("300x250")

        ttk.Label(add_window, text="ISBN").pack(pady=5)
        isbn_entry = ttk.Entry(add_window, width=30)
        isbn_entry.pack()

        ttk.Label(add_window, text="Название").pack(pady=5)
        title_entry = ttk.Entry(add_window, width=30)
        title_entry.pack()

        ttk.Label(add_window, text="Автор").pack(pady=5)
        author_entry = ttk.Entry(add_window, width=30)
        author_entry.pack()

        def save_book():
            isbn = isbn_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            if not isbn or not title or not author:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            if library.find_by_isbn(isbn) is not None:
                messagebox.showwarning("Ошибка", "Книга с таким ISBN уже существует")
                return
            library.add_book(Book(isbn, title, author))
            update_table()
            add_window.destroy()

        ttk.Button(add_window, text="Добавить", command=save_book).pack(pady=15)

    def delete_book():
        book = get_selected_book()
        if book is None:
            return
        if book.status == "Issued":
            messagebox.showwarning("Ошибка", "Нельзя удалить выданную книгу")
            return
        if messagebox.askyesno("Удаление", f"Удалить книгу «{book.title}»?"):
            library.delete_book(book.isbn)
            update_table()

    def add_user():
        add_window = tk.Toplevel(window)
        add_window.title("Добавить пользователя")
        add_window.geometry("300x300")

        ttk.Label(add_window, text="ID").pack(pady=5)
        id_entry = ttk.Entry(add_window, width=30)
        id_entry.pack()

        ttk.Label(add_window, text="Имя").pack(pady=5)
        name_entry = ttk.Entry(add_window, width=30)
        name_entry.pack()

        ttk.Label(add_window, text="Тип пользователя").pack(pady=5)
        user_type = ttk.Combobox(add_window, values=["Студент", "Преподаватель", "Гость"], state="readonly", width=27)
        user_type.set("Студент")
        user_type.pack()

        def save_user():
            user_id = id_entry.get()
            name = name_entry.get()
            user_type_value = user_type.get()

            if not user_id or not name:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return

            try:
                user_id = int(user_id)
            except ValueError:
                messagebox.showwarning("Ошибка", "ID должен быть числом")
                return

            if library.get_user(user_id) is not None:
                messagebox.showwarning("Ошибка", "Пользователь с таким ID уже существует")
                return

            if user_type_value == "Студент":
                user = Student(user_id, name)
            elif user_type_value == "Преподаватель":
                user = Teacher(user_id, name)
            else:
                user = Guest(user_id, name)

            library.add_user(user)
            user_select["values"] = [user.name for user in library.get_users().values()]
            user_select.set(user.name)
            add_window.destroy()
            messagebox.showinfo("Библиотека", "Пользователь добавлен")

        ttk.Button(add_window, text="Добавить", command=save_user).pack(pady=20)

    def show_book_history(event):
        selected = books_table.selection()
        if not selected:
            return

        values = books_table.item(selected[0], "values")
        isbn = values[2]
        book = library.get_book(isbn)

        history_window = tk.Toplevel(window)
        history_window.title(f"История: {book.title}")
        history_window.geometry("600x400")

        ttk.Label(
            history_window,
            text=f"История выдачи книги «{book.title}»",
            font=("Arial", 14)
        ).pack(pady=10)

        columns = ("user", "issue_date", "return_date")

        history_table = ttk.Treeview(
            history_window,
            columns=columns,
            show="headings"
        )

        history_table.heading("user", text="Пользователь")
        history_table.heading("issue_date", text="Дата выдачи")
        history_table.heading("return_date", text="Дата возврата")

        history_table.column("user", width=200)
        history_table.column("issue_date", width=150)
        history_table.column("return_date", width=150)

        history_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        for record in library.get_issue_history():
            if record["book"] == book:
                user = record["user"]

                issue_date = record["issue_date"].strftime("%d.%m.%Y")

                if record["return_date"] is None:
                    return_date = "Не возвращена"
                else:
                    return_date = record["return_date"].strftime("%d.%m.%Y")

                history_table.insert(
                    "",
                    "end",
                    values=(
                        user.name,
                        issue_date,
                        return_date
                    )
                )

    books_table.bind("<Double-1>", show_book_history)
    search_button.config(command=search_books)
    issue_button.config(command=issue_book)
    return_button.config(command=return_book)
    update_button.config(command=update_table)
    overdue_button.config(command=show_overdue_books)
    user_books_button.config(command=show_user_books)
    add_button.config(command=add_book)
    delete_button.config(command=delete_book)
    add_user_button.config(command=add_user)

    update_table()
    window.mainloop()