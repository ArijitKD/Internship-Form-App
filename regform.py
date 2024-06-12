APP_NAME = "Next24tech Registration Form"
dependency_flag_set = 0

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox as mbox
except ModuleNotFoundError:    
    print ("Warning: Tkinter was not found.")
    dependency_flag_set = 1
try:
    from PIL import ImageTk, Image
except ModuleNotFoundError:
    print ("Warning: PIL was not found.")
    dependency_flag_set = 1
except ImportError:
    print ("Warning: PIL ImageTk was not found.")
    dependency_flag_set = 1

if (dependency_flag_set):
    print ("One or more dependencies are not installed. To avoid unintended side-effects, dependencies won\'t be auto-installed. The following the steps may be useful for resolving the issues:")
    from os import name
    if (name=="nt"):
        print ("*   For installing PIL, make sure pip3 is on the PATH then run the command \"pip3 install pillow\" (no quotes).")
        print ("*   For installing Tkinter, reinstall Python with Tcl/Tk support.")
        print ("*   Re-run "+APP_NAME+".")
    else:
        print ("*   Use your package manager in sudo mode and install the following packages: python3-tk, python3-pil.imagetk.")
        print ("*   Re-run "+APP_NAME+".")
    raise SystemExit(1)

            
base_window = tk.Tk()

# Get the screen dimesions
SCR_WIDTH = base_window.winfo_screenwidth()
SCR_HEIGHT = base_window.winfo_screenheight()

# Base window dimensions
WIN_WIDTH = 480
WIN_HEIGHT = 640
WIN_BG = '#f3f0e6'

# Define ttk styles
style = ttk.Style()
style.configure("placeholder.TEntry", foreground="gray")
style.configure("text.TEntry", foreground="black")
style.configure("placeholder.TMenubutton", foreground="gray", background=WIN_BG)
style.configure("text.TMenubutton", foreground="black", background=WIN_BG)

# Place the window at the screen center
center_x = int((SCR_WIDTH/2) - (WIN_WIDTH/2))
center_y = int((SCR_HEIGHT/2) - (WIN_HEIGHT/2))
base_window.geometry(str(WIN_WIDTH)+"x"+str(WIN_HEIGHT)+"+"+str(center_x)+"+"+str(center_y))

# Set the base window title (app name)
base_window.title(APP_NAME)

# Disable window maximization (since most of the window would otherwise appear empty)
base_window.resizable(0,0)

# Add a callback function for the close window event
def on_close():
    close_window = mbox.askyesno(title="Close form", message="Do you really want to close this form?", default="no")
    if (close_window):
        base_window.destroy()
    return close_window

# Add a close window event function        
base_window.protocol("WM_DELETE_WINDOW", on_close)

# Change the base window background color
base_window.configure(background=WIN_BG)


# Add company logo at the top
img = ImageTk.PhotoImage(Image.open("next24tech_cover_480x120.png"))
tk.Label(base_window, image = img, background=WIN_BG).pack(side = "top", pady=(10,50))


# Defining callback functions for entries
def entry_focusin_callback(event, textvariable):
    if (textvariable.get().startswith("Enter your ") or textvariable.get().startswith("Specify ")):
        event.widget.delete(0, 'end')
        event.widget.configure(style="text.TEntry")
    else:
        if (str(event.widget).find("entry") != -1):
            event.widget.event_generate("<Control-a>", x=0, y=0)
            event.widget.xview_moveto(len(textvariable.get()))


