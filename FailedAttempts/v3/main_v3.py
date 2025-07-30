from Interface import GUI
from Contents import Movies
from Users import MovieUsers
from Ratings import SimpleRatings
import pickle

def save_pickle(rating, dataset, objecte):
    """Guarda un objecte en un arxiu pickle """
    nom_fitxer = f"recommender_{dataset}_{rating}.dat"
    with open(nom_fitxer, 'wb') as fitxer:
        pickle.dump(objecte, fitxer)

def recover_pickle(rating, dataset):
    """Recupera un objecte d'un arxiu pickle"""
    nom_fitxer = f"recommender_{dataset}_{rating}.dat"
    with open(nom_fitxer, 'rb') as fitxer:
        r = pickle.load(fitxer)
    return r

interface = GUI()
executing = True

db_to_load = interface.chose_db()

task_dict = {}


while executing:
    if db_to_load == "movies":
        print("Let's watch movies!")
        contents = Movies()
        contents.load_contents()
        users = MovieUsers()
        users.load_users()
        identity = interface.chose_identity()
        while identity not in users.users.keys() or identity == "B":
            interface.chose_identity()
        print(identity)
        
        if identity == "B": # code to go back
            db_to_load = interface.chose_db()
            continue
        action = interface.chose_action()
        if action == "recommend":
            r_method = interface.chose_method()
            if r_method == "simple":
                recommender = SimpleRatings(consumer=identity)
                