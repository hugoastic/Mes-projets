# Créé par Hugo, le 03/04/2022 en Python 3.7
import os
with open("min en degrés.txt", "r") as file:
    newline_break =[]
    for readline in file:
        line_strip = readline.strip()
        newline_break.append(line_strip)
    print(newline_break)
with open("min en degrés.txt", "w") as file:
    for i in newline_break:
        a=float(i)
        c=(a-32) * 5.0 / 9.0
        e=round(c,2)
        d=str(e)
        file.write(d)
        file.write("\n")


