from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.
def home(request):
    allMovies = Movie.objects.all()  # select * from movie
    
    context = {
        "movies": allMovies,
    }

    return render(request, 'main/index.html', context)

# detail page
def detail(request, id):
    movie = Movie.objects.get(id=id) # select * from movie where id=id

    context = {
        "movie": movie
    }
    return render(request, 'main/details.html', context)


# add movies to the database
def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = MovieForm(request.POST or None)

                # check if the form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form = MovieForm()
            return render(request, 'main/addmovies.html', {"form": form, "controller": "Add Movies"})
        
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login")    


# edit the movie
def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the movies linked with id
            movie = Movie.objects.get(id=id)

            # form check
            if request.method == "POST":
                form = MovieForm(request.POST or None, instance=movie)
                # check if form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:detail", id)
            else:
                form = MovieForm(instance=movie)
            return render(request, 'main/addmovies.html', {"form": form, "controller": "Edit Movies"})
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login") 


# delete movies
def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the moveis
            movie = Movie.objects.get(id=id)

            # delte the movie
            movie.delete()
            return redirect("main:home")
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login") 