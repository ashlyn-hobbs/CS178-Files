import boto3

TABLE_NAME = "PhoneBook"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def create_entry():
    
    name = input("Enter the name of the person you want to create a phonebook entry for:")
    phonenumber = int(input("Enter the phonenumber of your person (ex: 1234567891): "))
    addressSnum = input("Enter the address street number belonging to your person:")
    addressStreet = input("Enter the address street name belonging to your person:")
    addressCity = input("Enter the address city name belonging to your person:")
    addressState = input("Enter the address state name belonging to your person:")
    table.put_item(
    Item={
        'Name': name,
        'PhoneNumber': phonenumber,
        'AddressSNum': addressSnum,
        'AddressStreet': addressStreet,
        'AddressCity': addressCity,
        'AddressState': addressState
    }
)

def print_phonebook(phonebook_dict):
    # print out the values of the phonebook dictionary
    print("Name: ", phonebook_dict["Name"])
    print(" PhoneNumber: ", phonebook_dict.get("PhoneNumber"))
    print(" AddressSNum: ", phonebook_dict.get("AddressSNum"))
    print(" AddressStreet: ", phonebook_dict.get("AddressStreet"))
    print(" AddressCity: ", phonebook_dict.get("AddressCity"))
    print(" AddressState: ", phonebook_dict.get("AddressState"))
    print()

def print_all_phonebook():
    response = table.scan() #get all of the Names
    for Name in response["Items"]:
        print_phonebook(Name)

def main():
    print("----Create a new PhoneBook Entry----")
    create_entry()
    print("----Display all PhoneBook Info----")
    print_all_phonebook()

main()
