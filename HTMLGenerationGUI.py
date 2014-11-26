import tkinter
from tkinter import ttk
from tkinter import filedialog
import textGridDialog
import sqliteAccessors as sql

def main():
    root = tkinter.Tk()
    root.title('HTML Page Generator')    

    main_frame = ttk.Frame(root)

    directory_input = ttk.Entry(main_frame)
    filename_input = ttk.Entry(main_frame)
    body_text_frame = ttk.Frame(main_frame)
    body_text_input = tkinter.Text(body_text_frame)
    inputs = (directory_input, filename_input, body_text_input)

    default_html = "<html>\n\n<body>\n\n</body>\n\n</html>"
    body_text_input.insert('1.0', default_html)

    main_frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    placeBodyTextWidgets(main_frame,body_text_frame, body_text_input)
    placeContentSaveRetrieveWidgets(main_frame, root, body_text_input)
    placeDirectoryWidgets(main_frame, directory_input)
    placeFilenameWidgets(main_frame, filename_input)
    placeGenerateButton(main_frame, inputs)
    defineWidgetSpacing(main_frame, body_text_frame)

    tkinter.mainloop()

def placeBodyTextWidgets(parent_frame, body_text_frame, body_text_input):
    body_text_label = ttk.Label(parent_frame, text='Please enter HTML code here:').grid(column=0, row=0, columnspan=3)
    vertical_scrollbar = tkinter.Scrollbar(body_text_frame, orient=tkinter.VERTICAL)
    body_text_input.config(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.config(command=body_text_input.yview)
    body_text_input.pack(side='left', fill=tkinter.BOTH, expand=tkinter.YES)
    vertical_scrollbar.pack(side='right', fill='y')
    body_text_frame.grid(column=0, row=1, columnspan=3)

def placeContentSaveRetrieveWidgets(parent_frame, root, body_text_input):
    ttk.Button(parent_frame, text='Save content',\
        command=lambda: saveContentToDatabase(body_text_input, content_name_input)).grid(column=0, row=2)
    
    content_name_input = ttk.Entry(parent_frame)
    ttk.Label(parent_frame, text='Optional content name: ').grid(column=0, row=2, columnspan=2)
    content_name_input.grid(column=1, row=2, columnspan=2)

    ttk.Button(parent_frame, text='Get content',\
        command=lambda: insertContentFromDatabase(root, body_text_input)).grid(column=2, row=2)

def placeDirectoryWidgets(parent_frame, directory_input):
    ttk.Label(parent_frame, text='Please enter directory to store HTML file:').grid(column=0, row=4)
    directory_input.grid(column=1, row=4, sticky=(tkinter.W, tkinter.E))
    ttk.Button(parent_frame, text='Browse', command=lambda: setDirectoryBox(directory_input)).grid(column=2, row=4)

    return directory_input

def placeFilenameWidgets(parent_frame, filename_input):
    ttk.Label(parent_frame, text='Please enter the file name:').grid(column=0, row=5)
    filename_input.grid(column=1, row=5, sticky=(tkinter.W, tkinter.E))
    ttk.Label(parent_frame, text='File extension MUST be included in file name').grid(column=1, row=6)

def defineWidgetSpacing(parent_frame, body_text_frame):
    for child in parent_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    body_text_frame.grid_configure(padx=20)

def placeGenerateButton(parent_frame, inputs):
    directory_input, filename_input, body_text_input = inputs
    generate_html_button = ttk.Button(parent_frame, text='Generate HTML File',\
       command=lambda: generateHTML(directory_input, filename_input, body_text_input))
    generate_html_button.grid(column=0, row=7, columnspan=3)

def saveContentToDatabase(body_text_input, content_name_input):
    content = body_text_input.get('1.0', tkinter.END)
    content_name = content_name_input.get()
    sql.insertItem(content, content_name)

def insertContentFromDatabase(root, body_text_input):
    content = getContentFromDatabase(root)
    if content is not None:
        body_text_input.delete('1.0', tkinter.END)
        body_text_input.insert('1.0', content)

def getContentFromDatabase(root):
    row_ID = textGridDialog.contentChoiceDialog(root)
    if row_ID is not None:
        content = sql.queryContent(row_ID)
    else:
        content = None
    
    return content

def setDirectoryBox(directory_input):
    directory = filedialog.askdirectory()
    directory_input.delete('0', tkinter.END)
    directory_input.insert('0', directory)

def generateHTML(directory_input, filename_input, body_text_input):
    directory = directory_input.get()
    filename = filename_input.get()
    body_text = body_text_input.get('1.0', tkinter.END)

    path = createPath(directory, filename)

    writeToFile(path, body_text)

def createPath(directory, filename):
    if directory[-1] == '/':
        path = directory+filename
    else:
        path = directory+'/'+filename
    return path

def writeToFile(path, data_to_write):
    file=open(path, 'w')
    file.write(data_to_write)
    file.close()


if __name__ == '__main__':
    main()