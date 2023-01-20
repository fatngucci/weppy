from django.shortcuts import redirect, render

from Shoppingcart.forms import AddForm
from .forms import SnackForm, CommentForm, CommentEditForm, SearchForm
from .models import Snack, Comment
from Shoppingcart.models import ShoppingCart
from decimal import Decimal


# Create your views here.

def snack_list(request):
    if request.method == 'POST':
        search_string_name = request.POST['name']
        snacks_found = Snack.objects.filter(name__contains=search_string_name)

        search_string_beschreibung = request.POST['description']
        if search_string_beschreibung:
            snacks_found = snacks_found.filter(beschreibung__contains=search_string_beschreibung)

        search_bewertung = request.POST['rating']
        if search_bewertung:
            search_bewertung_as_float = float(search_bewertung)
            snacks_found = snacks_found.filter(produkt_bewertung__gte=search_bewertung_as_float)

        results = False
        if len(snacks_found) > 0:
            results = True

        form = SearchForm()
        context = {'form': form,
                   'snacks_found': snacks_found,
                   'show_results': results,
                   'search_name': search_string_name}
        return render(request, 'snack-search.html', context)
    else:
        all_the_snacks = Snack.objects.all()
        # form = SearchForm(request.POST)
        context = {'all_the_snacks': all_the_snacks,
               'form': SearchForm}
        return render(request, 'snack-list.html', context)


def snack_detail(request, **kwargs):
    snack_id = kwargs['pk']
    that_one_snack = Snack.objects.get(id=snack_id)

    if request.method == 'POST':

        if 'comment' in request.POST:
            that_one_snack.get_bewertung()
            form = CommentForm(request.POST)
            form.instance.poster = request.user
            form.instance.snack = that_one_snack
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

        elif 'cart' in request.POST:
            benutzer = request.user
            form = AddForm(request.POST)
            if form.is_valid():
                ShoppingCart.add_item(benutzer, that_one_snack, form.cleaned_data['menge'])

    comments = Comment.objects.filter(snack=that_one_snack)
    context = {'that_one_snack': that_one_snack,
               'comments_for_that_one_snack': comments,
               'comment_form': CommentForm,
               'add_form': AddForm,
               'user': request.user
               }

    return render(request, 'snack-detail.html', context)


def snack_create(request):
    if request.method == 'POST':
        # form = SnackForm(request.POST)
        form = SnackForm(request.POST, request.FILES)
        form.instance.hersteller = request.user
        if form.is_valid():
            form.save()
        else:
            pass

        return redirect('snack-manage')

    else:
        form = SnackForm()
        can_delete = False
        myuser = request.user

        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        context = {'form': form,
                   'can_delete': can_delete}
        return render(request, 'snack-create.html', context)


def snack_delete(request, **kwargs):
    snack_id = kwargs['pk']
    to_be_deleted = Snack.objects.get(id=snack_id)

    can_delete = False
    myuser = request.user

    if not myuser.is_anonymous:
        can_delete = myuser.can_delete()

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('snack-detail', request.POST['snack_id'])
        to_be_deleted.delete()
        return redirect('snack-list')

    context = {'that_one_snack': to_be_deleted,
               'can_delete': can_delete}

    return render(request, 'snack-delete.html', context)


def snack_search(request):
    if request.method == 'POST':
        search_string_name = request.POST['name']
        snacks_found = Snack.objects.filter(name__contains=search_string_name)

        search_string_beschreibung = request.POST['description']
        if search_string_beschreibung:
            snacks_found = snacks_found.filter(beschreibung__contains=search_string_beschreibung)

        search_bewertung = request.POST['rating']
        if search_bewertung:
            search_bewertung_as_float = float(search_bewertung)
            snacks_found = snacks_found.filter(produkt_bewertung__gte=search_bewertung_as_float)

        form = SearchForm()
        context = {'form': form,
                   'snacks_found': snacks_found,
                   'show_results': True,
                   'search_name': search_string_name}
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
