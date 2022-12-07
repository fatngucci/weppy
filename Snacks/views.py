from django.shortcuts import redirect, render
from .forms import SnackForm, CommentForm, SearchForm
from .models import Snack, Comment

# Create your views here.

def snacks_list(request):
    all_the_snacks = Snack.objects.all()
    form = SearchForm()
    context = {'all_the_snacks': all_the_snacks,
               'form': form}
    return render(request, 'snack-list.html', context)

def snacks_detail(request, **kwargs):
    snack_id = kwargs['pk']
    that_one_snack = Snack.objects.get(id=snack_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.poster = request.user
        form.instance.snack = that_one_snack
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    comments = Comment.objects.filter(snack=that_one_snack)
    context = {'that_one_snack': that_one_snack,
               'comments_for_that_one_snack': comments,
               'comment_form': CommentForm
               }

    return render(request, 'snack-detail.html', context)

def snacks_create(request):
    if request.method == 'POST':
        #form = SnackForm(request.POST)
        form = SnackForm(request.POST, request.FILES)
        print(request.POST)
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

def snack_search(request):
    if request.method == 'POST':
        search_string_name = request.POST['name']
        snacks_found = Snack.objets.filter(name__contains=search_string_name)

        search_string_beschreibung = request.POST['beschreibung']
        if search_string_beschreibung:
            snacks_found = snacks_found.filter(beschreibung__contains=search_string_beschreibung)

        form = SearchForm()
        context = {'form': form,
                   'snacks_found': snacks_found,
                   'show_results': True}
        return render(request, 'snack-search.html', context)

def vote(request, pk: str, up_or_down: str):
    comment = Comment.objects.get(id=int(pk))
    voter = request.user
    comment.vote(voter, up_or_down)
    snack_id = comment.snack.id
    return redirect('snack-detail', pk=snack_id)
