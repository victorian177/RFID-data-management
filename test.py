import pandas

d = {
    "first": ["Victor", "Jill", "Parker"],
    "last": ["Gerson", "Patterson", "Bridgerton"],
    "id": ["A12", "B30", "C49"],
}
a = pandas.DataFrame(d)
a.set_index('id', inplace=True)
a.drop(index="A12", inplace=True)

print(a)