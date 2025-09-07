from django.contrib import admin

from finance_bot.finance.models import Category, Transaction


class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_income',)
    search_fields = ('name', 'user__username',)


class CustomTransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'user', 'date',)
    search_fields = ('category__name', 'user__username',)


admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Transaction, CustomTransactionAdmin)
