import os
import xlrd
import pandas as pd

def extract_filename():
  path = os.getcwd() + '\dataset\Community Profile'
  return os.listdir(path)

def read_excel_file(filename):
    name = "./dataset/Community Profile/" + filename
    return xlrd.open_workbook(name)

def extract_LGA_name(workbook):
   worksheet = workbook.sheet_by_name('Cover')
   LGA = worksheet.cell(8,1).value
   LGAname = ""
   for char in LGA:
       LGAname += char
       if char == "(":
           break
   LGAname = LGAname[:-1]
   return LGAname

def extract_income_column(workbook):
	worksheet = workbook.sheet_by_name('B 17b')
	column = []
	for row in range(12, 23):
		column.append(worksheet.cell(row, 10).value)

	#append person that not stated
	column.append(worksheet.cell(24, 10).value)

	#append total female
	column.append(worksheet.cell(26, 10).value)
	return column

def extract_children_row(workbook):
	worksheet = workbook.sheet_by_name('B 24')
	row = []
	for column in range(1,10):
		row.append(worksheet.cell(28, column).value)
	return row




filelist = extract_filename()

i = 0
children_rows = []
income_rows = []
for filename in filelist:
	workbook = read_excel_file(filename)
	LGA = extract_LGA_name(workbook)
	income_row = [LGA] + extract_income_column(workbook)
	children_row = [LGA] + extract_children_row(workbook)
	children_rows.append(children_row)
	income_rows.append(income_row)


mother_by_children = pd.DataFrame(children_rows,
	columns = ("LGA(Number of Children)","0", "1", "2", "3", "4", "5", "6+", 
				"Not Stated", "Total"))


female_by_income_level = pd.DataFrame(income_rows,
	columns = ("LGA(income level)", "Negative/0", "$1-$199", "$200-$299","$300-$399",
		"$400-$599","$600-$799","$800-$999","$1,000-$1,249",
		"$1,250-$1,499", "$1,500-$1,999","$2,000+", "Not Stated",
		"Total"))

mother_by_children.to_csv("mother_by_children.csv")
female_by_income_level.to_csv("people_by_income_level.csv")