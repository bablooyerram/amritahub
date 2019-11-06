from django.contrib.auth import authenticate, login,logout

from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .form import *
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render, get_object_or_404
from amritahub import settings

def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            loguser=request.user
            userprofile = Profile.objects.get(username=loguser)
            friends=friendlist.objects.get(user=userprofile)
            friends=friends.friends.filter(activity_type='F')
            friend=[]
            for po in friends:
                friend.append(po.user)
            friend.append(userprofile)
            post = Post.objects.filter(username__in=friend).order_by('date')
            postid = {}
            for po in post:
                a = po.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
                if a:
                    postid[po.id] = 1
                else:
                    postid[po.id] = 0


            return render(request, 'home.html',{ 'user' : user  , 'profile' : userprofile , 'post' : post , 'friends':friends , 'likes': postid})
        # Redirect to a success page.
        else:
            return render(request,"login.html",{ 'message': 'Wrong credentials'} )


    else:
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            loguser = request.user
            userprofile = Profile.objects.get(username=loguser)
            friends = friendlist.objects.get(user=userprofile)
            friends = friends.friends.filter(activity_type='F')
            friend = []
            for po in friends:
                friend.append(po.user)
            friend.append(userprofile)
            post = Post.objects.filter(username__in=friend).order_by('-date')
            postid = {}
            for po in post:
                a = po.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
                if a:
                    postid[po.id] = 1
                else:
                    postid[po.id] = 0

            return render(request, 'home.html',
                          {'user': loguser, 'profile': userprofile, 'post': post, 'friends': friends, 'likes': postid})



def logout1(request):
    logout(request)
    request.session['emailid']=''
    request.session['user']=''
    return render(request, 'login.html',{'message':'logout successful'})


def forgot(request):
    if request.method == 'POST':
        ema = request.POST['email']
        if (User.objects.filter(email=ema).exists()):

            user = User.objects.get(email=ema)
            data = {'new_password1': request.POST['password'],
                'new_password2': request.POST['password2']}
            form = SetPasswordForm(user, data)
            if form.is_valid():
                form.save()
                return render(request, "login.html", {'message': 'password successfully changed.'})
            else:
                return render(request, 'resetpassword.html',{'message': 'Password change unsuccessful. Please try again'})
        else:
            return render(request, "resetpassword.html", {'message': 'User with specified email doesnot exist'})
    else:
        return render(request, 'resetpassword.html')






def signup1(request):
    if request.method == 'POST':
        ema= request.POST['email']
        use=request.POST['username']
        data = {'username': request.POST['username'], 'email': request.POST['email'],
                'password1': request.POST['password'],
                'password2': request.POST['password2']}
        if (User.objects.filter(email=ema).exists()):
            return render(request, 'signup.html', {'message': 'email already exists'})
        if (User.objects.filter(username=use).exists()):
            return render(request, 'signup.html', {'message': 'username already exists'})


        print(data)
        form = SignUpForm(data)


        if form.is_valid():
            form.save()
            user_in= User.objects.get(email=ema)
            profile=Profile.objects.create(username=user_in,name=user_in.username,count=0)
            friend=friendlist.objects.create(user=profile)







            return redirect('/home/')
        else:
            return render(request, 'signup.html', {'message': 'password doesnt meet the given constraints'})
    else:

        return render(request, 'signup.html')




def profilepage(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        post = Post.objects.filter(username=userprofile)
        return render(request, 'profile.html', {'user': request.user, 'profile': userprofile, 'post':post})




def profileEDIT(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        if request.method == 'POST':
            loguser = request.user
            userprofile = Profile.objects.get(username=loguser)
            loguser.email=request.POST['email']
            userprofile.name=request.POST['name']
            userprofile.city = request.POST['city']
            userprofile.state = request.POST['state']
            userprofile.zipcode = request.POST['zipcode']
            userprofile.campus = request.POST['campus']
            userprofile.phone = request.POST['phone']
            userprofile.dob = request.POST['dob']
            userprofile.bio = request.POST['bio']
            userprofile.address = request.POST['address']
            if 'proimage' in request.FILES:

                userprofile.img=request.FILES['proimage']
            loguser.save()
            userprofile.save()

            return redirect('/profile/')
        else:
            loguser = request.user
            userprofile = Profile.objects.get(username=loguser)
            return render(request, 'proedit.html', {'user': request.user, 'profile': userprofile})


def messages(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        return render(request, 'message.html', {'user': request.user, 'profile': userprofile })


def event(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        return render(request, 'events.html', {'user': request.user, 'profile': userprofile })

def friends(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')

        return render(request, 'friends.html', {'user': request.user, 'profile': userprofile,'friends':friends })


def photos(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        return render(request, 'photos.html', {'user': request.user, 'profile': userprofile })


def uploadphoto(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        post = Post.objects.filter(username=userprofile)
        if request.method == 'POST':


            if 'fileInput' in request.FILES:

                fileinput=request.FILES['fileInput']

                caption = request.POST['caption']
                currentpost = Post.objects.create(caption=caption,img=fileinput, username=userprofile, country='india')
                currentpost.save()

            else:

                caption = request.POST['caption']
                currentpost = Post.objects.create(caption=caption,username=userprofile,country='india')
                currentpost.save()
            post = Post.objects.filter(username=userprofile)
            return redirect('/home/')
        else:
            return redirect('/home/')





def likepost(request,postid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        post=Post.objects.get(id=postid)
        a = post.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
        if a:
            post.postactivity.filter(user=userprofile, activity_type=Activity.LIKE).delete()
        else:
            post.postactivity.create(activity_type=Activity.LIKE, user=userprofile)

        return redirect('/home/')


'''def comments(request, oid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        post = Post.objects.filter(username=userprofile)
        '''




