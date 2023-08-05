
import glob
from tqdm import tqdm
a =glob.glob('netflix-prize-data/combined_data_*')
every_files = []
for aa in a:
    every_files.append(open(aa, 'r').read().split('\n'))

res = []
for kke in tqdm(every_files):
    for kk in tqdm(kke[:300000]):
        if len(kk.split(',')) == 1:
            movie_id = kk[:-1]
        else:
            kr = kk.split(',')
            res.append(f'{movie_id},{kr[0]},{kr[1]},{kr[2]}')

open('small_dataset.txt', 'w').write('\n'.join(res))