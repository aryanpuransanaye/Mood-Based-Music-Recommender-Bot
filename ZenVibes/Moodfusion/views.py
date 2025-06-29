import random
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


#import things of quote app
from Quote.models import Quote
from Quote.serializers import QuoteSerializer

#import things of music app
from Music.models import Music
from Music.serializers import MusciSerializer


class RecommendationAPIView(APIView):

    def post(self, request):

        mood = request.data.get('mood')
        if not mood:
            return Response({
                'error': 'mood field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quote = Quote.objects.filter(mood__iexact=mood)
        music = Music.objects.filter(mood__iexact=mood)

        if not quote or not music:
            return Response(
                {'error': 'No quote or music found for this mood'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        #random choose by user mood
        random_quote = random.choice(quote)
        random_music = random.choice(music)

        quote_ser = QuoteSerializer(random_quote)
        music_ser = MusciSerializer(random_music, context={'request': request} if random_music else None)

        return Response(
            {
                'quote': quote_ser.data,
                'music': music_ser.data if music_ser else {}
            },
            status=status.HTTP_200_OK
        )
