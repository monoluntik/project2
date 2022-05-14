from tkinter import *
import psycopg2
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk


def validate(new_value):                             
    try: 
        if new_value == "" or new_value == "-" or new_value == "+":
            return True
        _str = str(float(new_value))
        return True
    except:
        return False    

def connection():
    conn = psycopg2.connect(
        database="project2",
        user='monoluntik',
        password='1',
        host='localhost',
        port='5432'
    )
    return conn

def frame2(f2, f3):

    def save():
        try:
            qt = quantityEntry.get()
            ch1 = variable.get()
            ch2 = var.get()
            crIndex = currency.index(ch1)
            if ch2 == 'Покупка':
                crIndex_side = 1
                text = results[crIndex][crIndex_side]
            elif ch2 == 'Продажа':
                crIndex_side = 2
                text = results[crIndex][crIndex_side]
            conn = connection()
            cursor = conn.cursor()
            dt = f'{datetime.now()}'.split(' ')
            cursor.execute(f"INSERT INTO history VALUES ('{ch1}', '{ch2}', '{text}', '{qt}', '{round(float(text)*float(qt), 2)}', '{dt[0]}', '{dt[1].split('.')[0]}') ")
            conn.commit()
            conn.close()
            refreshTable()
            totalPriceLabel['text'] = round(float(text)*float(qt), 2)
            messagebox.showinfo('Информация', "Данные успешно сохранены.")
        except ValueError:
            messagebox.showinfo("Ошибка", "Заполните все поля")

    def display_selected_side(choice):
        choice = var.get()
        ch = variable.get()
        crIndex = currency.index(ch)
        if choice == 'Покупка':
            crIndex_side = 1
            text = results[crIndex][crIndex_side]
        elif choice == 'Продажа':
            crIndex_side = 2
            text = results[crIndex][crIndex_side]
        else:
            text = 0.0
        priceLabel['text'] = text

    def count_total_price():
        try:
            choice = var.get()
            ch = variable.get()
            crIndex = currency.index(ch)
            if choice == 'Покупка':
                crIndex_side = 1
                text = results[crIndex][crIndex_side]
            elif choice == 'Продажа':
                crIndex_side = 2
                text = results[crIndex][crIndex_side]
            else:
                text = 0.0
            qt = quantityEntry.get()
            totalPriceLabel['text'] = round(float(text)*float(qt), 2)
        except ValueError:
            messagebox.showinfo("Ошибка", "Заполните все поля")


    def clear_f2():
        quantityEntry.delete(0, tk.END)
        quantityEntry.insert(0, '')
        variable.set("Выберите валюту")
        var.set('Выберите сторону сделки')
        priceLabel['text'] = '0.0'
        totalPriceLabel['text'] = '0.0'

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("select * from curs_balance")
    results = [i for i in cursor.fetchall()]
    currency = [i[0] for i in results]
    if currency == []:
        currency = ['']
    conn.commit()
    conn.close()

    vcmd = (f2.register(validate), '%P')  

    variable = StringVar(f2)
    variable.set("Выберите валюту")
    w = OptionMenu(f2, variable, *currency, command=display_selected_side)

    var = StringVar(f2)
    var.set('Выберите сторону сделки')
    sides = ['Покупка', "Продажа"]
    side = OptionMenu(f2, var, *sides, command=display_selected_side)

    currencyLabel = Label(f2, text="Валюта:", font=('Arial', 15), width=10)
    price = Label(f2, text="Цена:", font=('Arial', 15), width=10)
    qunatityLabel = Label(f2, text='Количество:', font=('Arial', 15), width=10)
    priceLabel = Label(f2, text='0.0', font=('Arial', 15), width=10)
    totalLabel = Label(f2, text='Итого:', font=('Arial', 15), width=10)
    totalPriceLabel = Label(f2, text='0.0', font=('Arial', 15), width=10)

    quantityEntry = Entry(f2, width=10, bd=5, font=('Arial', 15), justify='center', validate='key', validatecommand=vcmd)

    addBtn = Button(f2, text="Посчитать", padx=25, pady=5, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=count_total_price)
    clearBtn = Button(f2, text='Очистить', padx=25, pady=5, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=clear_f2)
    saveBtn = Button(f2, text='Сохрнаить запись', padx=25, pady=5, width=15, bd=5, font=('Arial', 15), bg="#84F894", command=save)
    
    quantityEntry.grid(row=7, column=2, columnspan=1, padx=25, pady=5)

    saveBtn.grid(row=11, column=2, columnspan=1, padx=25, pady=5)
    clearBtn.grid(row=11, column=4, columnspan=1, padx=25, pady=5)
    addBtn.grid(row=11, column=0, columnspan=1, padx=25, pady=5)

    w.grid(row=3, column=2, columnspan=1, padx=25, pady=5)
    side.grid(row=3, column=4, columnspan=1, padx=25, pady=5)

    totalLabel.grid(row=9, column=0, columnspan=1, padx=25, pady=5)
    qunatityLabel.grid(row=7, column=0, columnspan=1, padx=25, pady=5)
    priceLabel.grid(row=5, column=2, columnspan=1, padx=25, pady=5)
    currencyLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
    price.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
    totalPriceLabel.grid(row=9, column=2, columnspan=1, padx=50, pady=5)

    def clear():
        decision = messagebox.askquestion("Предупреждение!", "Очистить?")
        if decision != "yes":
            return 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history")
        conn.commit()
        conn.close()
        refreshTable()

    def delete():
        try:
            selected_item = my_tree_f3.selection()[0]

            decision = messagebox.askquestion("Предупреждение!", "Удалить?")
            if decision != "yes":
                return 
            else:
                deleteData = str(my_tree_f3.item(selected_item)['values'][-1])
                conn = connection()
                cursor = conn.cursor()
                cursor.execute(f"delete from history where wtime ='{deleteData}'")
                conn.commit()
                conn.close()
                refreshTable()
        except IndexError:
            messagebox.showerror('Ошибка', 'Выберите строку для удоления')


    def read():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def refreshTable():
        for data in my_tree_f3.get_children():
            my_tree_f3.delete(data)
        i = 1
        data = read()
        data.reverse()
        for array in data:
            list_ = [i]
            list_.extend(array)
            my_tree_f3.insert(parent='', index='end', iid=list_, text="", values=(list_), tag="orow")
            i += 1

        my_tree_f3.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree_f3.grid(row=0, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

    my_tree_f3 = ttk.Treeview(f3, height=10)
    my_tree_f3['columns'] = ('№','Валюта', 'Сторона сделки', 'Цена', 'Количество', 'Итого', 'Дата', 'Время')

    my_tree_f3.column("#0", width=0, stretch=NO)
    my_tree_f3.column("№", anchor=W, width=50)
    my_tree_f3.column("Валюта", anchor=W, width=100)
    my_tree_f3.column("Сторона сделки", anchor=W, width=195)
    my_tree_f3.column("Цена", anchor=W, width=75)
    my_tree_f3.column("Количество", anchor=W, width=150)
    my_tree_f3.column("Итого", anchor=W, width=150)
    my_tree_f3.column("Дата", anchor=W, width=120)
    my_tree_f3.column("Время", anchor=W, width=100)



    my_tree_f3.heading('№', text='№', anchor=W)
    my_tree_f3.heading("Валюта", text="Валюта", anchor=W)
    my_tree_f3.heading("Сторона сделки", text="Сторона сделки", anchor=W)
    my_tree_f3.heading("Цена", text="Цена", anchor=W)
    my_tree_f3.heading("Количество", text="Количество", anchor=W)
    my_tree_f3.heading("Итого", text="Итого", anchor=W)
    my_tree_f3.heading("Дата", text="Дата", anchor=W)
    my_tree_f3.heading("Время", text="Время", anchor=W)

    clearBtn = Button(f3, text='Удалить все', font=('Arial', 15), bg="#84F894", command=clear)
    clearBtn.grid(row=4, column=7, columnspan=1)
    deleteBtn = Button(f3, text='Удалить', font=('Arial', 15), bg="#84F894", command=delete)
    deleteBtn.grid(row=6, column=7, columnspan=1)


    refreshTable()