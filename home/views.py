from django.shortcuts import render
from django.core.paginator import Paginator
from posts.models import Food

def home(request):
    foods = Food.objects
    food_list = Food.objects.all()
    paginator = Paginator(food_list,4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'foods':foods, 'posts':posts})

def guide(request):
    return render(request, 'guide.html')

#홈화면의 서치바    
def search(request):
    search = request.GET['searchkeyword']
    posts = Food.objects.filter(title__icontains=search) | Food.objects.filter(category__icontains=search) | Food.objects.filter(category2__icontains=search) 
    return render(request,'searchFood.html',{'posts':posts})