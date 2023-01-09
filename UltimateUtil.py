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

