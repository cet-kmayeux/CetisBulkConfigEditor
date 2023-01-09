#!/usr/bin/env python3

#This tool is an attempt to combine all of the Cetis Configuration File Utilities into an AIO program.

import glob
import time
import tkinter.messagebox
import os, os.path
import progressbar
from re import match
from PIL import ImageTk, Image
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

class ConfigEditor():
    def __init__(self, master=None):
        # Create the GUI window
        self.ConfigEditor = Tk()
        self.ConfigEditor.title("Cetis Bulk Configuration Editor")
    
        # Create a dictionary to store the values to change
        self.values_to_change = {}
    
        # Create a drop down menu
        self.dropdown = ttk.Combobox(self.ConfigEditor, values=[])
    
        # Create an input box
        self.input_box = Entry(self.ConfigEditor)
    
        # Create a button to select the folder
        self.folder_button = Button(self.ConfigEditor, text='Select Folder', command=self.select_folder)
    
        # Create a button to insert the value
        self.insert_button = Button(self.ConfigEditor, text='Insert', command=self.insert_value)
    
        # Create a button to indicate that all values have been entered
        self.done_button = Button(self.ConfigEditor, text='DONE', command=self.done)
    
        # Place the GUI elements in the window
        self.dropdown.pack()
        self.input_box.pack()
        self.folder_button.pack()
        self.insert_button.pack()
        self.done_button.pack()

        self.mainwindow = self.ConfigEditor

# This function will be called when the "Select Folder" button is clicked
    def select_folder(self):
        global files
        # Ask the user to select a directory
        cwd = os.getcwd()
        folder_path = askdirectory(initialdir=cwd)
    
        # Search for files in the selected directory
        files = glob.glob(folder_path + '/*')
    
        # Scan the first file and find all values delimited by an equals sign "="
        with open(files[0], 'r') as f:
            lines = f.readlines()
    
        values = []
        for line in lines:
            # Split the line at the equals sign and store the left part in the list of values
            parts = line.split('=')
            values.append(parts[0].strip())
    
        # Populate the drop down menu with the values from the first file
        for value in values:
            self.dropdown['values'] = values
    
        # Set the default value for the drop down menu
        self.dropdown.current(0)
    
    # This function will be called when the "Insert" button or the Enter key is pressed
    def insert_value(self):
        # Get the selected value from the drop down menu
        selected_value = self.dropdown.get()
    
        # Get the value from the input box
        input_value = self.input_box.get()
    
        # Store the input value in the dictionary of values to change
        self.values_to_change[selected_value] = input_value
    
        # Clear the input box
        self.input_box.delete(0, 'end')
    
        # Show a message box with the old and new key-value pairs
        old_value = selected_value + ' = ' + self.values_to_change[selected_value]
        new_value = selected_value + ' = ' + input_value
        tkinter.messagebox.showinfo('Change Documented:\n', 'Old key-value pair:\n' + old_value + '\nNew key-value pair:\n' + new_value)
    
    # This function will be called when the "DONE" button is pressed
    def done(self):
        # Record the start time
        start_time = time.time()
    
        # Create a counter to keep track of the number of files changed
        counter = 0
    
        # Go through each file in the selected directory
        for file in files:
            counter += 1
            # Read the file
            with open(file, 'r') as f:
                lines = f.readlines()
    
            # Go through each line in the file
            for i in range(len(lines)):
                for key, value in self.values_to_change.items():
                    # If the line contains the key, replace it with the key and the new value
                    if key in lines[i]:
                        lines[i] = key + '=' + value + '\n'
    
            # Write the modified lines back to the file
            with open(file, 'w') as f:
                f.writelines(lines)
    
        # Calculate the total time taken
        total_time = time.time() - start_time
    
        # Round the total time to the nearest hundreth
        total_time = round(total_time, 2)
    
        # Show a pop-up window with the message "Changes Complete!" and the time taken
        tkinter.messagebox.showinfo('Changes Complete!', 'The changes have been applied to all ' + str(counter) + ' of the files.\n\nTotal time taken: ' + str(total_time) + ' seconds')

    def run(self):
        self.mainwindow.mainloop()
    
if __name__ == "__main__":
    app = ConfigEditor()
    app.run()
