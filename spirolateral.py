#!/usr/bin/env python3
"""
Program that allows for spirolaterals to be added and deleted to/from a list
and allows for saving/loading list of spirolaterals
"""

# import modules as necessary
# if tkinter isn't found, ask user to install
try:
    from tkinter import (
        Tk, Frame, Button, Label, Entry, END, DISABLED, NORMAL, Toplevel, Menu,
        Canvas)
    from tkinter.filedialog import askopenfilename, asksaveasfilename
except (ModuleNotFoundError, ImportError):
    print("Please install tkinter.")
    raise SystemExit
import pickle
import turtle
# if spirolateral drawing library isn't found, set variable to ask user
# to read README for dependency install.
try:
    from lib import otherSpiroClass as spirolateral_draw
    NO_DRAW = False
except (ModuleNotFoundError, ImportError):
    NO_DRAW = True


# define spirolateral class
class Spirolateral:
    """
    define spirolateral class and functions
    """

    def __init__(self, name: str, times_table: int, angle: int):
        self.name = name
        self.times_table = int(times_table)
        self.angle = int(angle)
        self.digital_root_list = []
        self.make_digital_root_list()

    @classmethod
    def digital_root(cls, n):
        """calculates a digital root"""
        return (n - 1) % 9 + 1 if n else 0

    def make_digital_root_list(self):
        """Makes a digital root list, stops when list repeats"""
        multiplier = 1
        while True:
            value = self.digital_root(int(multiplier * self.times_table))
            if value in self.digital_root_list:
                break
            else:
                self.digital_root_list.append(value)
                multiplier += 1


