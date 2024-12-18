from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Image
from .forms import AlbumForm, ImageForm, RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404



@login_required
def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        album.delete()
        return redirect('album_list')  # Redirect to the album list page or another page after deletion
    return render(request, 'delete.html', {'album': album})

@login_required
def album_list(request):
    albums = Album.objects.filter(user=request.user)
    return render(request, 'album_list.html', {'albums': albums})

@login_required
def page(request, album_id, page_number):
    
    # Fetch the album
    album = get_object_or_404(Album, id=album_id)

    # Pagination setup to show 1 image per page
    images_per_page = 1
    start_index = (page_number - 1) * images_per_page
    end_index = start_index + images_per_page

    # Fetch the single image for the current page
    images = album.images.all()[start_index:end_index]

    # If no images are found (e.g., page out of range), return 404
    if not images:
        raise Http404("No image found on this page")

    # Pagination logic: Do we have more pages?
    total_images = album.images.count()
    max_page_number = (total_images + images_per_page - 1) // images_per_page  # Calculate max pages
    has_next = end_index < total_images
    has_prev = start_index > 0

    # Determine the next and previous page numbers
    next_page = page_number + 1 if has_next else None
    prev_page = page_number - 1 if has_prev else None

    # Pass the pagination info to the template
    context = {
        'album_id': album_id,
        'album': album,
        'image': images[0],  # Pass the single image for the page
        'page_number': page_number,
        'max_page_number': max_page_number,  # Add max page number to context
        'next_page': next_page,
        'prev_page': prev_page,
    }

    return render(request, 'page.html', context)

    

@login_required
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    images = album.images.all()  # Fetch all images for the album

    context = {
        'album': album,
        'images': images,
        'album_id': album_id
    }
    return render(request, 'album_detail.html', context)

@login_required
def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            return redirect('album_list')
    else:
        form = AlbumForm()
    return render(request, 'create_album.html', {'form': form})

@login_required
def upload_image(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.album = album
            image.save()
            return redirect('album_detail', album_id=album_id)
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form, 'album': album})

def go_to_album_page(request, album_id):
    page_number = request.GET.get('page_number')  # Get the page number from the form submission
    
    if page_number:
        return redirect('page', album_id=album_id, page_number=page_number)
    else:
        # Handle the case where the page number is not provided
        return redirect('album_detail', album_id=album_id)
    


