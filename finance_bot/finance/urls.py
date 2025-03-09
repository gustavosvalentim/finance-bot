from django.urls import path, include
from rest_framework.routers import DefaultRouter

from finance_bot.finance import views


router = DefaultRouter()

router.register(r'categories', views.CategoryViewSet)
router.register(r'subcategories', views.SubcategoryViewSet)
router.register(r'goals', views.GoalViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
