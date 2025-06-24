**This is a simple app for sorting files.**
- V2 (current) adds the ability to add rules for sorting
- V1.1 is a GUI addition to V1
- V1 only sorts based on filetype


## Exmaple use case
You have a bunch of .pdf, .txt, and .docx files in a directory. This app will read through your directory and move all the .pdf files in a 'pdf' sub directoy, all the .txt files in a 'txt' sub directory, and all the .docx files in a 'docx' sub directory.

You do not have to provide an explicit list of file types or create the sub directories beforehand. It's smart enough to do that on its own :)

Additionally, you can sort by a file's contents now. The program uses the following stucture for searching & sorting:
- In this file type {x}, if the following text appears {y}, put the file in this folder {z}


## Pre-requisits

Run `pip install -r requirements.txt` to install the libraries that allow the program to read various file types
- If you plan on sorting through the text on images inside pdfs, you also need to install pytorch. Please visit https://pytorch.org/ to see which version is best suited for your hardware.


## How to use the app

Open the FileSorter.pyw app by double-clicking it, or running `python FileSorter.pyw` in a terminal. 
- The app starts off on the "Sort folders" tab. You can add folders you would like to sort, and your list of folders queued up to be sorted will be displayed. Once you finish queuing up all of your folders, you can sort their contents with the button in the bottom right. Once everything's been sorted, you'll get a pop-up notifying you the process finished.
- There is another "Console output" tab, where you can get insight into the app's individual steps. You'll have to use the "Refresh" button at the top to display logs on-screen (automatic refreshing is planned for future release), or simply save the logs to a .txt file with the button in the bottom right.
- There is a third Settings tab represented by a '⚙', where you can mess with various settings.


## Settings

**You can toggle on/off the ability to automatically convert scanned PDFs to text.**\
This feature allows the app to take in images of your PDF files and utilize Convolutional Neural Networks to extract text out of said images via a process called Optical Character Recognition. _This is done on your local machine to avoid exposing personal information to cloud services._ \
Unfortunately, OCR is not perfect. However, it's easier than manually typing out the contents of a pdf.\
That being said, it's also computationally taxing. It's recommended that you don't enable this setting if:
- you're going through a lot of files
- you're going through large files
- you have slower hardware (don't have CUDA cores)
- and/or you don't have a lot of time to let the computer processes the data.

Please make sure you visit https://pytorch.org/ before using this feature. It will tell tell you which versions of pytorch to install for your system's specifications. Otherwise, requirements.txt's installation will default to using your CPU (may result is extremely slow processing times).

**You can toggle on/off the ability to automatically add all child folders when you add a folder to sort through on the "Sort folders" tab**

**You can specify a parent folder to put all your sorted-by-filetype (default sorting method) files into** \
By default, the app creates sub-folders in every folder the app sorts through

**You can export/import your ruleset via .xlsx files.**\
Exporting will take all the rules from the table below and put them into an .xlsx file, which you can add back in later. You can also add rules directly into that exported .xlsx if you prefer\
Importing will take in a properly formatted .xlsx file and fill out the table below. It does some error-checking when importing to make sure everything is compatible:
- It checks if the file type provided in a rule is supported (.pdf, .txt, .docx, .xlsx, or "All" if the rule applies to any of them)
- It checks that the text match field isn't empty
- And it checks that the destination folder exists on your system
  
If any of the errors occur, the app will have a pop-up window explaining the issue and where it's happening.

**You can add rules into the app itself**\
There is a scrollable table that looks somewhat like this (same formatting as the exported/imported .xlsx):

| In this filetype | if the following text appears | put the file in this folder |
|------------------|-------------------------------|-----------------------------|
|                  |                               |                             |
|                  |                               |                             |
|                  |                               |                             |
|                  |                               |                             |
|                  |                               |                             |
|                  |                               |                             |

And an interactable row that has the following components:

|   File type   | Text match |            Destination folder             |
|---------------|------------|-------------------------------------------|
| Dropdown menu | Text input | Text input or Button to open file browser |

There are three ways to interface with the table using the interactable row:
- Update selected rule\
You can select one rule from the table above by clicking on the rule (the table must have at least one entry to do this).\
The rule's information will pre-fill in the interactable row, where you can change the rule based on your needs.\
To apply your changes, you must hit the button below labeled "Update selected rule"
- Add rule\
You can add a new rule to the table by filling out the File type, Text match, and Destination folder in the interactable row.
- Remove selected rule(s)
You can select one or more rule(s) from the above table by clicking on them.\
Shift-clicking and Ctrl-clicking functionality is enabled and works the same as in your file browser.

Whenever you Update or Add a rule, the app also does some error-checking to make sure everything is compatible:
- It checks that the text match field isn't empty
- And it checks that the destination folder exists on your system

If any of the errors occur, the app will have a pop-up window explaining the issue.
