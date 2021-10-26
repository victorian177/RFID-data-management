import purpose

infrmtn = {'f_name': "obj", 'l_name': "obj", 'sex': "cat", 'position': "obj"}
cat_inf = {"sex": ['male', "female"]}

office = purpose.Access('office')
# persons = [
#     ["A18", "059849", "Jason", "Sudeikis", "male", "Lead Actor"],
#     ["B02", "330939", "Hannah", "Waddingham", "female", "Supporting Actor"],
#     ["C30", "347863", "Jeremy", "Swift", "male", "Supporting Actor"],
#     ["D49", "489235", "Sarah", "Niles", "female", "Supporting Actor"],
#     ["E45", "053849", "Toheeb", "Jimoh", "male", "Guest Actor"],
#     ["F76", "637833", "Stephanie", "Manas", "female", "Extra Actor"]
#     ]
# for i in persons:
#     office.register(i)

office.remove("A18")
office.access_editor("B02")