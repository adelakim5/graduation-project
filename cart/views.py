from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from food.models import Food
from .cart import Cart
from .forms import AddToCartForm
# Create your views here.

@require_POST
def add_food(request, food_id):
    food = Food.objects.filter(pk=food_id)
    if food.exists():
        cart = Cart(request)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # type_list = request.POST.getlist['choices']
            # filter로 객체 가져옴. 그 객체를 사용할 때는 객체 뒤에 '[0]'을 붙여야 함
            cart.add(food=food[0], quantity=cd['quantity'], is_update=cd['is_update'])
            # choices=type_list[c]
        print(cart.cart.values())
        return redirect('cart_detail')

def remove_food(request, food_id):
    food = Food.objects.filter(pk=food_id)
    if food.exists():
        cart = Cart(request)
        cart.remove(food[0])
    return redirect('cart_detail')

def cart_detail(request):
    # 장바구니에 담겨있는 제품 목록 띄우기, 제품 수량 수정, 지우기, 장바구니 비우기 버튼 구현
    cart = Cart(request)
    for food in cart:
        food['quantity_form']=AddToCartForm(initial={'quantity':food['quantity'], 'is_update':True})
    continue_url = "/"
    # 현재 페이지 주소 얻기
    # 1) request.build_absolute_uri('?') : 쿼리스트링 없이 현재 페이지 주소 얻기
    # 2) request.build_absolute_uri() : 쿼리스트링까지 얻어오기
    current_url = request.build_absolute_uri('?')
    if 'HTTP_REFERER' in request.META and current_url != request.META['HTTP_REFERER']:
        # 이전 페이지로 이동하는 current_url 설정하기
        continue_url = request.META['HTTP_REFERER']
    return render(request, 'cart_detail.html', {'cart':cart, 'continue_url':continue_url})