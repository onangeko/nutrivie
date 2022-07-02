# classe pour reconnaitre un user
class Profile():
    def __init__(self, id, name, age, height, weight, seggs):
        self.id = id
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.seggs = seggs
        
# récuperer depuis la db
def load_profile(user_id):
    conn = sqlite3.connect('Nutrivie')
    curs = conn.cursor()
    curs.execute("SELECT * from profile where user_id = (?)", [user_id])
    result = curs.fetchone()
    if result is None:
        return None
    else:
        return User(result[0], result[1], result[2], result[3], result[4], result[5])

# fonction test
def taille_x_age(user_id):
    user = load_profile(user_id)
    return user.taille * user.age

# create route
@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    print(taille_x_age(1))
