from DatabaseConnection import *
from logger import *
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from ttkthemes import ThemedStyle
import logging

global curr_index
global index
global button_list
global button_dict
global tk_window_dict

curr_index: int = 0
index = 0
button_list = []
button_dict = {}
tk_window_dict = {}


def on_window_click(event):
    """
    Callback function to handle window click events and set the current index accordingly.
    """
    focused_widget = event.widget.focus_get()
    if focused_widget:
        global curr_index
        curr_index = focused_widget.winfo_toplevel().title()
        print('curr_index', curr_index)
        message = f"Current Window Title: {curr_index}"
        log_message(message)
        return curr_index
    else:
        message = "No focused window."
        log_message(message)
        return 0


def change_second_frame_style(style):
    """
    Function to change the style of the second frame text widget based on the given style.
    """
    Fonts = {
        "Bold": Font(weight="bold"),
        "Italic": Font(slant="italic"),
        "Underline": Font(underline=True),
        "Times_New_Roman": ('Times New Roman', 12),
        "Calibri": ('Calibri', 14),
        "Century_Gothic": ('Century Gothic', 16),
        "Verdana": ('Verdana', 20)
    }
    tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].configure(font=Fonts[style])
    message = (f"Changed the Font of the sticky note StickyNoteWindow.inputtxt_{curr_index}")
    log_message(message)

class SqlLite:
    """
    Class to manage the database operations
    """
    def __init__(self):
        self.db = Database()
        self.title = None
        self.notes = None
        self.color = None
        self.font = None
        global curr_index


    def add_note(self):
        self.title = tk_window_dict[f"StickyNoteWindow.heading_{curr_index}"].get()
        self.notes = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].get("1.0", "end-1c")
        self.color = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].cget("background")
        self.font = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].cget("font")

        if not self.title or not self.notes:
            messagebox.showerror(message="Enter Title!")
        else:
            self.db.cursor.execute("SELECT title from sticky_notes_db WHERE title=? and notes=?",
                                   (self.title, self.notes))
            title_check = self.db.cursor.fetchall()
            self.db.connection.commit()
            if len(title_check) == 0:
                self.db.connection.commit()
                self.db.cursor.execute("INSERT INTO sticky_notes_db VALUES (?,?,?,?)",
                                       (self.title, self.notes, self.color, self.font))
                messagebox.showinfo(message="Note added")
                self.db.connection.commit()
                button_dict[f"{self.title}"] = Button(tk_window_dict[f"main_frame"], text=self.title, command=lambda: OldStickyNote(self.title)).pack()
                button_list.append(button_dict[f"{self.title}"])
            else:
                messagebox.showinfo(message="Title already present!, Please enter a new title")

    def delete_note(self):
        messagebox.askquestion(message="Do you want to delete the current note")

        self.title = tk_window_dict[f"StickyNoteWindow.heading_{curr_index}"].get()
        self.notes = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].get("1.0", "end-1c")
        self.color = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].cget("background")
        self.font = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].cget("font")

        if not self.title or not self.notes:
            messagebox.showerror(message="Enter title and note!")
            return
        else:
            sql_statement = "DELETE FROM sticky_notes_db WHERE title=? AND notes=?"
            self.db.connection.commit()
            self.db.cursor.execute(sql_statement, (self.title, self.notes))
            for btn in button_list:
                if btn['text'] == self.title:
                    btn.destroy()
                    break
        messagebox.showinfo(message="Note Deleted!")
        self.db.connection.commit()

    def update_note(self):
        self.title = tk_window_dict[f"StickyNoteWindow.heading_{curr_index}"].get()
        self.notes = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].get("1.0", "end-1c")
        self.color = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].cget("background")
        self.font = tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].cget("font")

        if not self.title or not self.notes:
            messagebox.showerror(message="Enter title and note!")
        else:
            self.db.connection.commit()
            sql_statement = "UPDATE sticky_notes_db SET notes=?,color=?,font=? WHERE title=?"
            self.db.cursor.execute(sql_statement, (self.notes, self.color, self.font, self.title))
            messagebox.showinfo(message="Note Updated")
            self.db.connection.commit()

