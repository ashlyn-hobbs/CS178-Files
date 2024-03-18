import boto3

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

def main():
    print("----Create a Movie----")
    create_movie()
    print("----Display all Movies----")
    print_all_movies()

main()
