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

# 서비스 개요

본 서비스는 크라우드 펀딩 기능을 제공합니다. 게시자는 크라우드 펀딩을 받기위한 상품(=게시물)을 등록합니다.

유저는 해당 게시물의 펀딩하기 버튼을 클릭하여 해당 상품 ‘1회펀딩금액’ 만큼 펀딩합니다.

# 요구사항

- [x] 상품 등록 : `제목`, `게시자명`, `상품설명`, `목표금액`, `펀딩종료일`, `1회펀딩금액`로 구성
- [x] 상품 수정 : 단, 모든 내용이 수정 가능하나 `목표금액`은 수정이 불가능합니다.
- [x] 상품 삭제 : DB에서 삭제됩니다.
- [x] 상품 목록 : `제목`, `게시자명`, `총펀딩금액`, `달성률` 및 `D-day(펀딩 종료일까지)` 가 포함되어야 합니다.
  - [x] 상품 검색 : (상품 리스트 API 에 ?search=취미 조회 시 ,제목에  ‘내 취미 만들..’  ‘취미를 위한 ..’ 등 검색한 문자 포함된 상품 리스트만 조회)
  - [x] 상품 정렬 : `생성일기준`, `총펀딩금액` 두 가지 정렬이 가능해야합니다. `?order_by=생성일` / `?order_by=총펀딩금액`
  - [x] (`달성률`: 1,000,000원 목표금액 일때,  총 펀딩금액이 5,000,000원 이면 500%, 소수점 무시)
- [x] : 상품 상세 페이지 : `제목`, `게시자명`, `총펀딩금액`, `달성률`, `D-day(펀딩 종료일까지)`, `상품설명`, `목표금액`  및 `참여자 수` 가 포함되어야 합니다.

# 구현 과정

## Strat Project

과제 설명의 필수 기술요건에서 `REST API(Json response)`로 구현하라고 명시되었기에 Django Rest Framework를 활용해야겠다고 생각했다. 

그리고 효율적인 git commit 메시지 컨벤션을 위해 git commit template을 수정했다. 이후 Project를 만들고 `pipenv`로 가상환경을 세팅했다.

서비스 개요와 요구사항을 보면서 상품 CURD를 담당할 `products` app, 사용자 모델링을 위한 `users` app이 필요하다고 생각했다.


## users

`products` app에서 모델링을 하던 중, 각 상품의 게시자를 ForeignKey로 연결하여 1:N관계를 표현하기 위해서 `users` app을 먼저 구현해야 함을 깨달았다. 

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

### users/serializers.py

```python
# users/serializers.py
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['pk','username','gender','created_at','updated_at']
```

ModelSerializer를 상속받아 `UserSerializer` 클래스를 생성했고 직렬화해야 할 fields를 설정했다. 

### users/views.py

```python
# users/views.py
class UserViewSet(ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "destroy" or self.action == "partial_update":
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
```

인증, 권한 등은 평가요소에 포함되지 않아서 커스텀할 것이 별로 없다고 생각하여 ModelVieset을 이용해 `UserViewSet` 클래스를 생성하고, `queryset`과 `seriializer_class`를 설정했다. 

인증, 권한 관련 항목은 평가요소에 들어가지 않지만, 최소한의 구현을 위해 user 삭제와 수정은 인증된 사용자만 가능하고 나머지는 조회만 가능하도록 `IsAuthenticatedOrReadOnly`를 permission_classes로 지정했다.

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

- `v1/users` : users 목록 조회 및 생성('get':'list', 'post':'create')
- `v1/users/<int:pk>` : users 상세 및 수정, 삭제('get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy')

## products

### products/models.py

Model을 상속받아 `Product` 클래스 생성하고 `title(게시자명)`, `publisher(게시자명)`, `description(상품설명)`, `goal_amount(목표금액)`, `closing_date(펀딩종료일)`, `onetime_funding_amount(1회펀딩금액)`, `total_funding_amount(총펀딩금액)` fields 작성

`publisher`는 ForeignKey로 `User` 지정

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

상세 페이지에서 참여자 수를 나타내기 위해 `supporter` fields를 ManyToMany로 지정하고 count를 위해 `supporter_count` 함수 작성 

D-day 구현을 위해 `d_day` 함수 작성
datetime 라이브러리 활용하여 오늘 날짜인 `now`를 만들고 closing_date - now로 D-day를 구현하려 했지만,  `closing_date`는 DateField로 `now`와 type이 달라서 연산이 불가.

그래서 `closing_date`의 년,월,일을 '-'로 구분하여 나누고 datetime type으로 `target_day` 생성 후 D-day 구현

달성률을 구현하기 위해 `funding_rate` 함수 작성, f-string으로 소수점 제외하고 %가 표기되도록 구현

### products/serializers.py

### products/views.py






