from rest_framework import serializers
from posts.models import Posts
from django.utils.timezone import now

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length =100,  required=True) 
    content = serializers.CharField(required=True)
    date_created = serializers.DateTimeField(read_only=True)  
    
    class Meta:
        model = Posts
        fields = '__all__'