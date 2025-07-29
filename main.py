tuple_list = {(2,5), (6,89)}
max_list = max(item for tup in tuple_list for item in tup)
print(max_list)