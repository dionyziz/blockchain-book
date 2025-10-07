import hashlib

kappa = 256

def H(x):
  m = hashlib.sha256()
  m.update(x)
  return m.digest()

def empty_tree_roots():
  roots = [H(''.encode('utf-8'))]
  for ell in range(kappa - 1):
    # compute root of an ell-height tree, given a tree of height ell - 1
    roots.append(H(roots[-1] + roots[-1]))
  return roots

def sparse_root():
  y = H('hello'.encode('utf-8'))
  print(y.hex())
  roots = empty_tree_roots()
  for ell in range(kappa):
    y = H(y + roots[ell])
  return y

print(sparse_root().hex())