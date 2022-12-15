import glob
from tkinter import *
from tkinter import ttk
import time
import tkinter.messagebox
import os
from tkinter.filedialog import askdirectory

# This function will be called when the "Select Folder" button is clicked
def select_folder():
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
        dropdown['values'] = values

    # Set the default value for the drop down menu
    dropdown.current(0)

# This function will be called when the "Insert" button or the Enter key is pressed
def insert_value():
    # Get the selected value from the drop down menu
    selected_value = dropdown.get()

    # Get the value from the input box
    input_value = input_box.get()

    # Store the input value in the dictionary of values to change
    values_to_change[selected_value] = input_value

    # Clear the input box
    input_box.delete(0, 'end')

    # Show a message box with the old and new key-value pairs
    old_value = selected_value + ' = ' + values_to_change[selected_value]
    new_value = selected_value + ' = ' + input_value
    tkinter.messagebox.showinfo('Change Documented:\n', 'Old key-value pair:\n' + old_value + '\nNew key-value pair:\n' + new_value)

# This function will be called when the "DONE" button is pressed
def done():
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
            for key, value in values_to_change.items():
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

# Create the GUI window
root = Tk()
root.title("Cetis Bulk Configuration Editor")

# Create the progress bar
progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')

# Create a dictionary to store the values to change
values_to_change = {}

# Create a drop down menu
dropdown = ttk.Combobox(root, values=[])

# Create an input box
input_box = Entry(root)

# Create a button to select the folder
folder_button = Button(root, text='Select Folder', command=select_folder)

# Create a button to insert the value
insert_button = Button(root, text='Insert', command=insert_value)

# Bind the Enter key to the insert_value function
root.bind('<Return>', insert_value)

# Create a button to indicate that all values have been entered
done_button = Button(root, text='DONE', command=done)

# Place the GUI elements in the window
dropdown.pack()
input_box.pack()
folder_button.pack()
insert_button.pack()
done_button.pack()
progress.pack()

# Start the GUI event loop
root.mainloop()
