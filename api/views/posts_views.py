from datetime import datetime

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..decorators.response import response_handler
from ..models import Post, PostComments
from ..serializers import PostCommentsSerializer, PostSerializer
from ..utils.cript_utils import decrypt
from ..utils.request_utils import check_not_none
from ..utils.token_utils import AccessToken


class PostListAPIView(APIView):
    @response_handler
    def get(self, request) -> Response:
        all_news = Post.objects.all()
        news_list = []
        for news in all_news:
            comments = PostComments.objects.filter(news=news)
            comments_list = []
            for comment in comments:
                comment_dict = {
                    "commentId": comment.id,
                    "author": decrypt(comment.author.nickname),
                    "authorImg": comment.author.profile_img,
                    "creation_date": comment.creation_date,
                    "text": comment.text,
                }
                comments_list.append(comment_dict)
            news_dict = {
                "id": news.id,
                "title": news.title,
                "category": news.category,
                "date": news.creation_date,
                "text": news.content_text,
                "mainImg": news.main_img.url if news.main_img else None,
                "logoImg": news.logo_img.url if news.logo_img else None,
                "likes": news.likes,
                "comments": comments_list,
            }
            news_list.append(news_dict)
        return Response(news_list)


class PostAddAPIViews(APIView):
    parser_classes = [MultiPartParser]

    @response_handler
    def post(self, request) -> Response:
        title = request.data.get("title", "")
        text = request.data.get("text", "")
        logo_img = request.data.get("logoImg", "")
        main_img = request.data.get("mainImg", "")
        token_req = request.data.get("token", "")
        category = request.data.get("category", "")
        creation_date = datetime.utcnow()
        check_not_none(
            (title, "title"),
            (text, "text"),
            (logo_img, "logoImg"),
            (main_img, "mainImg"),
            (token_req, "token"),
            (category, "category"),
            (creation_date, "creationDate"),
        )

        token = AccessToken(token_value=token_req)
        check_res = token.check()
        try:
            if check_res != 1:
                raise
        except Exception:
            return Response("Token is invalid", status=401)

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
            saved_news = serializer.save()
            # Return created news id
            return Response(saved_news.id, status=201)
        else:
            print(serializer.errors)
            # Return generic error
            return Response("An error occurred", status=400)


class PostCommentsAPIView(APIView):
    @response_handler
    def post(self, request) -> Response:
        news_id = request.data.get("id", "")
        text = request.data.get("text", "")
        token_req = request.data.get("token", "")
        check_not_none((news_id, "id"), (text, "token"), (token_req, "token"))

        token = AccessToken(token_value=token_req)
        try:
            check_res = token.check(get_user=True)
            if check_res.__class__ == int:
                raise
        except Exception:
            return Response("Token is invalid", status=400)

        try:
            news = Post.objects.get(news_id=news_id)
        except Post.DoesNotExist:
            # Return generic error
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
            news.comments.add(serializer.instance)
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
            # Return generic error
            return Response("An error occurred", status=400)
