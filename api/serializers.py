from os import makedirs, path, remove
from shutil import copyfileobj

from rest_framework import serializers

from .models import Post, PostComments, Sessions, User
from .utils.cript_utils import encrypt, hash_password


class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    content_text = serializers.CharField()
    category = serializers.CharField()
    main_img = serializers.ImageField()
    logo_img = serializers.ImageField()
    creation_date = serializers.DateTimeField(
        input_formats=["iso-8601"], required=False
    )

    def create(self, validated_data):
        creation_date = validated_data.pop("creation_date", None)
        post_instance = Post.objects.create(
            **validated_data, creation_date=creation_date
        )
        folder_name = str(post_instance.id)
        image_path = path.join("media", "post-images", folder_name)
        makedirs(name=image_path, exist_ok=True)
        self.move_uploaded_file(
            uploaded_file=post_instance.logo_img,
            destination_path=path.join(image_path, "logo-img.jpg"),
        )
        self.move_uploaded_file(
            uploaded_file=post_instance.main_img,
            destination_path=path.join(image_path, "main-img.jpg"),
        )
        post_instance.logo_img.name = path.join(
            "post-images", folder_name, "logo-img.jpg"
        )
        post_instance.main_img.name = path.join(
            "post-images", folder_name, "main-img.jpg"
        )
        post_instance.save()
        return post_instance

    def move_uploaded_file(self, uploaded_file, destination_path):
        with open(file=uploaded_file.path, mode="rb") as source:
            with open(file=destination_path, mode="wb") as destination:
                copyfileobj(fsrc=source, fdst=destination)
        remove(path=uploaded_file.path)


class PostCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        validated_data["nickname"] = encrypt(data=validated_data["nickname"])
        validated_data["email"] = encrypt(data=validated_data["email"])
        validated_data["password"] = hash_password(password=validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = "__all__"


class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = "__all__"
