from django import template
import requests
register=template.Library()


@register.simple_tag
def transdata(data,lang):
    print(data,lang)
    import json
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"
    querystring = {"to":str(lang),"api-version":"3.0","profanityAction":"NoAction","textType":"plain"}
    payload =json.dumps([{"Text":str(data)}])
    headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
    'x-rapidapi-key': "71ef3c6507mshcbf3d807676c62fp17d5a5jsncc7169aa215b"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return response.text