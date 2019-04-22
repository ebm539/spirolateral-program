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
    """
    define spirolateral class and functions
    functions not currently used
    """
    def __init__(self, name: str, times_table: int, angle: int):
        self.name = name
        self.times_table = times_table
        self.angle = angle
        # self.digitalList = []

    """
    def digital_root(self, n):
        # calculates a digital root
        return (n - 1) % 9 + 1 if n else 0

    def digitCalc(self):
        '''Calculates a 'times table list' that is used
        as a range for the turtle to draw'''
        for i in range(20):
            test = (i+1)

            n = int(test * self.timestable)
            value = self.digital_root(n)
            if value in self.digitalList:
                break
            else:
                self.digitalList.append(value)
        return(self.digitalList)
    """


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
        self.add_spirolateral_grid()
        self.header_row.grid(row=0, column=0, sticky='nesw')
        self.no_spirolaterals.grid(row=1, column=0)

    def header_row_grid(self):
        """define and grid buttons"""
        self.add_btn = Button(self.header_row, text="Add a spirolateral",
                              command=self.change_to_add_spirolateral)
        self.add_btn.grid(row=0, column=0)
        self.show_btn = Button(
            self.header_row, text="Show spirolaterals",
            command=self.change_to_main_menu)
        self.delete_header_btn = Button(
            self.header_row, text="Delete spirolateral",
            command=self.delete_spirolateral)
        self.delete_header_btn.grid(row=0, column=1)
        self.delete_header_btn.configure(state=DISABLED)
        self.save_btn = Button(self.header_row, text="Save spirolaterals",
                               command=self.save_spirolateral_grid)
        self.save_btn.grid(row=0, column=2)
        self.load_btn = Button(self.header_row, text="Load spirolaterals",
                               command=self.load_spirolateral_grid)
        self.load_btn.grid(row=0, column=3)
        self.quit_btn = Button(self.header_row, text="Quit",
                               command=self.master.quit)
        self.quit_btn.grid(row=0, column=4)

    def main_menu_grid(self):
        """define and grid buttons and labels"""
        self.no_spirolaterals = Label(
            self.master, text="There are no spirolaterals")
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

        self.previous_btn = Button(
            self.main_menu, text="Previous", command=self.display_previous)
        self.previous_btn.grid(row=3, column=0)
        self.previous_btn.configure(state=DISABLED)
        self.delete_main_btn = Button(self.main_menu, text="Delete",
                                      command=self.delete_spirolateral)
        self.delete_main_btn.grid(row=3, column=1)
        self.next_btn = Button(
            self.main_menu, text="Next", command=self.display_next)
        self.next_btn.grid(row=3, column=2)
        self.next_btn.configure(state=DISABLED)

    def add_spirolateral_grid(self):
        """define and grid buttons, labels and text boxes"""
        self.vcmd = (self.master.register(self.validate), '%d', '%P', '%S')
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

    def change_to_main_menu(self):
        """
        forget add ui, grid show spirolateral ui
        and enable delete header button
        """
        self.add_spirolateral.grid_forget()
        self.show_btn.grid_forget()
        self.add_btn.grid(row=0, column=0)
        self.delete_header_btn.configure(state=NORMAL)
        self.update_display()

    def change_to_add_spirolateral(self):
        """
        forget show spirolateral ui, grid add ui
        and disable delete header button
        """
        self.main_menu.grid_forget()
        self.add_btn.grid_forget()
        self.show_btn.grid(row=0, column=0)
        self.delete_header_btn.configure(state=DISABLED)
        self.no_spirolaterals.grid_forget()
        self.add_spirolateral.grid(row=1, column=0, sticky='nesw')

    def save_spirolateral_grid(self):
        """save spirolaterals to file, supressing errors from dialog cancel"""
        try:
            pickle_out = open(asksaveasfilename(), 'wb')
            pickle.dump(self.spirolaterals, pickle_out)
            pickle_out.close()
        except (FileNotFoundError, TypeError):
            # user cancelled file selection
            pass

    def load_spirolateral_grid(self):
        """
        load spirolaterals from file, supressing errors from dialog cancel
        display error if pickle fails
        if loads, then show these spirolaterals"""
        try:
            pickle_in = open(askopenfilename(), 'rb')
            self.spirolaterals = pickle.load(pickle_in)
            self.change_to_main_menu()
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
        self.change_to_main_menu()

    def delete_spirolateral(self):
        """delete selected spirolateral and update display"""
        del self.spirolaterals[self.index]
        if self.index > 0:
            self.index -= 1
        self.update_display()

    def display_previous(self):
        """decrease index by 1, then update display"""
        self.index -= 1
        self.update_display()

    def display_next(self):
        """increase index by 1, then update display"""
        self.index += 1
        self.update_display()

    def update_display(self):
        """
        update display to show selected spirolateral
        then enable/disable previous/next buttons as necessary
        if no spirolaterals (ie deleted), then show message
        """
        if self.spirolaterals:
            self.no_spirolaterals.grid_forget()
            self.delete_header_btn.configure(state=NORMAL)
            self.delete_main_btn.configure(state=NORMAL)
            self.name_display.configure(
                text=self.spirolaterals[self.index].name)
            self.times_table_display.configure(
                text=self.spirolaterals[self.index].times_table)
            self.angle_display.configure(
                text=self.spirolaterals[self.index].angle)

            if self.index == 0:
                self.previous_btn.configure(state=DISABLED)
                if len(self.spirolaterals) > 1:
                    self.next_btn.configure(state=NORMAL)
                not_min = False
            else:
                not_min = True
            if len(self.spirolaterals) - 1 == self.index:
                self.next_btn.configure(state=DISABLED)
                if len(self.spirolaterals) > 1:
                    self.previous_btn.configure(state=NORMAL)
                not_max = False
            else:
                not_max = True

            # bodge, eww
            if not_min and not_max:
                self.previous_btn.configure(state=NORMAL)
                self.next_btn.configure(state=NORMAL)
            self.main_menu.grid(row=1, column=0, sticky='nesw')

        else:
            self.main_menu.grid_forget()
            self.no_spirolaterals.grid(row=1, column=0)
            self.delete_header_btn.configure(state=DISABLED)


if __name__ == '__main__':
    # make instance of tk and run gui
    root = Tk()
    gui = SpirolateralGUI(root)
    root.mainloop()

# vim: ts=8 et sw=4 sts=4 smarttab cc=80
