with open("rpl.txt") as file:
    x=file.read().replace("Buttoff","Button")
with open("rpl.txt", "w") as file:
    file.write(x)