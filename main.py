import csv
from tkinter import *
from tkinter import ttk
from views import view, add, update, remove, search
from tkinter import messagebox
from PIL import Image, ImageTk
import itertools

# Colors for the dark theme
co0 = "#2E2E2E"  
co1 = "#FFFFFF"  
co2 = "#3A3A3A"  
co3 = "#6A6A6A"  
co4 = "#FFD700"  

window = Tk()
window.title("Contact Book - Diwali Edition 🎉")
window.geometry('550x500')
window.configure(background=co0)
window.resizable(width=FALSE, height=FALSE)

# Frames
frame_up = Frame(window, width=550, height=50, bg=co2)
frame_up.grid(row=0, column=0, padx=0, pady=1)

frame_down = Frame(window, width=550, height=150, bg=co0)
frame_down.grid(row=1, column=0, padx=0, pady=1)

frame_table = Frame(window, width=550, height=100, bg=co0, relief="flat")
frame_table.grid(row=2, column=0, columnspan=2, padx=10, pady=1, sticky=NW)

left_image = Image.open("diwali.jpg")
left_image = left_image.resize((50, 50), Image.LANCZOS)
left_img = ImageTk.PhotoImage(left_image)
left_label = Label(window, image=left_img, bg=co0)
left_label.place(x=0, y=0)

right_image = Image.open("diwali.jpg")
right_image = right_image.resize((50, 50), Image.LANCZOS)
right_img = ImageTk.PhotoImage(right_image)
right_label = Label(window, image=right_img, bg=co0)
right_label.place(x=500, y=0)

def flicker_effect():
    flicker_colors = itertools.cycle([co2, co4])
    window.after(500, change_color, flicker_colors)

def change_color(colors):
    frame_up.configure(bg=next(colors))
    window.after(500, change_color, colors)

flicker_effect()

def show():
    global tree

    listheader = ['Name', 'Gender', 'Phone', 'Email']
    demo_list = view()

    tree = ttk.Treeview(
        frame_table, selectmode="extended", columns=listheader, 
        show="headings", style="mystyle.Treeview"
    )

    vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew', padx=10, pady=10)  
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    tree.heading(0, text='Name', anchor=CENTER)
    tree.heading(1, text='Gender', anchor=CENTER)
    tree.heading(2, text='Phone', anchor=CENTER)
    tree.heading(3, text='Email', anchor=CENTER)
    
    tree.column(0, width=120, anchor='center')
    tree.column(1, width=50, anchor='center')
    tree.column(2, width=100, anchor='center')
    tree.column(3, width=180, anchor='center')
    
    for item in demo_list:
        tree.insert('', 'end', values=item)
    
    style = ttk.Style()
    style.configure(
        "mystyle.Treeview", background= co3,  
        foreground="#000000", fieldbackground= co3 
    )
    style.configure("mystyle.Treeview.Heading", background="000000", foreground=co3)
show()
def insert():
    Name = e_name.get()
    Gender = c_gender.get()
    Telephone = e_telephone.get()
    Email = e_email.get()

    data = [Name, Gender, Telephone, Email]

    if Name == '' or Gender == '' or Telephone == '' or Email == '':
        messagebox.showwarning('Data', 'Please fill in all fields')
    else:
        add(data)
        messagebox.showinfo('Data', 'Data added successfully')

        clear_fields()
        show()

def to_update():
    try:
        tree_data = tree.focus()
        tree_dictionary = tree.item(tree_data)
        tree_list = tree_dictionary['values']

        Name = str(tree_list[0])
        Gender = str(tree_list[1])
        Telephone = str(tree_list[2])
        Email = str(tree_list[3])

        e_name.insert(0, Name)
        c_gender.set(Gender) 
        e_telephone.insert(0, Telephone)
        e_email.insert(0, Email)

        def confirm():
            new_name = e_name.get()
            new_gender = c_gender.get()
            new_telephone = e_telephone.get()
            new_email = e_email.get()

            if not new_name or not new_gender or not new_telephone or not new_email:
                messagebox.showwarning('Error', 'All fields are required')
                return

            data = [Telephone, new_name, new_gender, new_email]  
            update(data)

            messagebox.showinfo('Success', 'Data updated successfully')
            clear_fields()
            refresh_table()
            b_confirm.destroy()

        b_confirm = Button(
            frame_down, text="Confirm", width=10, height=1,
            bg=co2, fg=co1, font=('Ivy 8 bold'), command=confirm
        )
        b_confirm.place(x=290, y=110)

    except IndexError:
        messagebox.showerror('Error', 'Select a record from the table')

