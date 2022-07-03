# Formule besoins journaliers
def besoins(age, height, weight, seggs, sport):
    if seggs == 'f':
        return (((9.74*weight)+(172.9*(height/100))-(4.737*age)+667.051)*(1.2+(sport)*0.075))
    return (((13.707 * weight) + (492.3 * (height / 100)) - (6.673 * age) + 77.607) * (1.2 + (sport) * 0.075))
