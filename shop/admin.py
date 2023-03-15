from django.contrib import admin
from .models import Shop, Customer, Service, Comments, Reviews


admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Shop)
admin.site.register(Comments)
admin.site.register(Reviews)
