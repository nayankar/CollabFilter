import sys
import string
import re
import json
import itertools
import collections
import glob
import os
import itertools
from decimal import *
from itertools import combinations

document = str(sys.argv[1])
USER = str(sys.argv[2])
N = str(sys.argv[3])
k = str(sys.argv[4])

hugelist=[]
linelist = []
movies = {}

afinnfile = open(document)
for line in afinnfile:
	line = line.strip()
	linelist = line.split("\t")
	hugelist.append(linelist)
	if linelist[2] not in movies:
		movies[linelist[2]] = []
	movies[linelist[2]].append(linelist[0])

# for key in hugelist:
# 	movieset.add(key[2])

movieuserdic={}
for key in hugelist:
	if key[0] not in movieuserdic:
		movieuserdic[key[0]]=[]
usermovie = {}
for key in hugelist:
	if key[0] not in usermovie:
		usermovie[key[0]]={}
for key in hugelist:
	usermovie[key[0]].update({key[2]:float(key[1])})
movielist = sorted(movies.keys())
for key in usermovie:
	for movie in movielist:
		if movie in usermovie[key].keys():
			movieuserdic[key].append(float(usermovie[key][movie]))
		else:		
			movieuserdic[key].append(float(0))
			

wijs = {}
for pair in combinations(movielist, 2):
	pair = tuple(sorted(pair))
	movie_i = pair[0]
	movie_j = pair[1]
	co_rated_users = set(movies[movie_i]) & set(movies[movie_j])
	if len(co_rated_users)==0:
		wijs[pair] = 0
		continue
	ave_i = sum([usermovie[user][movie_i] for user in co_rated_users])/len(co_rated_users)
	ave_j = sum([usermovie[user][movie_j] for user in co_rated_users])/len(co_rated_users)
	norm_ri = []
	norm_rj = []
	for user in co_rated_users:
		norm_ri.append(usermovie[user][movie_i] - ave_i)
		norm_rj.append(usermovie[user][movie_j] - ave_j)
	numerator = sum([i*j for i,j in zip(norm_ri,norm_rj)])
	denominator = (sum([i**2 for i in norm_ri]) * sum([j**2 for j in norm_rj]))**0.5
	wijs[pair] = 0 if denominator==0 else numerator/denominator

def predict(movie, wijs, usermovie):
	rated_movies = usermovie[USER].keys()
	rated_movie_pairs =[]
	for rated_movie in rated_movies:
		rated_movie_pairs.append(tuple(sorted([movie, rated_movie])))
	relevant_wijs =[]
	for wij in rated_movie_pairs:
		relevant_wijs.append((wij, wijs[wij]))
	relevant_wijs = sorted(relevant_wijs, key=lambda x: x[1], reverse=True)
	if len(relevant_wijs)>N:
		relevant_wijs = relevant_wijs[0:N]
	n_movies=[]
	for wij in relevant_wijs:
		n_movies.append(wij[0][(wij[0].index(movie)-1)%2])	
	numerator = sum([usermovie[USER][n_movie] * wijs[win[0]] for n_movie,win in zip(n_movies, relevant_wijs)])
	denominator = sum([abs(wijs[win[0]]) for win in relevant_wijs])
	if denominator==0:
		return 0
	else:
		return numerator/denominator

unrated_movies = set(movielist) - set(usermovie[USER].keys())
predictions = {}
for movie in unrated_movies:
	predictions[movie] = predict(movie, wijs, usermovie)
sorted_predictions = sorted(predictions.items(), key=operator.itemgetter(1),reverse=True)[:k]
for key in sorted_predictions:
	print key[0],key[1]	
