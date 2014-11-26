import tkinter
from tkinter import filedialog
from tkinter import ttk
import sqliteAccessors as sql

def waitWindowDecorator(function):
    def wrapper(parent):
        parent.wait_window(function(parent))
    return wrapper


def contentChoiceDialog(parent):
    root = tkinter.Toplevel(parent)
    root.title('Content Selection')  
    global radio_result
    radio_result = tkinter.IntVar()
    number_of_columns = 3
    canvas_width = 220 * number_of_columns #Text box width + 2*padx
    canvas_height = 220 * 2 + 20 #(Text box height + 2*pady) * number of rows to display +20 pixels for submit button
    canvas_size = (canvas_width, canvas_height)
    content_choice = {'result' : None}

    root.grab_set()
    root.focus_set()
      
    main_frame = createMainFrame(root, canvas_size)

    query_results = sql.queryAll()
    
    my_list = makeListOfTextObjects(main_frame, query_results)
    createTextGrid(my_list, number_of_columns)
    addButtons(main_frame, number_of_columns, content_choice, root)

    root.bind("<Return>", lambda event: chooseContent(content_choice, root))
    root.bind("<Escape>", lambda event: cancelChoice(content_choice, root))

    tkinter.mainloop()

    return content_choice['result']

def createMainFrame(root, canvas_size):
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    return createScrollableFrame(main_frame, canvas_size) 
 
def createScrollableFrame(parent_frame, canvas_size):
    canvas = createScrollableCanvas(parent_frame, canvas_size)
    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0,0), window=scrollable_frame, anchor=tkinter.NW)
    scrollable_frame.bind('<Configure>', lambda event: frameConfigure(canvas))

    return scrollable_frame

def createScrollableCanvas(parent_frame, canvas_size):
    canvas_width, canvas_height = canvas_size
    canvas = tkinter.Canvas(parent_frame, width=canvas_width, height=canvas_height)
    vertical_scrollbar = tkinter.Scrollbar(parent_frame, orient=tkinter.VERTICAL)
    canvas.config(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.config(command=canvas.yview)
    canvas.pack(side='left', fill=tkinter.BOTH, expand=tkinter.YES)
    vertical_scrollbar.pack(side='right', fill='y')

    return canvas

def frameConfigure(scrollable_canvas):
    scrollable_canvas.configure(scrollregion=scrollable_canvas.bbox('all'))

def makeListOfTextObjects(parent_frame, sql_results_list):
    list_length = len(sql_results_list)
    text_object_list = []
    for i in range(0, list_length):
        sql_record = sql_results_list[i]
        text_frame = createFramedTextBoxWithRadio(parent_frame, sql_record)
        text_object_list.append(text_frame)

    return text_object_list

def createFramedTextBoxWithRadio(parent_frame, sql_record):
    record_ID, record_content, record_name = unpackSQLRecord(sql_record)
    text_frame = createTextFrame(parent_frame)
    createScrolledTextBox(text_frame, record_content)
    addRadioButton(text_frame, record_ID, record_name)
    return text_frame

def addRadioButton(parent_frame, record_ID, record_name):
    radio_display_text = str(record_ID) + ': ' + record_name
    radio_button = tkinter.Radiobutton(parent_frame, text=radio_display_text, value=record_ID, variable=radio_result)
    radio_button.grid(row=1, column=0, sticky=tkinter.W)
    if record_ID == 1:
        radio_button.invoke()

def unpackSQLRecord(sql_record):
    record = {}
    record['ID'], record['content'], record['name'] = sql_record
    for key in record:
        if record[key] is None:
            record[key] = ''

    return (record['ID'], record['content'], record['name'])


def createTextFrame(parent_frame):
    text_frame = ttk.Frame(parent_frame, width=200, height=200)
    text_frame.grid_propagate(False)
    text_frame.columnconfigure(0, weight=1)
    text_frame.rowconfigure(0, weight=1)

    return text_frame

def createScrolledTextBox(parent_frame, content):
    text_box = tkinter.Text(parent_frame)
    text_box.insert('1.0', content)
    text_box.config(state=tkinter.DISABLED)
    vertical_scrollbar = tkinter.Scrollbar(parent_frame, orient=tkinter.VERTICAL)
    text_box.config(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.config(command=text_box.yview)
    text_box.grid(row=0, column=0)
    vertical_scrollbar.grid(row=0, column=1, sticky=(tkinter.N, tkinter.S))

def createTextGrid(list_of_objects, number_of_columns):
    for i in range(0, len(list_of_objects), number_of_columns):
        createRow(list_of_objects, i, number_of_columns)

def createRow(list_of_objects, start_index, number_of_columns):
    row_number = int(start_index/number_of_columns)
    for j in range(start_index, start_index + number_of_columns):
        column_number = j % number_of_columns
        try:
            list_of_objects[j].grid(column=column_number, row=row_number, padx=10, pady=10)
        except IndexError:
            break

def addButtons(parent_frame, number_of_columns, content_choice, root):
    button_frame = ttk.Frame(parent_frame)
    button_frame.propagate(False)
    tkinter.Button(button_frame, text='Submit selection',\
        command=lambda: chooseContent(content_choice, root)).grid(row=0, column=0, padx=5)
    tkinter.Button(button_frame, text='Cancel',\
        command=lambda: cancelChoice(content_choice, root)).grid(row=0, column=1, padx=5)
    button_frame.grid(columnspan=number_of_columns)
    #button_frame.pack()

def chooseContent(content_choice, root):
    content_choice['result'] = radio_result.get()
    closeWindow(root)

def cancelChoice(content_choice, root):
    content_choice['result'] = None
    closeWindow(root)

def closeWindow(root):
    root.withdraw()
    root.update_idletasks()
    root.quit()
    root.destroy()


if __name__ == '__main__':
    root = tkinter.Tk()
    contentChoiceDialog(root)
    tkinter.mainloop()