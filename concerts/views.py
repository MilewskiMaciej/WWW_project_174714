from django.shortcuts import render
from .models import Concert

def concert_list(request):
    concerts = Concert.objects.filter(is_published=True).select_related('stage', 'organizer').prefetch_related('ticket_tiers', 'lineup_slots__artist')
    return render(request, 'concerts/concert_list.html', {'concerts': concerts})