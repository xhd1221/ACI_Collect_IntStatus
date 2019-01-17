
# list of packages that should be imported for this code to work
from pandas import ExcelWriter
from openpyxl import load_workbook
import os


# Export a pandas DataFrame to a excel file
#                 DataFrame, Excel File name, if export DataFrame index
# def to_excel_file(dataframe, file_name, if_index):
# 	writer = ExcelWriter(file_name, engine='xlsxwriter')
# 	dataframe.to_excel(writer, sheet_name=dataframe.name, index=if_index)
# 	writer.save()
# 	writer.close()


# Export a pandas DataFrame to a excel file
#                 DataFrame, Excel File name, if export DataFrame index
def to_excel_file(dataframe, file_name, if_index):
	writer = ExcelWriter(file_name, engine='openpyxl')
	if not os.path.exists(file_name):
		dataframe.to_excel(writer, dataframe.name, index=if_index)
	else:
		writer.book = load_workbook(writer.path)
		dataframe.to_excel(excel_writer=writer, sheet_name=dataframe.name, index=if_index)
	writer.save()
	writer.close()


def format_excel(excel_file):
	pass



