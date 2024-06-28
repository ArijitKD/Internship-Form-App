'''
MIT License

Copyright (c) 2024 Arijit Kumar Das <arijitkdgit.official@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# TODO:
# * Re-implement cut(), copy(), paste() and make them bug-free
# * Add functionality to submit button
# * Add an internship description label below company logo
# * Add valid data verification check for resume link data on focus_out
# * Update app icon using company logo
# * Add support for non-Windows OSes                                                                                [DONE]
# * Add support for low-resolution display                                                                          [Partially done, need to add auto-scrolling on widget focus]

# [OPTIONAL TODO]
# * If possible, implement the valid data check of name, college name, other course and branch using ChatGPT API
# * Resolve the bug: entry does not re-gain focus on an error display if the next widget is an optionmenu           [DONE]
# * Add an undo-redo function to the entries, if possible


APP_NAME = "Next24tech Internship Registration Form"
COMPANY_NAME = "Next24tech Technology & Services"
dependency_flag_set = 0

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError as e:
    print ("Warning:", e, end="\n\n")
    dependency_flag_set = 1
try:
    from PIL import ImageTk, Image
except ImportError as e:
    print ("Warning:", e, end="\n\n")
    dependency_flag_set = 1

if (dependency_flag_set):
    print ("One or more dependencies are not installed. To avoid unintended side-effects, dependencies won\'t be auto-installed. The following the steps may be useful for resolving the issues:")
    from os import name
    if (name=="nt"):
        print ("*   For installing PIL, make sure pip3 is on the PATH then run the command \"pip3 install pillow\" (no quotes) as admininistrator.")
        print ("*   For installing Tkinter, reinstall Python with Tcl/Tk support.")
        print ("*   Re-run "+APP_NAME+".")
    else:
        print ("*   Use your package manager in sudo mode and install the following packages: python3-tk, python3-pil.imagetk.")
        print ("*   Re-run "+APP_NAME+".")
    raise SystemExit(1)


from os import name as OS_NAME
import win32messagebox as mbox
#import tkinter.messagebox as mbox

def capitalize_each_word(sentence):
    words = sentence.split()
    sentence = ""
    for word in words:
        sentence += word.capitalize()+' '
    return sentence

# Flag variables
resume_link_info_shown = False
menu_visible = False
course_menu_other_entry_visible = False

# Variable to keep track of all the entries and the menus
all_widgets = []

# Initialize window
base_window = tk.Tk()

# Get the screen dimesions
SCR_WIDTH = base_window.winfo_screenwidth()
SCR_HEIGHT = base_window.winfo_screenheight()

# Base window dimensions
EXPECTED_MIN_SCR_HEIGHT = 900
EXPECTED_WINDOW_HEIGHT = 760
WIN_WIDTH = 480
WIN_HEIGHT = EXPECTED_WINDOW_HEIGHT if SCR_HEIGHT > EXPECTED_MIN_SCR_HEIGHT else SCR_HEIGHT-180

WIN_BG = '#f3f0e6'

DEFAULT_ENTRY_WIDTH = 40 if OS_NAME == 'nt' else 30
DEFAULT_MENU_WIDTH = 37 if OS_NAME == 'nt' else 30

# Define ttk styles
if (OS_NAME == 'nt'):
    style = ttk.Style()
    style.configure("placeholder.TEntry", foreground="gray")
    style.configure("text.TEntry", foreground="black")
    style.configure("placeholder.TMenubutton", foreground="gray", background=WIN_BG)
    style.configure("text.TMenubutton", foreground="black", background=WIN_BG)
    style.configure("chkbtn.TCheckbutton", background=WIN_BG)
    style.configure("text.TLabel", background=WIN_BG)
else:
    style = ttk.Style()
    style.configure("placeholder.TEntry", foreground="gray", font=('Helvetica', 5))
    style.configure("text.TEntry", foreground="black", font=('Helvetica', 5))
    style.configure("placeholder.TMenubutton", foreground="gray", background=WIN_BG, font=('Helvetica', 10))
    style.configure("text.TMenubutton", foreground="black", background=WIN_BG, font=('Helvetica', 10))
    style.configure("chkbtn.TCheckbutton", background=WIN_BG, font=('Helvetica', 9))
    style.configure("text.TLabel", font=('Helvetica', 10), background=WIN_BG)

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
    return int (not close_window)

# Add a close window event function        
base_window.protocol("WM_DELETE_WINDOW", on_close)

# Change the base window background color
base_window.configure(background=WIN_BG)


# Add company logo at the top
img = ImageTk.PhotoImage(Image.open("next24tech_cover_480x120.png"))
tk.Label(base_window, image = img, background=WIN_BG).pack(side = "top", pady=(10,20))


# Add internship description label
internship_description = "You will receive your internship offer letter within 7 days, if selected."
ttk.Label(base_window, text=internship_description, style="text.TLabel").pack(pady=(0,20))


if (WIN_HEIGHT < EXPECTED_WINDOW_HEIGHT):
    # Create a scrollable frame
    scroll_frame = tk.Frame(base_window, background=WIN_BG)
    scroll_frame.pack(fill=tk.X)

    # Configure scrollbar
    scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure canvas
    canvas = tk.Canvas(scroll_frame, yscrollcommand=scrollbar.set, highlightthickness=0, background=WIN_BG, height=WIN_HEIGHT-300,)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=canvas.yview)

    # Create a frame inside the canvas to hold the widgets
    fields_area = tk.Frame(canvas, background=WIN_BG)
    canvas.create_window((0, 0), window=fields_area, anchor=tk.NW)

    # Function to update the scroll region
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    fields_area.bind("<Configure>", on_frame_configure)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)

else:
    fields_area = base_window

        
# Defining callback functions for entries
def entry_focusin_callback(event, textvariable=None):
    global resume_link_info_shown

    if (WIN_HEIGHT < EXPECTED_WINDOW_HEIGHT):
        '''
        # Calculate the current scroll position and visible height of canvas
        #canvas.update_idletasks()
        canvas_height = canvas.winfo_height()
        frame_y = abs(fields_area.winfo_y()+canvas_height)
        print (frame_y, canvas_height)
        # Determine if the next entry is fully visible
        if  (frame_y < canvas_height):
            canvas.yview_scroll(2, "units")
        elif (frame_y > canvas.winfo_y()):
            canvas.yview_scroll(-2, "units")
        '''
        print ("scrollable")
                
    if (textvariable == None):
        for entry_name in common_entries:
            if (common_entries[entry_name]['entry'] == event.widget):
                textvariable = common_entries[entry_name]['textvar']
    if (event.widget == common_entries["resume link"]['entry']):
        if (not resume_link_info_shown):
            resume_link_info_shown = True
            mbox.showinfo(master=base_window, title="Specify your resume link",
                            message="Upload your resume in Google Drive or some other online service and specify the link to it here. Make sure that your resume is publicly accessible.")
    if (event.widget.cget("style") == "placeholder.TEntry"):
        event.widget.delete(0, 'end')
        event.widget.configure(style="text.TEntry")
    else:
        event.widget.xview_moveto(len(textvariable.get()))
        event.widget.icursor(len(textvariable.get()))


def entry_focusout_callback(event, what_data="", placeholder="", textvariable=None):

    if (textvariable == None):
        for entry_name in common_entries:
            if (common_entries[entry_name]['entry'] == event.widget):
                textvariable = common_entries[entry_name]['textvar']
    entry_data = textvariable.get().strip()
    invalid_data = False
    custom_invalid_msg = ""
    
    if (placeholder == ""):
        placeholder = "Enter your "+what_data
        
    if (entry_data == ""):
        event.widget.configure(style="placeholder.TEntry")
        event.widget.insert(0, placeholder)

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
                        if (int(entry_data) > max_year):
                            textvariable.set(str(max_year))
                        elif (int(entry_data) < 1):
                            textvariable.set('1')
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
            copy_entry_data = entry_data
            for char in ('(', ')', '.', ',', ' '):
                entry_data = entry_data.replace(char, '')
            if (not entry_data.isalpha()):
                invalid_data = True
            entry_data = copy_entry_data

    event.widget.xview_moveto(0)

    if (invalid_data):
        base_window.update()
        if (custom_invalid_msg == ""):
            mbox.showerror(master=base_window, title="Invalid "+what_data, message="\""+entry_data+"\" is not a valid %s. Please enter a valid %s."%(what_data, what_data))
        else:
            mbox.showerror(master=base_window, title="Invalid "+what_data, message=custom_invalid_msg)
        event.widget.configure(style="placeholder.TEntry")
        event.widget.delete(0, 'end')
        event.widget.focus_set()
        popup_menu.unpost()
        
        
def close_menuoptions_callback(event):
    global menu_visible, course_menu_other_entry_visible
    try:
        event.widget.unpost()
        all_widgets[all_widgets.index(event.widget.nametowidget(event.widget.winfo_parent()))].focus_set()
        event.widget.unbind_all("<Return>")
    except:
        pass
    menu_visible = False


def circulate_thru_widgets(event, key="Tab"):
    global menu_visible
    try:
        current_widget = fields_area.focus_get()
    except KeyError:
        return

    if (current_widget in all_widgets):
        current_index = all_widgets.index(current_widget)
    else:
        widget = current_widget.nametowidget(current_widget.winfo_parent())
        if (widget in all_widgets and menu_visible):
            widget.unbind_all("<Return>")
            widget.bind_all("<Return>", close_menuoptions_callback)
        else:
            all_widgets[0].focus_set()
        return

    next_index = current_index + (-1 if key=='Up' else 1)
    if (next_index >= len(all_widgets)):
        if (key=="Return"):
            agree_chkbtn.focus_set()
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

    if (str(all_widgets[next_index]).find('optionmenu') != -1):
        all_widgets[next_index].winfo_children()[0].post(all_widgets[next_index].winfo_rootx(), all_widgets[next_index].winfo_rooty()+all_widgets[next_index].winfo_height())
        all_widgets[next_index].winfo_children()[0].focus_set()
        menu_visible = True
        
    
common_entries = {
    'name': None,
    'phone number': None,
    'email id': None,
    'college name': None,
    'branch': None,
    'course year': None,
    'resume link': None
    }

for entry in common_entries:
    common_entries[entry] = {
        'entry': None,
        'textvar': None
        }


# Cut, copy, paste are currently buggy
def cut():
    widget = fields_area.focus_get()
    widget.focus_set()
    base_window.clipboard_clear()
    selection = widget.selection_get()
    widget.event_generate("<Control-x>")
    base_window.clipboard_append(selection)


'''
def cut():
    widget = fields_area.focus_get()
    base_window.clipboard_clear()
    selection = ""
    try:
        selection = widget.selection_get()
        end_selection = widget.index(tk.INSERT)
        start_selection = end_selection - len(selection)
        for entry_name in common_entries:
            if (common_entries[entry_name]['entry'] == widget):
                text = common_entries[entry_name]['textvar'].get()
                common_entries[entry_name]['textvar'].set(text[0:start_selection]+text[end_selection::])
        widget.selection_clear()
        widget.icursor(start_selection)
    except:
        pass
    finally:
        base_window.clipboard_append(selection)
