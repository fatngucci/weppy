from django.shortcuts import redirect, render
from .forms import SnackForm, CommentForm, CommentEditForm, SearchForm
from .models import Snack, Comment
from Shoppingcart.models import ShoppingCart
from decimal import Decimal

# Create your views here.

def snack_list(request):
    if request.method == 'POST':
        search_string_name = request.POST['name']
        snacks_found = Snack.objects.filter(name__contains=search_string_name)

        search_string_beschreibung = request.POST['beschreibung']
        if search_string_beschreibung:
            snacks_found = snacks_found.filter(beschreibung__contains=search_string_beschreibung)

        form = SearchForm()
        context = {'form': form,
                   'snacks_found': snacks_found,
                   'show_results': True}
        return render(request, 'snack-search.html', context)
    all_the_snacks = Snack.objects.all()
    form = SearchForm()
    context = {'all_the_snacks': all_the_snacks,
               'form': form}
    return render(request, 'snack-list.html', context)

def snack_detail(request, **kwargs):
    snack_id = kwargs['pk']
    that_one_snack = Snack.objects.get(id=snack_id)

    if request.method == 'POST':

        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            form.instance.poster = request.user
            form.instance.snack = that_one_snack
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

        elif 'cart' in request.POST:
            benutzer = request.user
            ShoppingCart.add_item(benutzer, that_one_snack)

    comments = Comment.objects.filter(snack=that_one_snack)
    context = {'that_one_snack': that_one_snack,
               'comments_for_that_one_snack': comments,
               'comment_form': CommentForm,
               'user': request.user
               }

    return render(request, 'snack-detail.html', context)

def snack_create(request):
    if request.method == 'POST':
        #form = SnackForm(request.POST)
        form = SnackForm(request.POST, request.FILES)
        form.instance.hersteller = request.user
        if form.is_valid():
            form.save()
        else:
            pass

        return redirect('snack-list')

    else:
        form = SnackForm()
        context = {'form': form}
        return render(request, 'snack-create.html', context)

def snack_delete(request, **kwargs):
    snack_id = kwargs['pk']
    to_be_deleted = Snack.objects.get(id=snack_id)
    context = {'that_one_snack': to_be_deleted}

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('snack-list')
        to_be_deleted.delete()
        return redirect('snack-list')

    return render(request, 'snack-delete.html', context)

def snack_search(request):
    if request.method == 'POST':
        search_string_name = request.POST['name']
        snacks_found = Snack.objects.filter(name__contains=search_string_name)

        search_string_beschreibung = request.POST['beschreibung']
        if search_string_beschreibung:
            snacks_found = snacks_found.filter(beschreibung__contains=search_string_beschreibung)

        search_bewertung = request.POST['produkt_bewertung']
        if search_bewertung:
            search_bewertung_as_decimal = Decimal(search_bewertung)
            print(search_bewertung_as_decimal)
            snacks_found = snacks_found.filter(produkt_bewertung__gte=search_bewertung_as_decimal)

        form = SearchForm()
        context = {'form': form,
                   'snacks_found': snacks_found,
                   'show_results': True}
        return render(request, 'snack-search.html', context)
    else:
        form = SearchForm()
        context = {'form': form,
                   'show_results': False}
        return render(request, 'snack-search.html', context)

def vote(request, pk: str, up_or_down: str):
    comment = Comment.objects.get(id=int(pk))
    voter = request.user
    comment.vote(voter, up_or_down)
    snack_id = comment.snack.id
    return redirect('snack-detail', pk=snack_id)

def report(request, pk: str):
    comment = Comment.objects.get(id=int(pk))
    subject = request.user
    comment.report(subject)
    snack_id = comment.snack.id
    return redirect('snack-detail', pk=snack_id)

def comment_edit(request, pk: str):
    comment_id = pk
    comment = Comment.objects.filter(id=comment_id).first()
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('snack-detail', comment.snack.id)
        form = CommentEditForm(request.POST)
        if form.is_valid():
            new_text = form.cleaned_data['text']
            new_bewertung = form.cleaned_data['sternbewertung']
            comment.text = new_text
            comment.sternbewertung = new_bewertung
            comment.save()
        return redirect('snack-detail', comment.snack.id)
    else:
        can_edit = False
        myuser = request.user
        if not myuser.is_anonymous:
            can_edit = comment.poster == myuser
        form = CommentEditForm(request.POST or None, instance=comment)
        context = {'form': form,
                   'can_edit': can_edit,
                   'comment': comment,
                   }
        return render(request, 'comment-edit.html', context)

def comment_delete(request, pk: str):
    comment = Comment.objects.get(id=int(pk))
    comment.delete()
    snack_id = comment.snack.id
    return redirect('snack-detail', pk=snack_id)