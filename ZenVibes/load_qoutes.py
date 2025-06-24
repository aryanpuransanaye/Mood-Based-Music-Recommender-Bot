import os, django, json
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZenVibes.settings")
django.setup()


def load_quotes(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


from Quote.models import Quote

def add_quotes_to_db(json_path):

    data = load_quotes(json_path)

    for mood_group in data:
        mood_name = mood_group['mood']

        for quote_data in mood_group['quotes']:
       
            Quote.objects.get_or_create(
                text=quote_data['text'],
                author=quote_data['author'],
                mood=mood_name
            )
    else:
        print("Quotes imported successfully.")


if __name__ == "__main__":
    add_quotes_to_db(config('FILE_PATH'))
