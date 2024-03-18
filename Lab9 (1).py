# name: Ashlyn Hobbs
# date: 2/28/2024
# description: Implementation of CRUD operations with DynamoDB database
#               CS 178 Lab #9
# proposed score: 5 (out of 5) --

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "Videogames"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def create_videogame():
    name = input("Enter the name of your videogame:")
    ratings_input = input("Enter the ratings your videogame has received (1-100, separated by spaces): ")
    ratings = [int(rating) for rating in ratings_input.split()]  # Split ratings string and convert each to integer
    year = int(input("Enter the year your videogame was released:"))
    genre = input("Enter the genre that your movie is:")
    table.put_item(
    Item={
        'Name': name,
        'Ratings': ratings,
        'Year': year,
        'Genre': genre
    }
)
    
def print_videogame(videogame_dict):
    # print out the values of the movie dictionary
    print("Name: ", videogame_dict["Name"])
    print(" Ratings: ", end="")
    for rating in videogame_dict["Ratings"]:
        print(rating, end=" ")
    print(" Year: ", videogame_dict.get("Year"))
    print(" Genre: ", videogame_dict.get("Genre"))
    print()
    
def print_all_videogames():
    response = table.scan() #get all of the movies
    for videogame in response["Items"]:
        print_videogame(videogame)

def update_rating():
    # prompt user for a Movie title
    # prompt user for a rating
    # update (add) rating to the database
    name = input("What is the name of the videogame:")
    try:
        rating = int(input("What is the rating: "))
        table.update_item(
            Key = { "Name": name },
            UpdateExpression = "SET Ratings = list_append(Ratings, :r)",
                ExpressionAttributeValues = { ':r' : [rating],}
        )
    except:
        print("Error in updating videogame rating")

def delete_videogame():
    # prompt user for a Movie title
    # delete item from the database
    name = input("What videogame do you want to delete? Enter the name: ")
    table.delete_item(
        Key = {
            "Name": name
        }
    )
    print("deleting videogame")

def query_videogame():
    # prompt user for the Movie title
    # print out the average review for all reviews in list
    name = input("What movie do you want to query? Enter the title: ")
    response = table.get_item(
        Key={
            "Name": name
        }
    )
    videogame = response.get("Item")
    if videogame:
        ratings_list = videogame["Ratings"] # get the Ratings list for the movie
        if ratings_list:
            average_rating = sum(ratings_list) / len(ratings_list)
            print("The average rating for", name, "is", average_rating)
        else:
            print("This videogame has no ratings.")
    else:
        print("Videogame not found.")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new videogame")
    print("Press R: to READ all videogames")
    print("Press U: to UPDATE a new videogame (add a rating)")
    print("Press D: to DELETE a videogame")
    print("Press Q: to Query a videogame's average ratings")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_videogame()
        elif input_char.upper() == "R":
            print_all_videogames()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_videogame()
        elif input_char.upper() == "Q":
            query_videogame()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print('Not a valid option. Try again.')
main()
    