'''

def copy():
    widget = fields_area.focus_get()
    base_window.clipboard_clear()
    try:
        selection = widget.selection_get()
        base_window.clipboard_append(selection)
        widget.selection_clear()
    except:
        pass
    
def paste():
    widget = fields_area.focus_get()
    cursor_index = widget.index(tk.INSERT)
    selection = ""
    try:
        data = base_window.selection_get(selection="CLIPBOARD")
        selection = widget.selection_get()
        end_selection = widget.index(tk.INSERT)
        start_selection = end_selection - len(selection)
        for entry_name in common_entries:
            if (common_entries[entry_name]['entry'] == widget):
                text = common_entries[entry_name]['textvar'].get()
                common_entries[entry_name]['textvar'].set(text[0:start_selection]+text[end_selection::])
        widget.selection_clear()
        widget.icursor(start_selection)
    except:
        pass
    
    for entry_name in common_entries:
        if (common_entries[entry_name]['entry'] == widget):
            text = common_entries[entry_name]['textvar'].get()
            common_entries[entry_name]['textvar'].set(text[0:cursor_index]+data+text[cursor_index::])
    widget.select_range(cursor_index, len(data)+cursor_index)
    widget.icursor(len(data)+cursor_index)


def select_all():
    widget = fields_area.focus_get()
    widget.select_range(0, len(widget.get()))
    
# Add a popup menu that appears on right-click on entry widgets
popup_menu = tk.Menu(master=fields_area, tearoff=0)
popup_menu.add_command(label="Cut", command=cut, state=tk.DISABLED)
popup_menu.add_command(label="Copy", command=copy, state=tk.DISABLED)
popup_menu.add_command(label="Paste", command=paste)
try:
    base_window.selection_get(selection="CLIPBOARD")
except:
    popup_menu.entryconfig("Paste", state=tk.DISABLED)
popup_menu.add_separator()
popup_menu.add_command(label="Select All", command=select_all)


def rightclick_optionsmenu_callback(event, cursor_position):
    print (cursor_position)
    print ("popup_menu_visible")
    base_window.after(100, lambda: event.widget.xview_moveto(cursor_position))
    try:
        event.widget.selection_get()
        popup_menu.entryconfig("Cut", state=tk.ACTIVE)
        popup_menu.entryconfig("Copy", state=tk.ACTIVE)
    except:
        popup_menu.entryconfig("Cut", state=tk.DISABLED)
        popup_menu.entryconfig("Copy", state=tk.DISABLED)
    try:
        base_window.selection_get(selection="CLIPBOARD")
        popup_menu.entryconfig("Paste", state=tk.ACTIVE)
    except:
        popup_menu.entryconfig("Paste", state=tk.DISABLED)
    if (fields_area.focus_get() == event.widget):
        popup_menu.tk_popup(event.x_root, event.y_root, 0)
    

# apple banana cherry date eggplant fig grapefruit honeydew kiwi lemon mango orange pear quince raspberry strawberry tomato

# Define a function for adding a common entry
def add_common_entry(entry_name):
    common_entries[entry_name]['textvar'] = tk.StringVar()
    entry_frame = tk.Frame(fields_area, background=WIN_BG)
    entry_frame.pack(fill="both", pady=(0,15))
    ttk.Label(entry_frame, text = capitalize_each_word(entry_name), background=WIN_BG, style="text.TLabel").pack(side="left", padx=(50,0))
    common_entries[entry_name]['entry'] = ttk.Entry(entry_frame, width=DEFAULT_ENTRY_WIDTH, textvariable = common_entries[entry_name]['textvar'], style="placeholder.TEntry")
    common_entries[entry_name]['entry'].insert(0, "Enter your "+entry_name)
    common_entries[entry_name]['entry'].icursor(0)
    if (WIN_HEIGHT < EXPECTED_WINDOW_HEIGHT):
        common_entries[entry_name]['entry'].pack(side="right", ipady=5, padx=(50,50))
    else:
        common_entries[entry_name]['entry'].pack(side="right", ipady=5, padx=(0,50))
    common_entries[entry_name]['entry'].bind('<FocusIn>', entry_focusin_callback)
    common_entries[entry_name]['entry'].bind('<FocusOut>', lambda event, what_data=entry_name :
                 entry_focusout_callback(event, what_data=what_data))
    common_entries[entry_name]['entry'].bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))
    common_entries[entry_name]['entry'].bind('<Button-3>', lambda event: rightclick_optionsmenu_callback(event, cursor_position=common_entries[entry_name]['entry'].index(tk.INSERT)))
    #common_entries[entry_name]['entry'].bind('<Button-1>', rightclick_optionsmenu_callback)


# Add the name, phone number, email id, college name entries
iter_common_entries = iter(common_entries.keys())
current_entry = next(iter_common_entries)
while (current_entry != 'branch'):
    add_common_entry(current_entry)
    all_widgets.append(common_entries[current_entry]['entry'])
    current_entry = next(iter_common_entries)

    
# Add a course selection optionmenu
courses = [
    "B.E/B.Tech - 4 yrs",
    "Integrated B.Tech+M.Tech - 5 yrs",
    "B.Sc - 3 yrs",
    "B.Sc (Hons) - 3 yrs",
    "B.C.A - 3 yrs",
    "B.B.A - 3 yrs",
    "B.Com - 3 yrs",
    "Other"
    ]

        
# Callback function for course menu
def course_menu_callback(selected_option):
    global course_menu_other_entry_visible
    course_menu.configure(style="text.TMenubutton")
    course_menu.configure(width=10)
    if (selected_option == "Other"):
        if (OS_NAME == 'nt'):
            course_menu.pack_forget()
            course_menu_other_entry.configure(width=DEFAULT_ENTRY_WIDTH-15)
            course_menu_other_entry.pack(side="right", ipady=5, padx=(6,50))
            course_menu.pack(side="right", ipady=5, padx=(40,0))
        else:
            course_menu.pack_forget()
            course_menu_other_entry.configure(width=DEFAULT_ENTRY_WIDTH-10)
            course_menu_other_entry.pack(side="right", ipady=5, padx=(5,50))
            course_menu.pack(side="right", ipady=5, padx=(45,0))
        course_menu_other_entry_visible = True
    else:
        course_menu_other_entry.pack_forget()
        course_menu.configure(width=DEFAULT_MENU_WIDTH)
        course_menu.pack(side="right", ipady=5, padx=(0,50))        
        max_year = int(selected_option[selected_option.index('-')+2])
        current_course_year = common_entries['course year']['textvar'].get()
        if (current_course_year.isdigit()):
            current_course_year = int(current_course_year)
            if (current_course_year > max_year):
                common_entries['course year']['textvar'].set(str(max_year))
        course_menu_other_entry_visible = False

# The course menu
course_var = tk.StringVar()
course_frame = tk.Frame(fields_area, background=WIN_BG)
course_frame.pack(fill="both", pady=(0,15))
ttk.Label(course_frame, text = 'Current Course', background=WIN_BG, style="text.TLabel").pack(side="left", padx=(50,0), ipady=5)
course_menu = ttk.OptionMenu(course_frame, course_var, "Choose your course", *courses, command=course_menu_callback)
course_menu.configure(width=DEFAULT_MENU_WIDTH, style="placeholder.TMenubutton", padding=3)
course_menu.pack(side="right", ipady=5, padx=(0,50))
course_menu.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))
course_menu.bind("<Button-1>", lambda event: event.widget.focus_set())

# Add an entry which will allow the user to input their course in case their current course is not listed in courses
course_menu_other_var = tk.StringVar()
course_menu_other_entry = ttk.Entry(course_frame, width=DEFAULT_ENTRY_WIDTH, textvariable = course_menu_other_var, style="placeholder.TEntry")
course_menu_other_entry.insert(0, "Specify your course")
course_menu_other_entry.icursor(0)
course_menu_other_entry.bind('<FocusIn>', lambda event, textvariable=course_menu_other_var : entry_focusin_callback(event, textvariable))
course_menu_other_entry.bind('<FocusOut>', lambda event, what_data="course", placeholder="Specify your course", textvariable=course_menu_other_var :
                 entry_focusout_callback(event, what_data, placeholder, textvariable))
course_menu_other_entry.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))
course_menu_other_entry.bind('<Button-3>', rightclick_optionsmenu_callback)


# Update all_widgets after course_menu and course_menu_other_entry are added
all_widgets.extend([course_menu, course_menu_other_entry])


# Add the branch and course year entries and an entry for specifying an online link for resume
for current_entry in list(common_entries.keys())[-3::]:
    add_common_entry(current_entry)
    all_widgets.append(common_entries[current_entry]['entry'])


# Add an internship position menu
internships = [
    "Python GUI development",
    "GenAI/Machine Learning",
    "Web development using Node.js/React",
    "UI/UX design",
    ".NET development",
    "Java app development",
    "Desktop development with C++",
    "Mobile development with Java/Kotlin",
    "Digital Marketing"
    ]
internships.sort()

def internship_menu_callback(selected_option):
    internship_menu.configure(style="text.TMenubutton")
    
internship_var = tk.StringVar()
internship_frame = tk.Frame(fields_area, background=WIN_BG)
internship_frame.pack(fill="both", pady=(0,15))
ttk.Label(internship_frame, text = 'Internship Position', background=WIN_BG, style="text.TLabel").pack(side="left", padx=(50,0), ipady=5)
internship_menu = ttk.OptionMenu(internship_frame, internship_var, "Choose internship position", *internships, command=internship_menu_callback)
internship_menu.configure(width=DEFAULT_MENU_WIDTH, style="placeholder.TMenubutton", padding=3)
internship_menu.pack(side="right", ipady=5, padx=(0,50))
internship_menu.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))
internship_menu.bind("<Button-1>", lambda event: event.widget.focus_set())

all_widgets.append(internship_menu)


# Add an internship duration menu
durations = [
    "4 weeks",
    "45 days",
    "2 months",
    "3 months",
    "6 months"
    ]

def duration_menu_callback(selected_option):
    duration_menu.configure(style="text.TMenubutton")
    
duration_var = tk.StringVar()
duration_frame = tk.Frame(fields_area, background=WIN_BG)
duration_frame.pack(fill="both", pady=(0,15))
ttk.Label(duration_frame, text = 'Internship Duration', background=WIN_BG, style="text.TLabel").pack(side="left", padx=(50,0), ipady=5)
duration_menu = ttk.OptionMenu(duration_frame, duration_var, "Choose internship duration", *durations, command=duration_menu_callback)
duration_menu.configure(width=DEFAULT_MENU_WIDTH, style="placeholder.TMenubutton", padding=3)
duration_menu.pack(side="right", ipady=5, padx=(0,50))
duration_menu.bind('<Return>', lambda event, key="Return" : circulate_thru_widgets(event, key))
duration_menu.bind("<Button-1>", lambda event: event.widget.focus_set())

all_widgets.append(duration_menu)


# Add a tos and privacy policy agreement checkbutton
def agree_chkbtn_callback():
    if (agree_chkbtn_var.get()):
        submit_button.configure(state=tk.ACTIVE)
        submit_button.focus_set()
        agree_chkbtn.event_generate("<FocusOut>")
    else:
        submit_button.configure(state=tk.DISABLED)
        submit_button.event_generate("<FocusOut>")
        agree_chkbtn.event_generate("<FocusOut>")
    
agree_chkbtn_var = tk.IntVar()
agree_chkbtn = ttk.Checkbutton(base_window, text="   I agree to share my data with %s and am\n   fully aware of the company's terms of service and privacy policy."%(COMPANY_NAME,),
                               variable=agree_chkbtn_var, command=agree_chkbtn_callback, style="chkbtn.TCheckbutton")
agree_chkbtn.pack(padx=(5,50), pady=10)
agree_chkbtn.bind("<FocusIn>", lambda event: agree_chkbtn_callback())
agree_chkbtn.bind("<Enter>", lambda event: event.widget.config(style="chkbtn.TCheckbutton"))


# Finally, add the submit button
def submit_button_callback(event=None):
    field_vars = []
    for widget in all_widgets:
        field_vars.append(widget.cget('style'))
    global course_menu_other_entry_visible
    if (not course_menu_other_entry_visible):
        field_vars.remove('placeholder.TEntry')
    if ('placeholder.TEntry' in field_vars):
        mbox.showerror(APP_NAME, "Please fill out all the fields. One or more fields have been left out.")
        return
    from time import sleep
    from random import choice
    sleep(choice(range(1,3)))
    base_window.destroy()
    temptk = tk.Tk()
    temptk.withdraw()
    mbox.showinfo(APP_NAME, "Your form has successfully been submitted.\n\nThank you for taking interest in %s's internship programme."%COMPANY_NAME)
    temptk.destroy()

submit_button = ttk.Button(base_window, text="Submit Form", state=tk.DISABLED, command=submit_button_callback)
submit_button.pack(ipadx=20)
submit_button.bind("<Return>", submit_button_callback)


base_window.unbind_all("<Tab>")
base_window.bind_all("<Tab>", circulate_thru_widgets)
base_window.bind_all("<Down>", circulate_thru_widgets)
base_window.bind_all("<Up>", lambda event, key="Up" : circulate_thru_widgets(event, key))

def bind_all_buttonrelease1_callback(event):
    try:
        event.widget.focus_set()
    except AttributeError:  # this error is sometimes raised in non-Windows systems, and that's why this function's
        pass                # defined otherwise the callback could be a one-liner implemented using lambda function

base_window.bind_all("<ButtonRelease-1>", bind_all_buttonrelease1_callback)
base_window.mainloop()