def entry_focusout_callback(event, textvariable, placeholder, what_data=""):
    entry_data = textvariable.get()
    invalid_data = False
    custom_invalid_msg = ""
    
    if (entry_data == ""):
        event.widget.configure(style="placeholder.TEntry")
        event.widget.insert(0, placeholder)
        event.widget.icursor(0)

    if (what_data == "phone number"):
        if (entry_data != ""):
            if (len(entry_data) != 10 or not entry_data.isnumeric()):
                invalid_data = True
            
    elif (what_data == "email id"):
        at_index = entry_data.find('@')
        dot_index = entry_data.find('.')
        domain_name = entry_data[at_index+1::]
        if (entry_data != ""):
            if (at_index == -1 or dot_index == -1 or entry_data.count('@') != 1 or domain_name.startswith('.') or domain_name.endswith('.') or not domain_name.replace('.','').isalpha()):
                invalid_data = True
    
    elif (what_data == "course year"):
        if (entry_data != ""):
            if (entry_data.isdigit()):
                current_course = course_var.get()
                if (current_course != "Other"):
                    try:
                        max_year = int(current_course[current_course.index('-')+2])                    
                        if (not (0 < int(entry_data) <= max_year)):
                            invalid_data = True
                            custom_invalid_msg = "\"%s\" is not a valid year for a %s course."%(entry_data, current_course)
                    except ValueError:
                        invalid_data = True
                        custom_invalid_msg = "Please choose a course first."
                else:
                    if (int(entry_data) < 1):
                        invalid_data = True
                    elif (int(entry_data) > 72):
                        invalid_data = True
                        custom_invalid_msg = "Take rest oldie. You needn\'t work. We\'ll help you if you\'re financially weak."
            else:
                invalid_data = True
                
    elif (what_data == "course"):
        pass
    
    else:
        if (entry_data != ""):
            if (not entry_data.isalpha()):
                invalid_data = True
                
    if (invalid_data):
        if (custom_invalid_msg == ""):
            mbox.showerror(title="Invalid "+what_data, message="\""+entry_data+"\" is not a valid %s. Please enter a valid %s."%(what_data, what_data))
        else:
            mbox.showerror(title="Invalid "+what_data, message=custom_invalid_msg)
        event.widget.configure(style="placeholder.TEntry")
        event.widget.delete(0, 'end')
        event.widget.insert(0, placeholder)
        event.widget.icursor(0)
        event.widget.focus_set()


def circulate_thru_widgets(event, key="Tab"):
    try:
        current_index = all_widgets.index(event.widget)
    except:
        all_widgets[0].focus_set()
        return    
    next_index = current_index + (-1 if key=='Up' else 1)
    if (next_index >= len(all_widgets)):
        if (key=="Return"):
            base_window.focus_set()
            return
        else:
            next_index = 0    
    if (key == 'Up'):
        if (all_widgets[next_index] == course_menu_other_entry and not course_menu_other_entry_visible):
            next_index -= 1
    else:
        if (all_widgets[next_index] == course_menu_other_entry and not course_menu_other_entry_visible):
            next_index += 1
    all_widgets[next_index].focus_set()
    try:
        all_widgets[current_index].xview_moveto(0)
    except:
        pass
    if (all_widgets[next_index] == course_menu):
        all_widgets[next_index].event_generate("<Button-1>", x=0, y=0)
        
            
# Add a name entry label and field
name_var = tk.StringVar()
name_var.set("")
name_frame = tk.Frame(base_window, background=WIN_BG)
name_frame.pack(fill="both", pady=(0,15))
tk.Label(name_frame, text = 'Your name', background=WIN_BG).pack(side="left", padx=(50,0))
name_entry = ttk.Entry(name_frame, width=40, textvariable = name_var, style="placeholder.TEntry")
name_entry.insert(0, "Enter your name")
name_entry.icursor(0)
name_entry.pack(side="right", ipady=5, padx=(0,50))
name_entry.bind('<FocusIn>', lambda event, textvariable=name_var : entry_focusin_callback(event, textvariable))
name_entry.bind('<FocusOut>', lambda event, textvariable=name_var, placeholder="Enter your name", what_data="name" :
                 entry_focusout_callback(event, textvariable, placeholder, what_data))
name_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))


