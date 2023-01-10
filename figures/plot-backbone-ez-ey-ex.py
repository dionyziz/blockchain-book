import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.stats import poisson, binom

plt.rcParams.update({
  'font.size': 14,
  'text.usetex': True,
  'text.latex.preamble': r'\usepackage{lmodern}\usepackage{amsfonts}'
})

binomial_n = 5000

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14, 5))
poisson_lambda = 50
binomial_p = poisson_lambda / binomial_n
min_x = 30
max_x = 120

exp_Z = poisson_lambda
exp_Y = poisson_lambda + 37
exp_X = poisson_lambda + 45
abs_epsilon = 25//3

x = np.arange(min_x, max_x, 1)
ax.set_xlabel('Number of successes in $|S| \geq \lambda$ rounds')
ax.set_ylabel('Probability')
ax.set_title('')

x_labels = {
  exp_Z: ('tab:blue', '$\mathbb{E}[Z(S)] = pqt|S|$'),
  exp_Y: ('tab:orange', '$\mathbb{E}[Y(S)]$'),
  exp_X: ('tab:green', '$\mathbb{E}[X(S)] = f|S|$'),
  exp_Z + abs_epsilon: ('red', '$(1 + \epsilon)\mathbb{E}[Z(S)]$'),
  exp_Y - abs_epsilon: ('red', '$(1 - \epsilon)\mathbb{E}[Y(S)]$'),
  exp_X - abs_epsilon//2: ('red', '$(1 - f)pq(n - t)|S|$'),
  exp_X + abs_epsilon//2: ('violet', '$pq(n - t)|S|$')
  # 100: 'pq(n - t)'
}
ax.set_yticks([])
ax.set_xticks(list(x_labels.keys()))
ax.set_xticklabels([label for color, label in x_labels.values()], rotation=90)
ticks = ax.get_xticklabels()
for (xc, (color, label)), tick in zip(x_labels.items(), ticks):
  plt.axvline(x=xc, linestyle='--', color=color)
  tick.set_color(color)

# plot random variable Z
curve_x = binom.pmf(x - exp_Z + poisson_lambda, binomial_n, binomial_p)
ax.plot(x, curve_x)
x_negl_z = np.arange(exp_Z + abs_epsilon, max_x, 1)
y_negl_z = binom.pmf(x_negl_z, binomial_n, binomial_p)
ax.fill_between(
  x_negl_z,
  y_negl_z,
  hatch='///',
  facecolor='lightsteelblue',
  edgecolor='white'
)

# plot random variable Y
curve_y = binom.pmf(x - exp_Y + poisson_lambda, binomial_n, binomial_p)
ax.plot(x, curve_y)
x_negl_y = np.arange(min_x, exp_Y - abs_epsilon + 1, 1)
y_negl_y = binom.pmf(x_negl_y - exp_Y + poisson_lambda, binomial_n, binomial_p)
ax.fill_between(
  x_negl_y,
  y_negl_y,
  hatch='///',
  facecolor='moccasin',
  edgecolor='white'
)

y_min, y_max = ax.get_ylim()
ANNOTATION_MARGIN = 0.002
ANNOTATION_TEXT_MARGIN = 0.002
def render_arrow_range(start_x, end_x, label, y_offset=0):
  y = y_max + ANNOTATION_MARGIN + y_offset
  ax.annotate('', xy=(start_x, y), xytext=(end_x, y), xycoords='data', textcoords='data',
              arrowprops={'arrowstyle': '<->'}, annotation_clip=False)
  ax.annotate(label, xy=(exp_Z, y + ANNOTATION_TEXT_MARGIN), xytext=((start_x + end_x)//2, y + ANNOTATION_TEXT_MARGIN), ha='center', va='bottom', annotation_clip=False)

render_arrow_range(exp_Z, exp_Z + abs_epsilon, '$\epsilon$')
render_arrow_range(exp_Y, exp_X, '$f$', 0.002)
render_arrow_range(exp_Y - abs_epsilon, exp_Y, '$\epsilon$')
render_arrow_range(exp_X - abs_epsilon//2, exp_X + abs_epsilon//2, '$f$')
render_arrow_range(exp_Z, exp_X + abs_epsilon//2, '$3\epsilon + 3f \leq \delta$', 0.013)

# plot random variable X
curve_x = binom.pmf(x - exp_X + poisson_lambda, binomial_n, binomial_p)
ax.plot(x, curve_x)

plt.tight_layout()
# plt.show()

fig.savefig('backbone-vars.pdf', bbox_inches='tight')
