from django.http import request
from films_app.forms import AddPostForm, AddtoFavour, EditPostForm, UserRegistrationForm
from django.db.models.expressions import OrderBy
from django.http.response import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Actor, Film, Film_to_user, Janr, Rejicer, Film_to_rejicer, Film_to_actor, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'html/registr/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'html/registr/registr.html', {'user_form': user_form})


class FilmHome(ListView):
    model = Film
    template_name = "html/index.html"
    paginate_by = 8
    allow_empty = False


    def get_context_data(self,*,objects_list=None,**kwargs):
        context = super(FilmHome, self).get_context_data(**kwargs) # Берём существующий контент
        list_film = Film.objects.all()
        new_films = Film.objects.all()[:3]
        all_janrs = Janr.objects.all()
        Euser = User.objects.get(username='egor')
        print(Euser)
        janrs_count = {}
        for i in range(len(all_janrs)):    
            j = Film.objects.filter(id_janr__pk = all_janrs[i].pk).count()
            janrs_count[all_janrs[i]] = j
        print(janrs_count)

        filtr_years = Film.objects.values_list('years',flat=True) # получаем только года
        filtr_country = Film.objects.values_list('country',flat=True)# получаем только страны
        paginator = Paginator(list_film, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            file_film = paginator.page(page)
        except PageNotAnInteger:
            file_film = paginator.page(1)
        except EmptyPage:
            file_film = paginator.page(paginator.num_pages)
        #['list_films'] с шаблона
        context['Euser'] = Euser
        context['new_films'] = new_films
        context['list_films'] = file_film
        context['all_janrs'] = all_janrs
        context['janrs_count'] = janrs_count
        context['filtr_years'] = sorted(set(filtr_years), reverse=True) # создаётся список годов без повторений
        context['filtr_country'] = sorted(set(filtr_country))
        return context

    def get_queryset(self):
        return Film.objects.filter(is_published=True)   


class Films_janr(ListView):
    model = Film
    template_name = 'html/janr_items.html'
    context_object_name = 'janr_items'
    
    def get_queryset(self):
        return Film.objects.filter(id_janr__pk = self.kwargs['id_janr'])

    def get_context_data(self,*,objects_list=None,**kwargs):
        context = super(Films_janr, self).get_context_data(**kwargs) # Берём существующий контент
        all_janrs = Janr.objects.all()
        new_films = Film.objects.all()[:3]
        janrs_count = {}
        for i in range(len(all_janrs)):    
            j = Film.objects.filter(id_janr__pk = all_janrs[i].pk).count()
            janrs_count[all_janrs[i]] = j
        filtr_years = Film.objects.values_list('years',flat=True)
        filtr_country = Film.objects.values_list('country',flat=True)
        count_films = Film.objects.filter(id_janr__id = self.kwargs['id_janr']).count()
        context['new_films']=new_films
        context['count_films'] = count_films
        context['all_janrs'] = all_janrs
        context['janrs_count'] = janrs_count
        context['filtr_years'] = sorted(set(filtr_years),reverse=True)
        context['filtr_country'] = sorted(set(filtr_country))
        return context    


class Disription_film(ListView):
    model = Film
    template_name = 'html/discription_item.html'
    context_object_name = 'janr_items'
    allow_empty = False
    def get_queryset(self):
        a = Film.objects.filter(slug = self.kwargs['slug'])
        return a
    
    def get_context_data(self,*,objects_list=None,**kwargs):
        context = super(Disription_film, self).get_context_data(**kwargs) # Берём существующий контент
        all_janrs = Janr.objects.all()
        filtr_years = Film.objects.values_list('years',flat=True)
        new_films = Film.objects.all()[:3]
        filtr_country = Film.objects.values_list('country',flat=True)
        janrs_count = {}
        for i in range(len(all_janrs)):    
            j = Film.objects.filter(id_janr__pk = all_janrs[i].pk).count()
            janrs_count[all_janrs[i]] = j
        context['actor_films'] = Actor.objects.filter(id_filma__slug=self.kwargs['slug'])  
        context['rejicer_films'] = Rejicer.objects.filter(fr__slug=self.kwargs['slug'])      
        context['janrs_count'] = janrs_count
        context['all_janrs'] = all_janrs
        context['new_films']= new_films
        context['filtr_years'] = sorted(set(filtr_years),reverse=True)
        context['filtr_country'] = sorted(set(filtr_country))
        return context    


def edit(request, slug):
    film = Film.objects.get(slug = slug)
    form = EditPostForm(instance=film)
    if request.method=='POST':
        form = EditPostForm(request.POST, instance = film)
        if form.is_valid():
            form.save()
            return redirect('show_items')
    context = {'form':form}
    return render(request,'html/editfilm.html',context)

def delet(request, slug):
    film = Film.objects.get(slug = slug)
    if request.method =='POST':
        film.delete()
        return redirect('show_items')

    context = {
        'film':film,
    }
    return render(request, 'html/del.html', context)

def filtrs_items(request, years):
    film_items = Film.objects.filter(years=years)
    all_janrs = Janr.objects.all()
    new_films = Film.objects.all()[:3]
    filtr_years = Film.objects.values_list('years',flat=True)
    filtr_country = Film.objects.values_list('country',flat=True)
    janrs_count = {}
    for i in range(len(all_janrs)):    
            j = Film.objects.filter(id_janr__pk = all_janrs[i].pk).count()
            janrs_count[all_janrs[i]] = j

    context = {
        'film_items': film_items,
        'filtr_years':sorted(set(filtr_years),reverse=True),
        'filtr_country':sorted(set(filtr_country)),
        'all_janrs':all_janrs,
        'janrs_count': janrs_count,
        'new_films': new_films,
    }
    
    return render(request,'html/filtr_name.html',context)

def filtrs_items_c(request, country):
    film_items_c = Film.objects.filter(country = country)
    all_janrs = Janr.objects.all()
    filtr_years = Film.objects.values_list('years',flat=True)
    filtr_country = Film.objects.values_list('country',flat=True)
    new_films = Film.objects.all()[:3]
    janrs_count = {}
    for i in range(len(all_janrs)):    
            j = Film.objects.filter(id_janr__pk = all_janrs[i].pk).count()
            janrs_count[all_janrs[i]] = j
    context = {
        'film_items_c': film_items_c,
        'filtr_years':sorted(set(filtr_years),reverse=True),
        'filtr_country':sorted(set(filtr_country)),
        'all_janrs':all_janrs,
        'janrs_count':janrs_count,
        'new_films': new_films,
    }
    return render(request,'html/filtr_country.html',context)

def show_actors(request):
    all_actor = Actor.objects.all()
    context = {
        'all_actor':all_actor,
    }
    return render(request,'html/Actor.html',context)

def show_about_actor(request, fullName):
    actor = Actor.objects.filter(fullName = fullName)
    all_actors = Actor.objects.all()  
    film_count = Film_to_actor.objects.filter(id_actor__fullName=fullName).count()
    all_actor_film = Film_to_actor.objects.filter(id_actor__fullName = fullName)
    context = {
        'actor':actor,
        'film_count':film_count,
        'all_actor_film':all_actor_film,
    }
    return render(request, 'html/Actor_discription.html', context)

def show_rejicer(request):
    all_rejicer = Rejicer.objects.all()
    print(all_rejicer)
    context = {
        'all_rejicer':all_rejicer,
    }
    return render(request,'html/Rejicer/Rejicer_form.html', context)

def show_about_rejicer(request, fullName):
    rejicer = Rejicer.objects.filter(fullName = fullName)
    all_rejicer = Rejicer.objects.all()  
    film_count = Film_to_rejicer.objects.filter(id_rejicer__fullName=fullName).count()
    all_rejicer_film = Film_to_rejicer.objects.filter(id_rejicer__fullName = fullName)
    context = {
        'rejicer':rejicer,
        'film_count':film_count,
        'all_rejicer_film':all_rejicer_film,
    }
    return render(request, 'html/Rejicer/Rejicer_discription.html', context)

def addfilm(request):
    if request.method == 'POST': 
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('show_items')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    return render(request,'html/addfilm.html',{'form':form})

def user_films(request):
    user_name = request.user.username
    list_films = Film.objects.filter(id_user__username=user_name)    
    context = {
        'user_name':user_name,
        'list_films':list_films,
    }
    return render(request,'html/user_film.html',context)


def addfilmtofavor(request, id):
    
    id_us = request.user.id
    if request.method == "POST":
        user_film = Film_to_user.objects.create(id_film_id = id, id_user_id = id_us)
            
    return HttpResponseRedirect("/USERFavorites")

def delfilmfavor(request, id):
    id_us = request.user.id
    if request.method == "POST":
        user_film = Film_to_user.objects.filter(id_film_id = id, id_user_id = id_us).delete()
    return HttpResponseRedirect("/USERFavorites")
