import json
import requests
from flask_babel import _
from app import app


def translate(text, source_language, dest_language):
    
    print(text + ' ' + source_language + ' ' + dest_language)
    print(app.config['MS_TRANSLATOR_KEY'])
    
    if 'MS_TRANSLATOR_KEY' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}
    
    print('auth: ' + auth)

    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    
    print('r status code: ' + r.status_code)

    if r.status_code != 200:
        return 'Error: the translation service failed.'
    return json.loads(r.content.decode('utf-8-sig'))
