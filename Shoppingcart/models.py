from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

from Snacks.models import Snack


# Create your models here.
class ShoppingCart(models.Model):
    zeitstempel = models.DateTimeField(default=timezone.now)
    benutzer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 )

    def add_item(myuser, snack, menge):
        shopping_carts = ShoppingCart.objects.filter(benutzer=myuser)
        shopping_cart = 0
        if shopping_carts:
            shopping_cart = shopping_carts.first()
        else:
            shopping_cart = ShoppingCart.objects.create(benutzer=myuser)

        snack_in_cart = ShoppingCartItem.objects.filter(produkt_id=snack.id, shopping_cart=shopping_cart)
        if snack_in_cart:
            the_snack = snack_in_cart.first()
            the_snack.menge += menge
            the_snack.save()

        else:

            produkt_id = snack.id
            produkt_name = snack.name + ' / ' + str(snack.gewicht) + 'g / ' + str(snack.artikelnummer)
            preis = snack.preis
            ShoppingCartItem.objects.create(produkt_id=produkt_id,
                                            produkt_name=produkt_name,
                                            preis=preis,
                                            menge=menge,
                                            shopping_cart=shopping_cart,
                                            )

    def get_number_of_items(self):
        number_of_items = 0
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        for item in shopping_cart_items:
            number_of_items += item.menge
        return number_of_items

    def get_total(self):
        total = Decimal(0.0)
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        for item in shopping_cart_items:
            total += item.preis * item.menge
        return total


class ShoppingCartItem(models.Model):
    produkt_id = models.IntegerField()
    produkt_name = models.CharField(max_length=100)
    preis = models.DecimalField(decimal_places=2, max_digits=10)
    menge = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    shopping_cart = models.ForeignKey(ShoppingCart,
                                      on_delete=models.CASCADE,
                                      )

    def remove(self):
        if self.menge > 1:
            self.menge -= 1
            self.save()
        else:
            self.delete()

    def add(self):
        self.menge += 1
        self.save()

    def get_snack(self):
        return Snack.objects.get(id=self.produkt_id)


class Payment(models.Model):
    kreditkartenr = models.CharField(max_length=19)  # nnnn nnnn nnnn nnnn
    ablaufsdatum = models.CharField(max_length=7)  # mm/yyyy
    betrag = models.DecimalField(decimal_places=2, max_digits=10)
    zeitstempel = models.DateTimeField(default=timezone.now)
    benutzer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 )
