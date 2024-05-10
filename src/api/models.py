from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.BinaryField(unique=True)
    nickname = models.BinaryField(unique=True)
    password = models.BinaryField()
    info = models.TextField(null=True, default="")
    role = models.CharField(
        max_length=20, choices=[("user", "User"), ("admin", "Admin")], default="user"
    )
    active = models.BooleanField(default=True)
    profile_img = models.TextField(null=True, default="/media/user-images/default.svg")


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(default="")
    category = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateField()
    content_text = models.TextField()
    main_img = models.ImageField(upload_to="post-images/")
    logo_img = models.ImageField(upload_to="post-images/")
    likes = models.IntegerField(default=0)
    comments = models.ManyToManyField("PostComments", default=[])


class PostComments(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    text = models.TextField()


class Sessions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
