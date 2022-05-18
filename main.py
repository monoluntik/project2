from tkinter import *
from tkinter import ttk
from frame import frame

def main():
    root = Tk()
    root.title("Программа")
    root.geometry("1120x620")
    nb = ttk.Notebook(root)
    nb.pack(fill='both', expand='yes')
    f2 = Frame(root)
    f1 = Frame(root)
    f3 = Frame(root)
    nb.add(f2, text='Сделка')
    nb.add(f1, text='Курс к сому')
    nb.add(f3, text='История сделок')
    frame(f1,f2,f3)

    root.mainloop()
        
if __name__ == '__main__':
    main()