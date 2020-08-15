from pathlib import Path
import random

p = Path('data/')

l = list(p.glob("*.txt"))
r = random.randrange(len(l))

print(l[r])