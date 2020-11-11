import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.10000recipe.com/recipe/list.html?q=김치찌개', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

recipes_image_url = soup.select_one('#contents_area_full > ul > ul > li:nth-child(1) > div.common_sp_thumb > a')['href']
recipes_image_url = 'https://www.10000recipe.com/'+recipes_image_url
print(recipes_image_url)
data = requests.get(recipes_image_url, headers=headers)
soup2 = BeautifulSoup(data.text, 'html.parser')

recipe_ingredient_raw = soup2.select('#divConfirmedMaterialArea > ul:nth-child(1) > a')

recipe_ingredient_list=[]
for a in recipe_ingredient_raw:
    recipe_ingredient_name = a.select_one('a > li').text
    recipe_ingredient_unit = a.select_one('a > li .ingre_unit').text.strip()
    recipe_ingredient_name = recipe_ingredient_name.replace(recipe_ingredient_unit, '').strip()
    print(recipe_ingredient_name,recipe_ingredient_unit)
    recipe_ingredient_list.append({
        'name' : recipe_ingredient_name,
        'unit' : recipe_ingredient_unit
    })

print(recipe_ingredient_list)