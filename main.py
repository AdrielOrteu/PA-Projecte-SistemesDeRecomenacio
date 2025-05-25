from Interface import GUI
from Users import MovieUsers, BookUsers
from Contents import Books, Movies
from Ratings import SimpleRatings, ContentRatings, CollaborativeRatings


interface = GUI()
executing = True
database = None
users = None
identity = None
action = None
contents = None
method = None
ratings = None

while executing:
    if database is None:
        database = GUI.chose_db()
        
        if database == "movies":
            users = MovieUsers()
            contents = Movies()
        else:
            users = BookUsers()
            contents = Books()
        
        # TODO Make else catch errors
        
        users.load_users()
        contents.load_contents()
    
    if identity not in users.users.keys():
        identity = GUI.chose_identity()
        while identity not in users.users.keys() and not ( identity == "B" ) :
            identity = GUI.chose_identity()
    if identity == "B":
        database = None
        users = None
        identity = None
        action = None
        continue
    else:
        pass
    
    if action is None:
        action = GUI.chose_action()
    
    if action == "back":
        identity = None
        action = None
        continue
        
    elif action == "exit":
        executing = False
        continue
    elif action == "recommend":
        if method is None:
            method = GUI.chose_method()
        
        if method == "simple":
            ratings = SimpleRatings(consumer=identity)
        elif method == "collaborative":
            ratings = CollaborativeRatings(consumer=identity)
        else:
            ratings = ContentRatings(consumer=identity)
        
        ratings.rate(users=users, contents=contents)
        print(f"{ratings.recommendations}\n{ratings.ratings}")
        
        for i in range(-5, 0):
            print(contents.contents[ratings.recommendations[i]])
        action = None
        method = None
    elif action == "evaluate":
        pass
