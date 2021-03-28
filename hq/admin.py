from django.contrib import admin
from .models import *
from .forms import *

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)

@admin.register(Book)
class ServiceAdmin(admin.ModelAdmin):
    form = BookForm

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
