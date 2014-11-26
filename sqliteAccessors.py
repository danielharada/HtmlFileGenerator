import sqlite3

db_name = 'HTMLContent.db'
table_name = 'webPageContent'

def connectionAndTableDecorator(function):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        table_create_query = "CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY, Content TEXT NOT NULL, Name TEXT);".format(table_name)
        cursor.execute(table_create_query)

        return_value = function(cursor, *args, **kwargs)

        connection.commit()
        connection.close()
        return return_value

    return wrapper

@connectionAndTableDecorator
def queryAll(cursor):
    query = 'SELECT * FROM {};'.format(table_name)
    query_results = cursor.execute(query)
    results_list = convertSQLResultsToList(query_results)
    
    return results_list

def convertSQLResultsToList(query_results):
    results_list = []
    for item in query_results:
        results_list.append(item)

    return results_list

@connectionAndTableDecorator
def queryContent(cursor, row_ID):
    query = 'SELECT Content FROM {} WHERE ID = {};'.format(table_name, row_ID)
    query_results = cursor.execute(query)
    content = convertSQLResultsToList(query_results)[0][0]

    return content

@connectionAndTableDecorator
def insertItem(cursor, content, name):
    insert = 'INSERT INTO {} (Content, Name) VALUES (?,?);'.format(table_name)
    values = (content, name)
    cursor.execute(insert, values)

def connectionOnlyDecorator(function, *args, **kwargs):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        function(cursor, *args, **kwargs)

        connection.commit()
        connection.close()

    return wrapper

@connectionOnlyDecorator
def dropTable(cursor, table_name):
    drop_table_query = "DROP TABLE IF EXISTS {};".format(table_name)
    cursor.execute(drop_table_query)

if __name__ == '__main__':
    #dropTable(table_name)
    
    #insertItem('Here is some conent', 'Item number 1')
    #insertItem('This is the content column', 'Item number 2')
    #insertItem('This record has None in the name', None)
    
    #query_results = queryAll()
    #print(type(query_results))
    #print(query_results)

    content = queryContent(1)
    print(type(content))
    #print(content)
    


