from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SnackEditForm
from Snacks.models import Snack

# Create your views here.

@staff_member_required(login_url='/useradmin/login/')
def snack_edit_view(request, pk: str):
    snack_id = pk
    if request.method == 'POST':
        form = SnackEditForm(request.POST)
        if form.is_valid():
            snack = Snack.objects.get(id=snack_id)
            new_pic = form.cleaned_data['bilder']
            new_file = form.cleaned_data['produkt_info']
            snack.bilder = new_pic
            snack.file = new_file
            snack.save()
        return redirect('snack-delete')
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
        return render(request, 'snack-edit.html')


def snack_delete_view(request, pk: str):
    snack_id = pk
    snack = Snack.objects.get(id=snack_id)
    can_delete = False
    myuser = request.user
    if not myuser.is_anonymous:
        can_delete = myuser.can_delete()
    context = {'snack': snack}

    if request.method == 'POST' and can_delete:
        snack.delete()
        return redirect('snack-delete')



