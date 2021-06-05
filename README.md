# nusmods-timetabling
Grabs NUS module details from nusmods api (which grabs it from LumiNUS) and determines which combinations of modules do not result in a clash


## nusmods.py
nusmods.py contains the file to grab timetable schedules of modules to be inputted into timetable.py.

mods_list variable contains a list of modules you could potentially take (In the code provided, there are 8)
the getter() function call in teh for loop after mods_list variable takes in the academic year (20 for AY20/21, 21 for AY21/22 etc), module code and semester (1 for semester 1, 2 for semester 2)

This information is saved as mods1.csv.

## timetable.py
This contains the clashing algorithm.

N_mods variable tells the algorithm how many modules you plan on taking the next semester.

Further selection criteria is provided in the code to allow you to select the maximum number of each level of modules you want to take in the semester.
