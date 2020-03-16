from django.contrib.auth import authenticate, login,logout
from django.utils import timezone
from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .form import *
from django.db.models import Q
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render, get_object_or_404
from amritahub import settings
from django.http import HttpResponseRedirect

def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            loguser=request.user
            userprofile = Profile.objects.get(username=loguser)
            if userprofile.count==0:
                return redirect('/proedit/')
            else:
                friends=friendlist.objects.get(user=userprofile)
                friends=friends.friends.filter(activity_type='F')
                requests=friendrequest.objects.filter(To_user=userprofile)
                if requests:
                    requests=requests[0]


                now = timezone.now()
                upcoming = Events.objects.filter(date__gte=now).order_by('date')
                event=upcoming[0]
                friend=[]
                for po in friends:
                    friend.append(po.user)

                friend.append(userprofile)


                post = Post.objects.filter(username__in=friend).order_by('date')
                comments={}
                postid = {}
                for po in post:
                    a = po.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
                    comments[po.id] = po.postactivity.filter(activity_type=Activity.COMMENT)
                    if a:
                        postid[po.id] = 1
                    else:
                        postid[po.id] = 0


                return render(request, 'home.html',{ 'user' : user  , 'profile' : userprofile , 'post' : post , 'friends':friends ,'event':event, 'likes': postid,'comments':comments,'requests':requests})
        # Redirect to a success page.
        else:
            return render(request,"login.html",{ 'message': 'Wrong credentials'} )


    else:
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            loguser = request.user
            userprofile = Profile.objects.get(username=loguser)
            if userprofile.count==0:
                return redirect('/proedit/')
            else:
                friends = friendlist.objects.get(user=userprofile)
                friends = friends.friends.filter(activity_type='F')
                requests = friendrequest.objects.filter(To_user=userprofile)
                if requests:
                    requests=requests[0]


                now = timezone.now()
                upcoming = Events.objects.filter(date__gte=now).order_by('date')
                event = upcoming[0]
                friend = []
                for po in friends:
                    friend.append(po.user)

                friend.append(userprofile)

                post = Post.objects.filter(username__in=friend).order_by('-date')
                postid = {}
                comments = {}
                for po in post:
                    a = po.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
                    comments[po.id] = po.postactivity.filter(activity_type=Activity.COMMENT)
                    if a:
                        postid[po.id] = 1
                    else:
                        postid[po.id] = 0

                return render(request, 'home.html',
                              {'user': loguser, 'profile': userprofile, 'post': post, 'friends': friends, 'event': event , 'likes': postid,'comments':comments,'requests':requests})



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
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])







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
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')
        requests = friendrequest.objects.filter(To_user=userprofile)
        if requests:
            requests = requests[0]

        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        event = upcoming[0]
        friend = []
        for po in friends:
            friend.append(po.user)

        friend.append(userprofile)


        post = Post.objects.filter(username=userprofile).order_by('-date')
        postid = {}
        comments = {}
        for po in post:
            a = po.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
            comments[po.id] = po.postactivity.filter(activity_type=Activity.COMMENT)
            if a:
                postid[po.id] = 1
            else:
                postid[po.id] = 0

        return render(request, 'profile.html',
                      {'user': request.user, 'profile': userprofile, 'post': post,'event':event, 'friends': friends, 'likes': postid,'comments':comments,'requests':requests})







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
            userprofile.count=1
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
        now = timezone.now()
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')
        requests = friendrequest.objects.filter(To_user=userprofile)
        if requests:
            requests = requests[0]

        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        event = upcoming[0]
        friend = []
        for po in friends:
            friend.append(po.user)



        upcoming = Events.objects.filter(date__gte=now).order_by('date')

        event = upcoming[0]

        return render(request, 'eventlist.html', {'user': request.user, 'profile': userprofile, 'events': upcoming,'event':event ,'requests':requests})


