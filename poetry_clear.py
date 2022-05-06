import sqlite3
from os import system, name

def clear():
     if name == "nt":
         _ = system('cls')
     else:
         _ = system('clear')


def query(search_terms):
    sql_query = "%" + search_terms + "%"
    return sql_query


db = sqlite3.connect('poems.sqlite')

greeting = """  Welcome to the Python Poetry Database  """

clear()
print()
print(greeting.center(60, "*"))
print()

while True:
    while True:
        answer = input("Enter the a title, poet's last name, or phrase from a poem: ")
        auth_search = query(answer)
        print()

        sqlite_query = "SELECT poems.title, poets.first_name, poets.last_name FROM poems INNER JOIN poets on " \
                       "poems.author = poets._id WHERE poets.last_name like ? OR poems.text like ? ORDER BY poems.title"

        results = [(title, first_name, last_name) for title, first_name, last_name in db.execute(sqlite_query,
                   (auth_search, auth_search,))]

        if not results:
            print("Sorry, no results. Please try again")
            continue
        else:
            break

    result_list = []
    for index, value in enumerate(results):  # value returns a three item tuple
        print(f"\t{index + 1}:\t{value[0]} by {value[1]} {value[2]}")  # value[0] is title, value[1] is first name,
        # value[2] is last name
        result_list.append(value[0])

    print()
    poem_choice = int(input("\tPlease select the poem you'd like to read: "))
    poem = result_list[poem_choice - 1]

    poem_query = [text for text in db.execute("SELECT text FROM poems WHERE title = ?", (poem,))]
    clear()
    print(poem_query[0][0])  # poem_query returns a list of tuples (really one single item tuple). Print using index of
    # first item in list (which is a tuple) and first item in tuple (which is text of poem)

    more = input("Would you like to search for another? ")
    if more.lower() == "yes" or more.lower() == "y":
        clear()
        continue
    else:
        break

clear()
print()
print()
print("Thanks for reading. Have a great day!")
print()
print()

db.close()
