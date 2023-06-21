list=["tony","ah","sf","tony"]
print(list)


result = []

[result.append(x) for x in list if x not in result]

print(result)