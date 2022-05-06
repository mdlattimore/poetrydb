import sqlite3
import textwrap
from os import system, name

system('printf "\e[8;35;90;t"')  # sets window size on mac os ONLY

def clear():
    """Determines operating system and invokes appropriate command to clear terminal screen"""
    if name == "nt":
        _ = system('cls')
    else:
        _ = system('clear')


def query(search_terms):
    """Formats user-supplied search terms for wildcard search in sqlite database"""
    sql_query = "%" + search_terms + "%"
    return sql_query


db = sqlite3.connect('poems.sqlite')

greeting = """  Welcome to the Python Poetry Database  """

clear()
print()
print(textwrap.indent((greeting.center(74, "*")), "\t"))
print()

while True:
    while True:
        answer = input("\n\tEnter a title, author's name, or phrase from the poem OR \n"
                       "\tpress 'enter' for complete list of available poems: ")
        auth_search = query(answer)
        print()

        sqlite_query = "SELECT poems.title, poets.first_name, poets.last_name FROM poems INNER JOIN poets on " \
                       "poems.author = poets._id WHERE poets.last_name like ? OR poems.text like ? ORDER BY poems.title"

        results = [(title, first_name, last_name) for title, first_name, last_name in db.execute(sqlite_query,
                   (auth_search, auth_search,))]

        if not results:
            print("\tSorry, no results. Please try again")
            print()
            continue
        else:
            break

    result_list = []
    for index, value in enumerate(results):  # value returns a three item tuple
        print(f"\t{index + 1}:\t{value[0]} by {value[1]} {value[2]}")  # value[0] is title, value[1] is first name,
        # value[2] is last name
        result_list.append(value[0])

    print()

    while True:
        try:
            poem_choice = int(input("\tPlease select the poem you'd like to read: "))
            poem = result_list[poem_choice - 1]
            break
        except (IndexError, ValueError):
            print("\tInvalid input. Please enter a number from the list")
            print()
            continue

    poem_query = [text for text in db.execute("SELECT text FROM poems WHERE title = ?", (poem,))]
    clear()

    # poem_query returns a list of tuples (really one single item tuple). Print using index of
    # first item in list (which is a tuple) and first item in tuple (which is text of poem). List comprehension might
    # not be best choice but it's the one I could get to work
    print(textwrap.indent(poem_query[0][0], '\t'))

    more = input("\tWould you like to search for another? ")
    if more.lower() == "yes" or more.lower() == "y":  # TODO add validation to force user to type yes/no or y/n
        clear()
        continue
    else:
        break

clear()
print()
print(textwrap.indent(("  Thanks for reading. Have a great day!  ".center(74, "*")), "\t"))
print()
print()

db.close()
