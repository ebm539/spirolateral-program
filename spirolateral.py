#!/usr/bin/env python3
try:
    from tkinter import (Tk, Frame, Button, Label,
                         Entry, END, DISABLED, NORMAL, Message)
    from tkinter.filedialog import askopenfilename, asksaveasfilename
except ModuleNotFoundError:
    print("Please install tkinter.")
    raise SystemExit
try:
    from dataclasses import dataclass
except ModuleNotFoundError:
    print("Please install Python 3.7 or above.")
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

        self.main_menu = Frame(master, width=640, height=480)
        self.main_menu.grid_propagate(0)

        self.spirolateral_list = Frame(master)
        self.add_spirolateral = Frame(master)
        self.delete_spirolateral = Frame(master)
        self.save_spirolateral = Frame(master)
        self.load_spirolateral = Frame(master)

        self.vcmd = (master.register(self.validate), '%d', '%P')
        self.main_menu_grid()
        self.spirolateral_list_grid()

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
        if len(self.spirolaterals):
            self.delete.configure(state=NORMAL)
        else:
            self.delete.configure(state=DISABLED)
        self.save = Button(self.main_menu, text="Save a spirolateral",
                           command=self.save_spirolateral_grid)
        self.save.grid(row=2, column=0)
        self.load = Button(self.main_menu, text="Load a spirolateral",
                           command=self.load_spirolateral_grid)
        self.load.grid(row=3, column=0)
        self.quit = Button(self.main_menu, text="Quit",
                           command=self.master.quit)
        self.quit.grid(row=4, column=0)
        self.vcmd = (self.master.register(self.validate), '%d', '%P')
        self.main_menu.grid()

    def spirolateral_list_grid(self):
        text = ""
        for i in self.spirolaterals:
            #text += "{} {} segments, {}°".format(i
            print(i)
        self.spirolateral_list_text = Message(self.spirolateral_list, text="Spirolateral list here")
        self.spirolateral_list_text.grid()
        self.spirolateral_list.grid(row=0, column=1)

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
            self.delete_spirolateral, validate='key',
            validatecommand=self.vcmd)
        self.spirolateral_delete_no_entry.grid(row=2, column=1)
        self.main_menu.grid_forget()
        self.quit = Button(self.delete_spirolateral, text="Quit",
                           command=self.master.quit)
        self.quit.grid(row=4, column=0)

        self.back = Button(self.delete_spirolateral, text="Back",
                           command=self.main_menu_grid)
        self.back.grid(row=5, column=0)

        self.delete = Button(self.delete_spirolateral,
                             text="Delete spirolateral",
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

    def validate(self, action, user_input):
        try:
            if action:
                return True
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
        self.spirolateral_list_grid()

    def delete_spirolateral(self):
        del self.spirolaterals[self.spirolateral_delete_no_entry.get()]
        self.spirolateral_delete_no_entry.delete(0, END)
        if not len(self.spirolaterals):
            self.main_menu_grid()
        self.spirolateral_list_grid()


if __name__ == '__main__':
    root = Tk()
    gui = SpirolateralGUI(root)
    root.mainloop()

# vim: ts=8 et sw=4 sts=4 smarttab
