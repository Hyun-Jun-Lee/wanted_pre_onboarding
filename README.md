# wanted_pre_onboarding

- [wanted_pre_onboarding](#wanted_pre_onboarding)
- [서비스 개요](#서비스-개요)
- [요구사항](#요구사항)
- [구현 과정](#구현-과정)
  - [Strat Project](#strat-project)
  - [users](#users)
    - [users/models.py](#usersmodelspy)
    - [users/serializers.py](#usersserializerspy)
    - [users/views.py](#usersviewspy)
    - [users/urls.py](#usersurlspy)
  - [products](#products)
    - [products/models.py](#productsmodelspy)
    - [products/serializers.py](#productsserializerspy)
    - [products/views.py](#productsviewspy)
    - [products/urls.py](#productsurlspy)

# 서비스 개요

본 서비스는 크라우드 펀딩 기능을 제공합니다. 게시자는 크라우드 펀딩을 받기위한 상품(=게시물)을 등록합니다.

유저는 해당 게시물의 펀딩하기 버튼을 클릭하여 해당 상품 ‘1회펀딩금액’ 만큼 펀딩합니다.

<br>

# 요구사항

- [x] 상품 등록 : `제목`, `게시자명`, `상품설명`, `목표금액`, `펀딩종료일`, `1회펀딩금액`로 구성
- [x] 상품 수정 : 단, 모든 내용이 수정 가능하나 `목표금액`은 수정이 불가능합니다.
- [x] 상품 삭제 : DB에서 삭제됩니다.
- [x] 상품 목록 : `제목`, `게시자명`, `총펀딩금액`, `달성률` 및 `D-day(펀딩 종료일까지)` 가 포함되어야 합니다.
  - [x] 상품 검색 : (상품 리스트 API 에 ?search=취미 조회 시 ,제목에  ‘내 취미 만들..’  ‘취미를 위한 ..’ 등 검색한 문자 포함된 상품 리스트만 조회)
  - [x] 상품 정렬 : `생성일기준`, `총펀딩금액` 두 가지 정렬이 가능해야합니다. `?order_by=생성일` / `?order_by=총펀딩금액`
  - [x] (`달성률`: 1,000,000원 목표금액 일때,  총 펀딩금액이 5,000,000원 이면 500%, 소수점 무시)
- [x] : 상품 상세 페이지 : `제목`, `게시자명`, `총펀딩금액`, `달성률`, `D-day(펀딩 종료일까지)`, `상품설명`, `목표금액`  및 `참여자 수` 가 포함되어야 합니다.

<br>

# 구현 과정

## Strat Project

과제 설명의 필수 기술요건에서 `REST API(Json response)`로 구현하라고 명시되었기에 Django Rest Framework를 활용해야겠다고 생각했다. 

그리고 효율적인 git commit 메시지 컨벤션을 위해 git commit template을 수정했다. 이후 Project를 만들고 `pipenv`로 가상환경을 세팅했다.

서비스 개요와 요구사항을 보면서 상품 CURD를 담당할 `products` app, 사용자 모델링을 위한 `users` app이 필요하다고 생각했다.

<br>

## users

`products` app에서 모델링을 하던 중, 각 상품의 게시자를 ForeignKey로 연결하여 1:N관계를 표현하기 위해서 `users` app을 먼저 구현해야 함을 깨달았다. 

<br>

### users/models.py

```python
# users/models.py
class User(AbstractUser):
    
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"))
    
    username = models.CharField(max_length=30, unique=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
```

`AbstractUser`를 상속 받아 `User` 클래스를 생성했고 간단하게 `gender`, `username` 필드와 생성일, 수정일을 알기 위한 `created_at`, `updated_at` 필드를 작성했다. 

<br>

### users/serializers.py

```python
# users/serializers.py
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['pk','username','gender','created_at','updated_at']
```

ModelSerializer를 상속받아 `UserSerializer` 클래스를 생성했고 직렬화해야 할 fields를 설정했다. 

<br>

### users/views.py

```python
# users/views.py
class UserViewSet(ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

인증, 권한 등은 평가요소에 포함되지 않아서 커스텀할 것이 별로 없다고 생각하여 ModelVieset을 이용해 `UserViewSet` 클래스를 생성하고, `queryset`과 `seriializer_class`를 설정했다. 

<br>

### users/urls.py

```python
# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include("products.urls")),
    path('v1/', include("users.urls")),
]

# users/urls.py
app_name = "users"

router = DefaultRouter()
router.register("users", views.UserViewSet)

urlpatterns =router.urls
```

- `v1/users` : users 목록 조회 및 생성
- `v1/users/<int:pk>` : users 상세 및 수정, 삭제

<br>

## products

<br>

### products/models.py

```python
# products/models.py
class Product(models.Model):
    
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    
    title = models.CharField(max_length=30)
    description = models.TextField()
    goal_amount = models.IntegerField()
    closing_date = models.DateField()
    onetime_funding_amount = models.IntegerField()
    total_funding_amount = models.IntegerField(default=0)
    
    publisher = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    supporter = models.ManyToManyField("users.User")
    
    def supporter_count(self):
        return self.supporter.count()
    
    def d_day(self):
        now = datetime.date.today()
        spplit = list(map(int,str(self.closing_date).split("-")))
        target_day = datetime.date(spplit[0],spplit[1],spplit[2])
        values = target_day - now
        return values.days
    
    def funding_rate(self):
        return f'{(self.total_funding_amount / self.goal_amount) *100 :.0f}%'
    
    def publisher_username(self):
        return self.publisher.username
```

Model을 상속받아 `Product` 클래스 생성하고 `title(게시자명)`, `publisher(게시자명)`, `description(상품설명)`, `goal_amount(목표금액)`, `closing_date(펀딩종료일)`, `onetime_funding_amount(1회펀딩금액)`, `total_funding_amount(총펀딩금액)` fields 작성

`publisher`는 ForeignKey로 `User` 지정

상세 페이지에서 참여자 수를 나타내기 위해 `supporter` fields를 ManyToMany로 지정하고 count를 위해 `supporter_count` 함수 작성 

D-day 구현을 위해 `d_day` 함수 작성

datetime 라이브러리 활용하여 오늘 날짜인 `now`를 만들고 closing_date - now로 D-day를 구현하려 했지만,  `closing_date`는 DateField로 `now`와 type이 달라서 연산이 불가.
그래서 `closing_date`의 년,월,일을 '-'로 구분하여 나누고 datetime type으로 `target_day` 생성 후 D-day 구현

달성률을 구현하기 위해 `funding_rate` 함수 작성, f-string으로 소수점 제외하고 %가 표기되도록 구현

<br>

### products/serializers.py

- `ProductSerializer`

```python
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'pk',
            'title',
            'publisher',
            'publisher_username',
            'total_funding_amount',
            'funding_rate',
            'd_day',
            'description',
            'goal_amount',
            'closing_date',
            'onetime_funding_amount',
            'supporter_count',
            'created_at',
            'updated_at'
            ]
        read_only_fields = ('total_funding_amount',)
        extra_kwargs = {
            'publisher' : {'write_only':True}
        }
```

상품목록을 조회하고 생성하는 역활을 하는 `ProductListAPIView` 클래스를 직렬화해줄 `ProductSerializer` 작성, 요구사항에 따라 제목, 게시자명, 총펀딩금액, 달성률 및 D-day(펀딩 종료일까지)가 포함

`total_funding_amount` 필드는 직접 작성하는 필드가 아니라 `onetime_funding_amount`의 값 만큼 누적되야 하기 때문에 `read_only_fields`로 지정

`publisher` 필드는 게시자명이 아니라 해당 게시자의 pk를 표시하기 때문에, `publish_username` 필드를 활용하여 게시자명만 나오게하고 상품을 생성할 때 게시자명을 지정할수 있도록 `write_only_fields` 지정

<br>

- `ProductDetailSerializer`

```python
class ProductDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'title',
            'publisher',
            'publisher_username',
            'total_funding_amount',
            'funding_rate',
            'd_day',
            'description',
            'goal_amount',
            'supporter_count',
            'closing_date',
            'onetime_funding_amount',
            'created_at',
            'updated_at'
            ]
        read_only_fields = ('total_funding_amount','goal_amount')
        extra_kwargs = {
            'publisher' : {'write_only':True}
        }
```

상품의 상세페이지를 가져오고 수정 및 삭제하는 역활을 하는 `ProductDetailAPIView` 클래스를 직렬화해줄 `ProductDetailSerializer` 작성

요구사항에 따라 `goal_amount`는 수정이 불가하도록 `read_only_fields` 지정, 나머지는 `ProductSerializer`와 동일

`goal_amount` 빼고는 같은 코드이기 때문에, 두 serializer를 합쳐서 사용 가능한 방법을 찾아서 개선해야함

<br>

- `FundingSerializer`

```python
class FundingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'supporter',
            'goal_amount',
            'supporter_count',
            'total_funding_amount',
            'onetime_funding_amount',
            'funding_rate',
            'd_day',
        ]
        read_only_fields = ('total_funding_amount','goal_amount')
        extra_kwargs = {
            'supporter' : {'write_only':True}
        }
        
    def update(self, instance, validated_data):
        instance.total_funding_amount += instance.onetime_funding_amount
        instance.save()
        return super().update(instance, validated_data)
```

펀딩 기능을 수행하는 `FundingAPIView`를 직렬화해줄 `FundingSerializer` 작성

`total_funding_amount` 필드가 `onetime_funding_amount`의 누적 값으로 구현되도록 `update` 함수 오버라이딩하여 커스텀.

이후 펀딩하며 지정하는 `supporter`의 count가 되지 않아서 `super()` 함수로 부모 클래스 호출

<br>

### products/views.py

- `ProductListAPIView`

```python
class ProductListAPIView(generics.ListCreateAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'total_funding_amount']
```

목록 조회와 생성을 지원하는 `ListCreateAPIVew`를 상속받아서 작성

요구사항에 따라 검색기능 및 정렬 기능을 구현하기 위해 rest_framework.filters 라이브러리에서 `SearchFilter`, `OrderingFilter` 사용하고 `search_fields`와 `ordering_fields` 지정

<br>

- `ProductDetailAPIView`

```python
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product.publisher.username != request.user.username:
            return Response("It's Not Your Room", status=status.HTTP_401_UNAUTHORIZED)
        product.delete()
        return Response("Delete Complete",status=status.HTTP_200_OK)
```

목록 조회, 수정, 삭제를 지원하는 `RetrieveUpdateDestroyAPIView`를 상속받아 작성

상품 게시자와 현재 사용자의 `username`이 같을 때만 상품을 삭제할 수 있도록 `delete` 함수 커스텀

<br>

- `FundingAPIView`

```python
class FundingAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = FundingSerializer
```

목록 조회와 수정을 지원하는 `RetrieveUpdateAPIView`를 상속받아 작성

<br>

### products/urls.py

```python
app_name = "products"

urlpatterns =[
    path("products", views.ProductListAPIView.as_view()),
    path("products/<int:pk>", views.ProductDetailAPIView.as_view()),
    path("products/<int:pk>/funding", views.FundingAPIView.as_view()),
]
```

- `v1/products` : products 목록 조회 및 생성
- `v1/products/<int:pk>` : products 상세 및 수정, 삭제
- `v1/products/<int:pk>/funding` : 펀딩 기능 구현