class SpirolateralGUI(Frame):
    """class for spirolateral gui"""
    def __init__(self, master):
        # init master, then set title, width, height and padding
        super().__init__(master)
        self.master = master
        master.title("Spirolateral")
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.PADX = 10
        self.PADY = 5
        # we need a scale to draw the spirolateral
        # this is changed later
        self.scale_to_use = 1

        # set spirolateral list, index and main non_draw frame
        self.spirolaterals = []
        self.index = 0
        self.text_data_frame = Frame(
            self.master, width=self.WIDTH/2, height=self.HEIGHT)

        # if no spirolateral drawing library, grid the message to install it
        # otherwise, run as normal, gridding menubar, footer, main_menu,
        # canvas
        if NO_DRAW:
            self.make_nodraw_widgets()
        else:
            self.make_menubar_widgets()
            self.make_main_menu_widgets()
            self.make_footer_row_widgets()
            self.make_add_spirolateral_widgets()
            self.make_draw_spirolateral_widgets()
            self.draw_spirolateral_frame.grid_propagate(0)
            self.draw_spirolateral_frame.grid(row=0, column=1, sticky='nesw')
            self.no_spirolaterals.grid(
                row=1, column=0, sticky='nesw',
                padx=self.PADX, pady=self.PADY, columnspan=2)
            self.master.config(menu=self.menubar)
            self.master.columnconfigure(1, weight=1)

        self.text_data_frame.grid_propagate(0)
        self.text_data_frame.grid(row=0, column=0, sticky='nesw')


    def make_nodraw_widgets(self):
        """make nodraw widgets"""
        self.master.title("Spirolateral - Error")
        self.nodraw = Label(
            self.text_data_frame,
            text="Can't draw spirolaterals, please read README "
            "and install requirements")
        self.nodraw.grid(row=0, column=0)
        self.nodraw_btn = Button(self.text_data_frame, text="Continue",
                                 command=self.master.quit)
        self.nodraw_btn.grid(row=1, column=0)

    def make_menubar_widgets(self):
        """make menubar widgets"""
        self.menubar = Menu(self.master)
        self.menubar.add_command(
            label="Add a spirolateral", command=self.show_add_spirolateral)
        self.menubar.add_command(
            label="Show spirolaterals", command=self.show_main_menu,
            state=DISABLED)
        self.menubar.add_command(
            label="Delete spirolateral", command=self.delete_spirolateral,
            state=DISABLED)
        self.menubar.add_command(
            label="Save spirolaterals", command=self.save_spirolateral)
        self.menubar.add_command(
            label="Load spirolaterals", command=self.load_spirolateral)
        self.menubar.add_command(label="Quit", command=self.master.quit)

    def make_main_menu_widgets(self):
        """make main_menu widgets and grid as necessary"""
        self.main_menu = Frame(self.text_data_frame)
        self.no_spirolaterals = Label(
            self.text_data_frame, text="There are no spirolaterals")
        self.name = Label(self.main_menu, text="Name", anchor='nw')
        self.name.grid(row=0, column=0, sticky='nw',
                       padx=self.PADX, pady=self.PADY)
        self.name_display = Label(self.main_menu, text="")
        self.name_display.grid(row=0, column=1, sticky='nw',
                               padx=self.PADX, pady=self.PADY)
        self.times_table = Label(
            self.main_menu, text="Times table", anchor='nw')
        self.times_table.grid(row=1, column=0, sticky='nw',
                              padx=self.PADX, pady=self.PADY)
        self.times_table_display = Label(self.main_menu, text="")
        self.times_table_display.grid(
            row=1, column=1, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.angle = Label(self.main_menu, text="Angle", anchor='nw')
        self.angle.grid(row=2, column=0, sticky='nw',
                        padx=self.PADX, pady=self.PADY)
        self.angle_display = Label(self.main_menu, text="")
        self.angle_display.grid(
            row=2, column=1, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.digital_root_list = Label(
            self.main_menu, text="Digital root list", anchor='nw')
        self.digital_root_list.grid(
            row=3, column=0, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.digital_root_list_display = Label(self.main_menu, text="")
        self.digital_root_list_display.grid(
            row=3, column=1, sticky='nw', padx=self.PADX, pady=self.PADY)

    def make_footer_row_widgets(self):
        """make footer_row widgets and grid as necessary, initally disabled"""
        self.footer_row = Frame(self.text_data_frame)
        self.previous_btn = Button(
            self.footer_row, text="Previous", command=self.display_previous)
        self.previous_btn.grid(row=0, column=0, padx=self.PADX, pady=self.PADY)
        self.previous_btn.configure(state=DISABLED)
        # self.draw_btn = Button(self.footer_row, text="Draw",
        #                       command=self.draw_spirolateral)
        # self.draw_btn.grid(row=0, column=1)
        self.next_btn = Button(
            self.footer_row, text="Next", command=self.display_next)
        # self.next_btn.grid(row=0, column=2)
        self.next_btn.grid(row=0, column=1, padx=self.PADX, pady=self.PADY)
        self.next_btn.configure(state=DISABLED)

    def make_add_spirolateral_widgets(self):
        """make add_spirolateral widgets and grid as necessary,
        with input validation"""
        self.add_spirolateral = Frame(self.text_data_frame)
        self.vcmd = (self.master.register(self.validate), '%d', '%P', '%S')
        # self.autoupdate = IntVar()
        # self.autoupdate_checkbtn = Checkbutton(
        #     self.add_spirolateral, text="Auto update drawing",
        #     variable=self.autoupdate)
        # self.autoupdate_checkbtn.grid(row=0, column=0, columnspan=2)
        self.spirolateral_name = Label(self.add_spirolateral, text="Name: ")
        self.spirolateral_name.grid(
            row=1, column=0, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.spirolateral_name_entry = Entry(self.add_spirolateral)
        self.spirolateral_name_entry.grid(
            row=1, column=1, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.spirolateral_name_error = Label(
            self.add_spirolateral, text="No name entered")

        self.spirolateral_times_table = Label(
            self.add_spirolateral, text="Times table: ")
        self.spirolateral_times_table.grid(
            row=3, column=0, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.spirolateral_times_table_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_times_table_entry.grid(
            row=3, column=1, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.spirolateral_times_table_error = Label(
            self.add_spirolateral, text="No times table above 0 entered")
        # self.spirolateral_times_table_entry.bind(
        #     "<Key>", self.draw_spirolateral_part)

        self.spirolateral_angle = Label(
            self.add_spirolateral, text="Angle of spirolateral: ", anchor='nw')
        self.spirolateral_angle.grid(
            row=5, column=0, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.spirolateral_angle_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_angle_entry.grid(
            row=5, column=1, sticky='nw', padx=self.PADX, pady=self.PADY)
        self.spirolateral_angle_error = Label(
            self.add_spirolateral, text="No angle above 0 entered")
        # self.spirolateral_angle_entry.bind(
        #     "<Key>", self.draw_spirolateral_part)

        self.enter = Button(self.add_spirolateral, text="Enter data",
                            command=self.new_spirolateral)
        self.enter.grid(row=7, column=0, columnspan=2)

    def make_draw_spirolateral_widgets(self):
        """make draw_spirolateral widgets and grid as necessary"""
        self.draw_spirolateral_frame = Frame(
            self.master, width=self.WIDTH/2, height=self.HEIGHT)
        canvas = Canvas(
            self.draw_spirolateral_frame, width=self.WIDTH/2,
            height=self.HEIGHT)
        canvas.grid(row=0, column=0)
        screen = turtle.TurtleScreen(canvas)
        screen.screensize(self.WIDTH/2, self.HEIGHT)
        # TODO: allow for dynamically changing scale (although the program
        # should automatically do that to fit to screen)
        self.drawing_turtle = spirolateral_draw.SpirolateralDrawer(
            screen, self.scale_to_use)

    def show_main_menu(self):
        """
        forget add ui, grid show spirolateral ui
        and enable add and delete menubar button
        """
        self.add_spirolateral.grid_forget()
        self.menubar.entryconfig("Show spirolaterals", state=DISABLED)
        self.menubar.entryconfig("Add a spirolateral", state=NORMAL)
        self.menubar.entryconfig("Delete spirolateral", state=NORMAL)
        self.update_display()

    def show_add_spirolateral(self):
        """
        forget show spirolateral ui, grid add ui
        and disable add and delete menubar button
        """
        self.main_menu.grid_forget()
        self.footer_row.grid_forget()
        self.menubar.entryconfig("Show spirolaterals", state=NORMAL)
        self.menubar.entryconfig("Add a spirolateral", state=DISABLED)
        self.menubar.entryconfig("Delete spirolateral", state=DISABLED)
        self.no_spirolaterals.grid_forget()
        self.add_spirolateral.grid(row=1, column=0, sticky='nesw')
        self.clear_spirolateral_drawing()

    def save_spirolateral(self):
        """save spirolaterals to file, supressing errors from dialog cancel"""
        try:
            pickle_out = open(asksaveasfilename(), 'wb')
            pickle.dump(self.spirolaterals, pickle_out)
            pickle_out.close()
        except (FileNotFoundError, TypeError):
            # user cancelled file selection
            pass

    def load_spirolateral(self):
        """
        load spirolaterals from file, supressing errors from dialog cancel
        display error if pickle fails
        if loads, then show these spirolaterals"""
        try:
            pickle_in = open(askopenfilename(), 'rb')
            self.spirolaterals = pickle.load(pickle_in)
            self.index = 0
            self.show_main_menu()
        except (FileNotFoundError, TypeError):
            # user cancelled file selection
            pass
        # would only catch pickle.UnpicklingError,
        # but it didn't catch all errors...
        except:
            # this is a popup
            toplevel = Toplevel()
            toplevel.title("Spirolateral - Error")
            error = Label(toplevel, text="The data cannot be read")
            error.grid()
            continue_button = Button(toplevel, text="Continue",
                                     command=toplevel.destroy)
            continue_button.grid(row=1, column=0)

    @classmethod
    def validate(cls, action, value_if_allowed, value):
        """validate input - allow if delete or entering int"""
        if action == "0":
            return True
        try:
            if value in '0123456789':
                int(value_if_allowed)
                return True
            raise ValueError
        except ValueError:
            return False

    def new_spirolateral(self):
        """
        make instance of spirolateral with data from text boxes,
        then append to list and delete text box data
        """
        # forget previous error messages
        self.spirolateral_name_error.grid_forget()
        self.spirolateral_times_table_error.grid_forget()
        self.spirolateral_angle_error.grid_forget()

        error_raised = False
        try:
            name = self.spirolateral_name_entry.get()
        except UnicodeDecodeError:
            # name is bad, so to not repeat code,
            # we set name to something known to raise error
            name = "🇳🇿"
        times_table = self.spirolateral_times_table_entry.get()
        angle = self.spirolateral_angle_entry.get()

        """if any entry is empty or if name contains emoji, raise error"""
        if name == "":
            self.spirolateral_name_error.configure(text="No name entered")
            self.spirolateral_name_error.grid(row=2, column=0, columnspan=2)
            error_raised = True
        for i in name:
            if ord(i) not in range(65536):
                self.spirolateral_name_error.configure(
                    text="Name contains emoji (or similar), "
                    "which are not supported")
                self.spirolateral_name_error.grid(
                    row=2, column=0, columnspan=2)
                error_raised = True
        if (times_table == "") or (times_table < 1):
            self.spirolateral_times_table_error.grid(
                row=4, column=0, columnspan=2)
            error_raised = True
        if (angle == "") or (angle < 1):
            self.spirolateral_angle_error.grid(row=6, column=0, columnspan=2)
            error_raised = True
        if not error_raised:
            self.spirolaterals.append(Spirolateral(
                self.spirolateral_name_entry.get(),
                self.spirolateral_times_table_entry.get(),
                self.spirolateral_angle_entry.get()))
            self.spirolateral_name_entry.delete(0, END)
            self.spirolateral_times_table_entry.delete(0, END)
            self.spirolateral_angle_entry.delete(0, END)
            self.show_main_menu()

    def delete_spirolateral(self):
        """delete selected spirolateral and update display"""
        del self.spirolaterals[self.index]
        if self.index > 0:
            self.index -= 1
        self.update_display()

    def display_previous(self):
        """decrease index by 1, then update display"""
        self.index -= 1
        # if index is lower than 0, wrap around
        if self.index < 0:
            self.index = len(self.spirolaterals) - 1
        self.update_display()

    def display_next(self):
        """increase index by 1, then update display"""
        self.index += 1
        # if index is higher than no. of spirolaterals, wrap around
        if self.index > len(self.spirolaterals) - 1:
            self.index = 0
        self.update_display()

    def update_display(self):
        """
        update display to show selected spirolateral
        then enable/disable previous/next buttons as necessary
        if no spirolaterals (ie deleted), then show message
        """
        if self.spirolaterals:
            self.no_spirolaterals.grid_forget()
            self.menubar.entryconfig("Delete spirolateral", state=NORMAL)
            self.name_display.configure(
                text=self.spirolaterals[self.index].name)
            self.times_table_display.configure(
                text=self.spirolaterals[self.index].times_table)
            self.angle_display.configure(
                text=self.spirolaterals[self.index].angle)
            self.digital_root_list_display.configure(
                text=self.spirolaterals[self.index].digital_root_list)

            if len(self.spirolaterals) == 1:
                self.previous_btn.configure(state=DISABLED)
                self.next_btn.configure(state=DISABLED)
            else:
                self.previous_btn.configure(state=NORMAL)
                self.next_btn.configure(state=NORMAL)

            self.main_menu.grid(row=1, column=0, sticky='nesw')
            self.footer_row.grid(row=2, column=0, sticky='nesw')
            self.draw_spirolateral()

        else:
            self.main_menu.grid_forget()
            self.footer_row.grid_forget()
            self.no_spirolaterals.grid(
                row=1, column=0, padx=self.PADX, pady=self.PADY, columnspan=2)
            self.menubar.entryconfig("Delete spirolateral", state=DISABLED)
            self.clear_spirolateral_drawing()

    def clear_spirolateral_drawing(self):
        """clear canvas. set variables so library is happy"""
        self.turtleObject = self.drawing_turtle.turtleObject
        self.ghostTurtle = self.drawing_turtle.ghostTurtle
        spirolateral_draw.SpirolateralDrawer.clearScreen(self)

    def draw_spirolateral(self):
        """Draw a spirolateral. This is a bodge (we draw once to get min/max
        values, then get scale, clear, regrid with new scale, then draw again),
        but works"""
        # we need this to determine min/max values
        self.drawing_turtle.loadRawValues(
            self.spirolaterals[self.index].name,
            self.spirolaterals[self.index].times_table,
            self.spirolaterals[self.index].angle)
        
        # get the scale
        self.scale_to_use = self.drawing_turtle.bestScale()

        # clear previous wrong scale drawing
        self.clear_spirolateral_drawing()
        # set new best scale
        self.make_draw_spirolateral_widgets()
        self.draw_spirolateral_frame.grid(row=0, column=1, sticky='nesw')

        # redraw
        self.drawing_turtle.loadRawValues(
            self.spirolaterals[self.index].name,
            self.spirolaterals[self.index].times_table,
            self.spirolaterals[self.index].angle)

    # def draw_spirolateral_part(self, *args):
    #     print(self.autoupdate)
    #     if self.autoupdate:
    #         self.drawing_turtle.loadSpiro(ModuleCompatibility(
    #             self.spirolateral_times_table_entry.get(),
    #             self.spirolateral_angle_entry.get()))


if __name__ == '__main__':
    # make instance of tk and run gui
    root = Tk()
    gui = SpirolateralGUI(root)
    root.mainloop()

# vim: ts=8 et sw=4 sts=4 smarttab cc=80
