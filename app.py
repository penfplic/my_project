from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta




@app.route('/')
def hello_world():
    return render_template('landing_page.html')

@app.route('/mainrecipe', methods=['POST'])
def get_main_recipe():
    db.user_main_recipe.drop()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    recipe_url_receive = request.form['recipe_url_give']
    recipe_name_receive = request.form['recipe_name_give']

    data = requests.get(recipe_url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    main_nth = 1
    recipes_image_url = soup.select_one(f'#contents_area_full > ul > ul > li:nth-child({main_nth}) > div.common_sp_thumb > a')['href']
    recipes_image_url = 'https://www.10000recipe.com/'+recipes_image_url

    data = requests.get(recipes_image_url, headers=headers)
    soup2 = BeautifulSoup(data.text, 'html.parser')

    recipe_name_check=soup2.select_one('#contents_area > div.view2_summary.st3 > h3').text.strip()
    recipe_ingredient_raw = soup2.select('#divConfirmedMaterialArea > ul:nth-child(1) > a')

    recipe_ingredient_list = []
    recipe_ingredient_list.append({
        'recipeName':recipe_name_check,
        'url':recipes_image_url,
        'nth':main_nth,
        'userRecipeName':recipe_name_receive
    })
    for a in recipe_ingredient_raw:
        recipe_ingredient_name = a.select_one('a > li').text
        recipe_ingredient_unit = a.select_one('a > li .ingre_unit').text.strip()
        recipe_ingredient_name = recipe_ingredient_name.replace(recipe_ingredient_unit, '').strip()
        recipe_ingredient_list.append({
            'name': recipe_ingredient_name,
            'unit': recipe_ingredient_unit
        })

    db.user_main_recipe.insert_many(recipe_ingredient_list)


    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


@app.route('/recipeCheck',methods=['GET'])
def show_check_page():
    return render_template('check_page.html')

@app.route('/recipeCheck',methods=['POST'])
def check_again():
    main_recipe_nth = list(db.user_main_recipe.find({},{'_id':False}))[0]
    user_input_name=main_recipe_nth['userRecipeName']
    user_input_url='https://www.10000recipe.com/recipe/list.html?q=' + user_input_name
    main_recipe_nth=main_recipe_nth['nth']
    tf_receive = request.form['tf_give']
    if tf_receive:

        db.user_main_recipe.drop()

        main_recipe_nth=main_recipe_nth+1
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(user_input_url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        recipes_image_url = soup.select_one(f'#contents_area_full > ul > ul > li:nth-child({main_recipe_nth}) > div.common_sp_thumb > a')['href']
        recipes_image_url = 'https://www.10000recipe.com/' + recipes_image_url

        data = requests.get(recipes_image_url, headers=headers)
        soup2 = BeautifulSoup(data.text, 'html.parser')

        recipe_name_check = soup2.select_one('#contents_area > div.view2_summary.st3 > h3').text.strip()
        recipe_ingredient_raw = soup2.select('#divConfirmedMaterialArea > ul:nth-child(1) > a')

        recipe_ingredient_list = []
        recipe_ingredient_list.append({
            'recipeName': recipe_name_check,
            'url': recipes_image_url,
            'nth': main_recipe_nth,
            'userRecipeName': user_input_name
        })

        for a in recipe_ingredient_raw:
            recipe_ingredient_name = a.select_one('a > li').text
            recipe_ingredient_unit = a.select_one('a > li .ingre_unit').text.strip()
            recipe_ingredient_name = recipe_ingredient_name.replace(recipe_ingredient_unit, '').strip()
            recipe_ingredient_list.append({
                'name': recipe_ingredient_name,
                'unit': recipe_ingredient_unit
            })

        db.user_main_recipe.insert_many(recipe_ingredient_list)



    return jsonify({'result': 'success'})



@app.route('/api/list',methods=['GET'])
def show_main_recipe():
    main_recipe_list = list(db.user_main_recipe.find({},{'_id':False}))
    return jsonify({'result': 'success', 'main_recipe_list': main_recipe_list})


@app.route('/newRecipes',methods=['GET'])
def get_new_recipe():
    return render_template('show_another_recipes.html')

    # main_recipe_list = list(db.user_main_recipe.find({}, {'_id': False}))


    # for a in main_recipe_list[1:]:
    #     ingredient_name=a['name']
    #     url_from_ingredient='https://www.10000recipe.com/recipe/list.html?q='+ingredient_name
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    #     data = requests.get(url_from_ingredient, headers=headers)
    #     soup = BeautifulSoup(data.text, 'html.parser')
    #
    #     recipes_image_url = soup.select_one('#contents_area_full > ul > ul > li:nth-child(1) > div.common_sp_thumb > a')['href']
    #     recipes_image_url = 'https://www.10000recipe.com/' + recipes_image_url
    #
    #     data = requests.get(recipes_image_url, headers=headers)
    #     soup2 = BeautifulSoup(data.text, 'html.parser')
    #
    #     recipe_name_check = soup2.select_one('#recipeIntro').text.strip()
    #     recipe_ingredient_raw = soup2.select('#divConfirmedMaterialArea > ul:nth-child(1) > a')
    #
    #     recipe_ingredient_list = []
    #     recipe_ingredient_list.append({
    #         'recipeName': recipe_name_check,
    #         'url': recipes_image_url
    #     })
    #     for a in recipe_ingredient_raw:
    #         recipe_ingredient_name = a.select_one('a > li').text
    #         recipe_ingredient_unit = a.select_one('a > li .ingre_unit').text.strip()
    #         recipe_ingredient_name = recipe_ingredient_name.replace(recipe_ingredient_unit, '').strip()
    #         recipe_ingredient_list.append({
    #             'name': recipe_ingredient_name,
    #             'unit': recipe_ingredient_unit
    #         })
    #
    #     db.user_another_recipe.insert_many(recipe_ingredient_list)


    return jsonify({'result':'success'})

def show_another_recipes():
    return render_template('show_another_recipes.html')





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)