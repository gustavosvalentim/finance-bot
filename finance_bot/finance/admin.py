from django.contrib import admin

from finance_bot.finance.models import Category, Transaction


admin.site.register(Category)
admin.site.register(Transaction)
