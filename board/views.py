from django.shortcuts import render

# Create your views here.
# 2015244044 이준희
from django.shortcuts import render,redirect, get_object_or_404,Http404
from .forms import *
from django.utils import timezone
from board.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
NUM_ITEMS = 5

# 자유게시판 목록
def post_list(request):
    borads = Post.objects.all()
    list = request.GET.get('list')
    if list:
        borads =borads.filter(title__contains = list)
    page = request.GET.get('page', 1)
    paginator = Paginator(borads.order_by('-created_at'), NUM_ITEMS)
    try:
        borads = paginator.page(page)
    except PageNotAnInteger:
        borads = paginator.page(1)
    except EmptyPage:
        borads = paginator.page(paginator.num_pages)
    return render(request,"post_list.html",{'item_page_offset': borads.paginator.num_pages - borads.number,"borads":borads})

#자유게시판 생성
@login_required
def post_create(request):
    if request.method=="POST":
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.author=request.user
            post.save()
            return redirect('post_list')
    elif request.method=="GET":
        form = Postform()
        return render(request, "post_create.html",{"form":form})

#자유게시판 목록
@login_required
def post_detail(request,id):
    post = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(post=post.id)
    return render(request,"post_detail.html",{"post":post,"comments":comments})

#자유게시판 수정하기
@login_required
def post_update(request,id):
    if request.method == "GET":
        post = get_object_or_404(Post, pk=id)
        form = Postform(instance=post)
        return render(request, "post_update.html",{"form":form,"post":post})
    elif request.method == "POST":
        post = get_object_or_404(Post, pk=id)
        form = Postform(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect("post_detail",id)
    return Http404()

#자유게시판 삭제
@login_required
def post_delete(request,id):
    post = get_object_or_404(Post,pk=id)
    if post.author != request.user:
        return redirect("main")
    post.delete()
    return redirect("post_list")

#댓글 생성
@login_required
def comment_create(request,id):
    if request.method=='POST':
        comment = Comment()
        comment.message = request.POST["message"]
        comment.post = get_object_or_404(Post, pk=id)
        comment.author = request.user
        comment.save()        
        return redirect("post_detail",id)
    return redirect("post_detail",id)

#댓글 삭제
@login_required
def comment_delete(request,id):
    comment = get_object_or_404(Comment,pk=id)
    if comment.author != request.user:
        return redirect("post_list")
    if request.method=='POST':
        comment_pk=comment.post.id
        comment.delete()
        return redirect("post_detail",comment_pk)
    return redirect("post_detail",comment_pk)
    
#댓글 수정
@login_required
def comment_update(request, id):
    comment=get_object_or_404(Comment, pk=id)   
    if comment.author != request.user:
        return redirect("index")
    if request.method=='POST':
        comment.message=request.POST["message"]
        comment_pk=comment.post.pk
        comment.save()
        return redirect("post_detail", id=comment_pk)
    elif request.method == 'GET':
        return render(request, "comment_update.html", {"comment": comment})

#문의하기 목록
def secret_list(request):
    secrets = SecretBorad.objects.all()
    list = request.GET.get('list')
    if list:
        secrets = secrets.filter(title__contains = list)
    page = request.GET.get('page', 1)
    paginator = Paginator(secrets.order_by('-created_at'), NUM_ITEMS)
    try:
        secrets = paginator.page(page)
    except PageNotAnInteger:
        secrets = paginator.page(1)
    except EmptyPage:
        secrets = paginator.page(paginator.num_pages)
    return render(request,"secret_list.html",{"secrets":secrets,'item_page_offset': secrets.paginator.num_pages - secrets.number})

#문의하기 생성
@login_required
def secret_create(request):
    if request.method=="POST":
        form = SecretForm(request.POST, request.FILES)
        if form.is_valid():
            secret = form.save(commit=False)
            secret.created_at = timezone.now()
            secret.author=request.user
            secret.save()
            return redirect('secret_list')
    elif request.method=="GET":
        form = SecretForm()
        return render(request, "secret_create.html",{"form":form})

#문의하기 자세히보기
@login_required
def secret_detail(request,id):
    secret = get_object_or_404(SecretBorad, pk=id)
    secretcomments = SecretComment.objects.filter(secretborad=secret.id)
    if secret.private and secret.author != request.user:
        messages.error(request, '비밀글은 글 작성자만 볼 수 있습니다.')
        return redirect('secret_list')
    else:
        return render(request,"secret_detail.html",{"secret":secret,"secretcomments":secretcomments})

#문의하기 삭제
@login_required
def secret_delete(request,id):
    secret = get_object_or_404(SecretBorad,pk=id)
    if secret.author != request.user:
        return redirect("main")
    secret.delete()
    return redirect("secret_list")
