TYPES = {
        's': "obj",
        'i': "int",
        'c': "cat"
    }

data = ["s: First Name, Last Name", "i: Age", "c: Sex|Male|Female"]

info = {}
cat_info = {}

if True:
    for i in data:
        fields = i.split(": ")[-1]
        for j in fields.split(", "):
            if TYPES[i.split(": ")[0]] == "cat":
                cat_info[j.split('|')[0]] = j.split('|')[1:]
                info[j.split('|')[0]] = TYPES[i.split(": ")[0]]
            else:
                info[j] = TYPES[i.split(": ")[0]]
print(info, cat_info)