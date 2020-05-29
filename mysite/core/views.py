from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import VideoForm
from .models import Video
from django.conf import settings
import sys
sys.path.insert(1,'/home/anushka/PersonalProjects/Amazon/VID2VID/')
import complete
your_media_root = settings.MEDIA_ROOT

class Home(TemplateView):
    template_name = 'home.html'


def Video_list(request):
    Videos = Video.objects.all()
    return render(request, 'Video_list.html', {
        'Videos': Videos
    })


def test(request):
    data="MONIKA_FINAL"
    return render(request,'test.html',{'data':data})

def upload_Video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Video_list')
    else:
        form = VideoForm()
    return render(request, 'upload_Video.html', {
        'form': form
    })

def Dub_Video(video_path,video_inputLang,video_outputLang):
    #video_path is the input video path link eg.Videos/123.mp4 
    #video_inputLang is the input language
    #video_outputLang is the input language
    #you should return output video path eg. Videos/example.mp4
    output_video_path=complete.changemavoice(video_path,video_inputLang,video_outputLang)
    return output_video_path

def view_Video(request,pk):
    original_video = Video.objects.get(pk=pk)
    video_path = original_video.video
    video_inputLang = original_video.inputLang
    video_outputLang = original_video.outputLang
    dub_video_link = Dub_Video(video_path,video_inputLang,video_outputLang)
    return render(request,'view_Video.html',{'dub_video_link':dub_video_link})


def delete_Video(request, pk):
    if request.method == 'POST':
        video = Video.objects.get(pk=pk)
        video.delete()
    return redirect('Video_list')
