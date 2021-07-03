from rest_framework.views import APIView
# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Blog, Comments, ReportedBlogs
from .serializers import  BlogSerializer, CommentsSerializer, ReportedBlogsSerializer

import logging
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger("blog_loggers")

# create Blog
class CreateBlog(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def post(self, request):
        try:
            context_dict = {"head":{}, "body":{}}
            serializer =  BlogSerializer(data=request.data)
            
            if serializer.is_valid():
                
                #create blog
                blog = Blog.objects.create(user=request.user, blog_name=serializer.validated_data.get("blog_name"), text=serializer.validated_data.get("text"))    
                
                context_dict["body"]["message"] = "Blog Created" 
                
                context_dict["head"]["status"] = 0
                context_dict["head"]["message"] = "Success"
                return Response(context_dict)

            context_dict["head"]["status"]= 2
            context_dict["head"]["message"] = "Failed"
            
        except Exception as e:
            logger.excepttion(e)
            context_dict["head"]["status"]= 2
            context_dict["head"]["message"] = "Failed"
        return Response(context_dict)



# Display Blog, display all the blogs or one blog with id
class DisplayBlog(APIView):
    # cache for 15 mins
    @method_decorator(cache_page(60*15))
    def get(self, request, *args, **kwargs):
        try:
            context_dict = {"head":{}, "body":{}}
            blog_id = kwargs.get("id")
            
            #  display all the blogs 
            if blog_id == "all":
                self.blogs = Blog.objects.all().prefetch_related("comments")
            else:
                self.blogs = Blog.objects.filter(pk=blog_id).prefetch_related("comments")
            
            
            context_dict['body'] = self.make_context_data()
            
            context_dict["head"]["status"] = 0
            context_dict["head"]["ResponseCode"] = "Success"
            
            raise Exception("custom")
            
        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"]= 2
            context_dict["head"]["message"] = "Failure"
            
        return Response(context_dict)
    
    # populate details of each blog
    def make_context_data(self):
        con_data = {"blogs_list":[]}

        for blog in self.blogs:
            tmp_dict = {}
            tmp_dict['blog_name'] = blog.blog_name
            tmp_dict['content'] = blog.text
            tmp_dict['user'] = blog.user.get_full_name()
            tmp_dict['likes'] = blog.likes
            tmp_dict['updated_date'] = blog.updated_date
            tmp_dict['comments'] = []
            
            #  appending all the comments of the blog
            for comment in blog.comments.all():
                tmp_dict['comments'].append({
                    "comment_by": comment.user.email,
                    "comment": comment.text,
                    "comment_date": comment.date
                })
            
            con_data['blogs_list'].append(tmp_dict)
        return con_data
            

# Update a blog, only owner can update
class UpdateBlog(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def post(self, request):
        try:
            now = timezone.localtime(timezone.now())
            
            context_dict = {"head":{}, "body":{}}
                
            blog_id = request.data.get("blog_id")
            content = request.data.get("text")
            blog_name = request.data.get("blog_name")
            
            if not blog_id:
                context_dict["head"]["status"] = 2
                context_dict["head"]["message"] = "Blog Id is required"
                return Response(context_dict)
            
            # get blog object from db
            blog_obj = Blog.objects.filter(pk=blog_id, user=request.user)
            
            if blog_obj:
                # both content and blog_name is updated
                if content and blog_name:
                    blog_obj.update(text = content, blog_name = blog_name, updated_date = now)
                elif content and not blog_name:
                    # only content is updated
                    blog_obj.update(text = content, updated_date = now)
                else:
                    # only blog name is updated
                    blog_obj.update(blog_name = blog_name, updated_date = now)
                    
                context_dict["body"]["message"] = "successfully Update"
                
            else:
                context_dict["body"]["message"] = "Cannot Update"
                    
            context_dict["head"]["status"] = 0
            context_dict["head"]["message"] = "success"

        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Failed"
        
        return Response(context_dict)

# Delete Blog, only owner of the blog or admin can delete 
class DeleteBlog(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def delete(self, request):
        context_dict = {"head":{}, "body":{}}
        try:
            blog_id = kwargs.get('id')
            
            #  Admin can delete all blogs
            if request.user.is_superuser:
                blog_obj = Blog.objects.filter(pk=blog_id)
            else:
                # user can delete its own blog.
                blog_obj = Blog.objects.filter(pk=blog_id,user=request.user)
            
            if blog_obj:
                blog_obj.delete()
                context_dict['body']['message'] = "successfully deleted"
            else:
                context_dict['body']['message'] = "Cannot delete"
                
            context_dict["head"]["status"] = 0
            context_dict["head"]["message"] = "success"

        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Failed"
        
        return Response(context_dict)

# report particular blog
class ReportBlog(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def post(self, request, *args, **kwargs):
        context_dict = {"head":{}, "body":{}}
        try:
            blog_id = kwargs.get('blog_id')
            
            # get blog object
            blog_obj = Blog.objects.filter(pk=blog_id).first()
            serializer =  ReportedBlogsSerializer(data=request.data)
            
            if serializer.is_valid():
                if blog_obj:
                    # add blog in ReportedBlogs models
                    ReportedBlogs.objects.create(blog=blog_obj, user=request.user, reason = serializer.validated_data.get("reason"))
                    context_dict['body']['message'] = "successfully Reported"
                else:
                    context_dict['body']['message'] = "Blog does not exists."
                
                context_dict["head"]["status"] = 0
                context_dict["head"]["message"] = "success"
                return Response(context_dict)
            
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Failed"

        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Failed"
        
        return Response(context_dict)

class CommentOnBlog(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def post(self, request, *args, **kwargs):
        context_dict = {"head":{}, "body":{}}
        try:
            
            blog_id = kwargs.get("blog_id")
            serializer = CommentsSerializer(data=request.data)
            
            if serializer.is_valid():
                # create comments
                Comments.objects.create(text=serializer.validated_data.get("text"), blog_id=blog_id, user=request.user)
                context_dict['body']['message'] = "successfully added comment"
                context_dict["head"]["status"] = 0
                context_dict["head"]["message"] = "success"
                return Response(context_dict)
                
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Failed"
            
        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Failed"
            
        return Response(context_dict)

# API called when a blog is liked
class LikeBlog(APIView):
    def post(self, request, *args, **kwargs):
        context_dict = {"head":{}, "body":{}}
        try:
            
            blog_id = kwargs.get("blog_id")
            
            # get blog
            blog_obj = Blog.objects.filter(pk=blog_id).first()
            if blog_obj:
                # increment likes of the blog
                if not blog_obj.likes:
                    blog_obj.likes = 0
                    
                blog_obj.likes += 1
                    
                blog_obj.save()
                
                context_dict['body']['message'] = "successfully Liked"
                context_dict["head"]["status"] = 0
                context_dict["head"]["message"] = "success"
            else:
                context_dict["head"]["status"] = 2
                context_dict["head"]["message"] = "Failed"
        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Failed"
            
        return Response(context_dict)

# when user logged in, return its token for accessing authentication urls.
class UserLogin(APIView):
    @method_decorator(cache_page(60*15))
    def post(self,request):
        try:
            context_dict = {"head":{}, "body":{}}
            
            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                # successfully logged in.
                # fetch token or create 
                token, created = Token.objects.get_or_create(user=user)
                context_dict["head"]["status"] = 0
                context_dict["head"]["message"] = "successfully logged in"
                
                context_dict["body"]["token"] = token.key
                
            else:
                # Return an 'invalid login' error message.
                context_dict["head"]["status"] = 2
                context_dict["head"]["message"] = "Invalid Username or password"
        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Invalid Username or password"
        
        return Response(context_dict)
            
# create new users, User signup
class UserSignUp(APIView):
    @method_decorator(cache_page(60*15))
    def post(self, request):
        try:
            context_dict = {"head":{}, "body":{}}
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            if not username or not email or not password:
                context_dict["head"]["status"] = 2
                context_dict["head"]["message"] = "username, email and password is required"
                return Response(context_dict)

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)

            token, created = Token.objects.get_or_create(user=user)

            context_dict["body"]["token"] = token.key
            context_dict["head"]["status"] = 0
            context_dict["head"]["message"] = "Account successfully created"
        except Exception as e:
            logger.exception(e)
            context_dict["head"]["status"] = 2
            context_dict["head"]["message"] = "Unable to signup"

        return Response(context_dict)
