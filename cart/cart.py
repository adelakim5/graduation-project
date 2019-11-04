from django.conf import settings
from food.models import Food

# https://chohyeonkeun.github.io/2019/06/16/190616-django-cart-function/
# product => food

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            # 세션에 없던 키 값을 생성하면 자동 저장
            cart = self.session[settings.CART_ID]={}
            # 세션에 이미 있는 키 값에 대한 값을 수정하면 수동으로 저장
        self.cart = cart

    def __len__(self):
        # 요소가 몇개인지 갯수를 반환해주는 함수
        """
        id:실제제품
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        # for문 같은 문법을 사용할 때 안에 있는 요소를 어떤 형태로 반환할 것인지 결정하는 함수
        food_ids = self.cart.keys()
        foods = Food.objects.filter(id__in=food_ids)
    
        for food in foods:
            self.cart[str(food.id)]['food'] = food
    
        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def add(self, food, quantity=1, is_update=False):
        food_id = str(food.id)
        if food_id not in self.cart:
            # 만약 제품 정보가 decimal이면 세션에 저장할때는 str로 형변환 해서 저장하고
            # 꺼내올 때는 decimal로 형변환해서 사용해야 한다.
            self.cart[food_id] = {'quantity':0, 'price':food.price}
        if is_update:
            self.cart[food_id]['quantity'] = quantity
        else:
            self.cart[food_id]['quantity'] += quantity
        self.save()
    
    def remove(self, food):
        food_id = str(food.id)
        if food_id in self.cart:
            del(self.cart[food_id])
        self.save()
    
    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True
    
    def clear(self):
        self.cart = {}
        self.save()
    
    # 전체 가격
    def get_total_price(self):
        return sum(item['quantity']*item['price'] for item in self.cart.values())

