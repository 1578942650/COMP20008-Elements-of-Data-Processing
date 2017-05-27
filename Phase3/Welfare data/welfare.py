from collections import defaultdict as dd
import pandas as pd
def SA2toSA1():
	#this function return a dictionary which help classify
	#SA2 to LGA
	#the value of each key in dicitonary is which LGA it belongs to
	LGA_dd = dd(str)
	LGA_list = []
	file = open("LGAlist.txt", "r")

	LGA_name = ""
	for line in file.readlines():
		if line[:7] == "City of":
			LGA_name = ""
			for char in line:
				if char.isdigit() == True:
					break
				else:
					LGA_name += char
			LGA_name = LGA_name.replace("\n", "")
			LGA_name = LGA_name.replace("City of ", "")

			#special Case:
			if "Brimbank" in line:
				LGA_name = "Brimbank"
			LGA_list.append(LGA_name)
			#LGA_dd[LGA_name] = []
			#print(LGA_name)
		elif line[:8] == "Shire of":
			LGA_name = ""
			for char in line:
				if char.isdigit() == True:
					break
				else:
					LGA_name += char
			LGA_name = LGA_name.replace("\n", "")
			LGA_name = LGA_name.replace("Shire of ", "")
			LGA_list.append(LGA_name)
		else:
			#print("start processing this", LGA_name)
			suburban = ""
			if "3" in line:
				#only tackle LGA that 
				for char in line:
					if char.isdigit() == True or char == "(":
						break
					else:
						suburban += char
				#print("   ", suburban)
				suburban = suburban[:-1]
				LGA_dd[suburban] = LGA_name
	return LGA_dd, LGA_list

def search_key(suburban, LGA_dd):
	#this functio take a suburban as input
	#and return the LGA of it
	#convert to valid data
	if "-" in suburban:
		temp = ""
		for char in suburban:
			if char != '-':
				temp += char
			else:
				break
		suburban = temp[:-1]
	elif "Vic" in suburban:
		suburban = suburban.replace(" (Vic.)", "")
		#All those special case
	if " (West)" in suburban:
		suburban = suburban.replace(" (West)", "")
	if " (East)" in suburban and "Wandin" not in suburban:
		suburban = suburban.replace(" (East)", "")
	if "Racecourse" in suburban:
		suburban = suburban.replace(" Racecourse", "")
	if "Industrial" in suburban:
		suburban = suburban.replace(" Industrial", "")


	#return key
	if suburban in LGA_dd.keys():
		return LGA_dd[suburban]

	if suburban == "Yarra":
		#return the LGA name
		return "Yarra"


def merge_welfare(filename, LGA_dd, LGA_list):
	welfare = pd.read_csv(filename)
	columns = welfare.columns
	welfare.replace("null", 0, inplace = True)
	welfare.replace("#VALUE!", 0, inplace = True)
	welfareT = welfare.T
	welfareT.columns = welfare[welfare.columns[0]]
	welfareT.drop("SAL2 Name", axis = 0, inplace = True)

	LGA_df = pd.DataFrame(columns = columns[1:])
	LGA_df.insert(0, "LGA", LGA_list)
	LGA_df = LGA_df.T
	LGA_df.columns = LGA_list
	LGA_df.drop("LGA", axis = 0, inplace = True)
	LGA_df.fillna(0, inplace = True)

	#there are two clayton south in Dataframe, this variable is to solve this duplicat column
	duplicate_solved = 0
	for suburban in list(welfare[welfare.columns[0]]):
		LGA = search_key(suburban, LGA_dd)
		if LGA != None:
			try:
				LGA_df[LGA] = LGA_df[LGA].add(welfareT[suburban].astype(float))
			except:
				if duplicate_solved == 0:
					print("fail", LGA, suburban, duplicate_solved)
					temp_df = pd.DataFrame(welfareT[suburban])
					temp_df.columns = ["A","B"]
					LGA_df[LGA] = LGA_df[LGA].add(temp_df["A"].astype(float))
					LGA_df[LGA] = LGA_df[LGA].add(temp_df["B"].astype(float))
					duplicate_solved = 1
				pass
	
	LGA_df = LGA_df.T
	for i in range(len(LGA_list)):
		LGA_list[i] += " "
	LGA_df.insert(0, "LGA", LGA_list)
	LGA_df.to_csv("welfare.csv")

		







LGA_dd, LGA_list = SA2toSA1()

merge_welfare("Needed Data.csv", LGA_dd, LGA_list)