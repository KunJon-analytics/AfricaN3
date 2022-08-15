from django.contrib import admin
from .models import Word, Sitting, Wordle, Winner, Letter

# Register your models here.
class WordleAdmin(admin.ModelAdmin):
    model = Wordle
    list_display = ('title', 'id', 'master', 'status',)

class WordAdmin(admin.ModelAdmin):
    model = Word
    list_display = ('content', 'wordle', 'found',)

class WinnerAdmin(admin.ModelAdmin):
    model = Winner
    list_display = ('sitting', 'claimed')

admin.site.register(Wordle, WordleAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Winner, WinnerAdmin)
admin.site.register(Sitting)
admin.site.register(Letter)