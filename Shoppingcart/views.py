from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import PaymentForm, AddForm
from .models import ShoppingCart, ShoppingCartItem

# Create your views here.
def show_shopping_cart(request):
    if request.method == 'POST':
        if 'empty' in request.POST:
            ShoppingCart.objects.get(benutzer=request.user).delete()

            context = {'shopping_cart_is_empty': True,
                       'shopping_cart_items': None,
                       'amount': 0.0}
            return render(request, 'shopping-cart.html', context)

        elif 'pay' in request.POST:
            return redirect('shopping-cart-pay')

        elif 'plus' in request.POST:
            produkt_id_as_int = int(request.POST['produkt_id'])
            print(produkt_id_as_int)
            the_snack = ShoppingCartItem.objects.get(id=produkt_id_as_int)
            print(the_snack)
            if the_snack:
                the_snack.add()
                print(+1)
            return redirect('shopping-cart-show')

        elif 'minus' in request.POST:
            produkt_id_as_int = int(request.POST['produkt_id'])
            print(produkt_id_as_int)
            the_snack = ShoppingCartItem.objects.get(id=produkt_id_as_int)
            print(the_snack)
            if the_snack:
                the_snack.remove()
                print(-1)
            return redirect('shopping-cart-show')


    else:
         shopping_cart_is_empty = True
         shopping_cart_items = None
         total = Decimal(0.0)

         benutzer = request.user
         if benutzer.is_authenticated:
             shopping_carts = ShoppingCart.objects.filter(benutzer=benutzer)
             if shopping_carts:
                 shopping_cart = shopping_carts.first()
                 shopping_cart_is_empty = False
                 shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
                 total = shopping_cart.get_total()

         context = {'shopping_cart_is_empty': shopping_cart_is_empty,
                    'shopping_cart_items': shopping_cart_items,
                    'total': total,
                    }
         return render(request, 'shopping-cart.html', context)

@login_required(login_url='/useradmin/login/')
def pay(request):
    shopping_cart_is_empty = True
    paid = False
    form = None

    if request.method == 'POST':
        benutzer = request.user
        form = PaymentForm(request.POST)
        form.instance.benutzer = benutzer
        if form.is_valid():
            form.save()
            paid = True

            ShoppingCart.objects.get(benutzer=benutzer).delete()
        else:
            print(form.errors)

    else:
        shopping_carts = ShoppingCart.objects.filter(benutzer=request.user)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
            shopping_cart_is_empty = False
            form = PaymentForm(initial={'betrag': shopping_cart.get_total()})

    context = {'shopping_cart_is_empty': shopping_cart_is_empty,
               'payment_form': form,
               'paid': paid,}
    return render(request, 'pay.html', context)
