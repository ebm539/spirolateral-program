#!/usr/bin/env python3
"""
Program that allows for spirolaterals to be added and deleted to/from a list
and allows for saving/loading list of spirolaterals
"""

# import modules as necessary
try:
    from tkinter import (
            Tk, Frame, Button, Label, Entry, END, DISABLED, NORMAL, Message,
            Toplevel)
    from tkinter.filedialog import askopenfilename, asksaveasfilename
except ModuleNotFoundError:
    print("Please install tkinter.")
    raise SystemExit
import pickle


# make class for spirolaterals
class Spirolateral:
    def __init__(self, name: str, times_table: int, angle: int):
        self.name = name
        self.times_table = times_table
        self.angle = angle


# make class for spirolateral gui
class SpirolateralGUI(Frame):
    def __init__(self, master):
        # set frames and input validation
        # then grid main menu and spirolateral list
        super().__init__(master)
        self.master = master
        master.title("Spirolateral")

        self.spirolaterals = []

        self.header_row = Frame(master)
        self.main_menu = Frame(master)
        self.add_spirolateral = Frame(master)

        self.vcmd = (master.register(self.validate), '%d', '%P')
        self.header_row_grid()
        self.main_menu_grid()

    def header_row_grid(self):
        self.add = Button(self.header_row, text="Add a spirolateral",
                          command=self.add_spirolateral_grid)
        self.add.grid(row=0, column=0)
        self.delete = Button(
            self.header_row, text="Delete spirolateral",
            command=self.delete_spirolateral)
        self.delete.grid(row=0, column=1)
        if len(self.spirolaterals):
            self.delete.configure(state=NORMAL)
        else:
            self.delete.configure(state=DISABLED)
        self.save = Button(self.header_row, text="Save spirolaterals",
                           command=self.save_spirolateral_grid)
        self.save.grid(row=0, column=2)
        self.load = Button(self.header_row, text="Load spirolaterals",
                           command=self.load_spirolateral_grid)
        self.load.grid(row=0, column=3)
        self.quit = Button(self.header_row, text="Quit",
                           command=self.master.quit)
        self.quit.grid(row=0, column=4)
        self.header_row.grid(row=0, column=0, sticky='nesw')

    def main_menu_grid(self):
        # forget previous grids, then grid main menu buttons as necessary
        self.add_spirolateral.grid_forget()
        self.name = Label(self.main_menu, text="Spirolateral name")
        self.name.grid(row=0, column=0)
        self.name_display = Label(self.main_menu, text="name here")
        self.name_display.grid(row=0, column=1)
        self.times_table = Label(self.main_menu,
                                 text="Spirolateral times table")
        self.times_table.grid(row=1, column=0)
        self.times_table_display = Label(self.main_menu,
                                         text="times_table here")
        self.times_table_display.grid(row=1, column=1)
        self.angle = Label(self.main_menu, text="Spirolateral name")
        self.angle.grid(row=2, column=0)
        self.angle_display = Label(self.main_menu, text="angle here")
        self.angle_display.grid(row=2, column=1)
        self.main_menu.grid(row=1, column=0, sticky='nesw')

    def add_spirolateral_grid(self):
        # forget previous grid, then grid labels and text boxes as necessary
        self.main_menu.grid_forget()
        self.spirolateral_name = Label(self.add_spirolateral, text="Name: ")
        self.spirolateral_name.grid(row=0, column=0)
        self.spirolateral_name_entry = Entry(self.add_spirolateral)
        self.spirolateral_name_entry.grid(row=0, column=1)

        self.spirolateral_times_table = Label(
            self.add_spirolateral, text="Number of times_table: ")
        self.spirolateral_times_table.grid(row=1, column=0)
        self.spirolateral_times_table_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_times_table_entry.grid(row=1, column=1)

        self.spirolateral_angle = Label(
            self.add_spirolateral, text="Angle of spirolateral: ")
        self.spirolateral_angle.grid(row=2, column=0)
        self.spirolateral_angle_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_angle_entry.grid(row=2, column=1)

        self.enter = Button(self.add_spirolateral, text="Enter data",
                            command=self.new_spirolateral)
        self.enter.grid(row=3, column=0)
        self.vcmd = (self.master.register(self.validate), '%d', '%P')

        self.add_spirolateral.grid(row=1, column=0, sticky='nesw')

    def save_spirolateral_grid(self):
        # save spirolaterals to file
        try:
            pickle_out = open(asksaveasfilename(), 'wb')
            pickle.dump(self.spirolaterals, pickle_out)
            pickle_out.close()
        except (FileNotFoundError, TypeError):
            # user cancelled file selection
            pass

    def load_spirolateral_grid(self):
        # load spirolaterals from file
        try:
            pickle_in = open(askopenfilename(), 'rb')
            self.spirolaterals = pickle.load(pickle_in)
        except pickle.UnpicklingError:
            toplevel = Toplevel()
            toplevel.title("Error")
            error = Label(toplevel, text="The data cannot be read")
            error.grid()
            continue_button = Button(toplevel, text="Continue",
                                     command=toplevel.destroy)
            continue_button.grid(row=1, column=0)
        except (FileNotFoundError, TypeError):
            # user cancelled file selection
            pass

    def validate(self, action, user_input):
        # validate input - allow if delete or entering int
        try:
            if action:
                return True
            if int(user_input):
                return True
            raise ValueError
        except ValueError:
            return False

    def new_spirolateral(self):
        # make instance of spirolateral with data from text boxes,
        # then append to list and delete text box data
        self.spirolaterals.append(Spirolateral(
            self.spirolateral_name_entry.get(),
            self.spirolateral_times_table_entry.get(),
            self.spirolateral_angle_entry.get()))
        self.spirolateral_name_entry.delete(0, END)
        self.spirolateral_times_table_entry.delete(0, END)
        self.spirolateral_angle_entry.delete(0, END)
        self.main_menu_grid()

    def delete_spirolateral(self):
        # delete spirolateral from list
        pass


if __name__ == '__main__':
    # make instance of tk and run gui
    root = Tk()
    gui = SpirolateralGUI(root)
    root.mainloop()

# vim: ts=8 et sw=4 sts=4 smarttab cc=80