def clear_fields():
    e_name.delete(0, 'end')
    c_gender.set('')  
    e_telephone.delete(0, 'end')
    e_email.delete(0, 'end')

def update(data):
    old_telephone = data[0]
    new_data = data[1:]

    updated_list = []
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] == old_telephone:
                updated_list.append(new_data)
            else:
                updated_list.append(row)

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_list)

def refresh_table():
    for item in tree.get_children():
        tree.delete(item)
    demo_list = view()
    for item in demo_list:
        tree.insert('', 'end', values=item)

def to_remove():
    try:
        tree_data = tree.focus()
        tree_dictionary = tree.item(tree_data)
        tree_list = tree_dictionary['values']
        tree_telephone = str(tree_list[2])

        remove(tree_telephone)

        messagebox.showinfo('Success', 'Data has been deleted successfully')
        refresh_table()

    except IndexError:
        messagebox.showerror('Error', 'Select a record from the table')

def to_search():
    telephone = e_search.get()
    data = search(telephone)
    delete_command()

    for item in data:
        tree.insert('', 'end', values=item)

    e_search.delete(0, 'end')

def delete_command():
    tree.delete(*tree.get_children())

# Frame widgets
app_name = Label(frame_up, text="Contact Book", height=1, font=('Verdana 17 bold'), bg=co2, fg=co1)
app_name.place(relx=0.5, rely=0.5, anchor=CENTER) 

l_name = Label(frame_down, text="Name *", width=20, height=1, font=('Ivy 10'), bg=co0, anchor=NW, fg=co1)
l_name.place(x=10, y=20)
e_name = Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid", bg=co3, fg=co1)
e_name.place(x=80, y=20)

l_gender = Label(frame_down, text="Gender *", width=20, height=1, font=('Ivy 10'), bg=co0, anchor=NW, fg=co1)
l_gender.place(x=10, y=50)
c_gender = ttk.Combobox(frame_down, width=27)
c_gender['values'] = ['', 'F', 'M']
c_gender.place(x=80, y=50)

l_telephone = Label(frame_down, text="Telephone*", height=1, font=('Ivy 10'), bg=co0, anchor=NW, fg=co1)
l_telephone.place(x=10, y=80)
e_telephone = Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid", bg=co3, fg=co1)
e_telephone.place(x=80, y=80)

l_email = Label(frame_down, text="Email *", height=1, font=('Ivy 10'), bg=co0, anchor=NW, fg=co1)
l_email.place(x=10, y=110)
e_email = Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid", bg=co3, fg=co1)
e_email.place(x=80, y=110)

b_search = Button(frame_down, text="Search", height=1, bg=co2, fg=co1, font=('Ivy 8 bold'), command=to_search)
b_search.place(x=290, y=20)

e_search = Entry(frame_down, width=16, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid", bg=co3, fg=co1)
e_search.place(x=347, y=20)

b_view = Button(frame_down, text="View", width=10, height=1, bg=co2, fg=co1, font=('Ivy 8 bold'), command=show)
b_view.place(x=290, y=50)

b_add = Button(frame_down, text="Add", width=10, height=1, bg=co2, fg=co1, font=('Ivy 8 bold'), command=insert)
b_add.place(x=290, y=80)

b_update = Button(frame_down, text="Update", width=10, height=1, bg=co2, fg=co1, font=('Ivy 8 bold'), command=to_update)
b_update.place(x=290, y=110)

b_remove = Button(frame_down, text="Remove", width=10, height=1, bg=co2, fg=co1, font=('Ivy 8 bold'), command=to_remove)
b_remove.place(x=390, y=110)

# Run the application
window.mainloop()
