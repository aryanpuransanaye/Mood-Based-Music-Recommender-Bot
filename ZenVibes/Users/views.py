from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import UserMoodSerializer
from .models import UserMood, TelegramUser, MoodType

class UserMoodView(APIView):

    def post(self, request):
        user_bot_id = request.data.get('bot_user_id')
        mood = request.data.get('mood')

        if not mood or not user_bot_id:
            return Response({
                'error': 'bot_user_id or mood fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user, _ = TelegramUser.objects.get_or_create(bot_user_id=user_bot_id)
        mood_obj, _ = MoodType.objects.get_or_create(name=mood)

        data = {
            'user': user.id,
            'mood': mood_obj.id,
        }

        serializer = UserMoodSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            return Response({
                'user_bot_id': user.bot_user_id,
                'mood': mood_obj.name,
                'mood_date': instance.mood_date.isoformat()
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):

        bot_user_id = request.query_params.get('bot_user_id')
        if not bot_user_id:
            return Response({
                'error': 'bot_user_id field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        moods = UserMood.objects.filter(user__bot_user_id=bot_user_id).order_by('-mood_date')
        serializer = UserMoodSerializer(moods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    


