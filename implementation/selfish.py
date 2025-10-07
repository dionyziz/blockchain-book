from random import random

MONTE_CARLO = 100

t = 4999
n = 10000
k = 10000

adversarial_domination = t / n

sum_mu = 0
for i in range(MONTE_CARLO):
  honest_blocks = 1 # genesis
  adversarial_blocks = 0
  adversarial_advantage = 0

  while honest_blocks + adversarial_blocks < k:
    if random() < adversarial_domination: # adversarial block
      adversarial_advantage += 1
    else: # honest block
      if adversarial_advantage > 0:
        adversarial_advantage -= 1
        adversarial_blocks += 1
      else:
        honest_blocks += 1
  mu = adversarial_blocks / (honest_blocks + adversarial_blocks)
  sum_mu += mu
print('Average quality: {}'.format(sum_mu / MONTE_CARLO))