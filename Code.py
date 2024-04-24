from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import re
from tkinter import colorchooser


# database stuff
# create database
def main_app():
    root = Tk()
    root.title('INSE 6260 project')

    root.geometry("1600x700")

    def validate_phone(phone):
        pattern = r"^\+1 \(\d{3}\) \d{3}-\d{4}$"
        return re.match(pattern, phone) is not None

    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def validate_website(website):
        pattern = r"^https?://[a-zA-Z0-9.-]+$"
        return re.match(pattern, website) is not None

    def validate_numeric(value):
        return value.isdigit()

    def validate_province(province):
        return len(province) == 2 and province.isupper()

    def validate_postal_code(postal_code):
        pattern = r"^[A-Z]\d[A-Z] \d[A-Z]\d$"
        return re.match(pattern, postal_code) is not None

    def validate_entries():
        errors = []
        if not validate_phone(Phone_entry.get()):
            errors.append("Invalid phone format. Required: +1 (xxx) xxx-xxxx.")
        if not validate_email(Email_entry.get()):
            errors.append("Invalid email format.")
        if not validate_website(Website_entry.get()):
            errors.append("Invalid website format. Required: http:// or https://")
        if not validate_numeric(Unit_Number_entry.get()):
            errors.append("Unit number must be numeric.")
        if not validate_numeric(Civic_Number_entry.get()):
            errors.append("Civic number must be numeric.")
        if not validate_province(Province_entry.get()):
            errors.append("Province must be two uppercase letters.")
        if not validate_postal_code(Postal_Code_entry.get()):
            errors.append("Postal code must be in the format ANA NAN.")

        return errors

    my_menu = Menu(root)
    root.config(menu=my_menu)
    # Add Fake Data

    # config
    option_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Options", menu=option_menu)

    def primary_color():
        primary_color = colorchooser.askcolor()[1]
        if primary_color:
            my_tree.tag_configure('evenrow', background=primary_color)

    def secondary_color():
        secondary_color = colorchooser.askcolor()[1]
        if secondary_color:
            my_tree.tag_configure('oddrow', background=secondary_color)

    def highlight_color():
        highlight_color = colorchooser.askcolor()[1]

        # Change Selected Color
        if highlight_color:
            style.map('Treeview',
                      background=[('selected', highlight_color)])

    # dropdown

    option_menu.add_command(label="Change primary Color", command=primary_color)
    option_menu.add_command(label="Secondary color ", command=secondary_color)
    option_menu.add_command(label="Highlight Color", command=highlight_color)
    option_menu.add_separator()
    option_menu.add_command(label="Exit", command="root.quit")


    data = [
        ["John", "Elder", 1,"Elder Corp", "+1 (702) 555-0123", "john.elder@example.com", "https://www.elder.com", "1", "100", "Elder Street", "Las Vegas", "NV", "A1B 2C3"],
        ["Mary", "Smith", 2,"Smith Ltd.", "+1 (312) 555-0198", "mary.smith@example.com", "https://www.smith.com", "2", "200", "West Lookout", "Chicago", "IL", "C4D 5E6"],
        ["Tim", "Tanaka", 3,"Tanaka Inc.", "+1 (212) 555-0156", "tim.tanaka@example.com", "https://www.tanaka.com", "3", "300", "Main Street", "New York", "NY", "E7F 8G9"],
        ["Erin", "Erinton",4, "Erintech", "+1 (213) 555-0189", "erin.erinton@example.com", "https://www.erinton.com", "4", "400", "Top Way", "Los Angeles", "CA", "G1H 2J3"],
        ["Bob", "Bobberly", 5,"Bobberly Goods", "+1 (901) 555-0110", "bob.bobberly@example.com", "https://www.bobberly.com", "5", "500", "Left Street", "Memphis", "TN", "K4L 5M6"],
        ["Steve", "Smith", 6,"Smith's Tech", "+1 (305) 555-0122", "steve.smith@example.com", "https://www.smithsteve.com", "6", "600", "Main Street", "Miami", "FL", "N7O 8P9"],
        ["Tina", "Browne", 7,"Browne Marketing", "+1 (312) 555-0133", "tina.browne@example.com", "https://www.browne.com", "7", "700", "Street Avenue", "Chicago", "IL", "Q1R 2S3"],
        ["Mark", "Lane", 8,"Lane Enterprises", "+1 (615) 555-0144", "mark.lane@example.com", "https://www.lane.com", "8", "800", "East Street", "Nashville", "TN", "T4U 5V6"],
        ["John", "Smith", 9,"Smith & Co.", "+1 (314) 555-0155", "john.smith@example.com", "https://www.smithjohn.com", "9", "900", "North Avenue", "St. Louis", "MO", "W7X 8Y9"],
        ["Mary", "Todd", 10,"Todd Interiors", "+1 (214) 555-0166", "mary.todd@example.com", "https://www.todd.com", "10", "1000", "Elder Way", "Dallas", "TX", "Z1A 2B3"],
        ["John", "Lincoln", 11,"Lincoln Tech", "+1 (702) 555-0177", "john.lincoln@example.com", "https://www.lincoln.com", "11", "1100", "Elder Street", "Las Vegas", "NV", "C4D 5E6"],
        ["Mary", "Bush", 12,"Bush Bakery", "+1 (312) 555-0188", "mary.bush@example.com", "https://www.bush.com", "12", "1200", "West Lookout", "Chicago", "IL", "G1H 2J3"],
        ["Tim", "Reagan", 13,"Reagan Realty", "+1 (212) 555-0199", "tim.reagan@example.com", "https://www.reagan.com", "13", "1300", "Main Street", "New York", "NY", "K4L 5M6"],
        ["Erin", "Smith", 14,"Smith Decor", "+1 (213) 555-0200", "erin.smith@example.com", "https://www.smith.com", "14", "1400", "Top Way", "Los Angeles", "CA", "N7O 8P9"],
        ["Bob", "Field", 15,"Field Tech", "+1 (901) 555-0211", "bob.field@example.com", "https://www.field.com", "15", "1500", "Left Street", "Memphis", "TN", "Q1R 2S3"],
        ["Steve", "Target", 16,"Target Innovations", "+1 (305) 555-0222", "steve.target@example.com", "https://www.target.com", "16", "1600", "Main Street", "Miami", "FL", "T4U 5V6"],
        ["Tina", "Walton", 17,"Walton Consult", "+1 (312) 555-0233", "tina.walton@example.com", "https://www.walton.com", "17", "1700", "Street Avenue", "Chicago", "IL", "W7X 8Y9"],
        ["Mark", "Erendale", 18,"Erendale Design", "+1 (615) 555-0244", "mark.erendale@example.com", "https://www.erendale.com", "18", "1800", "East Street", "Nashville", "TN", "Z1A 2B3"],
        ["John", "Nowerton", 19,"Nowerton Networks", "+1 (314) 555-0255", "john.nowerton@example.com", "https://www.nowerton.com", "19", "1900", "North Avenue", "St. Louis", "MO", "C4D 5E6"],
        ["Mary", "Hornblower", 20,"Hornblower Events", "+1 (214) 555-0266", "mary.hornblower@example.com", "https://www.hornblower.com", "20", "2000", "Elder Way", "Dallas", "TX", "G1H 2J3"]
    ]

    conn = sqlite3.connect('tree_crm.db')

    # create cursor instance - a robot does everything work you
    c = conn.cursor()
    c.execute("""
    CREATE TABLE if not exists contact (
        First_Name text,
         Last_Name text,
         ID integer,
         Company  text,                 
        Phone integer,
         Email text,
         Website text,
          Unit_Number text,
          Civic_Number text,
           Street text,
          City text,
          Province text,
          Postal_Code text
    )


    """)
    # Add dummy data to the database

    for record in data:
        c.execute("""
        INSERT INTO contact 
        (First_Name, Last_Name, ID, Company, Phone, Email, Website, Unit_Number, Civic_Number, Street, City, Province, Postal_Code) 
        VALUES 
        (:First_Name, :Last_Name, :ID, :Company, :Phone, :Email, :Website, :Unit_Number, :Civic_Number, :Street, :City, :Province, :Postal_Code)
        """, {
            'First_Name': record[0],
            'Last_Name': record[1],
            'ID': record[2],
            'Company': record[3],
            'Phone': record[4],
            'Email': record[5],
            'Website': record[6],
            'Unit_Number': record[7],
            'Civic_Number': record[8],
            'Street': record[9],
            'City': record[10],
            'Province': record[11],
            'Postal_Code': record[12]
        })

    # commit the chnages to the databases
    conn.commit()
    conn.close()

    def query_database():
        conn = sqlite3.connect('tree_crm.db')

        # create cursor instance - a robot does everything work you
        c = conn.cursor()

        c.execute("SELECT rowid, * from contact")
        records = c.fetchall()
        # fetching the data from records
        global count

        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(
                                   record[1], record[2], record[0], record[4], record[5], record[6], record[7],
                                   record[8], record[9], record[10], record[11], record[12], record[13]),
                               tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(
                                   record[1], record[2], record[0], record[4], record[5], record[6], record[7],
                                   record[8], record[9], record[10], record[11], record[12], record[13],),
                               tags=('oddrow',))
            # increment counter
            count += 1
        print(records)
        conn.commit()
        conn.close()

    # Add Some Style
    style = ttk.Style()

    # Pick A Theme
    style.theme_use('default')

    # Configure the Treeview Colors
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")

    # Change Selected Color
    style.map('Treeview',
              background=[('selected', "#347083")])

    # Create a Treeview Frame
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("First Name", "Last Name", "ID", "Company",
                          "Phone", "Email", "Website", "Unit Number", "Civic Number", "Street",
                          "City", "Province", "Postal Code")
    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("First Name", anchor=W, width=120)
    my_tree.column("Last Name", anchor=W, width=120)
    my_tree.column("ID", anchor=CENTER, width=50)
    my_tree.column("Company", anchor=CENTER, width=140)
    my_tree.column("Phone", anchor=CENTER, width=140)
    my_tree.column("Email", anchor=CENTER, width=140)
    my_tree.column("Website", anchor=CENTER, width=140)
    my_tree.column("Unit Number", anchor=CENTER, width=80)
    my_tree.column("Civic Number", anchor=CENTER, width=80)
    my_tree.column("Street", anchor=CENTER, width=140)
    my_tree.column("City", anchor=CENTER, width=120)
    my_tree.column("Province", anchor=CENTER, width=120)
    my_tree.column("Postal Code", anchor=CENTER, width=120)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("First Name", text="First Name", anchor=W)
    my_tree.heading("Last Name", text="Last Name", anchor=W)
    my_tree.heading("ID", text="ID", anchor=CENTER)
    my_tree.heading("Company", text="Company", anchor=CENTER)
    my_tree.heading("Phone", text="Phone", anchor=CENTER)
    my_tree.heading("Email", text="Email", anchor=CENTER)
    my_tree.heading("Website", text="Website", anchor=CENTER)
    my_tree.heading("Unit Number", text="Unit Number", anchor=CENTER)
    my_tree.heading("Civic Number", text="Civic Number", anchor=CENTER)
    my_tree.heading("Street", text="Street", anchor=CENTER)
    my_tree.heading("City", text="City", anchor=CENTER)
    my_tree.heading("Province", text="Province", anchor=CENTER)
    my_tree.heading("Postal Code", text="Postal Code", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    # Add our data to the screen

    # Add Record Entry Boxes
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(fill="x", expand="yes", padx=20)

    fn_label = Label(data_frame, text="First Name")
    fn_label.grid(row=0, column=0, padx=10, pady=10)
    fn_entry = Entry(data_frame)
    fn_entry.grid(row=0, column=1, padx=10, pady=10)

    ln_label = Label(data_frame, text="Last Name")
    ln_label.grid(row=0, column=2, padx=10, pady=10)
    ln_entry = Entry(data_frame)
    ln_entry.grid(row=0, column=3, padx=10, pady=10)

    id_label = Label(data_frame, text="ID")
    id_label.grid(row=0, column=4, padx=10, pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=5, padx=10, pady=10)

    Company_label = Label(data_frame, text="Company")
    Company_label.grid(row=1, column=0, padx=10, pady=10)
    Company_entry = Entry(data_frame)
    Company_entry.grid(row=1, column=1, padx=10, pady=10)

    Phone_label = Label(data_frame, text="Phone")
    Phone_label.grid(row=1, column=2, padx=10, pady=10)
    Phone_entry = Entry(data_frame)
    Phone_entry.grid(row=1, column=3, padx=10, pady=10)

    Email_label = Label(data_frame, text="Email")
    Email_label.grid(row=1, column=4, padx=10, pady=10)
    Email_entry = Entry(data_frame)
    Email_entry.grid(row=1, column=5, padx=10, pady=10)

    Website_label = Label(data_frame, text="Website")
    Website_label.grid(row=1, column=6, padx=10, pady=10)
    Website_entry = Entry(data_frame)
    Website_entry.grid(row=1, column=7, padx=10, pady=10)

    # new data frame for the address
    data_frame = LabelFrame(root, text="Address")
    data_frame.pack(fill="x", expand="yes", padx=20)

    Unit_Number_label = Label(data_frame, text="Unit number")
    Unit_Number_label.grid(row=0, column=1, padx=10, pady=10)
    Unit_Number_entry = Entry(data_frame)
    Unit_Number_entry.grid(row=0, column=2, padx=10, pady=10)

    Civic_Number_label = Label(data_frame, text="Civic Number")
    Civic_Number_label.grid(row=0, column=3, padx=10, pady=10)
    Civic_Number_entry = Entry(data_frame)
    Civic_Number_entry.grid(row=0, column=4, padx=10, pady=10)

    Street_label = Label(data_frame, text="Street")
    Street_label.grid(row=0, column=5, padx=10, pady=10)
    Street_entry = Entry(data_frame)
    Street_entry.grid(row=0, column=6, padx=10, pady=10)

    City_label = Label(data_frame, text="City")
    City_label.grid(row=1, column=1, padx=10, pady=10)
    City_entry = Entry(data_frame)
    City_entry.grid(row=1, column=2, padx=10, pady=10)

    Province_label = Label(data_frame, text="Province")
    Province_label.grid(row=1, column=3, padx=10, pady=10)
    Province_entry = Entry(data_frame)
    Province_entry.grid(row=1, column=4, padx=10, pady=10)

    Postal_Code_label = Label(data_frame, text="Postal Code")
    Postal_Code_label.grid(row=1, column=5, padx=10, pady=10)
    Postal_Code_entry = Entry(data_frame)
    Postal_Code_entry.grid(row=1, column=6, padx=10, pady=10)

    # fucntion

    def remove_all():
        response = messagebox.askyesno("Warning",
                                       "This will delete everything from the database. Are you sure you want to proceed?")
        if response:
            # Delete all records from the tree view
            for record in my_tree.get_children():
                my_tree.delete(record)

            # Update the database
            conn = sqlite3.connect('tree_crm.db')
            c = conn.cursor()
            c.execute("DELETE FROM contact")  # This deletes all rows in the table
            conn.commit()
            conn.close()
            clear_entries()
            messagebox.showinfo("Deleted", "All records have been deleted.")
        else:
            messagebox.showinfo("Cancelled", "Operation cancelled.")

    # remove one record

    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)

        # update the database
        conn = sqlite3.connect('tree_crm.db')

        # create cursor instance - a robot does everything work you
        c = conn.cursor()
        c.execute("DELETE from contact WHERE oid=" + id_entry.get())

        # fetching the data from records

        conn.commit()
        conn.close()
        clear_entries()
        messagebox.showinfo("Deleted", "Your record has been deleted")

    def remove_many():
        response = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected records?")
        if response:  # If the user clicks 'Yes', response will be True
            selected_items = my_tree.selection()
            ids_to_delete = []

            # Collect all IDs to delete
            for item in selected_items:
                ids_to_delete.append(my_tree.item(item, 'values')[2])
                my_tree.delete(item)

            # Delete from database
            conn = sqlite3.connect('tree_crm.db')
            c = conn.cursor()
            c.execute("DELETE FROM contact WHERE ID IN ({})".format(','.join('?' * len(ids_to_delete))), ids_to_delete)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Records have been deleted successfully.")
        else:
            messagebox.showinfo("Cancelled", "Operation cancelled.")

    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

    def clear_entries():
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        id_entry.delete(0, END)
        Company_entry.delete(0, END)
        Phone_entry.delete(0, END)
        Email_entry.delete(0, END)
        Website_entry.delete(0, END)
        Unit_Number_entry.delete(0, END)
        Civic_Number_entry.delete(0, END)
        Street_entry.delete(0, END)
        City_entry.delete(0, END)
        Province_entry.delete(0, END)
        Postal_Code_entry.delete(0, END)

    # Select Record
    def select_record(e):
        # Clear enrty boxes
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        id_entry.delete(0, END)
        Company_entry.delete(0, END)
        Phone_entry.delete(0, END)
        Email_entry.delete(0, END)
        Website_entry.delete(0, END)
        Unit_Number_entry.delete(0, END)
        Civic_Number_entry.delete(0, END)
        Street_entry.delete(0, END)
        City_entry.delete(0, END)
        Province_entry.delete(0, END)
        Postal_Code_entry.delete(0, END)

        # Grad Record
        seletced = my_tree.focus()
        # grab record value
        values = my_tree.item(seletced, 'values')

        # output entry boxes
        fn_entry.insert(0, values[0])
        ln_entry.insert(0, values[1])
        id_entry.insert(0, values[2])
        Company_entry.insert(0, values[3])
        Phone_entry.insert(0, values[4])
        Email_entry.insert(0, values[5])
        Website_entry.insert(0, values[6])
        Unit_Number_entry.insert(0, values[7])
        Civic_Number_entry.insert(0, values[8])
        Street_entry.insert(0, values[9])
        City_entry.insert(0, values[10])
        Province_entry.insert(0, values[11])
        Postal_Code_entry.insert(0, values[12])

    # update record

    def update_record():
        errors = validate_entries()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        selected = my_tree.focus()
        my_tree.item(selected, text="", values=(fn_entry.get(), ln_entry.get(), id_entry.get(), Company_entry.get(),
                                                Phone_entry.get(),
                                                Email_entry.get(),
                                                Website_entry.get()
                                                , Unit_Number_entry.get(),
                                                Civic_Number_entry.get(),
                                                Street_entry.get(),
                                                City_entry.get(),
                                                Province_entry.get(),
                                                Postal_Code_entry.get()))

        # update the database
        conn = sqlite3.connect('tree_crm.db')

        # create cursor instance - a robot does everything work you
        c = conn.cursor()

        c.execute("""
        UPDATE contact SET 
        first_name = :first,
        last_name = :last,
        ID = :id,
        Company = :company,
        Phone = :phone,
        Email = :email,
        Website = :website,
        Unit_Number = :unitnumber,
        Civic_Number = :civicnumber,
        Street = :street,
        City = :city,
        Province = :province,
        Postal_Code = :postalcode
        WHERE ROWID = :oid""",
                  {
                      'first': fn_entry.get(),
                      'last': ln_entry.get(),
                      'id': id_entry.get(),
                      'company': Company_entry.get(),
                      'phone': Phone_entry.get(),
                      'email': Email_entry.get(),
                      'website': Website_entry.get(),
                      'unitnumber': Unit_Number_entry.get(),
                      'civicnumber': Civic_Number_entry.get(),
                      'street': Street_entry.get(),
                      'city': City_entry.get(),
                      'province': Province_entry.get(),
                      'postalcode': Postal_Code_entry.get(),
                      'oid': id_entry.get(),
                  })
        # fetching the data from records

        conn.commit()
        conn.close()

    # aadd record

    # add record
    def add_record():
        errors = validate_entries()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        conn = sqlite3.connect('tree_crm.db')
        # create cursor instance - a robot does everything work you
        c = conn.cursor()
        # add new record
        c.execute(
            "INSERT INTO contact VALUES (:first, :last, :id, :company,:phone,:email,:website,:unitnumber,:civicnumber,:street,:city,:province,:postalcode)",
            {
                'first': fn_entry.get(),
                'last': ln_entry.get(),
                'id': id_entry.get(),
                'company': Company_entry.get(),
                'phone': Phone_entry.get(),
                'email': Email_entry.get(),
                'website': Website_entry.get(),
                'unitnumber': Unit_Number_entry.get(),
                'civicnumber': Civic_Number_entry.get(),
                'street': Street_entry.get(),
                'city': City_entry.get(),
                'province': Province_entry.get(),
                'postalcode': Postal_Code_entry.get(),
            })

        conn.commit()
        conn.close()
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        id_entry.delete(0, END)
        Company_entry.delete(0, END)
        Phone_entry.delete(0, END)
        Email_entry.delete(0, END)
        Website_entry.delete(0, END)
        Unit_Number_entry.delete(0, END)
        Civic_Number_entry.delete(0, END)
        Street_entry.delete(0, END)
        City_entry.delete(0, END)
        Province_entry.delete(0, END)
        Postal_Code_entry.delete(0, END)

        # clear tree view
        my_tree.delete(*my_tree.get_children())
        query_database()

    # Add Buttons
    button_frame = LabelFrame(root, text="Commands")
    button_frame.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame, text="Update Record", command=update_record)
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame, text="Add Record", command=add_record)
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
    remove_all_button.grid(row=0, column=2, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    remove_many_button = Button(button_frame, text="Remove Many Selected", command=remove_many)
    remove_many_button.grid(row=0, column=4, padx=10, pady=10)

    move_up_button = Button(button_frame, text="Move Up", command=up)
    move_up_button.grid(row=0, column=5, padx=10, pady=10)

    move_down_button = Button(button_frame, text="Move Down", command=down)
    move_down_button.grid(row=0, column=6, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Enrty", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)

    # bind with treeview
    my_tree.bind("<ButtonRelease-1>", select_record)
    query_database()
    root.mainloop()


def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "password":
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")


# Setup Login Window
login_window = Tk()
login_window.title("Login")
login_window.geometry("300x200")

username_label = Label(login_window, text="Username:")
username_label.pack(pady=(10, 0))
username_entry = Entry(login_window, width=25)
username_entry.pack()

password_label = Label(login_window, text="Password:")
password_label.pack(pady=(10, 0))
password_entry = Entry(login_window, width=25, show="*")
password_entry.pack()

login_button = Button(login_window, text="Login", command=login)
login_button.pack(pady=20)

login_window.mainloop()