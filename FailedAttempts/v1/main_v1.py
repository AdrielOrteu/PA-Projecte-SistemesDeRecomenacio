import pandas as pd
from FailedAttempts.v1.actors import User

users = []
content = []

def load_users(u):
    ratings = pd.read_csv("../../movies/ratings.csv")
    user_id = ratings.iloc[:, 0]
    tmp_lst = []
    for identifier in user_id:
        n=0
        if identifier not in tmp_lst:
            u.append( User(identifier) )
            tmp_lst.append(identifier)






#load_users(users)
#load_movies(content)
#load_user_ratings(users)

#recommender = Ratings(users=users, contents=content)

#print(recommender.user_based_recommendation(my_id=1, k=10))

#main_window = Tk()
#main_window.title("entertainment recommendations")
#main_window.state("zoomed")
#main_window.config(bg="white")
#
#gui_display = WindowManager(root_window=main_window)
#
#
#def x(event) -> str:
#    selected_item = event.widget.get()
#    print(f"Selected item: {selected_item}")
#    return selected_item
#
#
#def y():
#    print("opening settings...")
#
#
#gui_display.create_start_screen(databases=["movies", "books"], combo_command=x, button_command=y)
#
#main_window.mainloop()
#