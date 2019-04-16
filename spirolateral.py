#!/usr/bin/env python3
"""
Program that allows for spirolaterals to be added and deleted to/from a list
and allows for saving/loading list of spirolaterals
"""

# import modules as necessary
try:
    from tkinter import (
        Tk, Frame, Button, Label, Entry, END, DISABLED, NORMAL, Toplevel)
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
        self.digitalList = []

    def digital_root(self, n):
        # calculates a digital root
        return (n - 1) % 9 + 1 if n else 0

    def digitCalc(self):
        '''Calculates a 'times table list' that is used
        as a range for the turtle to draw'''
        for i in range(20):
            test = (i+1)

            n = int(test * self.timestable)
            value = self.digit_root(n)
            if value in self.digitalList:
                break
            else:
                self.digitalList.append(value)
        return(self.digitalList)


# make class for spirolateral gui
class SpirolateralGUI(Frame):
    def __init__(self, master):
        # set frames and input validation
        # then grid main menu and spirolateral list
        super().__init__(master)
        self.master = master
        master.title("Spirolateral")

        self.spirolaterals = []
        self.index = 0

        self.header_row = Frame(master)
        self.main_menu = Frame(master)
        self.add_spirolateral = Frame(master)

        self.header_row_grid()
        self.main_menu_grid()

    def header_row_grid(self):
        self.add = Button(self.header_row, text="Add a spirolateral",
                          command=self.add_spirolateral_grid)
        self.add.grid(row=0, column=0)
        self.show_spirolaterals = Button(
                self.header_row, text="Show spirolaterals",
                command=self.main_menu_grid)
        self.delete = Button(
            self.header_row, text="Delete spirolateral",
            command=self.delete_spirolateral)
        self.delete.grid(row=0, column=1)
        self.delete.configure(state=DISABLED)
        #if len(self.spirolaterals):
        #    self.delete.configure(state=NORMAL)
        #else:
        #    self.delete.configure(state=DISABLED)
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
        print(self.index)
        self.header_row.grid_forget()
        self.header_row_grid()
        self.add_spirolateral.grid_forget()
        self.name = Label(self.main_menu, text="Name")
        self.name_display = Label(self.main_menu, text="")
        self.times_table = Label(self.main_menu,
                                 text="Times table")
        self.times_table_display = Label(self.main_menu,
                                         text="")
        self.angle = Label(self.main_menu, text="Angle")
        self.angle_display = Label(self.main_menu, text="")

        self.previous = Button(self.main_menu, text="Previous",
                               command=self.display_previous)

        self.delete = Button(self.main_menu, text="Delete",
                             command=self.delete_spirolateral)

        self.next = Button(self.main_menu, text="Next",
                           command=self.display_next)
        self.no_spirolaterals = Label(
                self.main_menu, text="There are no spirolaterals")

        if len(self.spirolaterals):
            self.name.grid(row=0, column=0)
            self.name_display.grid(row=0, column=1)
            self.times_table.grid(row=1, column=0)
            self.angle.grid(row=2, column=0)
            self.angle_display.grid(row=2, column=1)
            self.update_display()
            self.previous.grid(row=3, column=0)
            self.delete.grid(row=3, column=1)
            self.next.grid(row=3, column=2)
        else:
            self.no_spirolaterals.grid(row=0, column=0)

        self.main_menu.grid(row=1, column=0, sticky='nesw')

    def add_spirolateral_grid(self):
        # forget previous grid, then grid labels and text boxes as necessary
        self.vcmd = (self.master.register(self.validate), '%d', '%P', '%S')
        self.main_menu.grid_forget()
        self.add.grid_forget()
        self.show_spirolaterals.grid(row=0, column=0)
        self.spirolateral_name = Label(self.add_spirolateral, text="Name: ")
        self.spirolateral_name.grid(row=0, column=0)
        self.spirolateral_name_entry = Entry(self.add_spirolateral)
        self.spirolateral_name_entry.grid(row=0, column=1)
        self.spirolateral_name_error = Label(
                self.add_spirolateral, text="No name entered")

        self.spirolateral_times_table = Label(
            self.add_spirolateral, text="Times table: ")
        self.spirolateral_times_table.grid(row=1, column=0)
        self.spirolateral_times_table_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_times_table_entry.grid(row=1, column=1)
        self.spirolateral_times_table_error = Label(
                self.add_spirolateral, text="No times table entered")

        self.spirolateral_angle = Label(
            self.add_spirolateral, text="Angle of spirolateral: ")
        self.spirolateral_angle.grid(row=2, column=0)
        self.spirolateral_angle_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_angle_entry.grid(row=2, column=1)
        self.spirolateral_angle_error = Label(
                self.add_spirolateral, text="No angle entered")

        self.enter = Button(self.add_spirolateral, text="Enter data",
                            command=self.new_spirolateral)
        self.enter.grid(row=3, column=0)

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

    def validate(self, action, value_if_allowed, value):
        # validate input - allow if delete or entering int
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
        # make instance of spirolateral with data from text boxes,
        # then append to list and delete text box data

        name = self.spirolateral_name_entry.get()
        times_table = self.spirolateral_times_table_entry.get()
        angle = self.spirolateral_angle_entry.get()

        error_raised = False
        # forget previous error messages
        self.spirolateral_name_error.grid_forget()
        self.spirolateral_times_table_error.grid_forget()
        self.spirolateral_angle_error.grid_forget()

        if name == "":
            self.spirolateral_name_error.grid(row=0, column=2)
            error_raised = True
        if times_table == "":
            self.spirolateral_times_table_error.grid(row=1, column=2)
            error_raised = True
        if angle == "":
            self.spirolateral_angle_error.grid(row=2, column=2)
            error_raised = True
        if error_raised:
            return False

        self.spirolaterals.append(Spirolateral(
            self.spirolateral_name_entry.get(),
            self.spirolateral_times_table_entry.get(),
            self.spirolateral_angle_entry.get()))
        self.spirolateral_name_entry.delete(0, END)
        self.spirolateral_times_table_entry.delete(0, END)
        self.spirolateral_angle_entry.delete(0, END)
        self.main_menu_grid()

    def delete_spirolateral(self):
        # TODO: fix
        self.spirolaterals.pop[self.index]
        self.index -= 1
        self.update_display()

    def display_previous(self):
        self.index -= 1
        if len(self.spirolaterals) == 0:
            self.previous.configure(state=DISABLED)
        else:
            self.previous.configure(state=NORMAL)
        self.update_display()

    def display_next(self):
        self.index += 1
        if len(self.spirolaterals) == self.index:
            self.next.configure(state=DISABLED)
        else:
            self.next.configure(state=NORMAL)
        self.update_display()

    def update_display(self):
        print(self.index)
        print(len(self.spirolaterals))
        if self.index:
            self.name_display.configure(
                    text=self.spirolaterals[self.index].name)
            self.times_table_display.configure(
                    text=self.spirolaterals[self.index].times_table)
            self.angle_display.configure(
                    text=self.spirolaterals[self.index].angle)


if __name__ == '__main__':
    # make instance of tk and run gui
    root = Tk()
    gui = SpirolateralGUI(root)
    root.mainloop()

# vim: ts=8 et sw=4 sts=4 smarttab cc=80
