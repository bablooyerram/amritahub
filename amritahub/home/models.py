from django.db import models
from django.contrib.auth.models import User,Group
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,default=None,unique=True)
    name = models.TextField(default=None, null=True )
    img= models.ImageField(null=True, blank=True, upload_to="home/static/images/")
    dob = models.DateField( null=True)
    phone = models.CharField(max_length=15,default=None,blank=True, null=True)
    country = models.TextField(default=None, null=True)
    count=models.IntegerField(default=0)
    zipcode = models.CharField(max_length=15,default=None,blank=True, null=True)
    state = models.CharField(max_length=15,default=None,blank=True, null=True)
    city = models.CharField(max_length=15,default=None,blank=True, null=True)
    campus = models.CharField(max_length=15,default=None,blank=True, null=True)
    address= models.TextField(default="address", null=True)
    bio=models.TextField(default=None, null=True)

    def __str__(self):
        return self.name

class Activity(models.Model):

    LIKE = 'L'
    COMMENT='C'
    ACTIVITY_TYPES = (
        (LIKE, 'Like'),
        (COMMENT,'Comment')

    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    comment=models.TextField(default=None, null=True )

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()






class Post(models.Model):
    username = models.ForeignKey(Profile, on_delete=models.CASCADE,default=None)
    caption = models.TextField(default=None, null=True )
    img= models.ImageField(null=True, blank=True, default=None, upload_to="home/static/images/")
    date = models.DateTimeField( default=datetime.now)
    postactivity=GenericRelation(Activity)
    Location = models.TextField(default=None, null=True)
    count=models.IntegerField(default=0)







class Friendactivity(models.Model):

    FRIEND = 'F'
    BLOCK='B'
    ACTIVITY_TYPES = (
        (BLOCK, 'Block'),
        (FRIEND,'Friend')

    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    name=models.TextField(default=None, null=True )

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()




class friendlist(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE,default=None)
    friends=GenericRelation(Friendactivity)
    date = models.DateTimeField(auto_now_add=True)


class friendrequest(models.Model):
    From_user=models.ForeignKey(Profile, related_name="requested_user_profile", primary_key=True, on_delete=models.CASCADE,default=None)
    To_user= models.ForeignKey(Profile, related_name="assigned_user_profile", on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)

class Events(models.Model):
    SESSION = 'S'
    WORKSHOP = 'B'
    TYPES = (
        (SESSION, 'Session'),
        (WORKSHOP, 'Workshop')

    )
    Owner=models.ForeignKey(Profile, on_delete=models.CASCADE,default=None)
    Name=models.TextField(default=None, null=True,unique=True)
    date=models.DateTimeField( null=False)
    Description=models.TextField(default=None, null=False)
    type=models.CharField(max_length=1, choices=TYPES)
    public=models.BooleanField(default=True)
    venue=models.TextField(default=None, null=False)


class Groupprofile(models.Model):
    groupname = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, unique=True)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE,default=None)
    DP = models.ImageField(null=True, blank=True, upload_to="home/static/images/")
    Dateofcreation = models.DateTimeField(auto_now_add=True)

    count = models.IntegerField(default=0)


class messages(models.Model):
    pass


class groupmessages(models.Model):
    pass