import requests

def get_recommendations(user_mood):
    print(user_mood)
    url = 'http://127.0.0.1:8000/api/recommendation/'
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
            response = requests.get(music_url, timeout=60)
            audio_data = response.content
            return audio_data, caption
        else:
            return None, "❌ There is no music for this mood"

    except requests.exceptions.ConnectionError as errc:
        print("❌ Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print("❌ Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("❌ Other Error:", err)