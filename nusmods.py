import requests
import csv

def convert(letter):
	if letter == 'Tu':
		return 'Tutorial'
	elif letter == 'La':
		return 'Tutorial'
	elif letter == 'Le':
		return 'Lecture'

def checker(class_row):
	#print(class_row)
	for combi_row in class_row:
		module_name = combi_row[0]
		first = combi_row[1:4]
		second = combi_row[4:7]
		third = combi_row[7:10]
		fourth = combi_row[10:13]
		if first == second:
			combi_row[4:7] = [0, 0, 0]

		if first == third:
			combi_row[7:10] = [0, 0, 0]
		if first == fourth:
			combi_row[10:13] = [0, 0, 0]

		if second == third:
			combi_row[7:10] = [0, 0, 0]
		if second == fourth:
			combi_row[10:13] = [0, 0, 0]
		if third == fourth:
			combi_row[10:13] = [0, 0, 0]
	return class_row

def getter(AY,module_code,semester):
	response = requests.get(f'https://api.nusmods.com/v2/20{AY}-20{AY+1}/modules/{module_code}.json')

	text = response.text

	#print(text)

	index_sD = text.find('semesterData')
	index_prereq = text.find("prereqTree")


	filtered_text = text[index_sD+15:index_prereq]
	#print(filtered_text)

	sem_index = filtered_text.find(f'"semester":{semester}')

	sem_filtered_text = (filtered_text[sem_index:])

	#print(sem_filtered_text)

	n_classes = sem_filtered_text.count('classNo') 
	classes_dict = {'Lecture':[], 'Tutorial':[], 'Laboratory':[]}

	day_dict = {'Monday':1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4,'Friday':5}

	while n_classes > 0:
		start_index = sem_filtered_text.find('"startTime":"')
		start_time = sem_filtered_text[start_index+13:start_index+15]

		end_index = sem_filtered_text.find('"endTime":"')
		end_time = sem_filtered_text[end_index+11:end_index+13]

		temp_text = sem_filtered_text[end_index+13:]

		day_index = temp_text.find('"day":')
		temp_text = temp_text[day_index:]
		comma_index = temp_text.find(',')
		temp_text = temp_text[:comma_index-1]
		day_text = temp_text[7:]
		day_num = day_dict[day_text]

		#print('\n')
		#print(sem_filtered_text)

		lessonType_index = sem_filtered_text.find('"lessonType":"')


		letter = sem_filtered_text[lessonType_index+14:lessonType_index+16]
		lessonType = convert(letter)

		classes_dict[lessonType].append([day_num,start_time,end_time])

		sem_filtered_text = sem_filtered_text[lessonType_index+14:]
		n_classes -= 1

	#print(classes_dict)
	#print(len(classes_dict['Tutorial']))

	class_row = []
	

	if len(classes_dict['Tutorial']) < 1:
		ael = [module_code]
		for lecture in classes_dict['Lecture']:
			for i in lecture:
				ael.append(i)

		while len(ael) < 13:
			ael.append(0)

		class_row.append(ael)
		return checker(class_row)

	else:

		ael = [module_code]
		for lecture in classes_dict['Lecture']:
			for i in lecture:
				ael.append(i)

		for tut in classes_dict['Tutorial']:
			aelc = ael.copy()
			for j in tut:
				aelc.append(j)
			while len(aelc) < 13:
				aelc.append(0)
			class_row.append(aelc)

		return checker(class_row)

mods_list = ['LSM3234','COS2000','LSM2241','LSM4227','LSM3233','LSM3235','LSM3227','LSM4243']
rows = []
for mod in mods_list:
	for row in getter(20,mod,1):
		rows.append(row)
		#print(row)

temp_row = []

for row in rows:
	if row not in temp_row:
		temp_row.append(row)

rows = temp_row

#print(rows)


#print(rows)

with open('mods1.csv', mode = 'w', newline='\n') as file:
	Fwriter = csv.writer(file, delimiter=',')
	Fwriter.writerow(['module,day1,start1,end1,day2,start2,end2,day3,start3,end3,day4,start4,end4'])
	for mod in rows:
		print(mod)
		Fwriter.writerow(mod)
