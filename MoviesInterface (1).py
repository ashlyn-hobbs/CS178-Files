# name: Ashlyn Hobbs
# date: 2/28/2024
# description: Implementation of CRUD operations with DynamoDB database
#               CS 178 Lab #9
# proposed score: 5 (out of 5) -- I know this is for Question 1 specifically so technically its out of 3 points, but still I say 5 out of 5

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "Movies"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def create_movie():
    title = input("Enter the title of your movie:")
    ratings_input = input("Enter the ratings your movie has received (1-100, separated by spaces): ")
    ratings = [int(rating) for rating in ratings_input.split()]  # Split ratings string and convert each to integer
    year = int(input("Enter the year your movie was released:"))
    genre = input("Enter the genre that your movie is:")
    table.put_item(
    Item={
        'Title': title,
        'Ratings': ratings,
        'Year': year,
        'Genre': genre
    }
)
    
def print_movie(movie_dict):
    # print out the values of the movie dictionary
    print("Title: ", movie_dict["Title"])
    print(" Ratings: ", end="")
    for rating in movie_dict["Ratings"]:
        print(rating, end=" ")
    print(" Year: ", movie_dict.get("Year"))
    print(" Genre: ", movie_dict.get("Genre"))
    print()
    
def print_all_movies():
    response = table.scan() #get all of the movies
    for movie in response["Items"]:
        print_movie(movie)

def update_rating():
    # prompt user for a Movie title
    # prompt user for a rating
    # update (add) rating to the database
    title = input("What is the movie title:")
    try:
        rating = int(input("What is the rating: "))
        table.update_item(
            Key = { "Title": title },
            UpdateExpression = "SET Ratings = list_append(Ratings, :r)",
                ExpressionAttributeValues = { ':r' : [rating],}
        )
    except:
        print("Error in updating movie rating")

def delete_movie():
    # prompt user for a Movie title
    # delete item from the database
    title = input("What movie do you want to delete? Enter the title: ")
    table.delete_item(
        Key = {
            "Title": title
        }
    )
    print("deleting movie")

def query_movie():
    # prompt user for the Movie title
    # print out the average review for all reviews in list
    title = input("What movie do you want to query? Enter the title: ")
    response = table.get_item(
        Key={
            "Title": title
        }
    )
    movie = response.get("Item")
    if movie:
        ratings_list = movie["Ratings"] # get the Ratings list for the movie
        if ratings_list:
            average_rating = sum(ratings_list) / len(ratings_list)
            print("The average rating for", title, "is", average_rating)
        else:
            print("This movie has no ratings.")
    else:
        print("Movie not found.")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a new movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to Query a movie's average ratings")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print('Not a valid option. Try again.')
main()
    
