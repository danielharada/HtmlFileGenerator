HtmlFileGenerator
=================

GUI to write HTML content, or pick from content saved to a database, then write that content to a file.  Written in Python.  

HTMLGnerationGUI.py will run the GUI and make calls to sqliteAccessors.py and textGridDialog.py, which provide connections to the database and a dialog pop-up to display and select the content stored in the database, respectively.


Prompt:

Scenario: Your company's users are asking for a tool that can automatically create a basic HTML web page.

Your task is to create a GUI that will enable the users to set the body text for this web page. There should also be a control in the GUI that initiates the process of making the new web page.
You should be able to navigate to your newly-created .html page using a browser (Internet Explorer, Chrome, Firefox) and see the resulting web page.

In addition, your managers have asked to have functionality added to the web page creation tool that allows for the storage of pre-made content, and that allows the user to choose from that pre-made content when creating a web page.
This will require modification of the GUI and also the creation of a database that can store the content for later use in creating a web page.

The GUI will need a set of controls for creating new body text, and also a set of controls for fetching all content from the database, displaying that content in a grid, selecting one of the content choices, and using that selection in creating a new web page.

Guidelines:
Use Python 3.x, tKinter, sqlite3 and Visual Studio 2013 for this drill.
