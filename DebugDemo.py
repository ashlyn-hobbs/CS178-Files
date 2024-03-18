# Name: Ashlyn Hobbs
# Demo For Debugging

i = 10

print("Hello Cloud9!")
print("i is", i)

input_val = ""
while input_val != "q":
    input_val = input("Enter a number (or 'q' to quit): ")
    if input_val == 'q':
        print("OK, exiting...")
    else:
        i += int(input_val)
        print("i is now", i)
        
print("Goodbye")