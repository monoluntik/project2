from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

from datetime import datetime
import sqlite3 as db
from db import create_tables, connection



def validate(new_value):                             
    try: 
        if new_value == "" or new_value == "-" or new_value == "+":
            return True
        _str = str(float(new_value))
        return True
    except:
        return False    





def frame(f1,f2,f3):
    create_tables()




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
                cursor.execute(f"INSERT INTO curs_balance VALUES('{currency}','{buy}','{sell}','{quantity}') ")
                conn.commit()
                conn.close()
                refreshTable()
                messagebox.showinfo('Информация', "Данные успешно сохранены.")
            except db.IntegrityError:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute(f"""UPDATE curs_balance SET buy='{buy}', sell='{sell}', quantity='{quantity}' where currency='{currency}'""")
                conn.commit()
                conn.close()
                refreshTable()
                messagebox.showinfo('Информация', "Данные успешно  обновлены.")
            except Exception as E:
                print(E)
                messagebox.showinfo("Ошибка", "Поля заполнены неверно")
                return
        

    def delete():
        try:
            selected_item = my_tree.selection()[0]
            decision = messagebox.askquestion("Предупреждение!", "Удалить?")
            if decision != "yes":
                return 
            else:
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
                    refreshTable()
                    messagebox.showinfo('Информация', "Данные успешно удалены.")           


                    
                except:
                    messagebox.showinfo("Ошибка", "Ошибка удаления")
                    return

        except IndexError:
            messagebox.showerror('Ошибка', 'Выберите строку для удоления')
            
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

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)

        for array in read():
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)
    
    my_tree = ttk.Treeview(f1)

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

    def saveF2():
        try:
            qt = quantityEntryF2.get()
            ch1 = variableF2.get()
            ch2 = varF2.get()
            crIndex = currencyF2.index(ch1)
            if ch2 == 'Покупка':
                crIndex_side = 1
                text = resultsF2[crIndex][crIndex_side]
            elif ch2 == 'Продажа':
                crIndex_side = 2
                text = resultsF2[crIndex][crIndex_side]
            ttprice = round(float(text)*float(qt), 2)
            conn = connection()
            cursor = conn.cursor()
            dt = f'{datetime.now()}'.split(' ')
            cursor.execute(f"INSERT INTO history VALUES('{ch1}', '{ch2}', '{text}', '{qt}', '{ttprice}', '{dt[0]}', '{dt[1].split('.')[0]}')")
            cursor.execute(f"select * from curs_balance where currency='{ch1}'")
            quantity = float([i for i in cursor.fetchall()[0]][3])
            if crIndex_side == 1:
                quantity += ttprice 
            elif crIndex_side == 2:
                quantity -= ttprice
            cursor.execute("UPDATE curs_balance SET quantity='"+
            f'{quantity}'+"' where currency='"+ch1+"'")
            conn.commit()
            conn.close()            
            refreshTableF3()
            refreshTable()
            totalPriceLabelF2['text'] = ttprice
            messagebox.showinfo('Информация', "Данные успешно сохранены.")
        except ValueError:
            messagebox.showinfo("Ошибка", "Заполните все поля")

    def display_selected_sideF2(choice):
        choice = varF2.get()
        ch = variableF2.get()
        crIndex = currencyF2.index(ch)
        if choice == 'Покупка':
            crIndex_side = 1
            text = resultsF2[crIndex][crIndex_side]
        elif choice == 'Продажа':
            crIndex_side = 2
            text = resultsF2[crIndex][crIndex_side]
        else:
            text = 0.0
        priceLabelF2['text'] = text

    def count_total_priceF2():
        try:
            choice = varF2.get()
            ch = variableF2.get()
            crIndex = currencyF2.index(ch)
            if choice == 'Покупка':
                crIndex_side = 1
                text = resultsF2[crIndex][crIndex_side]
            elif choice == 'Продажа':
                crIndex_side = 2
                text = resultsF2[crIndex][crIndex_side]
            else:
                text = 0.0
            qt = quantityEntryF2.get()
            totalPriceLabelF2['text'] = round(float(text)*float(qt), 2)
        except ValueError:
            messagebox.showinfo("Ошибка", "Заполните все поля")

    def clear_f2():
        quantityEntryF2.delete(0, tk.END)
        quantityEntryF2.insert(0, '')
        variableF2.set("Выберите валюту")
        varF2.set('Выберите сторону сделки')
        priceLabelF2['text'] = '0.0'
        totalPriceLabelF2['text'] = '0.0'

    
    connF2 = connection()
    cursorF2 = connF2.cursor()
    cursorF2.execute("select * from curs_balance")
    resultsF2 = [i for i in cursorF2.fetchall()]
    currencyF2 = [i[0] for i in resultsF2]
    if currencyF2 == []:
        currencyF2 = ['']
    connF2.commit()
    connF2.close()

    vcmdF2 = (f2.register(validate), '%P')  

    variableF2 = StringVar(f2)
    variableF2.set("Выберите валюту")
    wF2 = OptionMenu(f2, variableF2, *currencyF2, command=display_selected_sideF2)
    varF2 = StringVar(f2)
    varF2.set('Выберите сторону сделки')
    sidesF2 = ['Покупка', "Продажа"]
    sideF2 = OptionMenu(f2, varF2, *sidesF2, command=display_selected_sideF2)

    currencyLabelF2 = Label(f2, text="Валюта:", font=('Arial', 15), width=10)
    priceF2 = Label(f2, text="Цена:", font=('Arial', 15), width=10)
    qunatityLabelF2 = Label(f2, text='Количество:', font=('Arial', 15), width=10)
    priceLabelF2 = Label(f2, text='0.0', font=('Arial', 15), width=10)
    totalLabelF2 = Label(f2, text='Итого:', font=('Arial', 15), width=10)
    totalPriceLabelF2 = Label(f2, text='0.0', font=('Arial', 15), width=10)

    quantityEntryF2 = Entry(f2, width=10, bd=5, font=('Arial', 15), justify='center', validate='key', validatecommand=vcmdF2)

    addBtnF2 = Button(f2, text="Посчитать", padx=25, pady=5, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=count_total_priceF2)
    clearBtnF2 = Button(f2, text='Очистить', padx=25, pady=5, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=clear_f2)
    saveBtnF2 = Button(f2, text='Сохрнаить запись', padx=25, pady=5, width=15, bd=5, font=('Arial', 15), bg="#84F894", command=saveF2)
    
    quantityEntryF2.grid(row=7, column=2, columnspan=1, padx=25, pady=5)

    saveBtnF2.grid(row=11, column=2, columnspan=1, padx=25, pady=5)
    clearBtnF2.grid(row=11, column=4, columnspan=1, padx=25, pady=5)
    addBtnF2.grid(row=11, column=0, columnspan=1, padx=25, pady=5)

    wF2.grid(row=3, column=2, columnspan=1, padx=25, pady=5)
    sideF2.grid(row=3, column=4, columnspan=1, padx=25, pady=5)

    totalLabelF2.grid(row=9, column=0, columnspan=1, padx=25, pady=5)
    qunatityLabelF2.grid(row=7, column=0, columnspan=1, padx=25, pady=5)
    priceLabelF2.grid(row=5, column=2, columnspan=1, padx=25, pady=5)
    currencyLabelF2.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
    priceF2.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
    totalPriceLabelF2.grid(row=9, column=2, columnspan=1, padx=50, pady=5)


    def clearF3():
        decision = messagebox.askquestion("Предупреждение!", "Очистить?")
        if decision != "yes":
            return 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history")
        conn.commit()
        conn.close()
        refreshTableF3()

    def deleteF3():
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
                refreshTableF3()
        except IndexError:
            messagebox.showerror('Ошибка', 'Выберите строку для удоления')


    def readF3():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def refreshTableF3():
        for data in my_tree_f3.get_children():
            my_tree_f3.delete(data)
        i = 1
        data = readF3()
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

    clearBtnF3 = Button(f3, text='Удалить все', font=('Arial', 15), bg="#84F894", command=clearF3)
    clearBtnF3.grid(row=4, column=7, columnspan=1)
    deleteBtnF3 = Button(f3, text='Удалить', font=('Arial', 15), bg="#84F894", command=deleteF3)
    deleteBtnF3.grid(row=6, column=7, columnspan=1)

    refreshTableF3()
    refreshTable()
