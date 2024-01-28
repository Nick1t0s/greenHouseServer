def g01():
    return random.randint(0,1)
def f12():
    return random.randint(200,600)
def gt():
    return random.randint(10,30)
def gh():
    return random.randint(50,80)
import random
i=15
k=500
for i in range(i,i+k+1):
    with open(f"C:\\my3\\{str(i)}.txt","w") as file:
        data=f"{i};1;'2008-10-23 10:37:22';{g01()};{g01()};{g01()};{g01()};{gt()};{gh()};{gt()};{gh()};{f12()};{f12()};{f12()}"
        file.write(data)