s = "doc1: dasha, doc2: sveta, doc3: vitalic"
start = 0
substrings_index_list = []
sub_index = 1

while sub_index != -1:
    sub_index = s.find("doc", start)
    start = sub_index + 3
    if sub_index != -1:
        substrings_index_list.append(sub_index)

print(substrings_index_list)

sp = s.split("doc")
print(sp)