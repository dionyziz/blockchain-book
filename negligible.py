import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(0.0, 20.0, 0.01)
s = np.exp(-t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='problem size (n)', ylabel='probability of success (0 <= Pr <= 1)',
       title='Negligible probability of success')
ax.grid()

plt.show()
