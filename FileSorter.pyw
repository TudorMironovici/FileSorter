import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# import necessary libraries
try:
    import mymodule
except ImportError as e:
    pass 


# Global vars
dirList = []
log = []
includeSubfolders = False
enableRootDir = False
rootDirectory = ""
ruleCount = 0
ruleID = 0
rules = {}

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Sorter v2")
        self.geometry("550x800")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Switches views
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=15)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ConsoleTab, SortTab, OptionsTab):
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

        self.sortingButton = ttk.Button(self, text="⚙", command=lambda: controller.show_frame("OptionsTab"))
        self.sortingButton.grid(row=0, column=2)

        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(15,0))
######################### End of Tab logic #########################

# This ConsoleTab obj generates the Console tab by calling all necessary components
class ConsoleTab(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, weight=1)

        self.tabs = Tabs(self, controller)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 15))

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
        self.tabs.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0,15))

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
                    
                    #keep track of folders we know exist along the way to prevent repeat create dir requests
                    folders = {}
                    
                    for file in os.listdir(directory):
                        filename = os.fsdecode(file)
                        # Skip over the script
                        if (filename == "FileSorter.pyw"):
                            continue

                        filenameSplit = filename.split(".")

                        # We know this is a file
                        if (os.path.isfile(directoryText+"/"+filename)):  
                            if (len(filenameSplit) > 1):
                                extension = filenameSplit[-1]
                            else:
                                extension = "file"
                            log.append("INFO:\tFile '"+filename+"' is of type: "+extension)

                            ruleMatched = False

                            # we have a dictionary of rules: {All: [[word1,dir1,id1], [word2,dir2, id2]], .pdf: [[word3,dir3,id3], [word4,dir4,id4]]}
                            # prioritize all files types, then All
                            supportedExtensions = ['.pdf', '.txt', '.docx']
                            
                            if (('.'+extension) in supportedExtensions):
                                # if the filetype is supported and there are rules for it
                                if (('.'+extension) in rules):
                                    currRuleset = rules.get('.'+extension)
                                    allRuleset = rules.get('All')
                                    currRuleset += allRuleset
                                    
                                    for rule in currRuleset:
                                        # check if any of the filetype keywords are present, and if so move them into that special directory
                                        fileToText = "" #TODO
                                        if (rule[0] in fileToText):
                                            ruleMatched = True
                                            log.append("INFO:\t Found '"+rule[0]+"' in "+filename)
                                            
                                            make_dir(rule[1], folders)
                                            move_file(directoryText+'/'+filename, rule[1], filename)
            
                                # Checks for just the 'All' in case filetype isn't specified
                                else:
                                    currRuleset = rules.get('All')
                                    for rule in currRuleset:
                                        # check if any of the filetype keywords are present, and if so move them into that special directory
                                        fileToText = "" #TODO
                                        if (rule[0] in fileToText):
                                            ruleMatched = True
                                            log.append("INFO:\t Found '"+rule[0]+"' in "+filename)
                                    log.append("INFO:")
                                    #look at the "all" ruleset

                            # default interaction if the filetype is unsupported or does not match any rules
                            if (not ruleMatched):
                                make_dir(directoryText+'/'+extension.lower(), folders)
                                move_file(directoryText+'/'+filename, directoryText+'/'+extension.lower()+'/'+filename, filename)

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

        def make_dir(dir, folders):
            # Make sub-directory if it doesn't already exist
            if (dir not in folders):
                folders[dir] = True
                try:
                    os.mkdir(dir)
                    log.append("INFO:\tCreated folder: "+dir)
                except FileExistsError:
                    log.append("INFO:\tFolder aready exists: "+dir)
                except Exception as e:
                    log.append(e)

        def move_file(curr, new, filename):
            # Move file to its respective sub-directory
            try:
                shutil.move(curr, new)
                log.append("Successfully moved "+curr+" to "+new)
            except PermissionError:
                log.append("ERROR:\tFile '"+filename+"' failed to be moved due to a lack of permissions. Make sure this file isn't open in another program!")
                log.append(e)
            except Exception as e:
                log.append("ERROR:\tFile '"+filename+"' failed to be moved: ")
                log.append(e)
