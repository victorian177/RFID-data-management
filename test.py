# import pandas

# d = {
#     "first": ["Victor", "Jill", "Parker"],
#     "last": ["Gerson", "Patterson", "Bridgerton"],
#     "id": ["A12", "B30", "C49"],
# }
# a = pandas.DataFrame(d)
# a.set_index('id', inplace=True)
# a.drop(index="A12", inplace=True)

# # print(a)
# # s: First Name, Last Name
# # i: Age
# # c: Sex|Male|Female
# # server storage warehouse floor office powerhouse

a = "Hello, my name is Victor Momodu. I am currently a student at Obafemi Awolowo University, Ile-Ife, Nigeria. I am in my second year, studying Electrical and Electronics Engineering. My only source of income is from my parents and occasionally jobs I get. This coupled with the economic hardships in my country has made my income barely enough to handle all my essential expenses thus, paying for this course would be very challenging indeed. The course's cost is very well justified given the immense benefits it offers to everyone who has partaken in it seen by its 4.8-star ratings. Had I the financial ability to afford it, it would be a no-brainer purchase, I am certain I would not regret it the slightest bit. This, unfortunately, is not the case and thus, getting Financial Aid will help me improve both my skill set and resume, both of which I hope to apply to good use. Thanks in advance."
print(len(a.split()))