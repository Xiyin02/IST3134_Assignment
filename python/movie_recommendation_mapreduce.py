from mrjob.job import MRJob
from mrjob.step import MRStep
import os
import math

class MyMRJob(MRJob):

    def configure_args(self):
        super(MyMRJob, self).configure_args()
        self.add_file_arg('--user-ratings-dict')
        self.add_passthru_arg('--user_id')

    @staticmethod
    def cosine_similarity(user1, user2):
        # Find common movies rated by both users
        movies = set(user1.keys()) & set(user2.keys())

        if len(movies) == 0:
            return (0,[])

        dot_product = 0.0
        magnitude1 = 0.0
        magnitude2 = 0.0

        for movie in movies:
            dot_product += user1[movie] * user2[movie]
            magnitude1 += user1[movie] ** 2
            magnitude2 += user2[movie] ** 2

        magnitude1 = math.sqrt(magnitude1)
        magnitude2 = math.sqrt(magnitude2)

        return (dot_product / (magnitude1 * magnitude2), list(movies))
    
    def reducer_init(self):
        # Read the distributed cache file and initialize the user_ratings_dict here.
        self.user_ratings_dict = {}
        with open(os.path.basename(self.options.user_ratings_dict)) as file:
            for line in file:
                user_id, movie_ratings = line.strip().split('\t')
                if user_id.replace('"','') != self.options.user_id:
                    continue
                if user_id not in self.user_ratings_dict:
                    self.user_ratings_dict[user_id] = []
                self.user_ratings_dict[user_id].append(movie_ratings)

    def mapper(self, _, line):
        # Use the user_ratings_dict in the Mapper.
        # For example, if you want to use it to find common movies:
        user_id, movie_ratings = line.split('\t')
        yield user_id, movie_ratings
                # Process the common movies between 'movie_ratings' and 'ratings'
                # and yield the results as needed.

    def reducer(self, user_id, values):
        movie_ratings = [i.replace('["', '').replace(']"', '') for i in values][0]
        user_id = user_id.replace('"', '')
        for user1, ratings1 in self.user_ratings_dict.items():
            user1 = user1.replace('"', '')
            ratings1 = [i.replace('["', '').replace(']"', '') for i in ratings1][0]
            if user1 == user_id:
                continue
            similarity = self.cosine_similarity(dict(eval(ratings1)),
                                                dict(eval(movie_ratings)))
            if similarity[0]>0:
                yield [user1, user_id], similarity


    def steps(self):
        return [
            MRStep(
                   mapper=self.mapper,
                    reducer_init=self.reducer_init,
                   reducer=self.reducer)
        ]

if __name__ == '__main__':

    MyMRJob.run()
