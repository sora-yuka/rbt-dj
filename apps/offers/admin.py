from django.contrib import admin

from .models import CategoryModel, OfferModel, OfferMediaModel

admin.site.register(CategoryModel)
admin.site.register(OfferModel)
admin.site.register(OfferMediaModel)
