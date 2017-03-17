# CollabFilter
Item-based collaborative filtering recommender system
- We are provided with the input data file ratings-dataset.tsv. The file consists of one rating event per line. Each rating event is of the form:
user_id\trating\tmovie_title
- The user_id is a string that contains only alphanumeric characters with hyphens or spaces (no tabs). The rating is one of the float values 0.5,
1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, and 5.0 The movie_title is a string that may contain space characters (to separate the words). The three
fields -- user_id, rating, and the movie_title -- are separated by a single tab character (\t).

## Running your code
- python <lastname>_<firstname>_collabFilter.py <ratingsFileName> <user> <n> <k>
- The program should take 4 arguments:
  - ratingsFileName: The name of the ratings file.
  - user: The id of the user (string) for whom you should make recommendations.
  - n: The size of the neighborhood N to be used in the prediction equation.
  - k: The number of recommendations that should be made for the specified user.

