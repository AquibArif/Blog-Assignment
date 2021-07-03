from models import Blog, Comments, ReportedBlogs
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    
    user = serializers.RelatedField(many=True, read_only=True)

    class Meta:
    	model = Blog
    	fields = "__all__"
    
class CommentsSerializer(serializers.ModelSerializer):

    blog = serializers.RelatedField(many=True, read_only=True)
    user = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"

class ReportedBlogsSerializer(serializers.ModelSerializer):

    blog = serializers.RelatedField(many=True, read_only=True)
    user = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = ReportedBlogs
        fields = "__all__"
