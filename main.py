# imports
import tkinter
from tkinter import ttk


#code
root_window = tkinter.Tk()

frame = tkinter.Frame(root_window)
frame.pack()

user_info_frame = tkinter.LabelFrame(frame, text = "User Information")
user_info_frame.grid(row=0, column=0)

first_name_label = tkinter.Label(user_info_frame, text= "First Name")
first_name_label.grid(row=0, column=0)

last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0,column=1)

first_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1,column=0)

last_name_label_entry = tkinter.Entry(user_info_frame)
last_name_label_entry.grid(row=1,column=1)

title_label = tkinter.Label(user_info_frame, text="Title")
title_label.grid(row=1,column=2)

title_label = tkinter.Label(user_info_frame, text="Title")
title_label.grid(row=0,column=2)

combobox_values = ["998", "Mr", "Ms", "Dr"]
title_combobox = ttk.Combobox(user_info_frame, values= combobox_values)
title_combobox.grid(row=1,column=2)

age_label = tkinter.Label(user_info_frame, text="Age")
age_label.grid(row=2, column=0)

age_spinbox = tkinter.Spinbox(user_info_frame,from_=18,to=110)
age_spinbox.grid(row=3, column=0)

combobox_values = ["Africa", "Antarctica", "Asia", "North America", "South America","Oceania"]
nationality_label = tkinter.Label(user_info_frame, text= "Nationality")
nationality_label.grid(row=2, column=1)

nationality_combobox = ttk.Combobox(user_info_frame, values=combobox_values)
nationality_combobox.grid(row=3,column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# saving courses Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news",padx=20, pady=20)

registered_label = tkinter.Label(courses_frame, text="Registration Status")
registered_label.grid(row=0, column=0)
registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registerd")
registered_check.grid(row=1, column=0)

numcourses_label =tkinter.Label(courses_frame, text="# Completed Courses")
numcourses_label.grid(row=0, column=1)
numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0,to ="infinity")
numcourses_spinbox.grid(row=1, column=1)

numsemesters_label =tkinter.Label(courses_frame, text="# Completed Courses")
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0,to ="infinity")
numsemesters_spinbox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)


# accept therms

terms_frame =  tkinter.LabelFrame(frame, text="Terms and conditions")

root_window.mainloop()


root_window.mainloop()


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#   root_window.mainloop()


