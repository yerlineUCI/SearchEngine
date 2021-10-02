from tkinter import *
import search

class Application(Frame):
    def __init__(self, master=NONE):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.create_button()

    def create_button(self):
        b1=Button(self.master,text="Search",command= lambda: search.search(self.entry.get()),bg='light blue',fg = 'black', font='Helvetica 10 bold')
        b1.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        

    def create_widgets(self):
        self.frame = Frame(self)
        self.entry = Entry(self.master,bd=6,width=50, fg='black', font='Helvetica 10 bold', bg='light grey')
        self.entry.modified = False
        self.entry.insert(END, "Search Here!")
        self.entry.bind("<Key>", self.entry_key)
        self.entry.pack()
        self.frame.pack()

    def entry_key(self, event):
        if not self.entry.modified:
            self.entry.delete(0, END)
            self.entry.modified = True

if __name__ == "__main__":
    root = Tk()
    f = Frame(root, width=600,height=600)
    app = Application(master=root)
    f.pack(fill=X, expand=True)
    app.mainloop()
