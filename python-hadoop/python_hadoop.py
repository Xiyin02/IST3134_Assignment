from mrjob.job import MRJob
from mrjob.step import MRStep

import csv
import math

class MovieRecommendation(MRJob):
 
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                    reducer=self.reducer_count_ratings),
        ]

    def mapper_get_ratings(self, _, line):
        user_id, movie_id, rating, _ = line.strip().split(',')
        yield user_id, (movie_id, float(rating))

    def reducer_count_ratings(self, user_id, values):
        user_ratings = [(movie_id, rating) for movie_id, rating in values]
        yield user_id, user_ratings
        
if __name__ == '__main__':
    MovieRecommendation.run()
