from django.apps import AppConfig
import requests
from IPython.display import Image
from IPython.core.display import HTML


class RecipeCatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipe_catalog'

    # url = "http://catfact.ninja/fact"
    # session = requests.Session()
    # resp = session.get(url)
    # print(resp.content)

    # url2 = "https://api.thecatapi.com/v1/images/search"
    # session_cat = requests.Session()
    # resp_cat = session_cat.get(url2)
    # resp_cat.json()
    # Image(
    #     url=resp_cat.json()[0]['url'],
    #     width=resp_cat.json()[0]['width'],
    #     height=resp_cat.json()[0]['height']
    # )
