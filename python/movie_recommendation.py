import math
import argpase

class MovieRecommendation:

    def __init__(self, user_ratings_file):
        self.user_ratings_dict = {}
        with open(user_ratings_file) as file:
            for line in file:
                user_id, movie_ratings = line.strip().split('\t')
                if user_id.replace('"','') != args.user_id:
                    continue
                if user_id not in self.user_ratings_dict:
                    self.user_ratings_dict[user_id] = []
                self.user_ratings_dict[user_id].append(movie_ratings)

    @staticmethod
    def cosine_similarity(user1, user2):
        movies = set(user1.keys()) & set(user2.keys())
        if len(movies) == 0:
            return 0.0

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

    def recommend_movies(self, user_id):
        movie_ratings = self.user_ratings_dict[user_id][0]
        recommendations = []
        for user1, ratings1 in self.user_ratings_dict.items():
            user1 = user1.replace('"', '')
            ratings1 = [i.replace('["', '').replace(']"', '') for i in ratings1][0]
            if user1 == user_id:
                continue
            similarity = self.cosine_similarity(dict(eval(ratings1)), dict(eval(movie_ratings)))
            if similarity > 0:
                recommendations.append((user1, similarity))

        # Sort the recommendations based on similarity score in descending order
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="user_id")
    parser.add_argument("input_file", help="user_id")

    args = parser.parse_args()

    movie_recommendation = MovieRecommendation(args.input_file)

    recommendations = movie_recommendation.recommend_movies(args.user_id)
    print("Recommendations for user {}: {}".format(args.user_id, recommendations))
