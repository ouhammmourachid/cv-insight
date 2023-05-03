import openpyxl
import os
def data_to_xlsx(data):
    filename='business_layer/Documents/cv_infos.xlsx'
    if os.path.exists(filename):
        os.remove(filename)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    for row in data:
        worksheet.append(row)
    workbook.save(filename)