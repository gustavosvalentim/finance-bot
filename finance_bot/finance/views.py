from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from finance_bot.finance import models, serializers


@extend_schema(tags=['Users'])
class UserViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


@extend_schema(tags=['Categories'])
class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


@extend_schema(tags=['Goals'])
class GoalViewSet(ModelViewSet):
    queryset = models.Goal.objects.all()
    serializer_class = serializers.GoalSerializer


@extend_schema(tags=['Transactions'])
class TransactionViewSet(ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
