from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SnackEditForm, CommentEditForm
from Snacks.models import Snack, Comment

# Create your views here.

@staff_member_required(login_url='/useradmin/login/')
def snack_edit_view(request, pk: str):
    snack_id = pk
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('snack-manage')
        form = SnackEditForm(request.POST, request.FILES)
        if form.is_valid():
            snack = Snack.objects.get(id=snack_id)
            new_pic = form.cleaned_data['bilder']
            new_file = form.cleaned_data['produkt_info']
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
    if not myuser.is_anonymous:
        can_delete = myuser.can_delete()
    context = {
               'all_the_snacks': all_the_snacks,
                'can_delete': can_delete}

    if request.method == 'POST' and can_delete:
        if 'delete' in request.POST:
            return redirect('snack-delete', request.POST['snack_id'])
        elif 'edit' in request.POST:
            return redirect('snack-edit', request.POST['snack_id'])

    return render(request, 'snack-manage.html', context)


def comment_edit(request, pk: str):
    comment_id = pk
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        form = CommentEditForm(request.POST)
        if form.is_valid():
            new_text = form.cleaned_data['text']
            new_stern = form.cleaned_data['sternbewertung']
            comment.text = new_text
            comment.sternbewertung = new_stern
            comment.save()

    else:
        is_own_comment = False
        myuser = request.user
        if not myuser.is_anonymous:
            is_own_comment = (comment.poster == myuser)
        form = CommentEditForm(request.POST or None, instance=comment)
        context = {'form': form,
                   'is_own_comment': is_own_comment,
                   'comment': comment,
                   }
        return render(request, 'comment-edit.html', context)



