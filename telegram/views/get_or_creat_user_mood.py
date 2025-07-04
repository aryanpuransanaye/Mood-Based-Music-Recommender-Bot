import requests

def create_user_mood(user_mood: str, bot_id: str) -> dict:

    url = 'http://127.0.0.1:8000/api/users-mood/'
    payload = {'bot_user_id': bot_id, 'mood': user_mood}

    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return {'ok': True, 'data': response.json()}

    except requests.exceptions.RequestException as e:
       
        print(f'HTTP error: {e}')
        return {'ok': False, 'error': str(e)}
    
def get_mood_history(bot_id: str) -> dict:
    url = 'http://127.0.0.1:8000/api/users-mood/'  

    params = {'bot_user_id': bot_id} 

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return {'ok': True, 'data': response.json()}

    except requests.exceptions.RequestException as e:
        print(f'HTTP error: {e}')
        return {'ok': False, 'error': str(e)}
