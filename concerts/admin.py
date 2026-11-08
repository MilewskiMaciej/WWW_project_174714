from django.contrib import admin
from .models import Stage, Artist, Concert, LineupSlot, TicketTier

class LineupSlotInline(admin.TabularInline):
    model = LineupSlot
    extra = 1

class TicketTierInline(admin.TabularInline):
    model = TicketTier
    extra = 1

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'hourly_rental_rate', 'concerts_count')
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description="Liczba koncertów")
    def concerts_count(self, obj):
        return obj.concerts.count()

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'country', 'created_at')
    list_filter = ('genre', 'country')
    search_fields = ('name', 'genre')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage', 'organizer', 'start_time', 'end_time', 'status', 'is_published')
    list_filter = ('status', 'is_published', 'stage', 'start_time')
    search_fields = ('title', 'stage__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_published')
    date_hierarchy = 'start_time'
    ordering = ('start_time',)
    inlines = [LineupSlotInline, TicketTierInline]

    fieldsets = (
        ("Podstawowe informacje", {
            'fields': ('title', 'slug', 'organizer')
        }),
        ("Rezerwacja sceny", {
            'fields': ('stage', 'start_time', 'end_time', 'status', 'is_published')
        }),
    )

@admin.register(LineupSlot)
class LineupSlotAdmin(admin.ModelAdmin):
    list_display = ('artist', 'concert', 'performance_start', 'performance_end', 'artist_fee')
    search_fields = ('artist__name', 'concert__title')

@admin.register(TicketTier)
class TicketTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'concert', 'price', 'quantity_available')
    list_filter = ('concert',)
    search_fields = ('name', 'concert__title')
    list_editable = ('price', 'quantity_available')