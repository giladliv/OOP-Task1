import os

import pandas as pd

column_names = ["str", "dt", "src", "dst", "state", "alc"]
df = pd.read_csv("input\\calls\\Calls_a_2.csv", names=column_names)

print(df)

counter = 0

def allOpBin(df, arr, count, max):
    if (max == count):
        global counter
        name = "outT\\test_" + str(counter) + ".csv"
        df.to_csv(name, index=False, header=None)
        counter += 1

        return
    for i in arr:
        df["alc"][count] = i
        allOpBin(df, arr, count+1, max)

#java -jar Ex1_checker_V1.2_obf.jar 1111,2222,3333 B2.json Ex1_Calls_case_2_b.csv out.log

#allOpBin(df, [0,1], 0, 10)
end = []
for i in range(1024):
    st = str(i)
    with open("out\\out_" + st +".log") as f:
       lines = f.readlines()
       end.append(lines[len(lines) - 1] + "\t(" + st + ")")


    # os.system(
    #    "java -jar Ex1_checker_V1.2_obf.jar 1111,2222,3333 input\\building\\B3.json outT\\test_" + st + ".csv out\\out_" + st +".log > t.txt")

end.sort()
print(end[0])
print(end[1])
print(end[2])