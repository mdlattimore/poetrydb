import sqlite3


# TODO -- Wrap in while loop to keep running until user exits


def query(answer):
    query = "%" + answer + "%"
    return query


db = sqlite3.connect('poems.sqlite')

while True:
    answer = input("Enter the a title, poet's last name, or phrase from a poem: ")
    auth_search = query(answer)

    sqlite_query = "SELECT poems.title, poets.first_name, poets.last_name FROM poems INNER JOIN poets on poems.author "\
                   "= poets._id WHERE poets.last_name like ? OR poems.text like ? ORDER BY poems.title"

    results = [(title, first_name, last_name) for title, first_name, last_name in db.execute(sqlite_query, (auth_search,
               auth_search,))]

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

while True:
    try:
        poem_choice = int(input("\tPlease select the poem you'd like to read: "))
        poem = result_list[poem_choice - 1]
    except IndexError or ValueError:
        print("Invalid input")
        print()
        continue

poem_query = [text for text in db.execute("SELECT text FROM poems WHERE title = ?", (poem,))]
print(poem_query[0][0])  # poem_query returns a list of tuples (really one single item tuple). Print using
# index of
# first item in list (which is a tuple) and first item in tuple (which is text of poem)


# choice = input("Type 1 to search by title keyword or 2 to search by author's last name: ")
#
# if choice == "1":
#     answer = input("Enter a title keyword: ")
#     search = query(answer)
#     for title, author1, author2 in db.execute(
#             "SELECT books.title, authors.first_name, authors.last_name from books inner "
#             "join authors on books.author = authors._id where (books.title LIKE ?)",
#             (search,)):
#         print(title + " by " + author1, author2)
#
# else:
#     answer = input("Enter author's last name: ")
#     search = query(answer)
#     for title, author1, author2 in db.execute(
#             "SELECT books.title, authors.first_name, authors.last_name from books inner "
#             "join authors on books.author = authors._id where (authors.last_name LIKE ?)",
#             (search,)):
#         print(title + " by " + author1, author2)

db.close()
