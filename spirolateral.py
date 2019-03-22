#!/usr/bin/env python3
from tkinter import Tk, Frame, Button, Label, Entry
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dataclasses import dataclass


@dataclass
class Spirolateral:
    name: str
    segment: int
    angle: int


class SpirolateralGUI(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Spirolateral")

        self.main_menu = Frame(master, width=300, height=200)
        self.main_menu.grid_propagate(0)
        self.main_menu.grid()

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

    def add_spirolateral_grid(self):
        self.main_menu.grid_forget()
        self.spirolateral_name = Label(self.add_spirolateral, text="Name:")
        self.spirolateral_name.grid(row=0, column=0)
        self.spirolateral_name_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_name_entry.grid(row=0, column=1)

        self.spirolateral_segments = Label(
            self.add_spirolateral, text=" Number of segments")
        self.spirolateral_segments.grid(row=1, column=0)
        self.spirolateral_segments_entry = Entry(
            self.add_spirolateral, validate='key', validatecommand=self.vcmd)
        self.spirolateral_segments_entry.grid(row=1, column=1)

        self.spirolateral_angle = Label(
            self.add_spirolateral, text="Angle of spirolateral")
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
                           command=pass)
        self.enter.grid(row=6, column=0)

        self.add_spirolateral.grid()

    def delete_spirolateral_grid(self):
        self.main_menu.grid_forget()

    def save_spirolateral_grid(self):
        # self.main_menu.grid_forget()
        filename = asksaveasfilename()

    def load_spirolateral_grid(self):
        # self.main_menu.grid_forget()
        filename = askopenfilename()

    def validate(self, user_input):
        try:
            if int(user_input):
                return True
            raise ValueError
        except ValueError:
            return False


if __name__ == '__main__':
    root = Tk()
    gui = SpirolateralGUI(root)
    root.mainloop()

# vim: ts=8 et sw=4 sts=4 smarttab
