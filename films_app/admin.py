from django.contrib import admin
from .models import Film, Janr, Rejicer, Film_to_rejicer, Actor, Film_to_actor, Film_to_user

admin.site.register(Film)
admin.site.register(Film_to_user)
admin.site.register(Janr)
admin.site.register(Rejicer)
admin.site.register(Film_to_rejicer)
admin.site.register(Actor)
admin.site.register(Film_to_actor)
# Register your models here.
