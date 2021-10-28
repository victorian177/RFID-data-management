# import os
import purpose

infrmtn = {'f_name': "obj", 'l_name': "obj", 'sex': "cat", 'position': "obj"}
cat_inf = {"sex": ['male', "female"]}

persons = [
    ["A18", "059849", "Jason", "Sudeikis", "male", "Lead Actor"],
    ["B02", "330939", "Hannah", "Waddingham", "female", "Supporting Actor"],
    ["C30", "347863", "Jeremy", "Swift", "male", "Supporting Actor"],
    ["D49", "489235", "Sarah", "Niles", "female", "Supporting Actor"],
    ["E45", "053849", "Toheeb", "Jimoh", "male", "Guest Actor"],
    ["F76", "637833", "Stephanie", "Manas", "female", "Extra Actor"]
    ]

office = purpose.Access('office')
for i in persons:
    office.register(i)

office.remove("A18")
office.access_editor("B02")

school = purpose.Attendance("school")
for i in persons:
    school.register(i)

for i in persons:
    school.attendance_logger(i[0])

centre = purpose.Record("centre", infrmtn, cat_inf)
for i in persons:
    centre.register(i)

for i in persons:
    centre.record_editor(i[0], "Just testing this out if this works")

