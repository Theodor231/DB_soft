import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='adauga',
                                    command=self.open_dialog,
                                    bg='#d7d8e0',
                                    bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        btn_open_dialog2 = tk.Button(toolbar, text='Sterge',
                                    command=self.del_records,
                                     bg='#d7d8e0',
                                    bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog2.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'Description', 'cost', 'total'), height='15',
                                 show='headings')

        self.tree.column('ID', width=150, anchor=tk.CENTER)
        self.tree.column('Description', width=150, anchor=tk.CENTER)
        self.tree.column('cost', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Description', text='Denumire')
        self.tree.heading('cost', text='cost(lei)')
        self.tree.heading('total', text='venit/consum')

        self.tree.pack()

    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def del_record(self, insert_id):
        self.db.del_data_id(insert_id)
        self.view_records()
    def open_dialog(self):
        Child()

    def del_records(self):
        Del_records()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('adaugare venit/consum')
        self.geometry("400x220+400+300")
        self.resizable(False, False)

        label_description = tk.Label(self, text='Denumirea')
        label_description.place(x=50, y=50)
        label_selection = tk.Label(self, text='venit/consum')
        label_selection.place(x=50, y=80)
        label_sum = tk.Label(self, text='suma(lei)')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)



        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.Combobox = ttk.Combobox(self, values=[u'venit', u'consum'])
        self.Combobox.current(0)
        self.Combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='inchide', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='adauga')
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                 self.entry_money.get(),
                                                                 self.Combobox.get()))

        self.grab_set()
        self.focus_set()

class Del_records(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view2 = app

    def init_child(self):
        self.title('Stergere venit/consum')
        self.geometry("400x220+400+300")
        self.resizable(False, False)

        label_id = tk.Label(self, text='Dati ID pentru stergere: ')
        label_id.place(x=50, y=50)

        self.entry_id = ttk.Entry(self)
        self.entry_id.place(x=200, y=50)

        btn_cancel = ttk.Button(self, text='inchide', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='sterge')
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>', lambda event: self.view2.del_record(self.entry_id.get()))

        self.grab_set()
        self.focus_set()

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.bd')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance(id integer primary key , description text, costs text, total real)'''
        )
        self.conn.commit()

    def insert_data(self, description, costs, total):
        self.c.execute('''INSERT INTO finance(description, costs, total) VALUES (?, ?, ?)''',
                       (description, costs, total))
        self.conn.commit()

    def del_data_id(self, insert_id):
        self.c.execute('''DELETE FROM finance WHERE id=? ''', (insert_id,))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Finance")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()