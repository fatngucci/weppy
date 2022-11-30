from django.db import models
from django.conf import settings

# Create your models here.
class Snack(models.Model):
    name = models.CharField(max_length=50) # z.B. Chilli Chips Extra Hot
    gewicht = models.IntegerField() # z.B. 400g
    beschreibung = models.CharField(max_length=1000, blank=True) # zutaten usw.
    pictures = models.ImageField(upload_to='snack_pictures/', blank=True, null=True)
    artikelnummer = models.CharField(max_length=100)
    hersteller = models.ForeignKey(settings.AUTH_USER_MODEL, # Private User, Firma, usw. muss eigenes Profil haben
                                   on_delete=models.CASCADE,
                                   related_name='Hersteller',
                                   related_query_name='Hersteller'
                                   )
    preis = models.FloatField() # in € z.B. 2.50 €
    erstellungs_zeitstempel = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['erstellungs_zeitstempel', 'name']
        verbose_name = 'Snacks'
        verbose_name_plural = 'Snacks'

    def __str__(self):
        return self.name + ' / ' + str(self.gewicht) + ' / ' + str(self.preis)

    def __repr__(self):
        return self.name + ' / ' + self.artikelnummer + ' / ' + self.hersteller

# Rezensionen
# Class Comment

# Vote
# Class Vote