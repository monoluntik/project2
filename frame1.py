from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import psycopg2
from psycopg2.errors import UniqueViolation

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


def frame1(f1):

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)

        for array in read():
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)


    my_tree = ttk.Treeview(f1)

    ph1 = tk.StringVar()
    ph2 = tk.StringVar()
    ph3 = tk.StringVar()
    ph4 = tk.StringVar()
    ph5 = tk.StringVar()

    def setph(word,num):
        if num ==1:
            ph1.set(word)
        if num ==2:
            ph2.set(word)
        if num ==3:
            ph3.set(word)
        if num ==4:
            ph4.set(word)
        if num ==5:
            ph5.set(word)

    def read():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM curs_balance")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def add():
        currency = str(currencyEntry.get())
        buy = str(buyEntry.get())
        sell = str(sellEntry.get())
        quantity = str(quantityEntry.get()) 
        currencyEntry.delete(0, tk.END)
        currencyEntry.insert(0,'')
        buyEntry.delete(0, tk.END)
        buyEntry.insert(0,'')
        sellEntry.delete(0, tk.END)
        sellEntry.insert(0,'')
        quantityEntry.delete(0, tk.END)
        quantityEntry.insert(0,'')

        if (currency == "" or currency == " ") or (buy == "" or buy == " ") or (sell == "" or sell == " ") or (quantity == "" or quantity == " "):
            messagebox.showinfo("Ошибка", "Заполните все поля")
            return
        else:
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO curs_balance VALUES ('{currency}','{buy}','{sell}','{quantity}') ")
                conn.commit()
                conn.close()
            except UniqueViolation:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE curs_balance SET buy='"+
                buy+"', sell='"+
                sell+"', quantity='"+
                quantity+"' where currency='"+currency+"'")
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Ошибка", "Поля заполнены неверно")
                return

        refreshTable()
        

    def delete():
        decision = messagebox.askquestion("Предупреждение!", "Удалить?")
        if decision != "yes":
            return 
        else:
            selected_item = my_tree.selection()[0]
            deleteData = str(my_tree.item(selected_item)['values'][0])
            currencyEntry.delete(0, tk.END)
            currencyEntry.insert(0,'')
            buyEntry.delete(0, tk.END)
            buyEntry.insert(0,'')
            sellEntry.delete(0, tk.END)
            sellEntry.insert(0,'') 
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM curs_balance WHERE currency='"+str(deleteData)+"'")
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Ошибка", "Ошибка удаления")
                return

            refreshTable()

    def select():
        try:
            selected_item = my_tree.selection()[0]
            currency = str(my_tree.item(selected_item)['values'][0])
            buy = str(my_tree.item(selected_item)['values'][1])
            sell = str(my_tree.item(selected_item)['values'][2])
            quantity = str(my_tree.item(selected_item)['values'][3])
            setph(currency,1)
            setph(buy,2)
            setph(sell,3)
            setph(quantity,4)
        except:
            messagebox.showinfo("Ошибка", "Сделайте выбор")





    vcmd = (f1.register(validate), '%P')  

    currencyLabel = Label(f1, text="Валюта:", font=('Arial', 15), width=10)
    buyLabel = Label(f1, text="Покупка:", font=('Arial', 15), width=10)
    sellLabel = Label(f1, text="Продажа:", font=('Arial', 15), width=10)
    quantityLabel = Label(f1, text="Количество:", font=('Arial', 15), width=10)

    currencyLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
    buyLabel.grid(row=5, column=0, columnspan=1, padx=25, pady=5)
    sellLabel.grid(row=5, column=2, columnspan=1, padx=25, pady=5)
    quantityLabel.grid(row=7, column=0, columnspan=1, padx=25, pady=5)


    currencyEntry = Entry(f1, width=55, bd=5, font=('Arial', 15), textvariable = ph1, justify='right')
    buyEntry = Entry(f1, width=10, bd=5, font=('Arial', 15), textvariable = ph2, justify='right', validate='key', validatecommand=vcmd)
    sellEntry = Entry(f1, width=10, bd=5, font=('Arial', 15), textvariable = ph3, justify='right', validate='key', validatecommand=vcmd)
    quantityEntry = Entry(f1, width=10, bd=5, font=('Arial', 15), textvariable = ph4, justify='right', validate='key', validatecommand=vcmd)

    currencyEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
    buyEntry.grid(row=5, column=0, columnspan=4, padx=5, pady=0)
    sellEntry.grid(row=5, column=2, columnspan=4, padx=5, pady=0)
    quantityEntry.grid(row=7, column=0, columnspan=4, padx=5, pady=0)

    addBtn = Button(
        f1, text="Add/Update", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#84F894", command=add)
    deleteBtn = Button(
        f1, text="Delete", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#FF9999", command=delete)
    selectBtn = Button(
        f1, text="Select", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#EEEE5E", command=select)

    addBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
    deleteBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
    selectBtn.grid(row=11, column=5, columnspan=1, rowspan=2)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial Bold', 15))

    my_tree['columns'] = ('Валюта', 'Покупка', 'Продажа', 'Количество')

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Валюта", anchor=W, width=150)
    my_tree.column("Покупка", anchor=W, width=165)
    my_tree.column("Продажа", anchor=W, width=150)
    my_tree.column("Количество", anchor=W, width=150)


    my_tree.heading("Валюта", text="Валюта", anchor=W)
    my_tree.heading("Покупка", text="Покупка", anchor=W)
    my_tree.heading("Продажа", text="Продажа", anchor=W)
    my_tree.heading("Количество", text="Количество", anchor=W)


    refreshTable()


