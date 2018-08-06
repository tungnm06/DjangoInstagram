from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from posts.models import Post
from comments.models import Comment
from images.models import Image
from likes.models import Like
from followings.models import Follow
from notifications.models import Notification
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
import uuid
import json
import os
from django.template import RequestContext
from django.shortcuts import render_to_response
from operator import and_
from django.db.models import Q


# Create your views here.


def create(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password'] and request.POST['fullname'] and request.POST[
            'email'] and request.POST['phone']:
            try:
                customers = Customer.objects.get(username=request.POST['username'])
                return render(request, 'customers/create.html', {'error': 'Tên đăng nhập đã tồn tại'})
            except Customer.DoesNotExist:
                customer = Customer()
                customer.address = ""
                customer.avatar = ""
                customer.email = request.POST['email']
                customer.fullname = request.POST['fullname']
                customer.gender = ""
                customer.info = ""
                customer.password = request.POST['password']
                customer.phone = request.POST['phone']
                customer.status = 1
                customer.username = request.POST['username']
                customer.save()
                follow = Follow()
                follow.cusdetail_id = customer.id
                follow.customer_id = customer.id
                follow.save()
                request.session['username'] = customer.username
            return redirect('/customers/detail/' + str(customer.id))
        else:
            return render(request, 'customers/create.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'customers/create.html')


def detail(request, customer_id):
    if request.session.has_key('username'):
        customer = get_object_or_404(Customer, pk=customer_id)
        posts = Post.objects.filter(customer_id=customer_id).order_by('-createtime')
        user_id = customer_id
        list_customer = Customer.objects.all()
        follows = len(Follow.objects.filter(cusdetail_id=customer_id))
        followings = len(Follow.objects.filter(customer_id=customer_id))
        len_post = len(Post.objects.filter(customer_id=customer_id))
        notifi = Notification.objects.filter(customer_id=customer_id).order_by('-createtime')
        listcm1 = list()
        listcm2 = list()
        listimg1 = list()
        listimg2 = list()
        for post in posts:
            listcm1 = Comment.objects.filter(post_id=post.id)
            listcm2.append(listcm1)
            listimg1 = Image.objects.filter(post_id=post.id)
            for img in listimg1:
                listimg2.append(img)
        return render(request, 'customers/detail.html',
                      {'customer': customer, 'list_customer': list_customer, 'notifi': notifi, 'user_id': user_id,
                       'customer_id': customer_id,
                       'listcm2': listcm2, 'listimg2': listimg2, 'follows': follows, 'followings': followings,
                       'len_post': len_post})
    else:
        return render(request, 'customers/login.html')


def login(request):
    if request.session.has_key('username'):
        username2 = request.session['username']
        cus = Customer.objects.get(username=username2)
        return redirect('/customers/' + 'detail/' + str(cus.id))
    else:
        if request.method == 'POST':
            if request.POST['username'] and request.POST['password']:
                cus = Customer.objects.get(username=request.POST['username'])
                _pass = request.POST['password']
                username = request.POST['username']
                request.session['username'] = username
                request.session.set_expiry(300);
                customer_id = cus.id
                if cus.password == _pass:
                    return redirect('/customers/' + 'detail/' + str(cus.id))
                else:
                    return render(request, 'customers/login.html',
                                  {'error': 'Tên đăng nhập hoặc mật khẩu không đúng !'})
            else:
                return render(request, 'customers/login.html', {'error': 'All fields are required.'})
        else:
            return render(request, 'customers/login.html')


# if request.method == 'POST':
#     if request.POST['username'] and request.POST['password']:
#         cus = Customer.objects.get(username=request.POST['username'])
#         _pass = request.POST['password']
#         customer_id = cus.id
#         if cus.password == _pass:
#             return redirect('/customers/'+ 'detail/'+ str(cus.id))
#
#         else:
#             return render(request, 'customers/login.html', {'error': 'Tên đăng nhập hoặc mật khẩu không đúng !'})
#     else:
#         return render(request, 'customers/login.html', {'error': 'All fields are required.'})
# else:
#     return render(request, 'customers/login.html')


def upload(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST' and request.POST['content']:

        myfile = request.FILES['myfile']
        post = Post()
        post.content = request.POST['content']
        post.createtime = timezone.now()
        post.updatetime = timezone.now()
        post.customer = Customer.objects.get(id=customer_id)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # image = Image()
        post.save()
        for file in request.FILES.getlist('myfile'):
            image = Image()
            post.save()
            image.imageurl = file
            image.post = Post.objects.get(id=post.id)
            image.save()
        # image.imageurl = filename
        # image.post = Post.objects.get(id=post.id)
        # post.save()
        # image.save()
        return redirect('/customers/' + 'detail/' + str(customer_id))
    return render(request, 'customers/detail.html', {
        'customer': customer
    })


def newfeed(request, customer_id):
    if request.session.has_key('username'):
        customer = get_object_or_404(Customer, pk=customer_id)
        customers = Customer.objects
        notifi = Notification.objects.filter(customer_id=customer_id).order_by('-createtime')
        follow = Follow.objects.filter(customer_id=customer_id)
        follow2 = Follow.objects.filter(cusdetail_id=customer_id)
        posts = Post.objects.order_by('-createtime')
        images = Image.objects
        comment2 = Comment.objects
        likes = Like.objects
        namecus = customer.fullname
        dictlike = {'x': [1, 2]}
        dictcmt = {'x': [1, 2]}
        listcmt = []
        listcmt2 = []
        listimg1 = []
        listimg2 = []
        for post in posts.all():
            listimg1 = Image.objects.filter(post_id=post.id)
            listimg2.append(listimg1)
        for post in posts.all():
            listcmt = Comment.objects.filter(post_id=post.id)
            listcmt = listcmt.order_by('-createtime')
            listcmt2.append(listcmt)
        for post in posts.all():
            listlike = Like.objects.filter(post_id=post.id)
            dictlike[post.id] = len(listlike)
        return render(request, 'customers/newfeed.html', {'customer_id': customer_id, 'customer': customer,
                                                          'customers': customers, 'listimg2': listimg2, 'posts': posts,
                                                          'listcmt2': listcmt2, 'likes': likes, 'dictlike': dictlike,
                                                          'namecus': namecus, 'follow': follow, 'user_id': customer_id,
                                                          'notifi': notifi, 'follow2': follow2})
    else:
        return render(request, 'customers/login.html')


def upload_avatar(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        customer.avatar = filename
        customer.save()
        #        uploaded_file_url = fs.url(filename)
        uploaded_file_url = 'hehe'
        return redirect('/customers/detail/' + str(customer.id))

    return render(request, 'customers/detail.html')


def comments(request, post_id, id_customer):
    post = get_object_or_404(Post, pk=post_id)
    customer = get_object_or_404(Customer, pk=id_customer)
    fullname = customer.fullname
    if request.method == 'POST' and request.POST['text']:
        cmt = request.POST['text']
        if len(cmt) <= 1:
            data = {'Erro': "There was an error logging you in. Please Try again"}
            return JsonResponse(data)
    if request.method == 'POST' and request.POST['text']:
        comment = Comment()
        comment.createtime = timezone.now()
        comment.updatetime = timezone.now()
        comment.post = post
        comment.text = request.POST['text']
        comment.customer = customer
        comment.save()
        if id_customer != post.customer.id:
            notifi = Notification()
            notifi.customer_id = post.customer.id
            notifi.customer_user = customer
            notifi.createtime = timezone.now()
            notifi.description = customer.fullname + " đã bình luận bài viết của bạn..."
            notifi.post = post
            notifi.status = 1
            notifi.save()
        newcoments = comment.text
        fullname = customer.fullname
        createtime = comment.createtime
        data = {
            'datacmt': newcoments,
            'dataname': fullname,
            'Erro': "",
            'createtime': str(createtime)
        }
        return JsonResponse(data)
    else:
        data = {'Erro': "There was an error logging you in. Please Try again"}
        return JsonResponse(data)

    #     return  redirect('/customers/newfeed/' +str(customer.id))
    # return render(request, 'customers/newfeed.html')


def like_post(request):
    # if request.method == 'POST':
    post_id = request.POST.get('post_id', False)
    customer_id = request.POST.get('customer_id', False)
    data = {
        'datatrave': customer_id
    }
    return JsonResponse(data)


def like(request):
    post_id = request.POST.get('post_id', False)
    customer_id = request.POST.get('customer_id', False)
    post = Post.objects.get(id=post_id)
    customer = Customer.objects.get(id=customer_id)
    like = Like.objects.filter(post=post, customer=customer_id)
    if like.exists():
        like.delete()
        nlikes = len(Like.objects.filter(post_id=post_id))
        data = nlikes
        notifi2 = Notification.objects.filter(customer_id=customer_id, post_id=post_id, status=2)
        notifi2.delete()

    else:
        like2 = Like()
        like2.customer = customer
        like2.post = post
        like2.save()
        nlikes = len(Like.objects.filter(post_id=post_id))
        data = nlikes
        notifi = Notification()
        notifi.customer_id = post.customer.id
        notifi.createtime = timezone.now()
        notifi.customer_user = customer
        notifi.description = customer.fullname + " đã yêu thích bài viết của bạn..."
        notifi.post = post
        notifi.status = 2
        notifi.save()

    return HttpResponse(data)


def edit(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.address = request.POST['address']
        customer.email = request.POST['email']
        customer.fullname = request.POST['fullname']
        customer.gender = request.POST['gender']
        customer.info = request.POST['info']
        customer.phone = request.POST['phone']
        if request.POST['status'] == 'no':
            customer.status = 1
        if request.POST['status'] == 'yes':
            customer.status = 2
        customer.username = request.POST['username']
        customer.save()
        if customer.status == 2:
            return redirect('/customers/login')
        return redirect('/customers/edit/' + str(customer.id))
    return render(request, 'customers/edit.html', {'customer': customer, 'user_id': customer_id})


def editpass(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        pwOld = request.POST['passwordOld']
        pwNew = request.POST['passwordNew']
        pwConfirm = request.POST['passwordConfirm']
        if pwOld != customer.password:
            return_submit = 'Sai mật khẩu cũ'
            return render(request, 'customers/editpass.html', {'customer': customer,'user_id': customer_id, 'return_submit': return_submit})
        if pwNew != pwConfirm:
            return_submit = 'Mật Khẩu Xác Nhận Không Đúng'
            return render(request, 'customers/editpass.html', {'customer': customer, 'user_id': customer_id, 'return_submit': return_submit})
        if len(pwNew) < 8:
            return_submit = 'Mật Khẩu Quá Ngắn !'
            return render(request, 'customers/editpass.html', {'customer': customer, 'user_id': customer_id, 'return_submit': return_submit})
        customer.password = pwNew
        customer.save()
        return_submit = 'Đổi Mật Khẩu Thành Công !'
        return render(request, 'customers/editpass.html', {'customer': customer,'user_id': customer_id, 'return_submit': return_submit})
    return render(request, 'customers/editpass.html', {'customer': customer, 'user_id': customer_id})


def edit_cmt(request):
    comment_id = request.POST.get('comment_id', False)
    comment = Comment.objects.get(id=comment_id)
    data = comment
    return HttpResponse(data)


def search(request, user_id):
    customer = get_object_or_404(Customer, pk=3)
    customer_dict = {}
    customer_record = []
    if request.method == 'POST':
        query = request.POST.get('q')
        if not query:
            return render(request, 'customers/search.html')
        else:
            results = []
            results1 = []

            results = Customer.objects.filter(username__icontains=query)
            results1 = Customer.objects.filter(fullname__icontains=query)
            if len(results) == 0:
                results = results1;
            for item in results:
                record = {
                    "fullname": item.fullname,
                    "id": item.id,
                    "avarta": str(item.avatar),
                    "user_id": user_id
                }
                customer_record.append(record)
            customer_dict["customer"] = customer_record
            return JsonResponse(customer_dict)
    return render(request, 'customers/search.html')

    #         return render(request, 'customers/search.html', {'customer': customer, 'results': results})
    # else:
    #     return render(request, 'customers/search.html')


def follow(request):
    customerdetail_id = request.POST.get('customerdetail_id', False)
    customer_id = request.POST.get('customer_id', False)
    follow = Follow.objects.filter(customer_id=customer_id, cusdetail_id=customerdetail_id)
    if follow.exists():
        follow.delete()
        nfollow = len(Follow.objects.filter(cusdetail_id=customerdetail_id))
        len_followings = len(Follow.objects.filter(customer_id=customerdetail_id))

        # len_followings = len(Follow.objects.filter(customer=customerdetail_id))
        # data = {
        # 'datatrave' : customer_id}
    else:
        follow2 = Follow()
        follow2.cusdetail_id = customerdetail_id
        follow2.customer_id = customer_id
        follow2.save()
        nfollow = len(Follow.objects.filter(cusdetail_id=customerdetail_id))
        len_followings = len(Follow.objects.filter(customer_id=customerdetail_id))
        data = nfollow

    data = {
        'nfollow': nfollow,
        'len_followings': len_followings
    }
    return HttpResponse(json.dumps(data))


def viewdetail(request, customer_id, user_id):
    if request.session.has_key('username') is False:
        return render(request, 'customers/login.html')
    customer = get_object_or_404(Customer, pk=customer_id)
    posts = Post.objects.filter(customer_id=customer_id).order_by('-createtime')
    notifi = Notification.objects.filter(customer_id=user_id).order_by('-createtime')
    len_follows = len(Follow.objects.filter(cusdetail_id=customer_id))
    follows = Follow.objects.filter(cusdetail_id=customer_id)
    followings = Follow.objects.filter(customer_id=customer_id)
    checkfollow = Follow.objects.filter(cusdetail_id=customer_id,customer_id=user_id )
    if checkfollow.exists():
        check = 'UnFollow'
    else:
        check = 'Follow'
    len_followings = len(Follow.objects.filter(customer_id=customer_id))
    len_post = len(Post.objects.filter(customer_id=customer_id))
    listcm1 = list()
    listcm2 = list()
    listimg1 = list()
    listimg2 = list()
    for post in posts:
        listcm1 = Comment.objects.filter(post_id=post.id)
        listcm2.append(listcm1)
        listimg1 = Image.objects.filter(post_id=post.id)
        for img in listimg1:
            listimg2.append(img)
    return render(request, 'customers/viewdetail.html',
                  {'customer': customer, 'user_id': user_id, 'customer_id': customer_id, 'listcm2': listcm2,
                   'listimg2': listimg2, 'follows': follows,
                   'len_follows': len_follows, 'len_followings': len_followings, 'len_post': len_post, 'notifi': notifi,
                   'followings': followings, 'check': check})


def postdetail(request, user_id, post_id):
    if request.session.has_key('username') is False:
        return render(request, 'customers/login.html')
    id_post = post_id;
    customer = get_object_or_404(Customer, pk=user_id)
    notifi = Notification.objects.filter(customer_id=user_id).order_by('-createtime')
    post = Post.objects.get(id=id_post)
    listlike = Like.objects.filter(post_id=id_post)
    images = Image.objects.filter(post_id=id_post)
    listcmt = Comment.objects.filter(post_id=id_post)
    nlike = len(listlike)
    return render(request, 'customers/postdetail.html',
                  {'customer': customer, 'images': images, 'id_customer': user_id, 'nlike': nlike, 'post': post,
                   'user_id': user_id, 'notifi': notifi, 'post_id': id_post, 'listcmt': listcmt})


def logout(request):
    if request.session.has_key('username'):
        request.session.flush()
    return render(request, 'customers/login.html')
