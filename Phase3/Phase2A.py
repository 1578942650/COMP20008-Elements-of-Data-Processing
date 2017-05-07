import os
def extract_filename(path):
	return os.listdir(path)

path = "c:/Users/Administrator/OneDrive/UNIMELB/COMP20008/Phase2A/dataset"
name = extract_filename(path)
print(name)