######################### End of Sort tab logic #########################

# This OptionsTab obj generates the Sort tab by calling all necessary components
class OptionsTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, weight=1)

        self.tabs = Tabs(self, controller)
        self.tabs.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0,15))

        self.content = OptionsContent(self)
        self.content.grid(row=1, column=0, columnspan=4, sticky="nsew")

class OptionsContent(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(3, weight=1)
        
        self.subDirsBool = tk.BooleanVar()
        self.rootDirBool = tk.BooleanVar()
        
        self.subDirs = ttk.Checkbutton(self, text="Automatically include all sub-folders", command=self.sub_dirs, variable=self.subDirsBool, onvalue=True, offvalue=False)
        self.subDirs.grid(row=0, column=0, sticky='w')

        self.rootDir = ttk.Checkbutton(self, text="Put all my sorted files under this parent folder:", command=self.root_dir, variable=self.rootDirBool, onvalue=True, offvalue=False)
        self.rootDir.grid(row=1, column=0, sticky='w', pady=(15,0))

        self.rootDirLabel = ttk.Label(self, text="No folder selected")
        self.rootDirLabel.grid(row=2, column=0, sticky='w')

        self.rootDirLocation = ttk.Button(self, text="Change folder", command=self.update_root_dir)
        self.rootDirLocation.grid(row=2, column=1, sticky='w')

        self.exportRules = ttk.Button(self, text="Export ruleset", command=self.export_rules)
        self.exportRules.grid(row=3, column=0, sticky='w', pady=15)

        self.importRules = ttk.Button(self, text="Import ruleset", command=self.import_rules)
        self.importRules.grid(row=3, column=3, sticky='e', pady=15)

        self.table = Table(self)
        self.table.grid(row=4, column=0, columnspan=4)

    def sub_dirs(self):
        global includeSubfolders
        if self.subDirsBool.get():
            includeSubfolders = True
            log.append("INFO:\tEnabled auto adding sub-directories")
        else:
            includeSubfolders = False
            log.append("INFO:\tDisabled auto adding sub-directories")

    def root_dir(self):
        global enableRootDir
        if self.rootDirBool.get():
            enableRootDir = True
            log.append("INFO:\tEnabled root folder")
        else:
            enableRootDir = False
            log.append("INFO:\tDisabled root folder")

    def update_root_dir(self):
        global rootDirectory
        folderPath = filedialog.askdirectory()

        if folderPath:
            self.rootDirLabel.config(text=folderPath)
            rootDirectory = folderPath

    #TODO
    def export_rules(self):
        files = [('Excel', '*.xlsx')]
        file = filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        # if file:
        #     try:
        #         for msg in log:
        #             file.write(msg+"\n")
        #     except Exception as e:
        #         log.append("Error writing to file:")
        #         log.append(e)
        #     finally:
        #         file.close()
    #TODO
    def import_rules(self):
        files = [('Excel', '*.xlsx'),]
        file = filedialog.askopenfilename(filetypes=files)
        #TODO: convert xlsx to gridif file:
        # this is going to be useful when importing xlsx
        # data = [
        #     ["John", 1, "Pepperoni"],
        #     ["Mary", 2, "Cheese"],
        #     ["Tim", 3, "Mushroom"],
        #     ["Erin", 4, "Ham"],
        #     ["Bob", 5, "Onion"],
        #     ["Steve", 6, "Peppers"],
        #     ["Tina", 7, "Cheese"],
        #     ["Mark", 8, "Supreme"],
        #     ["John", 1, "Pepperoni"],
        #     ["Mary", 2, "Cheese"],
        #     ["Tim", 3, "Mushroom"],
        #     ["Erin", 4, "Ham"],
        #     ["Bob", 5, "Onion"],
        #     ["Steve", 6, "Peppers"],
        #     ["Tina", 7, "Cheese"],
        #     ["Mark", 8, "Supreme"],
        #     ["John", 1, "Pepperoni"],
        #     ["Mary", 2, "Cheese"],
        #     ["Tim", 3, "Mushroom"],
        #     ["Erin", 4, "Ham"],
        #     ["Bob", 5, "Onion"],
        #     ["Steve", 6, "Peppers"],
        #     ["Tina", 7, "Cheese"],
        #     ["Mark", 8, "Supreme"],
        #     ["Ruth", 9, "Vegan"]
        # ]

        # self.rulesTable.tag_configure('white', background="white")

        # 
        # global ruleCount

        # for record in data:
        #     self.rulesTable.insert(parent='', index='end', iid=ruleCount, text="", values=(record[0], record[1], record[2]), tags=('white'))
        #     ruleCount += 1
            
class Table(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Creating the table
        self.rulesTable = ttk.Treeview(self, selectmode="extended", columns=("In this file type", "if the following text appears", "put the file in this folder"), show="headings")
        self.rulesTable.grid(row=0, column=0, sticky="nesw")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.rulesTable.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.rulesTable.configure(yscrollcommand=self.scrollbar.set)

        self.rulesTable.column("#0", width=0, stretch=False)
        self.rulesTable.column("In this file type", anchor='w', width=100)
        self.rulesTable.column("if the following text appears", anchor='w', width=175)
        self.rulesTable.column("put the file in this folder", anchor='w', width=150)

        self.rulesTable.heading("#0", text="", anchor='w')
        self.rulesTable.heading("In this file type", text="In this file type", anchor='w')
        self.rulesTable.heading("if the following text appears", text="if the following text appears", anchor='w')
        self.rulesTable.heading("put the file in this folder", text="put the file in this folder", anchor='w')


        # Creating the inputs section in separate Frame
        self.inputFrame = ttk.Frame(self)
        self.inputFrame.grid(row=1, column=0)

        self.extensionLabel = ttk.Label(self.inputFrame, text="File type")
        self.extensionLabel.grid(row=0, column=0, pady=(15,5), padx=5)

        self.separator1 = ttk.Separator(self.inputFrame, orient='vertical')
        self.separator1.grid(row=0, column=1, rowspan=2, sticky='ns', pady=(20,0))

        self.keywordLabel = ttk.Label(self.inputFrame, text="Text match")
        self.keywordLabel.grid(row=0, column=2, pady=(15,5), padx=5)

        self.separator2 = ttk.Separator(self.inputFrame, orient='vertical')
        self.separator2.grid(row=0, column=3, rowspan=2, sticky='ns', pady=(20,0))

        self.desiredDirectoryLabel = ttk.Label(self.inputFrame, text="Destination folder")
        self.desiredDirectoryLabel.grid(row=0, column=4, columnspan=2, pady=(15,5), padx=5)

        self.extensionString = tk.StringVar(self)
        options = ["All", "All", ".docx", ".pdf"]
        self.extensionDropdown = ttk.OptionMenu(self.inputFrame, self.extensionString, *options)
        self.extensionDropdown.grid(row=1, column=0, padx=(0,5))

        self.keywordInput = ttk.Entry(self.inputFrame)
        self.keywordInput.grid(row=1, column=2, padx=5)

        self.desiredDirectoryInput = ttk.Entry(self.inputFrame)
        self.desiredDirectoryInput.grid(row=1, column=4, padx=5)

        self.desiredDirectoryButton = ttk.Button(self.inputFrame, text="Select folder", command=self.select_dir)
        self.desiredDirectoryButton.grid(row=1, column=5)


        # Creating the button section in separate Frame
        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.grid(row=2, column=0)

        self.updateButton = ttk.Button(self.buttonFrame, text="Update selected rule", command=self.update)
        self.updateButton.grid(row=0, column=0, pady=10, padx=0)

        self.addNewButton = ttk.Button(self.buttonFrame, text="➕ Add rule", command=self.add)
        self.addNewButton.grid(row=0, column=1, pady=10, padx=0)

        self.removeSelectedButton = ttk.Button(self.buttonFrame, text="Remove selected rules", command=self.remove_selected)
        self.removeSelectedButton.grid(row=0, column=3, pady=10, padx=(90,0))


        # Enables clicking on a row -> populating the inputs section
        def select_record():
            self.extensionString.set("All")
            self.keywordInput.delete(0, tk.END)
            self.desiredDirectoryInput.delete(0, tk.END)

            selected = self.rulesTable.focus()
            values = self.rulesTable.item(selected, 'values')

            self.extensionString.set(values[0])
            self.keywordInput.insert(0, values[1])
            self.desiredDirectoryInput.insert(0, values[2])

        def clicker(e):
            select_record()

        self.rulesTable.bind("<ButtonRelease-1>", clicker)

        # Enables esc press -> deselect row
        def deselect_record():
            x = self.rulesTable.selection()
            for record in x:
                self.rulesTable.selection_remove(record)

        def esc(e):
            deselect_record()

        self.rulesTable.bind("<Escape>", esc)

    def select_dir(self):
        folderPath = filedialog.askdirectory()

        if folderPath:
            
            self.desiredDirectoryInput.delete(0, tk.END)
            self.desiredDirectoryInput.insert(tk.END, folderPath)

    def add(self):
        if (not os.path.isdir(self.desiredDirectoryInput.get())):
            if (not self.keywordInput.get()):
                messagebox.showwarning("Warning", "You have not specified a text match\n and the destination folder is invalid.")
            else: 
                messagebox.showwarning("Warning", "Destination folder is invalid.")
        elif (not self.keywordInput.get()):
            messagebox.showwarning("Warning", "You have not specified a text match")
        
        else:
            self.rulesTable.tag_configure('white', background="white")
            global ruleCount
            global ruleID
            
            # adds to dictionary
            if (self.extensionString.get() not in rules):
                rules[self.extensionString.get()] = [[self.keywordInput.get(), self.desiredDirectoryInput.get(), ruleID]]
            else:
                temp = rules.get(self.extensionString.get())
                temp.append([self.keywordInput.get(), self.desiredDirectoryInput.get(), ruleID])
                rules[self.extensionString.get()] = temp
            
            self.rulesTable.insert(parent='', index='end', iid=ruleCount, text=ruleID, values=(self.extensionString.get(), self.keywordInput.get(), self.desiredDirectoryInput.get()), tags=('white'))

            ruleCount += 1
            ruleID += 1

            # Clear the boxes
            self.extensionString.set("All")
            self.keywordInput.delete(0, tk.END)
            self.desiredDirectoryInput.delete(0, tk.END)

    def remove_selected(self):
        global ruleCount
        global rules

        if (ruleCount > 0):
            selection = self.rulesTable.selection()

            for record in selection:
                prevRule = self.rulesTable.item(record)
                ruleset = rules[prevRule['values'][0]]
                id = prevRule['text']

                # removes from dictionary
                for i in range(len(ruleset)):
                    if (ruleset[i][2] == id):
                        ruleset.pop(i)
                        break
                
                # and from treeview
                self.rulesTable.delete(record)
                ruleCount -= 1

    def update(self):
        # Grab record number
        selected = self.rulesTable.focus()
        
        if (not os.path.isdir(self.desiredDirectoryInput.get())):
            if (not self.keywordInput.get()):
                messagebox.showwarning("Warning", "You have not specified a text match\n and the destination folder is invalid.")
            else:
                messagebox.showwarning("Warning", "Destination folder is invalid.")
        elif (not self.keywordInput.get()):
            messagebox.showwarning("Warning", "You have not specified a text match")
        
        else:
            global rules
            global ruleCount

            if (ruleCount > 0):
                prevRule = self.rulesTable.item(selected)
                ruleset = rules[prevRule['values'][0]]
                id = prevRule['text']

                # updates dictionary
                for i in range(len(ruleset)):
                    if (ruleset[i][2] == id):
                        rule = [self.keywordInput.get(), self.desiredDirectoryInput.get(), id]
                        ruleset[i] = rule

                # and treeview
                self.rulesTable.item(selected, text=id, values=(self.extensionString.get(), self.keywordInput.get(), self.desiredDirectoryInput.get()))

                # Clear entry boxes
                self.extensionString.set("All")
                self.keywordInput.delete(0, tk.END)
                self.desiredDirectoryInput.delete(0, tk.END)
######################### End of Options tab logic #########################
        
app = Application()
app.mainloop()