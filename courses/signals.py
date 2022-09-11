# import ffmpeg_streaming
# from ffmpeg_streaming import Formats, Bitrate, Representation, Size
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# @receiver(post_save, sender=Lesson)
# def post_save_create_lesson(created, sender, instance, *args, **kwargs):
#     _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    
#     video_path=instance.video.path
    
#     #split path video and get folder to cut video into
#     get_folder_video = video_path.split("\\")
    
#     save_to = f'media/videos/{get_folder_video[-2]}/{instance.name}_key'

#     url = f'http://127.0.0.1:8000/media/videos/{get_folder_video[-2]}/{instance.name}_key'

#     if created:
#         video = ffmpeg_streaming.input(str(instance.video.path))
#         hls = video.hls(Formats.h264())
#         hls.representations(_720p)
#         hls.encryption(save_to, url)
        
#         hls.output(f'media/videos/{get_folder_video[-2]}/{instance.name}.m3u8')        
#         instance.video.name = f'videos/{get_folder_video[-2]}/{instance.name}_720p.m3u8'
#         instance.save()
# from django.db.models.signals import post_save, post_delete, pre_save
# from django.dispatch import receiver
# from .models import Lesson
# from core.settings import BASE_DIR
# import shutil
# import os


# @receiver(post_delete, sender=Lesson)
# def post_delete_video_Lesson(sender, instance, *args, **kwargs):
#     if instance.video:
#         p = f'{instance.video.name}'.replace('streaming_720p.m3u8', '')
#         file_location = os.path.join(BASE_DIR, f'media/{p}')
#         print(file_location)
#         shutil.rmtree(file_location)