def addevent(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        if request.method == 'POST':
            loguser = request.user
            userprofile = Profile.objects.get(username=loguser)
            name= request.POST['name']
            date=request.POST['date']
            desc=request.POST['description']
            type=request.POST['evttype']
            venue=request.POST['venue']
            a=Events.objects.create(Name=name,Owner=userprofile,date=date,Description=desc,type=type,venue=venue)
            a.save()
            return redirect('/event/')


        else :
            loguser = request.user
            userprofile = Profile.objects.get(username=loguser)
            friends = friendlist.objects.get(user=userprofile)
            friends = friends.friends.filter(activity_type='F')
            requests = friendrequest.objects.filter(To_user=userprofile)
            if requests:
                requests = requests[0]

            now = timezone.now()
            upcoming = Events.objects.filter(date__gte=now).order_by('date')
            event = upcoming[0]
            friend = []
            for po in friends:
                friend.append(po.user)

            friend.append(userprofile)


            now = timezone.now()
            upcoming = Events.objects.filter(date__gte=now).order_by('date')

            event = upcoming[0]
            return render(request, 'events.html', {'user': request.user, 'profile': userprofile, 'event':event  ,'requests':requests})

def friends(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')
        requests = friendrequest.objects.filter(To_user=userprofile)

        req=friendrequest.objects.filter(From_user=userprofile)
        list = []

        for po in req:
            list.append(po.To_user.id)
        for po in requests:
            list.append(po.From_user.id)
        if requests:
            requests = requests[0]

        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        event = upcoming[0]
        friend = []
        for po in friends:
            friend.append(po.user)
            list.append(po.user.id)

        list.append(userprofile.id)
        persons = Profile.objects.filter(~Q(id__in=list))
        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        friend = []
        for po in friends:
            friend.append(po.user)

        event = upcoming[0]

        return render(request, 'friends.html', {'user': request.user, 'profile': userprofile,'friends': friend,'event':event ,'persons':persons,'requests':requests})


def photos(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')
        requests = friendrequest.objects.filter(To_user=userprofile)
        if requests:
            requests = requests[0]


        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        post = Post.objects.filter(username=userprofile).order_by('date')


        event = upcoming[0]
        return render(request, 'photos.html', {'user': request.user, 'profile': userprofile,'event':event, 'photos':post ,'requests':requests})


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
                currentpost = Post.objects.create(caption=caption,img=fileinput, username=userprofile, Location='india')
                currentpost.save()

            else:

                caption = request.POST['caption']
                currentpost = Post.objects.create(caption=caption,username=userprofile,Location='india')
                currentpost.save()
            post = Post.objects.filter(username=userprofile)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





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

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def commentpost(request,postid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        post=Post.objects.get(id=postid)
        comment=request.POST['comments']

        post.postactivity.create(activity_type=Activity.COMMENT,comment=comment, user=userprofile)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deletepost(request,postid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        post=Post.objects.get(id=postid)
        post.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def friendprofile(request,userid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        friendpro=Profile.objects.get(id=userid)
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')
        requests = friendrequest.objects.filter(To_user=userprofile)
        if requests:
            requests = requests[0]


        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        event = upcoming[0]
        friend = []
        for po in friends:
            friend.append(po.user)

        friend.append(userprofile)


        post = Post.objects.filter(username=friendpro).order_by('-date')
        postid = {}
        comments = {}
        for po in post:
            a = po.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
            comments[po.id] = po.postactivity.filter(activity_type=Activity.COMMENT)
            if a:
                postid[po.id] = 1
            else:
                postid[po.id] = 0

        return render(request, 'friendprofile.html',
                      {'user': request.user, 'profile': userprofile, 'friendpro':friendpro, 'post': post, 'event': event, 'friends': friends,
                       'likes': postid,'requests':requests,'comments':comments})





def friendreq(request,id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        touser=Profile.objects.get(id=id)
        A=friendrequest.objects.create(From_user=userprofile,To_user=touser)
        A.save()
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')
        requests = friendrequest.objects.filter(To_user=userprofile)

        req = friendrequest.objects.filter(From_user=userprofile)
        list = []

        for po in req:
            list.append(po.To_user.id)
        for po in requests:
            list.append(po.From_user.id)
        if requests:
            requests = requests[0]

        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        event = upcoming[0]
        friend = []
        for po in friends:
            friend.append(po.user)
            list.append(po.user.id)

        list.append(userprofile.id)
        persons = Profile.objects.filter(~Q(id__in=list))

        event = upcoming[0]
        message="Friend Request Sent to "+touser.name

        return render(request, 'friends.html',
                      {'user': request.user, 'profile': userprofile, 'friends': friend, 'event': event, 'message':message,'persons':persons ,'requests':requests})



def deletereq(request,id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        req=friendrequest.objects.get(id=id)
        req.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def acceptreq(request,id):

    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        req = friendrequest.objects.get(id=id)
        friend1 = friendlist.objects.get(user=req.From_user)
        friend1 = friend1.friends.create(activity_type='F',user=req.To_user,name=req.To_user.name)
        friend2 = friendlist.objects.get(user=req.To_user)
        friend2 = friend2.friends.create(activity_type='F', user=req.From_user, name=req.From_user.name)
        name=req.From_user.name
        userid=req.From_user.id
        req.delete()
        message = name+" is successfully added to your friendlist, press ok to view his profile"
        loguser = request.user
        userprofile = Profile.objects.get(username=loguser)
        friendpro = Profile.objects.get(id=userid)
        friends = friendlist.objects.get(user=userprofile)
        friends = friends.friends.filter(activity_type='F')
        requests = friendrequest.objects.filter(To_user=userprofile)
        if requests:
            requests = requests[0]

        now = timezone.now()
        upcoming = Events.objects.filter(date__gte=now).order_by('date')
        event = upcoming[0]
        friend = []
        for po in friends:
            friend.append(po.user)

        friend.append(userprofile)

        post = Post.objects.filter(username=friendpro).order_by('-date')
        postid = {}
        comments = {}
        for po in post:
            a = po.postactivity.filter(user=userprofile, activity_type=Activity.LIKE)
            comments[po.id] = po.postactivity.filter(activity_type=Activity.COMMENT)
            if a:
                postid[po.id] = 1
            else:
                postid[po.id] = 0

        return render(request, 'friendprofile.html',
                      {'user': request.user, 'profile': userprofile, 'friendpro': friendpro, 'post': post,
                       'event': event, 'friends': friends,
                       'likes': postid, 'requests': requests,'message':message, 'comments': comments})




