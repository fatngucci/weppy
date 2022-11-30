from django.shortcuts import redirect, render
from .forms import SnackForm
from .models import Snack

# Create your views here.

def snacks_list(request):
    all_the_snacks = Snack.objects.all()
    context = {'all_the_snacks': all_the_snacks}
    return render(request, 'snack-list.html', context)

