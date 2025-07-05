import requests
from decouple import config

def get_recommendations(user_mood):
    print(user_mood)
    url = config('API_RECOMMENDATION_UR')
    data = {
        'mood': user_mood
        }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        quote_data = result.get('quote',{})
        caption = f"💬 *{quote_data.get('text', 'No qoute')}*\n\n— _{quote_data.get('author', 'Unknown')}_"

        music_data = result.get('music',{})
        if music_data:
            music_url = music_data.get('file_url')
            response = requests.get(music_url, timeout=120)
            audio_data = response.content
            
            music_title = music_data.get('title','Unknown')
            music_artist = music_data.get('artist', 'Unknown')
            
            return audio_data, caption, music_title, music_artist
        else:
            return None, None, None, None

    except requests.exceptions.ConnectionError as errc:
        print("❌ Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print("❌ Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("❌ Other Error:", err)