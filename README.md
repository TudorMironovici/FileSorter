**This is a simple app for sorting files.**
- V1.1 (Current) is a GUI addition to V1
- V1 only sorts based on filetype

**Exmaple:**

You have a bunch of .pdf, .txt, and .docx files in a directory. This app will read through your directory and move all the .pdf files in a 'pdf' sub directoy, all the .txt files in a 'txt' sub directory, and all the .docx files in a 'docx' sub directory.

You do not have to provide an explicit list of file types or create the sub directories beforehand. It's smart enough to do that on its own :)


**How to use the app:**

Open the FileSorter.pyw app by double-clicking it, or running `python FileSorter.pyw` in a terminal. 
- The app starts off on the "Sort folders" tab. You can add folders you would like to sort, and your list of folders queued up to be sorted will be displayed. Once you finish queuing up all of your folders, you can sort their contents with the button in the bottom right. Once everything's been sorted, you'll get a pop-up notifying you the process finished.
- There is another "Console output" tab, where you can get insight into the app's individual steps. You'll have to use the "Refresh" button at the top to display logs on-screen (automatic refreshing is planned for future release), or simply save the logs to a .txt file with the button in the bottom right.