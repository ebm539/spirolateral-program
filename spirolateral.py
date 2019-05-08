#!/usr/bin/env python3
"""
Program that allows for spirolaterals to be added and deleted to/from a list
and allows for saving/loading list of spirolaterals
"""

# import modules as necessary
try:
    from tkinter import (
        Tk, Frame, Button, Label, Entry, END, DISABLED, NORMAL, Toplevel, Menu,
        Canvas)
    from tkinter.filedialog import askopenfilename, asksaveasfilename
except ModuleNotFoundError:
    print("Please install tkinter.")
    raise SystemExit
import pickle
import turtle
try:
    from lib import otherSpiroClass as spirolateral_draw
    NO_DRAW = False
except ModuleNotFoundError:
    print("Spirolateral drawing library not found, cannot draw spirolaterals")
    NO_DRAW = True


# define spirolateral class
class Spirolateral:
    """
    define spirolateral class and functions
    functions not currently used
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
        """Makes a times table list"""
        multipler = 1
        while True:
            value = self.digital_root(int(multipler * self.times_table))
            if value in self.digital_root_list:
                break
            else:
                self.digital_root_list.append(value)
                multipler += 1


class ModuleCompatibility:
    def __init__(self, dRootList: list, angle: int):
        self.dRootList = dRootList
        self.angle = angle


class SpirolateralGUI(Frame):
    def __init__(self, master):
        # set frames and input validation
        # then grid main menu and spirolateral list
        super().__init__(master)
        self.master = master
        master.title("Spirolateral")

        self.spirolaterals = []
        self.index = 0
        self.text_data_frame = Frame(self.master)

        self.make_menubar_widgets()
        self.make_main_menu_widgets()
        self.make_footer_row_widgets()
        self.make_add_spirolateral_widgets()
        self.make_draw_spirolateral_widgets()

        self.draw_spirolateral_frame.grid(row=0, column=1, sticky='nes')
        self.no_spirolaterals.grid(row=1, column=0)
        self.text_data_frame.grid(row=0, column=0, sticky='nsw')
        self.master.config(menu=self.menubar)
        self.master.columnconfigure(1, weight=1)

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
        self.name = Label(self.main_menu, text="Name")
        self.name.grid(row=0, column=0)
        self.name_display = Label(self.main_menu, text="")
        self.name_display.grid(row=0, column=1)
        self.times_table = Label(self.main_menu, text="Times table")
        self.times_table.grid(row=1, column=0)
        self.times_table_display = Label(self.main_menu, text="")
        self.times_table_display.grid(row=1, column=1)
        self.angle = Label(self.main_menu, text="Angle")
        self.angle.grid(row=2, column=0)
        self.angle_display = Label(self.main_menu, text="")
        self.angle_display.grid(row=2, column=1)
        self.digital_root_list = Label(
            self.main_menu, text="Digital root list")
        self.digital_root_list.grid(row=3, column=0)
        self.digital_root_list_display = Label(self.main_menu, text="")
        self.digital_root_list_display.grid(row=3, column=1)

    def make_footer_row_widgets(self):
        """make footer_row widgets and grid as necessary"""
        self.footer_row = Frame(self.text_data_frame)
        self.previous_btn = Button(
            self.footer_row, text="Previous", command=self.display_previous)
        self.previous_btn.grid(row=0, column=0)
        self.previous_btn.configure(state=DISABLED)
        # self.draw_btn = Button(self.footer_row, text="Draw",
        #                       command=self.draw_spirolateral)
        # self.draw_btn.grid(row=0, column=1)
        # if NO_DRAW:
        #     self.draw_btn.configure(state=DISABLED)
        self.next_btn = Button(
            self.footer_row, text="Next", command=self.display_next)
        # self.next_btn.grid(row=0, column=2)
        self.next_btn.grid(row=0, column=1)
        self.next_btn.configure(state=DISABLED)

    def make_add_spirolateral_widgets(self):
        """make add_spirolateral widgets and grid as necessary"""
        self.add_spirolateral = Frame(self.text_data_frame)
        self.vcmd = (self.master.register(self.validate), '%d', '%P', '%S')
        # self.autoupdate = IntVar()
        # self.autoupdate_checkbtn = Checkbutton(
        #     self.add_spirolateral, text="Auto update drawing",
        #     variable=self.autoupdate)
        # self.autoupdate_checkbtn.grid(row=0, column=0, columnspan=2)
        self.spirolateral_name = Label(self.add_spirolateral, text="Name: ")
        self.spirolateral_name.grid(row=1, column=0)
        self.spirolateral_name_entry = Entry(self.add_spirolateral)
        self.spirolateral_name_entry.grid(row=1, column=1)
        self.spirolateral_name_error = Label(
            self.add_spirolateral, text="No name entered")

        self.spirolateral_times_table = Label(
            self.add_spirolateral, text="Times table: ")
        self.spirolateral_times_table.grid(row=2, column=0)
        self.spirolateral_times_table_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_times_table_entry.grid(row=2, column=1)
        self.spirolateral_times_table_error = Label(
            self.add_spirolateral, text="No times table entered")
        # self.spirolateral_times_table_entry.bind(
        #     "<Key>", self.draw_spirolateral_part)

        self.spirolateral_angle = Label(
            self.add_spirolateral, text="Angle of spirolateral: ")
        self.spirolateral_angle.grid(row=3, column=0)
        self.spirolateral_angle_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_angle_entry.grid(row=3, column=1)
        self.spirolateral_angle_error = Label(
            self.add_spirolateral, text="No angle entered")
        # self.spirolateral_angle_entry.bind(
        #     "<Key>", self.draw_spirolateral_part)

        self.enter = Button(self.add_spirolateral, text="Enter data",
                            command=self.new_spirolateral)
        self.enter.grid(row=4, column=0)

    def make_draw_spirolateral_widgets(self):
        """make draw_spirolateral widgets and grid as necessary"""
        self.draw_spirolateral_frame = Frame(self.master)
        canvas = Canvas(self.draw_spirolateral_frame, height=480, width=480)
        canvas.grid(row=0, column=0)
        screen = turtle.TurtleScreen(canvas)
        screen.screensize(480, 480)
        # TODO: allow for dynamically changing scale (although the program
        # should automatically do that to fit to screen)
        self.drawing_turtle = spirolateral_draw.SpirolateralDrawer(screen, 6)

    def show_main_menu(self):
        """
        forget add ui, grid show spirolateral ui
        and enable delete menubar button
        """
        self.add_spirolateral.grid_forget()
        self.menubar.entryconfig("Show spirolaterals", state=DISABLED)
        self.menubar.entryconfig("Add a spirolateral", state=NORMAL)
        self.menubar.entryconfig("Delete spirolateral", state=NORMAL)
        self.update_display()

    def show_add_spirolateral(self):
        """
        forget show spirolateral ui, grid add ui
        and disable delete menubar button
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
            toplevel = Toplevel()
            toplevel.title("Error")
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

        if name == "":
            self.spirolateral_name_error.configure(text="No name entered")
            self.spirolateral_name_error.grid(row=1, column=2)
            error_raised = True
        for i in name:
            if ord(i) not in range(65536):
                self.spirolateral_name_error.configure(
                    text="Name contains emoji (or similar), "
                    "which are not supported")
                self.spirolateral_name_error.grid(row=1, column=2)
                error_raised = True
        if times_table == "":
            self.spirolateral_times_table_error.grid(row=2, column=2)
            error_raised = True
        if angle == "":
            self.spirolateral_angle_error.grid(row=3, column=2)
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
            self.no_spirolaterals.grid(row=1, column=0)
            self.menubar.entryconfig("Delete spirolateral", state=DISABLED)
            self.clear_spirolateral_drawing()

    def clear_spirolateral_drawing(self):
        # more compatibility...
        self.turtleObject = self.drawing_turtle.turtleObject
        self.ghostTurtle = self.drawing_turtle.ghostTurtle
        spirolateral_draw.SpirolateralDrawer.clearScreen(self)

    def draw_spirolateral(self):
        """Draw a spirolateral"""
        # drawing_turtle.loadSpiro(self.spirolaterals[self.index])

        # compatibility, so that module can access digital root list and angle

        self.drawing_turtle.loadSpiro(ModuleCompatibility(
            self.spirolaterals[self.index].digital_root_list,
            self.spirolaterals[self.index].angle))

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
