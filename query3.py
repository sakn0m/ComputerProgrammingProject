import csv
import json
import pickle

#import files
production_countries_file = '/Users/giorgiovanini/Desktop/Group Project/Dataset/production_countries_table.csv'
movies_file = '/Users/giorgiovanini/Desktop/Group Project/Dataset/movies_table.csv'
output_file = '/Users/giorgiovanini/Desktop/Group Project/Coding/top_5_countries.pkl'

#1: load production countries
production_countries = {}

with open(production_countries_file, 'r') as pc_file:
    reader = csv.reader(pc_file)
    rows = list(reader)  #convert to list for manual indexing
    header = rows[0]  #the first row is the header
    for i in range(1, len(rows)):  #process rows starting from index 1
        row = rows[i]
        movie_id = row[0].strip()
        countries_data = row[1].strip()  #second column: production_countries as a json string
        countries = json.loads(countries_data)  #parse the json string into a python object
        for country in countries:
            country_name = country["name"]
            if country_name not in production_countries:
                production_countries[country_name] = []
            production_countries[country_name].append(movie_id)

#2: load movie ratings
movie_ratings = {}

with open(movies_file, 'r') as movies_file:
    reader = csv.reader(movies_file)
    rows = list(reader)  #convert to list for manual indexing
    header = rows[0]  #the first row is the header
    for i in range(1, len(rows)):  #process rows starting from index 1
        row = rows[i]
        movie_id = row[0].strip()
        #check for numeric values in 'vote_average'
        vote_average_data = row[8].strip()
        is_numeric = True
        for char in vote_average_data:
            if not (char.isdigit() or char == '.'):
                is_numeric = False
                break
        if is_numeric:
            vote_average = float(vote_average_data)
            movie_ratings[movie_id] = vote_average

#step 3: calculate average ratings by country
country_avg_ratings = []

for country, movie_ids in production_countries.items():
    ratings = []
    for movie_id in movie_ids:
        if movie_id in movie_ratings:
            ratings.append(movie_ratings[movie_id])
    if len(ratings) > 0:
        avg_rating = sum(ratings) / len(ratings)
        country_avg_ratings.append((country, avg_rating))

#4: sorting to get top 5
for i in range(len(country_avg_ratings)):
    for j in range(i + 1, len(country_avg_ratings)):
        if country_avg_ratings[i][1] < country_avg_ratings[j][1]:  #compare average ratings
            country_avg_ratings[i], country_avg_ratings[j] = country_avg_ratings[j], country_avg_ratings[i]

top_5_countries = []
for i in range(5):
    if i < len(country_avg_ratings):
        top_5_countries.append(country_avg_ratings[i])

#5: save to a pickle file
with open(output_file, 'wb') as pickle_file:
    pickle.dump(top_5_countries, pickle_file)

print("Top 5 countries:", top_5_countries)