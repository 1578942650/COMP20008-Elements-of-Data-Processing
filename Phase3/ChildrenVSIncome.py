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

def extract_multichildren_number(workbook):
  worksheet = workbook.sheet_by_name('B 24')
  
  total_number = 0

  for column in range(4, 8):
    total_number += worksheet.cell(28, column).value

  return total_number

def exrtract_total_family_number(workbook):
  worksheet = workbook.sheet_by_name('B 24')
  total_family_reported = worksheet.cell(28,9).value - worksheet.cell(28,8).value
  return total_family_reported

def extract_high_income_people(workbook):
  worksheet = workbook.sheet_by_name('B 17b')

  total_high_income_female = 0

  for row in range(21,23):
    total_high_income_female += worksheet.cell(row, 10).value
  return total_high_income_female

def extract_low_income_people(workbook):
  worksheet = workbook.sheet_by_name('B 17b')

  total_low_income_female = 0

  for row in range(12,22):
    total_low_income_female += worksheet.cell(row, 10).value

  return total_low_income_female

def exrtract_total_income_people(workbook):
  worksheet = workbook.sheet_by_name('B 17b')
  total_female = worksheet.cell(26,10).value - worksheet.cell(26,9).value
  return total_female



not_in_Greater_melbourne = ["Ballarat", "Greater Bendigo","Greater Geelong",
"Greater Shepparton", "Latrobe", "Warrnambool"]
#implement of function
filelist = extract_filename()

name_list = []
high_income = []
low_income = []
children_number = []
total_incomer = []
total_mother = []

ChildrenVsIncome = pd.DataFrame()

for filename in filelist:
    #basics data extract
    workbook = read_excel_file(filename)

    #exclude region that is not in greater melbourne
    name = extract_LGA_name(workbook)[:-1]
    if name in not_in_Greater_melbourne:
      print(name, filename)
    else:
      name_list.append(extract_LGA_name(workbook))
      children_number.append(extract_multichildren_number(workbook))
      high_income.append(extract_high_income_people(workbook))
      low_income.append(extract_low_income_people(workbook))
      total_mother.append(exrtract_total_family_number(workbook))
      total_incomer.append(exrtract_total_income_people(workbook))

ChildrenVsIncome.insert(0, "LGA", name_list)
ChildrenVsIncome.insert(1, "female born >=3 children", children_number)
ChildrenVsIncome.insert(2, "Income >= 1500/week", high_income)
ChildrenVsIncome.insert(3, "Income < 1500/week", low_income)
ChildrenVsIncome.insert(4, "Total mother", total_mother)
ChildrenVsIncome.insert(5, "Total worker", total_incomer)
ChildrenVsIncome.to_csv("ChildrenVsIncome.csv")