from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Stage(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Nazwa sceny")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Slug")
    location = models.CharField(max_length=255, verbose_name="Miejsce występu")
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(10)],
        verbose_name="Maksymalna pojemność"
    )
    hourly_rental_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Stawka za wynajem"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    class Meta:
        verbose_name = "Scena"
        verbose_name_plural = "Sceny"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (pojemność: {self.capacity})"

class Artist(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nazwa artysty/zespołu")
    slug = models.SlugField(max_length=170, unique=True, verbose_name="Slug")
    genre = models.CharField(max_length=100, verbose_name="Gatunek muzyczny")
    country = models.CharField(max_length=100, default="Polska", verbose_name="Kraj pochodzenia")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    class Meta:
        verbose_name = "Artysta"
        verbose_name_plural = "Artyści"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.genre})"

class Concert(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Zaplanowany'
        CONFIRMED = 'CONFIRMED', 'Potwierdzony'
        CANCELLED = 'CANCELLED', 'Odwołany'
        COMPLETED = 'COMPLETED', 'Zakończony'

    title = models.CharField(max_length=200, verbose_name="Nazwa eventu")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="Slug")
    stage = models.ForeignKey(
        Stage,
        on_delete=models.PROTECT,
        related_name="concerts",
        verbose_name="Scena"
    )
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organized_concerts",
        verbose_name="Organizator"
    )
    artists = models.ManyToManyField(
        Artist,
        through='LineupSlot',
        related_name="concerts",
        verbose_name="Line-up koncertu"
    )
    start_time = models.DateTimeField(verbose_name="Czas rozpoczęcia eventu")
    end_time = models.DateTimeField(verbose_name="Czas zakończenia eventu")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name="Status"
    )
    is_published = models.BooleanField(default=True, verbose_name="Opublikowany")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ostatnia aktualizacja")

    class Meta:
        verbose_name = "Koncert"
        verbose_name_plural = "Koncerty"
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} @ {self.stage.name} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

class LineupSlot(models.Model):
    concert = models.ForeignKey(
        Concert,
        on_delete=models.CASCADE,
        related_name="lineup_slots",
        verbose_name="Koncert"
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="lineup_appearances",
        verbose_name="Artysta"
    )
    performance_start = models.DateTimeField(verbose_name="Rozpoczęcie występu")
    performance_end = models.DateTimeField(verbose_name="Zakończenie występu")
    artist_fee = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Wynagrodzenie dla artysty"
    )

    class Meta:
        verbose_name = "Pozycja w Line-upie"
        verbose_name_plural = "Harmonogram"
        ordering = ['performance_start']
        constraints = [
            models.UniqueConstraint(
                fields=['concert', 'artist'],
                name='unique_artist_per_concert_lineup'
            )
        ]

    def __str__(self):
        return f"{self.artist.name} -> {self.concert.title} ({self.performance_start.strftime('%H:%M')})"

class TicketTier(models.Model):
    concert = models.ForeignKey(
        Concert,
        on_delete=models.CASCADE,
        related_name="ticket_tiers",
        verbose_name="Koncert"
    )
    name = models.CharField(max_length=100, verbose_name="Rodzaj biletu")
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Cena"
    )
    quantity_available = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Pula dostępnych biletów"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    class Meta:
        verbose_name = "Cena biletów"
        verbose_name_plural = "Ceny biletów"
        ordering = ['price']
        constraints = [
            models.UniqueConstraint(
                fields=['concert', 'name'],
                name='unique_ticket_tier_name_per_concert'
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.price} PLN ({self.concert.title})"