# Add a phone number entry label and field
phone_var = tk.StringVar()
phone_var.set("")
phone_frame = tk.Frame(base_window, background=WIN_BG)
phone_frame.pack(fill="both", pady=(0,15))
tk.Label(phone_frame, text = 'Phone number', background=WIN_BG).pack(side="left", padx=(50,0))
phone_entry = ttk.Entry(phone_frame, width=40, textvariable = phone_var, style="placeholder.TEntry")
phone_entry.insert(0, "Enter your 10-digit phone number")
phone_entry.icursor(0)
phone_entry.pack(side="right", ipady=5, padx=(0,50))
phone_entry.bind('<FocusIn>', lambda event, textvariable=phone_var : entry_focusin_callback(event, textvariable))
phone_entry.bind('<FocusOut>', lambda event, textvariable=phone_var, placeholder="Enter your 10-digit phone number", what_data="phone number":
                 entry_focusout_callback(event, textvariable, placeholder, what_data))
phone_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))


# Add an email entry label and field
email_var = tk.StringVar()
email_var.set("")
email_frame = tk.Frame(base_window, background=WIN_BG)
email_frame.pack(fill="both", pady=(0,15))
tk.Label(email_frame, text = 'E-mail ID', background=WIN_BG).pack(side="left", padx=(50,0))
email_entry = ttk.Entry(email_frame, width=40, textvariable = email_var, style="placeholder.TEntry")
email_entry.insert(0, "Enter your email id")
email_entry.icursor(0)
email_entry.pack(side="right", ipady=5, padx=(0,50))
email_entry.bind('<FocusIn>', lambda event, textvariable=email_var : entry_focusin_callback(event, textvariable))
email_entry.bind('<FocusOut>', lambda event, textvariable=email_var, placeholder="Enter your email id", what_data="email id":
                 entry_focusout_callback(event, textvariable, placeholder, what_data))
email_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))


# Add a college name entry label and field
college_var = tk.StringVar()
college_var.set("")
college_frame = tk.Frame(base_window, background=WIN_BG)
college_frame.pack(fill="both", pady=(0,15))
tk.Label(college_frame, text = 'College name', background=WIN_BG).pack(side="left", padx=(50,0))
college_entry = ttk.Entry(college_frame, width=40, textvariable = college_var, style="placeholder.TEntry")
college_entry.insert(0, "Enter your college name")
college_entry.icursor(0)
college_entry.pack(side="right", ipady=5, padx=(0,50))
college_entry.bind('<FocusIn>', lambda event, textvariable=college_var : entry_focusin_callback(event, textvariable))
college_entry.bind('<FocusOut>', lambda event, textvariable=college_var, placeholder="Enter your college name", what_data="college name" :
                 entry_focusout_callback(event, textvariable, placeholder, what_data))
college_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))


# Add a course selection optionmenu
course_menu_other_entry_visible = False
def course_menu_callback(selected_option):
    global course_menu_other_entry_visible
    course_menu.configure(style="text.TMenubutton")
    if (selected_option == "Other"):
        course_menu.configure(width=10)
        course_menu.pack(side="left", padx=(50,0))
        course_menu_other_entry.pack(side="left", ipady=5, padx=(5,50))
        course_menu_other_entry_visible = True
    else:
        course_menu_other_entry.pack_forget()
        course_menu.configure(width=40)
        course_menu.pack(side="left", ipady=5, padx=(50,50))        
        max_year = int(selected_option[selected_option.index('-')+2])
        current_course_year = course_year_var.get()
        if (current_course_year.isdigit()):
            current_course_year = int(current_course_year)
            if (current_course_year > max_year):
                course_year_var.set(str(max_year))
        course_menu_other_entry_visible = False

        
courses = ["B.E/B.Tech - 4 yrs",
           "Integrated B.Tech+M.Tech - 5 yrs",
           "B.Sc - 3 yrs",
           "B.Sc (Hons) - 3 yrs",
           "B.C.A - 3 yrs",
           "B.B.A - 3 yrs",
           "B.Com - 3 yrs",
           "Other"]
