from multielo import MultiElo
import numpy as np

elo = MultiElo()

# player with 1200 rating beats a player with 1000 rating
print(elo.get_new_ratings(np.array([1000, 1000])))
#  array([1207.68809835,  992.31190165])

# player with 900 rating beats player with 1000 rating
elo.get_new_ratings(np.array([900, 1000]))
#  array([920.48207999, 979.51792001])

# 3-way matchup
print(elo.get_new_ratings(np.array([1000, 1000, 1000])))