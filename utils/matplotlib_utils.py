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

xpoints = [0, 50, 6]
ypoints = [0, 50, 250]

plt.scatter(xpoints, ypoints, edgecolors='hotpink', color = '#88c999')

plt.show()