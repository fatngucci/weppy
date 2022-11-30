from django.shortcuts import redirect, render
from .forms import SnackForm
from .models import Snack

# Create your views here.

def snacks_list(request):
    all_the_snacks = Snack.objects.all()
    context = {'all_the_snacks': all_the_snacks}
    return render(request, 'snack-list.html', context)

def snacks_detail(request, **kwargs):
    snack_id = kwargs['pk']
    that_one_snack = Snack.objects.get(id=snack_id)

    context = {'that_one_snack': that_one_snack,
               }

    return render(request, 'snack-detail.html', context)

def snacks_create(request):
    if request.method == 'POST':
        form = SnackForm(request.POST)
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

def snacks_delete(request, **kwargs):
    snack_id = kwargs['pk']
    to_be_deleted = Snack.objects.get(id=snack_id)
    context = {'that_one_snack': to_be_deleted}

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('snack-list')
        to_be_deleted.delete()
        return redirect('snack-list')

    return render(request, 'snack-delete.html', context)
