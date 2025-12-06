import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
# URL du menu
url = "https://www.crous-poitiers.fr/restaurant/la-rochelle-ru-republique/"

# Dico
repas = {}

# Requête HTTP
response = requests.get(url)
response.raise_for_status()  # Vérifie que la requête a réussi

# Parser le contenu HTML
soup = BeautifulSoup(response.text, "html.parser")

# Trouver la div du menu
menu_div = soup.find("div", class_="menu")
if menu_div:
    # Récupérer la date du menu
    date = menu_div.find("time", class_="menu_date_title").text.strip()
    repas["Date"] = date
    # Récupérer les repas
    meals = menu_div.find_all("div", class_="meal")
    
 
    
    for meal in meals:
        meal_title = meal.find("div", class_="meal_title").text.strip()
        
        # Récupérer les catégories et les plats
        categories = meal.find("ul", class_="meal_foodies").find_all("li", recursive=False)
        for category in categories:
            cat_name = category.contents[0].strip()  # Nom de la catégorie (ENTREE, PLAT SELF...)
            items = [li.text.strip() for li in category.find_all("li")]
            if cat_name == "ENTREE":
                repas["Entrées"] = items
            if cat_name == "PLAT SELF":
                repas["Plats"] = items
            if cat_name == "DESSERT":
                repas["Desserts"] = items


    
else:
    raise Exception
    
print(repas)
filename = "menu.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(repas, f, ensure_ascii=False, indent=4)
