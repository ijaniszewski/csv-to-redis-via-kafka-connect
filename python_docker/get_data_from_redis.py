import argparse
import json
import os
from dataclasses import dataclass

import redis
from dotenv import load_dotenv

load_dotenv()


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--movie_id',
        help="Movie ID that you want to check. String, default: '1'",
        type=str,
        required=False,
        default='1')
    movie_id = parser.parse_args().movie_id
    return movie_id


@dataclass
class RedisConnection:
    def __post_init__(self):
        REDIS_HOST = os.environ['REDIS_HOST']
        REDIS_PORT = os.environ['REDIS_PORT']
        REDIS_DB = 0
        self.redis_con = redis.Redis(REDIS_HOST, REDIS_PORT, REDIS_DB)

    def get_title_by_movie_id(self, movie_id):
        movie_record = self.redis_con.get(f"movie-{str(movie_id)}")
        movie_record_json = json.loads(movie_record)
        title = movie_record_json['title']
        print(f'Title of movie with ID {str(movie_id)} is: "{title}".')

    def get_title_by_movie_id(self, movie_id):
        movie_record = self.redis_con.get(f"movie-{str(movie_id)}")
        if movie_record:
            movie_record_json = json.loads(movie_record)
            title = movie_record_json['title']
            return title

    def get_number_of_comments_by_movie_id(self, movie_id):
        number_of_comments =\
            self.redis_con.zcount(f"id_movie-{str(movie_id)}", "-inf", "+inf")
        return number_of_comments

    def get_title_and_number_of_comments(self, movie_id):
        title = self.get_title_by_movie_id(movie_id)
        if title:
            number_of_comments =\
                self.get_number_of_comments_by_movie_id(movie_id)
            print(
                f'Title of movie with ID {str(movie_id)} is: "{title}".'
                f'\nThis movie has {number_of_comments} comments'
            )
        else:
            print("Didn't find movie with such ID in our Redis database :(")


if __name__ == "__main__":
    movie_id = get_argument()
    print(f"Will search Redis databse for movie ID: {movie_id}")
    rc = RedisConnection()
    rc.get_title_and_number_of_comments(movie_id)
