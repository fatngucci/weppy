from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SnackEditForm, CommentEditForm
from Snacks.models import Snack, Comment


# Create your views here.


# @staff_member_required(login_url='/useradmin/login/')
def menu_view(request):
    can_delete = False
    myuser = request.user
    if not myuser.is_anonymous:
        can_delete = myuser.can_delete()
    context = {
        'can_delete': can_delete,
    }
    return render(request, 'menu.html', context)


# @staff_member_required(login_url='/useradmin/login/')
def snack_edit_view(request, pk: str):
    snack_id = pk
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('snack-manage')
        form = SnackEditForm(request.POST, request.FILES)
        if form.is_valid():
            snack = Snack.objects.get(id=snack_id)
            new_name = form.cleaned_data['name']
            new_gewicht = form.cleaned_data['gewicht']
            new_artikelnummer = form.cleaned_data['artikelnummer']
            new_preis = form.cleaned_data['preis']
            new_hersteller = form.cleaned_data['hersteller']
            new_pic = form.cleaned_data['bilder']
            new_file = form.cleaned_data['produkt_info']
            snack.name = new_name
            snack.gewicht = new_gewicht
            snack.artikelnummer = new_artikelnummer
            snack.preis = new_preis
            snack.hersteller = new_hersteller
            snack.bilder = new_pic
            snack.produkt_info = new_file
            snack.save()
        return redirect('snack-manage')
    else:
        can_delete = False
        myuser = request.user
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
        snack = Snack.objects.get(id=snack_id)
        form = SnackEditForm(request.POST or None, instance=snack)
        context = {'form': form,
                   'can_delete': can_delete,
                   'snack': snack,
                   }
        return render(request, 'snack-edit.html', context)


def snack_manage_view(request):
    all_the_snacks = Snack.objects.all()
    can_delete = False
    myuser = request.user
    delete_button_clicked = False
    the_snack = 0
    the_id = 0
    if not myuser.is_anonymous:
        can_delete = myuser.can_delete()

    if request.method == 'POST' and can_delete:
        if 'delete' in request.POST:
            # return redirect('snack-delete', request.POST['snack_id'])
            delete_button_clicked = True
            the_id = request.POST['snack_id']
            the_snack = Snack.objects.get(id=the_id)
        elif 'edit' in request.POST:
            return redirect('snack-edit', request.POST['snack_id'])
        elif 'yes' in request.POST:
            the_id = request.POST['snack_id']
            the_snack = Snack.objects.get(id=the_id)
            the_snack.delete()
            delete_button_clicked = False
        elif 'no' in request.POST:
            delete_button_clicked = False

    context = {
        'all_the_snacks': all_the_snacks,
        'can_delete': can_delete,
        'delete_button_clicked': delete_button_clicked,
        'the_snack': the_snack
    }

    return render(request, 'snack-manage.html', context)


def comment_edit_view(request, pk: str):
    comment_id = pk
    myuser = request.user
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('comment-manage')
        form = CommentEditForm(request.POST)
        if form.is_valid():
            new_text = form.cleaned_data['text']
            new_stern = form.cleaned_data['sternbewertung']
            comment.text = new_text
            comment.sternbewertung = new_stern
            comment.save()

    else:
        can_delete = False
        is_own_comment = False
        if not myuser.is_anonymous:
            can_delete = myuser.can_delete()
            is_own_comment = (comment.poster == myuser)
        form = CommentEditForm(request.POST or None, instance=comment)
        context = {'form': form,
                   'is_own_comment': is_own_comment,
                   'comment': comment,
                   'can_delete': can_delete,
                   }
        return render(request, 'comment-edit-cs.html', context)


def comment_manage_view(request):
    all_the_comments = Comment.objects.all()
    can_delete = False
    myuser = request.user
    delete_button_clicked = False
    the_comment = 0
    the_id = 0
    if not myuser.is_anonymous:
        can_delete = myuser.can_delete()

    if request.method == 'POST' and can_delete:
        if 'delete' in request.POST:
            # return redirect('snack-delete', request.POST['comment_id'])
            delete_button_clicked = True
            the_id = request.POST['comment_id']
            the_comment = Comment.objects.get(id=the_id)
        elif 'edit' in request.POST:
            return redirect('comment-edit-cs', request.POST['comment_id'])
        elif 'yes' in request.POST:
            the_id = request.POST['comment_id']
            the_comment = Comment.objects.get(id=the_id)
            the_comment.delete()
            delete_button_clicked = False
        elif 'no' in request.POST:
            delete_button_clicked = False

    context = {
        'all_the_comments': all_the_comments,
        'can_delete': can_delete,
        'delete_button_clicked': delete_button_clicked,
        'the_comment': the_comment
    }

    return render(request, 'comment-manage.html', context)
