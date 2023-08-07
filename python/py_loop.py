from tqdm import tqdm
import argparse


def main(args):
    r = open(f'{args.input_file}','r').read().split('\n')
    fulldict = {}
    for rr in tqdm(r,total=len(r)):
        splited = rr.split(',')
        user_id = splited[1]
        movie_id = splited[0]
        ratings = splited[2]
        if user_id not in fulldict.keys():  
            fulldict[user_id] = []
            fulldict[user_id].append([movie_id,ratings])
        else:
            fulldict[user_id].append([movie_id,ratings])
    open(f'{args.output_file}','w').write('\n'.join(f'{k}\t{v}' for k,v in fulldict.items()))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, help='path to input file')
    parser.add_argument('--output_file', type=str, help='path to output file')
    args = parser.parse_args()
    main(args)