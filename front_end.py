__author__ = "Theresa De Ocampo"
__version__ = "3.8.2"
__email__ = "maria.theresa.g.de.ocampo@gmail.com"

from tkinter import *
from tkinter import ttk
import datetime as dt
import back_end
from tkinter import messagebox


class Resident:
    def __init__(self, root):
        self.root = root
        self.root.title("Barangay Profiling System")
        self.root.state('zoomed')
        self.root.config(bg="teal")

        fname = StringVar()
        mname = StringVar()
        lname = StringVar()
        cellphone = StringVar()
        house_num = StringVar()
        street = StringVar()

        # ************************************   Methods   ************************************ #
        # ------------- Helper Methods ------------- #
        def get_selected_record(event):
            global record
            if residents_list.curselection():                # Handles the situation when nothing is selected
                target = residents_list.curselection()[0]
                if target % 2 == 0:                          # Handles the situation when a seperator row is selected
                    record = residents_list.get(target)

                    clear_registration()
                    self.fname_entry.insert(END, record[1])
                    self.mname_entry.insert(END, record[2])
                    self.lname_entry.insert(END, record[3])

                    i = get_index(record[4], self.gender_cb['values'])
                    self.gender_cb.delete(0, END)
                    self.gender_cb.current(i)

                    self.occupation_cb.delete(0, END)
                    self.occupation_cb.insert(END, record[5])

                    self.cellphone_entry.insert(END, record[6])

                    i = get_index(record[7], self.educ_cb['values'])
                    self.educ_cb.delete(0, END)
                    self.educ_cb.current(i)

                    i = get_index(record[8], self.bmonth_cb['values'])
                    self.bmonth_cb.delete(0, END)
                    self.bmonth_cb.current(i)

                    i = get_index(record[9], self.bday_cb['values'])
                    self.bday_cb.delete(0, END)
                    self.bday_cb.current(i)

                    i = get_index(record[10], self.byear_cb['values'])
                    self.byear_cb.delete(0, END)
                    self.byear_cb.current(i)

                    self.house_num_entry.insert(END, record[11])
                    self.street_entry.insert(END, record[12])

        def clear_registration():
            self.fname_entry.delete(0, END)
            self.mname_entry.delete(0, END)
            self.lname_entry.delete(0, END)
            self.gender_cb.set('')
            self.occupation_cb.delete(0, END)
            self.cellphone_entry.delete(0, END)
            self.educ_cb.delete(0, END)
            self.bmonth_cb.set('')
            self.bday_cb.set('')
            self.byear_cb.set('')
            self.house_num_entry.delete(0, END)
            self.street_entry.delete(0, END)

        def clear_journal():
            residents_list.delete(0, 'end')

        def insert_curr_entry():
            clear_journal()
            residents_list.insert(END, fname.get(), mname.get(), lname.get(), self.gender_cb.get(),
                                  self.occupation_cb.get(), self.cellphone_entry.get(), self.educ_cb.get(),
                                  self.bmonth_cb.get(), self.bday_cb.get(), self.byear_cb.get(), house_num.get(),
                                  street.get())

        def clear_data():
            clear_registration()
            clear_journal()

        def show_confirmation_message():
            answer = messagebox.askquestion("Dulao",
                                            '''Are you sure you want to delete this record?\nYou cannot undo this 
                                            action.''', icon='warning')
            if answer == 'no':
                return 0
            else:
                return 1

        def get_index(selected, options):
            i = 0
            for item in options:
                if str(item) == str(selected):
                    return i
                else:
                    i += 1

        # ------------- Validation Methods ------------- #
        def check_for_completion():
            error_message = ""
            if len(fname.get()) == 0:
                error_message += "\n\tFirst Name"
            if len(lname.get()) == 0:
                error_message += "\n\tLast Name"
            if len(self.gender_cb.get()) == 0:
                error_message += "\n\tGender"
            if len(self.occupation_cb.get()) == 0:
                error_message += "\n\tOccupation"
            if len(self.educ_cb.get()) == 0:
                error_message += "\n\tEducation"

            if len(self.bmonth_cb.get()) == 0 and len(self.bday_cb.get()) == 0 and len(self.byear_cb.get()) == 0:
                error_message += "\n\tBirthday"
            else:
                if len(self.bmonth_cb.get()) == 0:
                    error_message += "\n\tBirth Month"
                if len(self.bday_cb.get()) == 0:
                    error_message += "\n\tBirth Day"
                if len(self.byear_cb.get()) == 0:
                    error_message += "\n\tBirth Year"

            if len(house_num.get()) == 0 and len(street.get()) == 0:
                error_message += "\n\tAddress"
            else:
                if len(house_num.get()) == 0:
                    error_message += "\n\tHouse Number"
                if len(street.get()) == 0:
                    error_message += "\n\tStreet Address"
            return error_message

        def show_incomplete_error_message(error_message):
            error_message = "The following field(s) is/are required.\n" + error_message
            messagebox.showerror("Dulao", error_message)

        def show_not_following_instructions_message(operation):
            error_message = "To " + operation + " a record, please select it from the journal first.\n"
            error_message += "If you are having a hard time scrolling for the record, use the search feature."
            messagebox.showerror("Dulao", error_message)

        def show_invalid_cp_message():
            messagebox.showerror("Dulao", "Please enter a phone number in the format 09XXXXXXXXX.")

        def cp_is_valid(phone_number):
            if len(phone_number) == 0:
                return True
            if len(phone_number) != 11:
                return False
            if phone_number[0] != '0':
                return False
            if phone_number[1] != '9':
                return False
            for i in range(11):
                if not (phone_number[i].isdigit()):
                    return False
            return True

        # ------------- Main Methods ------------- #
        def add_record():
            error_message = check_for_completion()
            if error_message:
                show_incomplete_error_message(error_message)
            else:
                if cp_is_valid(cellphone.get()):
                    back_end.add_resident(fname.get().title(), mname.get().title(), lname.get().title(),
                                          self.gender_cb.get(), self.occupation_cb.get().title(), cellphone.get(),
                                          self.educ_cb.get(), self.bmonth_cb.get(), self.bday_cb.get(),
                                          self.byear_cb.get(), house_num.get(), street.get())
                    insert_curr_entry()
                else:
                    show_invalid_cp_message()

        def delete_record():
            if check_for_completion():
                show_not_following_instructions_message("delete")
            else:
                flag = show_confirmation_message()
                if flag == 1:
                    back_end.delete_resident(record[0])
                    view_records()

        def view_records():
            clear_data()
            for row in back_end.view_residents():
                residents_list.insert(END, row, str(""))

        def search_records():
            clear_journal()
            results = back_end.search_residents(fname.get().title(), mname.get().title(), lname.get().title(),
                                                self.gender_cb.get(), self.occupation_cb.get().title(), cellphone.get(),
                                                self.educ_cb.get(), self.bmonth_cb.get(), self.bday_cb.get(),
                                                self.byear_cb.get(), house_num.get(), street.get())
            if len(results) == 0:
                residents_list.insert(END, "Your search did not match any records.")
            for row in results:
                residents_list.insert(END, row, str(""))

        def update_record():
            if check_for_completion():
                show_not_following_instructions_message("update")
            else:
                if cp_is_valid(cellphone.get()):
                    back_end.delete_resident(record[0])
                    back_end.add_resident(fname.get().title(), mname.get().title(), lname.get().title(),
                                          self.gender_cb.get(), self.occupation_cb.get().title(), cellphone.get(),
                                          self.educ_cb.get(), self.bmonth_cb.get(), self.bday_cb.get(),
                                          self.byear_cb.get(), house_num.get(), street.get())
                    insert_curr_entry()
                else:
                    show_invalid_cp_message()

        # *******************************************   Frames   ******************************************* #
        main_frame = Frame(self.root, bg="teal", pady=20)
        main_frame.pack()

        header_frame = Frame(main_frame, bg="cadet blue", bd=20, relief=RIDGE)
        header_frame.pack(side=TOP)

        self.logo = PhotoImage(file="logo.png")
        self.logo_container = Label(header_frame, image=self.logo, bg="navy", padx=310)
        self.logo_container.pack(side=LEFT)

        self.title_label = Label(header_frame, bg="beige", padx=200, pady=12, font=("Glacial Indifference", 50, 'bold'),
                                 text="Barangay Dulao", bd=5, relief=RIDGE)
        self.title_label.pack(side=LEFT)

        content_frame = Frame(main_frame, bg="teal", padx=20, pady=20, relief=RIDGE)
        content_frame.pack(side=BOTTOM)

        buttons_frame_holder = Frame(main_frame, bg="teal", pady=10)
        buttons_frame = Frame(buttons_frame_holder, bg="cadet blue", padx=10, pady=10, relief=RIDGE)
        buttons_frame.pack()
        buttons_frame_holder.pack(side=TOP)

        registration_frame = LabelFrame(content_frame, bg="alice blue", padx=10, pady=10, bd=5, relief=SOLID,
                                        width=970, height=600, font=("Glacial Indifference", 25, 'bold'),
                                        text="Registration", labelanchor=N)
        registration_frame.pack(side=LEFT)
        registration_frame.grid_propagate(False)
        seperator_frame = Frame(content_frame, bg="teal", width=30, height=600)
        seperator_frame.pack(side=LEFT)
        journal_frame = LabelFrame(content_frame, bg="alice blue", padx=10, pady=10, bd=5, relief=SOLID, width=830,
                                   height=600, font=("Glacial Indifference", 25, 'bold'), text="Journal", labelanchor=N)
        journal_frame.pack(side=RIGHT)
        journal_frame.grid_propagate(False)

        # ***************************************   Labels & Entry Widgets   *************************************** #
        # ------------- Name ------------- #
        self.name_frame = LabelFrame(registration_frame, bg="alice blue", font=("Glacial Indifference", 20),
                                     text="Name", padx=10)
        self.name_frame.grid(row=0, columnspan=2)

        self.fname_label = Label(self.name_frame, bg="alice blue", padx=10, pady=8,
                                 font=("Glacial Indifference", 15), text="First Name")
        self.fname_label.grid(row=0, column=0, stick=W)
        self.fname_entry = Entry(self.name_frame, font=("Courier New", 15), textvariable=fname, bg="alice blue",
                                 relief=SOLID, width=15)
        self.fname_entry.grid(row=0, column=1)

        self.mname_label = Label(self.name_frame, bg="alice blue", padx=10, pady=8,
                                 font=("Glacial Indifference", 15), text="Middle Name")
        self.mname_label.grid(row=1, column=0, stick=W)
        self.mname_entry = Entry(self.name_frame, font=("Courier New", 15), textvariable=mname, bg="alice blue",
                                 relief=SOLID, width=15)
        self.mname_entry.grid(row=1, column=1)

        self.lname_label = Label(self.name_frame, bg="alice blue", padx=10, pady=8, font=("Glacial Indifference", 15),
                                 text="Last Name")
        self.lname_label.grid(row=2, column=0, stick=W)
        self.lname_entry = Entry(self.name_frame, font=("Courier New", 15), textvariable=lname, bg="alice blue",
                                 relief=SOLID, width=15)
        self.lname_entry.grid(row=2, column=1)

        # ------------- Gender ------------- #
        self.gender_label = Label(registration_frame, bg="alice blue", padx=10, pady=8,
                                  font=("Glacial Indifference", 15), text="Gender")
        self.gender_label.grid(row=1, column=0, stick=W)
        self.gender_cb = ttk.Combobox(registration_frame, font=("Courier New", 15), width=8, state="readonly")
        self.gender_cb['values'] = ("Male", "Female")
        self.gender_cb.grid(row=1, column=1, stick=W)

        # ------------- Occupation ------------- #
        self.occupation_label = Label(registration_frame, bg="alice blue", padx=10, pady=8,
                                      font=("Glacial Indifference", 15), text="Occupation")
        self.occupation_label.grid(row=2, column=0, stick=W)
        self.occupation_cb = ttk.Combobox(registration_frame, font=("Courier New", 15), width=14)
        self.occupation_cb['values'] = ("None",)
        self.occupation_cb.grid(row=2, column=1, stick=W)

        # ------------- Cellphone Number ------------- #
        self.cellphone_label = Label(registration_frame, bg="alice blue", padx=10, pady=8,
                                     font=("Glacial Indifference", 15), text="Contact No.")
        self.cellphone_label.grid(row=3, column=0, stick=W)
        self.cellphone_entry = Entry(registration_frame, font=("Courier New", 15), textvariable=cellphone,
                                     bg="alice blue", relief=SOLID, width=15)
        self.cellphone_entry.grid(row=3, column=1)

        # ------------- Seperator ------------- #
        self.sub_seperator_frame = Frame(registration_frame, bg="alice blue", width=40)
        self.sub_seperator_frame.grid(row=0, column=2)

        # ------------- Birthday ------------- #
        self.bday_frame = LabelFrame(registration_frame, bg="alice blue", font=("Glacial Indifference", 20),
                                     text="Birthday", padx=40)
        self.bday_frame.grid(row=0, column=3, columnspan=2)

        self.bmonth_label = Label(self.bday_frame, bg="alice blue", padx=10, pady=8, font=("Glacial Indifference", 15),
                                  text="Month")
        self.bmonth_label.grid(row=0, column=0, stick=W)
        self.bmonth_cb = ttk.Combobox(self.bday_frame, font=("Courier New", 15), width=10, state="readonly")
        self.bmonth_cb['values'] = ("January", "February", "March", "April", "May", "June", "July", "August",
                                    "September", "October", "November", "December")
        self.bmonth_cb.grid(row=0, column=1, stick=W)

        self.bday_label = Label(self.bday_frame, bg="alice blue", padx=10, pady=8, font=("Glacial Indifference", 15),
                                text="Day")
        self.bday_label.grid(row=1, column=0, stick=W)
        self.bday_cb = ttk.Combobox(self.bday_frame, font=("Courier New", 15), width=3, state="readonly")
        day_choices = list(range(1, 32))
        self.bday_cb['values'] = day_choices
        self.bday_cb.grid(row=1, column=1, stick=W)

        self.byear_label = Label(self.bday_frame, bg="alice blue", padx=10, pady=8, font=("Glacial Indifference", 15),
                                 text="Year")
        self.byear_label.grid(row=2, column=0, stick=W)
        self.byear_cb = ttk.Combobox(self.bday_frame, font=("Courier New", 15), width=5, state="readonly")
        curr_year = dt.date.today().year
        year_choices = list(range(curr_year - 110, curr_year + 1))
        year_choices = reverse_tuple(year_choices)
        self.byear_cb['values'] = year_choices
        self.byear_cb.grid(row=2, column=1, stick=W)

        # ------------- Address ------------- #
        self.address_frame = LabelFrame(registration_frame, bg="alice blue", font=("Glacial Indifference", 20),
                                        text="Address", padx=10)
        self.address_frame.grid(row=1, rowspan=3, column=3, columnspan=2, stick=W)

        self.house_num_label = Label(self.address_frame, bg="alice blue", padx=10, pady=8,
                                     font=("Glacial Indifference", 15), text="House No.")
        self.house_num_label.grid(row=0, column=0, stick=W)
        self.house_num_entry = Entry(self.address_frame, font=("Courier New", 15), textvariable=house_num,
                                     bg="alice blue", relief=SOLID, width=4)
        self.house_num_entry.grid(row=0, column=1, stick=W)

        self.street_label = Label(self.address_frame, bg="alice blue", padx=10, pady=8,
                                  font=("Glacial Indifference", 15), text="Street")
        self.street_label.grid(row=1, column=0, stick=W)
        self.street_entry = Entry(self.address_frame, font=("Courier New", 15), textvariable=street,
                                  bg="alice blue", relief=SOLID, width=12)
        self.street_entry.grid(row=1, column=1)

        # ------------- Highest Educational Attainment ------------- #
        self.educ_label = Label(registration_frame, bg="alice blue", padx=10, pady=8, font=("Glacial Indifference", 15),
                                text="Highest Educational Attainment")
        self.educ_label.grid(row=4, column=0, columnspan=2, stick=W)
        self.educ_cb = ttk.Combobox(registration_frame, font=("Courier New", 15), width=20)
        self.educ_cb['values'] = ("Some Elementary", "Elementary Graduate", "Some High School", "High School Graduate",
                                  "Some College", "Bachelor's Degree", "Vocational", "Advanced Degree")
        self.educ_cb.grid(row=5, column=0, columnspan=2, stick=E)

        # ************************************   Listbox & Scrollbar Widgets   ************************************ #
        yscrollbar = Scrollbar(journal_frame)
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar = Scrollbar(journal_frame, orient='horizontal')
        xscrollbar.grid(row=1, column=0, sticky="we")

        residents_list = Listbox(journal_frame, width=44, height=13, font=("Glacial Indifference", 15),
                                 yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        residents_list.bind('<<ListboxSelect>>', get_selected_record)
        residents_list.grid(row=0, column=0, padx=8)
        yscrollbar.config(command=residents_list.yview)
        xscrollbar.config(command=residents_list.xview)

        # ************************************   Button Widgets   ************************************ #
        self.add_button = Button(buttons_frame, text="Add", font=("Glacial Indifference", 15, 'bold'), bd=4, width=10,
                                 bg="light blue2", command=add_record)
        self.add_button.grid(row=0, column=0, padx=5)

        self.view_button = Button(buttons_frame, text="View", font=("Glacial Indifference", 15, 'bold'), bd=4, width=10,
                                  bg="light blue2", command=view_records)
        self.view_button.grid(row=0, column=1, padx=5)

        self.clear_button = Button(buttons_frame, text="Clear", font=("Glacial Indifference", 15, 'bold'), bd=4,
                                   width=10, bg="light blue2", command=clear_data)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.delete_button = Button(buttons_frame, text="Delete", font=("Glacial Indifference", 15, 'bold'), bd=4,
                                    width=10, bg="light blue2", command=delete_record)
        self.delete_button.grid(row=0, column=3, padx=5)

        self.search_button = Button(buttons_frame, text="Search", font=("Glacial Indifference", 15, 'bold'), bd=4,
                                    width=10, bg="light blue2", command=search_records)
        self.search_button.grid(row=0, column=4, padx=5)

        self.update_button = Button(buttons_frame, text="Update", font=("Glacial Indifference", 15, 'bold'), bd=4,
                                    width=10, bg="light blue2", command=update_record)
        self.update_button.grid(row=0, column=5, padx=5)

        self.analyze_button = Button(buttons_frame, text="Analyze", font=("Glacial Indifference", 15, 'bold'), bd=4,
                                     width=10, bg="light blue2", command=back_end.analyze)
        self.analyze_button.grid(row=0, column=6, padx=5)


def reverse_tuple(t):
    new_tup = t[::-1]
    return new_tup


window = Tk()
application = Resident(window)
window.mainloop()
