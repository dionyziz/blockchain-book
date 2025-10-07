from random import random

MONTE_CARLO = 100

n = 1000
t = 499

k = 10000

sum_mu = 0
for _ in range(MONTE_CARLO):
  adversarial_advantage = 0
  honest_blocks = 1
  adversarial_blocks = 0

  while honest_blocks + adversarial_blocks < k:
    if random() < t / n:
      # adversarial block
      adversarial_advantage += 1
    else:
      # honest block
      if adversarial_advantage > 0:
        adversarial_advantage -= 1
        adversarial_blocks += 1
      else:
        honest_blocks += 1
  mu = honest_blocks / (honest_blocks + adversarial_blocks)
  sum_mu += mu

print('Average quality: ', sum_mu / MONTE_CARLO)