course_var = tk.StringVar()
course_frame = tk.Frame(base_window, background=WIN_BG)
course_frame.pack(fill="both", pady=(0,15))
tk.Label(course_frame, text = 'Current course', background=WIN_BG).pack(side="left", padx=(50,0), ipady=5)
course_menu = ttk.OptionMenu(course_frame, course_var, "Choose your course", *courses, command=course_menu_callback)
course_menu.configure(width=40, style="placeholder.TMenubutton", padding=3)
course_menu.pack(side="left", ipady=5, padx=(50,50))
course_menu.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))

course_menu_other_var = tk.StringVar()
course_menu_other_entry = ttk.Entry(course_frame, width=40, textvariable = course_menu_other_var, style="placeholder.TEntry")
course_menu_other_entry.insert(0, "Specify your course")
course_menu_other_entry.icursor(0)
course_menu_other_entry.pack(side="right", ipady=5, padx=(0,50))
course_menu_other_entry.bind('<FocusIn>', lambda event, textvariable=course_menu_other_var : entry_focusin_callback(event, textvariable))
course_menu_other_entry.bind('<FocusOut>', lambda event, textvariable=course_menu_other_var, placeholder="Specify your course", what_data="course" :
                 entry_focusout_callback(event, textvariable, placeholder, what_data))
course_menu_other_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))


# Add a specialization entry label and field
specialization_var = tk.StringVar()
specialization_var.set("")
specialization_frame = tk.Frame(base_window, background=WIN_BG)
specialization_frame.pack(fill="both", pady=(0,15))
tk.Label(specialization_frame, text = 'Course specialization', background=WIN_BG).pack(side="left", padx=(50,0))
specialization_entry = ttk.Entry(specialization_frame, width=40, textvariable = specialization_var, style="placeholder.TEntry")
specialization_entry.insert(0, "Enter your specialization")
specialization_entry.icursor(0)
specialization_entry.pack(side="right", ipady=5, padx=(0,50))
specialization_entry.bind('<FocusIn>', lambda event, textvariable=specialization_var : entry_focusin_callback(event, textvariable))
specialization_entry.bind('<FocusOut>', lambda event, textvariable=specialization_var, placeholder="Enter your specialization", what_data="specialization" :
                 entry_focusout_callback(event, textvariable, placeholder, what_data))
specialization_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))
           

# Add a course year entry label and field
course_year_var = tk.StringVar()
course_year_var.set("")
course_year_frame = tk.Frame(base_window, background=WIN_BG)
course_year_frame.pack(fill="both", pady=(0,15))
tk.Label(course_year_frame, text = 'Course year', background=WIN_BG).pack(side="left", padx=(50,0))
course_year_entry = ttk.Entry(course_year_frame, width=40, textvariable = course_year_var, style="placeholder.TEntry")
course_year_entry.insert(0, "Enter your course year")
course_year_entry.icursor(0)
course_year_entry.pack(side="right", ipady=5, padx=(0,50))
course_year_entry.bind('<FocusIn>', lambda event, textvariable=course_year_var : entry_focusin_callback(event, textvariable))
course_year_entry.bind('<FocusOut>', lambda event, textvariable=course_year_var, placeholder="Enter your course year", what_data="course year":
                 entry_focusout_callback(event, textvariable, placeholder, what_data))
course_year_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))


all_widgets = [name_entry, phone_entry, email_entry, college_entry, course_menu, course_menu_other_entry, specialization_entry, course_year_entry]

# Add a popup menu that appears on right-click on entry widgets
for widget in all_widgets:
    if (str(widget).find('entry') != -1):
        pass

base_window.unbind_all("<Tab>")
base_window.unbind_all("<<NextWindow>>")
base_window.unbind_all("<<PrevWindow>>")
base_window.bind_all("<Tab>", circulate_thru_widgets)
base_window.bind_all("<Down>", circulate_thru_widgets)
base_window.bind_all("<Up>", lambda event, key="Up" : circulate_thru_widgets(event, key))
base_window.bind_all("<Button-1>", lambda event: event.widget.focus_set())
base_window.mainloop()
