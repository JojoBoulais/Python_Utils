import matplotlib.pyplot as plt
import numpy as np


# lines
# xpoints = [0, 6]
# ypoints = [0, 50, 250]
#
# plt.subplot(1, 2, 1)
# plt.plot(ypoints, marker = 'o', linestyle = 'dotted')
#
# plt.subplot(1, 3, 3)
# plt.plot(xpoints, marker = 'o', linestyle = 'dotted')
# plt.show()


# scatter
# importing package
import matplotlib.pyplot as plt

# # create data
# x = [10, 100, 200, 500, 1000,2000 ,5000 ,10000, 20000, 50000, 100000]
# y = [43200, 804000, 1621000, 5864900, 7441000,13795400 ,37863000 ,144127100, 431224600, 3800652600, 29687963400]
#
# plt.plot(x, y, label="Tri par insertion", color="red")
#
#
# v = [10, 100, 200, 500, 1000,2000 ,5000 ,10000, 20000, 50000, 100000]
# w = [56800, 200300, 325700, 800500, 1663200,3406600 ,5903800 ,8821800, 14870400, 49673300, 84402700]
#
#
# plt.plot(v, w, label="Tri par fusion", color="blue")
# #
# #
# a = [10, 100, 200, 500, 1000,2000 ,5000 ,10000, 20000, 50000, 100000]
# b = [253500, 361000, 415300, 917900, 1342000,2454400 ,5593000 ,7645900, 8519300, 16683000, 36231600]
#
#
# plt.plot(a, b, label="Collections.sort()", color="orange")








# create data
x = [10, 100, 200, 500, 1000,2000 ,5000]
y = [43200, 804000, 1621000, 5864900, 7441000,13795400 ,37863000]

plt.plot(x, y, label="Tri par insertion", color="red")


v = [10, 100, 200, 500, 1000,2000 ,5000]
w = [56800, 200300, 325700, 800500, 1663200,3406600 ,5903800]


plt.plot(v, w, label="Tri par fusion", color="blue")
#
#
# a = [10, 100, 200, 500, 1000,2000 ,5000]
# b = [253500, 361000, 415300, 917900, 1342000,2454400 ,5593000]
#
#
# plt.plot(a, b, label="Collections.sort()", color="orange")




plt.legend()
plt.xlabel('Taille du probleme')
plt.ylabel("Temps d'execution (nano sec.)")
plt.show()