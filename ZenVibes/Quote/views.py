import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quote
from .serializers import QuoteSerializer


# api for get an random quote by user mood
class QuoteViewSet(APIView):

   def post(self, request):
      
      mood = request.data.get('mood')
      if not mood:
         return Response({'error': 'Mood parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
      
      quotes = Quote.objects.filter(mood__iexact = mood)
      if not quotes.exists():
         return Response({"error": "No quotes found for this mood."}, status=status.HTTP_404_NOT_FOUND)
      
      random_quote = random.choice(quotes)
      serializer = QuoteSerializer(random_quote)
      return Response(serializer.data)