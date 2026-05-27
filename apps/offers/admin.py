from django.contrib import admin

from .models import Category, OfferModel, OfferMediaModel

admin.site.register(Category)
admin.site.register(OfferModel)
admin.site.register(OfferMediaModel)
