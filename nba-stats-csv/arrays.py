## When we use pandas, there's no escaping numpy arrays since pandas is built on numpy.
## Numpy gives us array data structure that is similar to lists with subtle benefits like being more compact, faster to read, and
## more memory efficient. This may not seem like a big deal, but it is at large scale.
import numpy as np
kawhi_steals = [4, 5, 2, 1, 3]

klaw = np.array(kawhi_steals)
print(klaw.mean())