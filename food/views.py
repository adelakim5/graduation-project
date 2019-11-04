from django.shortcuts import render, get_object_or_404, redirect
from .models import Food, Comment
from django.core.paginator import Paginator
from django.utils import timezone 
from .forms import FoodPost, CommentForm
from cart import forms
from decimal import Decimal
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    foods = Food.objects
    food_list = Food.objects.all()
    print(type(food_list))
    paginator = Paginator(food_list,4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'foods':foods, 'posts':posts})

def detail(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    return render(request, 'detail.html', {'food':food_detail})


# class FoodDetail(DetialView):
#     model = Food
#     template_name = 'detail.html'

    def get_contenxt_data(self, **kwargs):
        form = AddToCartForm()
        kwargs.update({'form':form})
        return super().get_context_data(**kwargs)

@login_required
def add_comment_to_food(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=food_detail)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = food_detail
            comment.save()
            return redirect('detail', food_id=food_id)
        else:
            form = CommentForm(instance=food_detail)
        return render(request, 'comment.html', {'form':form})
        # context_instance=RequestContext(request), 

def foodpost(request):
    if request.method == 'POST':
        form = FoodPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date=timezone.now()
            post.save()
            return redirect('home')
    else:
        form = FoodPost()
    return render(request,'new.html', {'form':form})

def edit(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        form = FoodPost(request.POST, instance=food_detail)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date=timezone.now()
            post.save()
            return redirect('detail', food_id=food_id)
    else:
        form = FoodPost(instance=food_detail)
    return render(request, 'edit.html', {'form':form})        

# def foodAdmin(request):
#     return render(request, 'admin.html')

def search(request):
    search = request.GET['searchkeyword']
    posts = Food.objects.filter(title__icontains=search) | Food.objects.filter(category__icontains=search) | Food.objects.filter(category2__icontains=search) 
    return render(request,'search.html',{'posts':posts})

def delete(request, food_id):
    deleted_food = get_object_or_404(Food, pk=food_id)
    deleted_food.delete()
    return redirect('home')



