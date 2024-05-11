from datetime import datetime

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from icecream import ic

from ..decorators.response import response_handler
from ..models import Post, PostComments
from ..serializers import PostCommentsSerializer, PostSerializer
from ..utils.cript_utils import decrypt
from ..utils.request_utils import check_not_none
from ..utils.token_utils import AccessToken, to_message


class PostListAPIView(APIView):
    @response_handler
    def get(self, request) -> Response:
        all_posts = Post.objects.all()
        posts_list = []
        for post in all_posts:
            comments = PostComments.objects.filter(post=post)
            comments_list = []
            for comment in comments:
                comment_dict = {
                    "commentId": comment.id,
                    "author": decrypt(data=comment.author.nickname),
                    "authorImg": comment.author.profile_img,
                    "creation_date": comment.creation_date,
                    "text": comment.text,
                }
                comments_list.append(comment_dict)
            posts_dict = {
                "id": post.id,
                "title": post.title,
                "category": post.category,
                "date": post.creation_date,
                "text": post.content_text,
                "mainImg": post.main_img.url if post.main_img else None,
                "logoImg": post.logo_img.url if post.logo_img else None,
                "likes": post.likes,
                "comments": comments_list,
            }
            posts_list.append(posts_dict)
        return Response(posts_list)


class PostAddAPIViews(APIView):
    parser_classes = [MultiPartParser]

    @response_handler
    def put(self, request) -> Response:
        # TODO Decide what to do with default images
        title = request.data.get("title", "")
        text = request.data.get("text", "")
        logo_img = request.data.get("logoImg", "")
        main_img = request.data.get("mainImg", "")
        access_token_req = request.COOKIES.get("accessToken")
        category = request.data.get("category", "")
        creation_date = datetime.utcnow()
        check_not_none(
            (title, "title"),
            (text, "text"),
            (logo_img, "logoImg"),
            (main_img, "mainImg"),
            (access_token_req, "token"),
            (category, "category"),
            (creation_date, "creationDate"),
        )
        token = AccessToken(token_value=access_token_req)
        check_res = token.check()

        if check_res.__class__ == int:
            return Response(to_message(result_code=check_res), status=401)
        user_role = check_res.role
        if user_role != "admin":
            return Response(data={"message": "You don't have a permission"}, status=400)

        input_data = {
            "title": title,
            "content_text": text,
            "logo_img": logo_img,
            "main_img": main_img,
            "creation_date": creation_date,
            "category": category,
        }
        serializer = PostSerializer(data=input_data)

        if serializer.is_valid():
            saved_post = serializer.save()
            return Response(saved_post.id, status=201)
        else:
            ic(serializer.errors)
            return Response("An error occurred", status=400)


class PostCommentsAPIView(APIView):
    @response_handler
    def put(self, request) -> Response:
        post_id = request.data.get("id", "")
        text = request.data.get("text", "")
        access_token_req = request.COOKIES.get("accessToken")
        check_not_none((post_id, "post_id"), (text, "text"), (access_token_req, "accessToken"))

        access_token = AccessToken(token_value=access_token_req)
        check_res = access_token.check()
        if check_res.__class__ == int:
            return Response(to_message(result_code=check_res), status=401)
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response("An error occurred", status=400)

        user = check_res
        creation_date = datetime.utcnow().date()
        input_data = {
            "author": user.id,
            "creation_date": creation_date,
            "text": text,
        }

        serializer = PostCommentsSerializer(data=input_data)
        if serializer.is_valid():
            serializer.save()
            post.comments.add(serializer.instance)
            return Response(serializer.data, status=201)
        else:
            ic(serializer.errors)
            return Response("An error occurred", status=400)

    def get(self, request):
        # TODO Implement comments for one post with given id only
        pass


class PostDeleteAPIView(APIView):
    @response_handler
    def post(self, request) -> Response:
        # TODO Implement posts deleting by admin by id
        pass
