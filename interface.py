"""
A python tool for batch importing excel/csv files into mysql database.
Author: ryjfgjl
Date: 2020-01-05

"""

Version = "V1.1"

print("Initializing program...")

# import GUI model
import easygui
import traceback

# The interface for the program
while True:
    choice = easygui.buttonbox(msg="Make Your Choice", title="Excel Importer {}".format(Version),
                               choices=["Import Excel", "●", "Quit"])

    if choice == "Import Excel":
        try:
            from excelimporter.excelimporter import ImportExcel
            ImportExcel = ImportExcel()
            ImportExcel.main()

        except:
            easygui.exceptionbox()

    elif choice == "Quit":
        break
