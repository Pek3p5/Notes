import tkinter as tk
import customtkinter
import sqlite3


def db_start():
    global conn, cur

    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)""")


def save_note():
    note = note_entry.get()
    cur.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    update_notes_list()
    note_entry.delete(0, customtkinter.END)


def delete_note():
    index = notes_list.curselection()
    if index:
        selected_note = notes_list.get(index)
        cur.execute("DELETE FROM notes WHERE note=?", (selected_note,))
        conn.commit()
        update_notes_list()


def edit_note():
    index = notes_list.curselection()
    note = note_entry.get()
    if index:
        delete_note()
    if note != "":
        save_note()
    update_notes_list()


def delete_all_note():
    sql = 'DELETE FROM notes'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    update_notes_list()



def update_notes_list():
    notes_list.delete(0, customtkinter.END)
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    for note in notes:
        note_text = note[1]
        notes_list.insert(customtkinter.END, note_text)


base = customtkinter.CTk()
base.title("Заметки")
base.geometry("700x500")

note_label = customtkinter.CTkLabel(base, text="Заметки:")
note_label.place(anchor = "center", relx = 0.5, rely = 0.025)

enter_label = customtkinter.CTkLabel(base, text="Введите Заметку:")
enter_label.place( relx = 0.775, rely = 0.15)

note_entry = customtkinter.CTkEntry(base)
note_entry.place(relx = 0.775, rely = 0.2)

save_button = customtkinter.CTkButton(base, text="Добавить", command=save_note)
save_button.place(relx = 0.775, rely = 0.3)

edit_button = customtkinter.CTkButton(base, text="Изменить", command=edit_note)
edit_button.place(relx = 0.775, rely = 0.4)

delete_button = customtkinter.CTkButton(base, text="Удалить", command=delete_note)
delete_button.place(relx = 0.775, rely = 0.5)

delete_all_button = customtkinter.CTkButton(base, text="Удалить все", command=delete_all_note)
delete_all_button.place(relx = 0.775, rely = 0.6)

exit_button = customtkinter.CTkButton(base, text="Закрыть", command= exit)
exit_button.place(relx = 0.775, rely = 0.9)


notes_list = tk.Listbox(base)
notes_list.place(relwidth=0.7, relheight= 0.75, relx = 0.05, rely = 0.2)

db_start()
update_notes_list()

base.mainloop()
conn.close()
