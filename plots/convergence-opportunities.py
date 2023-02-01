import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

plt.rcParams['text.latex.preamble'] = r"\usepackage{lmodern}"

rc('text', usetex=True)
rc(
    'font',
    family='serif',
    serif=['Computer Modern Roman'],
    monospace=['Computer Modern Typewriter'],
    size=25
)

n = 10
t = 2
q = 100
p = np.arange(0.0, 1.0, 0.01)
f = 1 - (1 - p)**((n - t) * p)
conv_opp = f - f**2

fig, ax = plt.subplots()
ax.plot(n * p * q, conv_opp)

ax.set(xlabel='$npq$', ylabel='\# of convergence opportunities per unit of time',
       title='Parametrizations for block generation rate')
ax.grid()

fig.savefig("conv-opp.pdf")
plt.show()
