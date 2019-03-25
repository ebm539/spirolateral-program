#!/usr/bin/env python3
from tkinter import Tk, Frame, Button, Label, Entry, END
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dataclasses import dataclass
import pickle


@dataclass
class Spirolateral:
    name: str
    segments: int
    angle: int


class SpirolateralGUI(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Spirolateral")

        self.spirolaterals = []

        self.main_menu = Frame(master, width=300, height=200)
        self.main_menu.grid_propagate(0)

        self.add_spirolateral = Frame(master, width=300, height=200)
        self.add_spirolateral.grid_propagate(0)

        self.delete_spirolateral = Frame(master, width=300, height=200)
        self.delete_spirolateral.grid_propagate(0)

        self.save_spirolateral = Frame(master, width=300, height=200)
        self.save_spirolateral.grid_propagate(0)

        self.load_spirolateral = Frame(master, width=300, height=200)
        self.load_spirolateral.grid_propagate(0)

        self.vcmd = (master.register(self.validate), '%P')
        self.main_menu_grid()

    def main_menu_grid(self):
        self.add_spirolateral.grid_forget()
        self.delete_spirolateral.grid_forget()
        self.save_spirolateral.grid_forget()
        self.load_spirolateral.grid_forget()
        self.main_menu.grid_propagate(0)
        self.add = Button(self.main_menu, text="Add a spirolateral",
                          command=self.add_spirolateral_grid)
        self.add.grid(row=0, column=0)
        self.delete = Button(
            self.main_menu, text="Delete a spirolateral",
            command=self.delete_spirolateral_grid)
        self.delete.grid(row=1, column=0)
        self.save = Button(self.main_menu, text="Save a spirolateral",
                           command=self.save_spirolateral_grid)
        self.save.grid(row=2, column=0)
        self.load = Button(self.main_menu, text="Load a spirolateral",
                           command=self.load_spirolateral_grid)
        self.load.grid(row=3, column=0)
        self.quit = Button(self.main_menu, text="Quit",
                           command=self.master.quit)
        self.quit.grid(row=4, column=0)
        self.vcmd = (self.master.register(self.validate), '%P')
        self.main_menu.grid()

    def add_spirolateral_grid(self):
        self.main_menu.grid_forget()
        self.spirolateral_name = Label(self.add_spirolateral, text="Name: ")
        self.spirolateral_name.grid(row=0, column=0)
        self.spirolateral_name_entry = Entry(self.add_spirolateral)
        self.spirolateral_name_entry.grid(row=0, column=1)

        self.spirolateral_segments = Label(
            self.add_spirolateral, text="Number of segments: ")
        self.spirolateral_segments.grid(row=1, column=0)
        self.spirolateral_segments_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_segments_entry.grid(row=1, column=1)

        self.spirolateral_angle = Label(
            self.add_spirolateral, text="Angle of spirolateral: ")
        self.spirolateral_angle.grid(row=2, column=0)
        self.spirolateral_angle_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_angle_entry.grid(row=2, column=1)

        self.quit = Button(self.add_spirolateral, text="Quit",
                           command=self.master.quit)
        self.quit.grid(row=4, column=0)

        self.back = Button(self.add_spirolateral, text="Back",
                           command=self.main_menu_grid)
        self.back.grid(row=5, column=0)

        self.enter = Button(self.add_spirolateral, text="Enter data",
                            command=self.new_spirolateral)
        self.enter.grid(row=6, column=0)

        self.add_spirolateral.grid()

    def delete_spirolateral_grid(self):
        self.spirolateral_delete_no = Label(
            self.delete_spirolateral, text="Spirolateral no. to delete: ")
        self.spirolateral_delete_no.grid(row=2, column=0)
        self.spirolateral_delete_no_entry = Entry(
            self.delete_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_delete_no_entry.grid(row=2, column=1)
        self.main_menu.grid_forget()
        self.quit = Button(self.delete_spirolateral, text="Quit",
                           command=self.master.quit)
        self.quit.grid(row=4, column=0)

        self.back = Button(self.delete_spirolateral, text="Back",
                           command=self.main_menu_grid)
        self.back.grid(row=5, column=0)

        self.delete = Button(self.delete_spirolateral, text="Delete spirolateral",
                             command=self.delete_spirolateral)
        self.delete.grid(row=6, column=0)
        self.delete_spirolateral.grid()

    def save_spirolateral_grid(self):
        # self.main_menu.grid_forget()
        filename = asksaveasfilename()
        try:
            pickle_out = open(filename, 'wb')
            pickle.dump(self.spirolaterals, pickle_out)
            pickle_out.close()
        except FileNotFoundError:
            # user cancelled file selection
            pass

    def load_spirolateral_grid(self):
        # self.main_menu.grid_forget()
        filename = askopenfilename()
        try:
            pickle_in = open(filename, 'rb')
            self.spirolaterals = pickle.load(pickle_in)
        except pickle.UnpicklingError:
            print("This error should be in the GUI. The data cannot be read.")
        except FileNotFoundError:
            # user cancelled file selection
            pass

    def validate(self, user_input):
        try:
            if int(user_input):
                return True
            raise ValueError
        except ValueError:
            return False

    def new_spirolateral(self):
        self.spirolaterals.append(Spirolateral(
            self.spirolateral_name_entry.get(),
            self.spirolateral_segments_entry.get(),
            self.spirolateral_angle_entry.get()))
        self.spirolateral_name_entry.delete(0, END)
        self.spirolateral_segments_entry.delete(0, END)
        self.spirolateral_angle_entry.delete(0, END)

    def delete_spirolateral(self):
        del self.spirolaterals[self.spirolateral_delete_no_entry.get()]
        self.spirolateral_delete_no_entry.delete(0, END)
        if not len(self.spirolaterals):
            self.main_menu_grid()


if __name__ == '__main__':
    root = Tk()
    gui = SpirolateralGUI(root)
    root.mainloop()

# vim: ts=8 et sw=4 sts=4 smarttab
