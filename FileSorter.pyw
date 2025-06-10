import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Global vars
dirList = []
log = []

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Sorter v1.1")
        self.geometry("500x300")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # # Tabs are always at the top of the window
        # tabs = Tabs(self)
        # tabs.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # Switches views
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=15)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ConsoleTab, SortTab):
            pageName = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[pageName] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # The Sort tab is opened by default
        self.show_frame("SortTab")

    def show_frame(self, pageName):
        self.frames[pageName].tkraise()

# This Tab obj is used on all pages to switch between tab in the app
class Tabs(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.consoleButton = ttk.Button(self, text="Console output", command=lambda: controller.show_frame("ConsoleTab"))
        self.consoleButton.grid(row=0, column=0, sticky="ew")

        self.sortingButton = ttk.Button(self, text="Sort folders", command=lambda: controller.show_frame("SortTab"))
        self.sortingButton.grid(row=0, column=1, sticky="ew")
######################### End of Tab logic #########################

# This ConsoleTab obj generates the Console tab by calling all necessary components
class ConsoleTab(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, weight=1)

        self.tabs = Tabs(self, controller)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(10,15))

        self.content = ConsoleContent(self)
        self.content.grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.saveButton = Save(self)
        self.saveButton.grid(row=2, column=3, sticky="e", pady=(10,0))

class ConsoleContent(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.saveButton = ttk.Button(self, text="Refresh", command=self.refresh)
        self.saveButton.grid(row=0, column=0, columnspan=2, pady=(0,5))

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky='ns')

        self.logOutput = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.logOutput.grid(row=1, column=0, sticky='nsew')

        self.scrollbar.config(command=self.logOutput.yview)
    
    def refresh(self):
        self.logOutput.delete(0, tk.END)
        for msg in log:
            self.logOutput.insert(tk.END, msg)

class Save(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.sortButton = ttk.Button(self, text="Save logs to .txt file", command=self.save)
        self.sortButton.grid(row=3, column=3, sticky="e")
    
    def save(self):
        files = [('Text Document', '*.txt'),('All Files', '*.*')]
        file = filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        if file:
            try:
                for msg in log:
                    file.write(msg+"\n")
            except Exception as e:
                log.append("Error writing to file:")
                log.append(e)
            finally:
                file.close()
######################### End of Console tab logic #########################

# This SortTab obj generates the Sort tab by calling all necessary components
class SortTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, weight=1)

        self.tabs = Tabs(self, controller)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(10,15))

        self.content = SortContent(self)
        self.content.grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.sort = Sort(self)
        self.sort.grid(row=2, column=3, sticky="e", pady=(10,0))

class SortContent(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(1, weight=1)

        self.addDirectoryButton = ttk.Button(self, text="Add folder", command=self.select_dir)
        self.addDirectoryButton.grid(row=0, column=1)

        self.clearListButton = ttk.Button(self, text="Clear", command=self.clear_list)
        self.clearListButton.grid(row=0, column=2)

        self.directoryList = tk.Listbox(self)
        self.directoryList.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(5,0))

    def clear_list(self):
        log.append("INFO:\tCleared list of directories")
        self.directoryList.delete(0, tk.END)
        dirList.clear()

    def select_dir(self):
        folderPath = filedialog.askdirectory()

        if folderPath:
            if (folderPath not in dirList):
                log.append("INFO:\tSelected folder: "+folderPath)
                self.directoryList.insert(tk.END, folderPath)
                dirList.append(folderPath)
        else:
            log.append("INFO:\tNo folder selected.")

class Sort(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.sortButton = ttk.Button(self, text="Sort contents of above folders", command=self.sort_by_filetype)
        self.sortButton.grid(row=3, column=3, sticky="e")

    # This is the sorting algorithm
    def sort_by_filetype(self):
        try:
            if (not dirList):
                log.append("WARNING:\tNo directories present when user tried to sort.")
                messagebox.showwarning("Warning", "You haven't selected any folders to sort.")
            else:
                for directoryText in dirList:
                    directory = os.fsencode(directoryText)
                    # Throw warning if directory wasn't found
                    if (not os.path.isdir(directory)):
                        log.append("WARNING:\tDirectory '"+directoryText+"' was not found.")
                        continue
                    
                    folders = {}
                    
                    for file in os.listdir(directory):
                        filename = os.fsdecode(file)
                        # Skip over the config file
                        if (filename == "FileSorter.config" or filename == "FileSorter.py"):
                            continue

                        filenameSplit = filename.split(".")

                        # We know this is a file
                        if (os.path.isfile(directoryText+"/"+filename)):  
                            if (len(filenameSplit) > 1):
                                extension = filenameSplit[-1]
                            else:
                                extension = "file"
                            log.append("INFO:\tFile '"+filename+"' is of type: "+extension)

                            # Make sub-directory if it doesn't already exist
                            if (extension.lower() not in folders):
                                folders[extension.lower()] = True
                                try:
                                    os.mkdir(directoryText+'/'+extension.lower())
                                    log.append("INFO:\tCreated folder: "+directoryText+'/'+extension.lower())
                                except FileExistsError:
                                    folders[extension.lower()] = True
                                    log.append("INFO:\tFolder aready exists: "+directoryText+'/'+extension.lower())
                                except Exception as e:
                                    log.append(e)

                            # Move file to its respective sub-directory
                            try:
                                shutil.move(directoryText+'/'+filename, directoryText+'/'+extension.lower()+'/'+filename)
                                log.append("Successfully moved "+directoryText+'/'+filename+" to "+directoryText+'/'+extension.lower()+'/'+filename)
                            except PermissionError:
                                log.append("ERROR:\tFile '"+filename+"' failed to be moved due to a lack of permissions. Make sure this file isn't open in another program!")
                                log.append(e)
                            except Exception as e:
                                log.append("ERROR:\tFile '"+filename+"' failed to be moved: ")
                                log.append(e)

                        # We know this is a folder
                        else:
                            log.append("INFO:\tFound existing folder: "+filename)
                            if (filename.lower() not in folders):
                                folders[filename.lower()] = True
                messagebox.showinfo("Complete", "Your folders have been sorted.\nPlease check the logs if any files have not been moved.")
        
        except Exception as e:
            log.append("ERROR:\tAn unexpected error occured in the sorting algorithm:")
            log.append(e)
            messagebox.showerror("Error occured", "An unexpected error occured.\nPlease go into the 'Console output' tab and save the log.\nContact: tmironovici@gmail.com")
######################### End of Sort tab logic #########################
        
app = Application()
app.mainloop()