class StickyNoteWindow:
    """
    Class to manage the main sticky note window.
    """
    def __init__(self):
        global index
        global curr_index
        self.db_notes = SqlLite()

        tk_window_dict[f"second_window_{index}"] = Tk()
        tk_window_dict[f"second_window_{index}"].geometry('250x250')
        tk_window_dict[f"second_window_{index}"].attributes('-alpha', 1.0)
        tk_window_dict[f"second_window_{index}"].resizable(False, False)
        self.mainloop = tk_window_dict[f"second_window_{index}"].mainloop

        tk_window_dict[f"second_window_{index}"].title(f"{index}")

        # Creates a new second frame
        second_frame = Frame(tk_window_dict[f"second_window_{index}"])
        second_frame.pack(fill=BOTH, expand=True)

        # Creates a new third frame
        third_frame = Frame(tk_window_dict[f"second_window_{index}"])
        third_frame.pack(fill=BOTH, expand=True)

        # Theme selection for the window
        style = ThemedStyle(tk_window_dict[f"second_window_{index}"])
        style.set_theme("arc")

        # Creates title with entry widget
        tk_window_dict[f"StickyNoteWindow.heading_{index}"] = Entry(second_frame)
        tk_window_dict[f"StickyNoteWindow.heading_{index}"].insert(1, "Enter Title Here!")
        tk_window_dict[f"StickyNoteWindow.heading_{index}"].pack(fill=BOTH, expand=True)

        # Creates input text frame
        tk_window_dict[f"StickyNoteWindow.inputtxt_{index}"] = Text(third_frame)
        tk_window_dict[f"StickyNoteWindow.inputtxt_{index}"].pack(fill=BOTH, expand=True)

        menubar = Menu(tk_window_dict[f"second_window_{index}"])
        tk_window_dict[f"second_window_{index}"].config(menu=menubar)

        # creates a binding on focus to the window to get current window title
        global curr_index
        tk_window_dict[f"second_window_{index}"].bind("<Enter>", on_window_click)
        message = (f"curr_index:{curr_index}")
        log_message(message)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_window)
        file_menu.add_command(label="Save", command=lambda: self.db_notes.add_note())
        file_menu.add_command(label="Update", command=lambda: self.db_notes.update_note())
        file_menu.add_command(label="Delete", command=lambda: self.db_notes.delete_note())
        menubar.add_cascade(label="File", menu=file_menu)

        style_menu = Menu(menubar, tearoff=0)

        style_menu.add_command(label="Bold", command=lambda: change_second_frame_style("Bold"))
        style_menu.add_command(label="Italics", command=lambda: change_second_frame_style("Italic"))
        style_menu.add_command(label="Underlined", command=lambda: change_second_frame_style("Underline"))

        menubar.add_cascade(label="Style", menu=style_menu)

        font_menu = Menu(menubar, tearoff=0)

        font_menu.add_command(label="Times_New_Roman",
                              command=lambda: change_second_frame_style("Times_New_Roman"))
        font_menu.add_command(label="Calibri", command=lambda: change_second_frame_style("Calibri"))
        font_menu.add_command(label="Century_Gothic", command=lambda: change_second_frame_style("Century_Gothic"))
        font_menu.add_command(label="Verdana", command=lambda: change_second_frame_style("Verdana"))

        menubar.add_cascade(label="Font", menu=font_menu)

        color_menu = Menu(menubar, tearoff=0)
        color_menu.add_command(label="Purple", command=lambda: self.change_background_color('#dbcdf0'))
        color_menu.add_command(label="Green", command=lambda: self.change_background_color('#d0f4de'))
        color_menu.add_command(label="Yellow", command=lambda: self.change_background_color('#fcf6bd'))
        color_menu.add_command(label="Pink", command=lambda: self.change_background_color('#f2c6de'))
        menubar.add_cascade(label="Color", menu=color_menu)

    @staticmethod
    def new_window():
        NewStickyNote()

    @staticmethod
    def old_window(title):
        OldStickyNote(title)

    @staticmethod
    def change_background_color(color):
        tk_window_dict[f"StickyNoteWindow.inputtxt_{curr_index}"].configure(background=color)


class NewStickyNote:
    """
    class to create a new sticky note
    """
    def __init__(self):
        global index
        index = index + 1
        self.obj2 = StickyNoteWindow()


class OldStickyNote:
    """
    Class to open old note
    """
    def __init__(self, title):
        global index
        index = index + 1
        self.title = title
        self.db = Database()
        self.obj2 = StickyNoteWindow()

        self.db.connection.commit()
        self.db.cursor.execute("SELECT * FROM sticky_notes_db WHERE title = '%s'" % self.title)

        self.old = self.db.cursor.fetchall()
        self.db.connection.commit()

        tk_window_dict[f"StickyNoteWindow.heading_{index}"].delete(0, END)
        tk_window_dict[f"StickyNoteWindow.heading_{index}"].insert(1, title)
        tk_window_dict[f"StickyNoteWindow.heading_{index}"].pack()

        tk_window_dict[f"StickyNoteWindow.inputtxt_{index}"].insert(INSERT, str(self.old[0][1]))
        tk_window_dict[f"StickyNoteWindow.inputtxt_{index}"].configure(background=str(self.old[0][2]))
        tk_window_dict[f"StickyNoteWindow.inputtxt_{index}"].configure(font=str(self.old[0][3]))
        tk_window_dict[f"StickyNoteWindow.inputtxt_{index}"].pack(fill=BOTH, expand=True)



class FirstWindow:
    """
    Class to create root window
    """
    def __init__(self):
        self.db = Database()
        tk_window_dict[f"main_window"] = Tk()
        tk_window_dict[f"main_window"].title(f"{index}")
        tk_window_dict[f"main_window"].geometry('150x400')
        tk_window_dict[f"main_window"].attributes('-alpha', 1.0)
        tk_window_dict[f"main_window"].resizable(False, False)
        style = ThemedStyle(tk_window_dict[f"main_window"], )
        style.set_theme("arc")

        tk_window_dict[f"main_window"].configure(bg='#ffffff')
        self.mainloop = tk_window_dict[f"main_window"].mainloop

        canvas = Canvas(tk_window_dict[f"main_window"])
        canvas.pack(side=TOP, fill=BOTH, expand=True)

        scrollbar = Scrollbar(canvas, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", on_canvas_configure)

        tk_window_dict[f"main_frame"] = Frame(canvas)
        canvas.create_window(canvas.winfo_width() // 2, 0, window=tk_window_dict[f"main_frame"], anchor="nw")

        sql_statement = "SELECT title FROM sticky_notes_db"
        self.db.cursor.execute(sql_statement)
        row = self.db.cursor.fetchall()
        self.db.connection.commit()
        
        Label(tk_window_dict[f"main_frame"], text="Sticky Note Titles").pack(fill=BOTH, expand=True)
        if len(row) <= 0:
            NewStickyNote()
            messagebox.showerror(message="No note found")
        else:
            for k, i in enumerate(row):
                button_dict[f"{i[0]}"] = Button(tk_window_dict[f"main_frame"], text=str(i[0]), command=lambda pi=i[0]: OldStickyNote(pi))
                button_dict[f"{i[0]}"].pack(fill=BOTH, expand=True)
                button_list.append(button_dict[f"{i[0]}"])
