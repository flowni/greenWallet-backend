import requests

products_columns = ['id','barcode', 'product_name', 'brands', 'image', 'categories_hierarchy',
       'nova_score', 'ingredients_analysis_tags', 'ecoscore_grade',
       'manufacturing_places', 'green_score']


def calculate_green_score(barcode):
    parameters = { 
    "UserAgent": "GreenWallet - Android - Version 1.0 - https://devpost.com/software/greenwallet-0xgfsu?ref_content=my-projects-tab&ref_feature=my_projects",
    "json": True,
    "code": barcode
    }

    score = 0

    response = requests.get("https://en.openfoodfacts.org/", params=parameters)
    content = response.json()
    eco_grade = content['products'][0]['ecoscore_grade']

    if eco_grade == 'a':
        score = score+5.5
    elif eco_grade == 'b':
        score = score+3
    elif eco_grade == 'c':
        score = score+1

    elif eco_grade == 'unknown':
        analysis = content['products'][0]['ingredients_analysis_tags']

        for a in analysis:
            if (a == 'en:palm-oil-free') or (a=='en:vegan') or (a=='en:vegetarian'):
                     score = score+1

        location = content['products'][0]['manufacturing_places']

        if ('Germany' in location) or ('Deutschland' in location) or ('Allemagne' in location):
            score = score+1

        nova = content['products'][0]['nova_group']

        if nova == 1:
            score = score+1
        elif nova == 2:
            score = score+0.5

    return score/5.5
