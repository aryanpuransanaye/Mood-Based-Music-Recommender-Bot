import requests
from decouple import config

def create_user_mood(user_mood: str, mood_detail:str, bot_user_id: str) -> dict:

    url = config('API_USERS_MOOD_URL')
    payload = {'bot_user_id': bot_user_id, 'mood': user_mood, 'mood_description': mood_detail}

    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return {'ok': True, 'data': response.json()}

    except requests.exceptions.RequestException as e:
       
        print(f'HTTP error: {e}')
        return {'ok': False, 'error': str(e)}
    
def get_mood_history(bot_id: str) -> dict:

    url = config('API_USERS_MOOD_URL')
    params = {'bot_user_id': bot_id} 

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return {'ok': True, 'data': response.json()}

    except requests.exceptions.RequestException as e:
        print(f'HTTP error: {e}')
        return {'ok': False, 'error': str(e)}
