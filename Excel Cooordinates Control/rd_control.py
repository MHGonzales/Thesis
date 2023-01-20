import openpyxl
  
# Opening an excel file
wb_obj = openpyxl.load_workbook('coordinates_py.xlsx')
 
# Get workbook active sheet object
# from the active attribute
sheet_obj = wb_obj.active
 
# Cell objects also have a row, column,
# and coordinate attributes that provide
# location information for the cell.
 
# Note: The first row or
# column integer is 1, not 0.
 
# Cell object is created by using
# sheet object's cell() method.
cell_obj = sheet_obj.cell(row = 1, column = 1)
 
# Print value of cell object
# using the value attribute
print(cell_obj.value)
