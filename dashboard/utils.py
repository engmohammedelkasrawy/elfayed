import json
import requests
from requests_toolbelt import MultipartEncoder


def upload_video_serve(request):
    ############# STEP 1 ####################
    video_name = request.POST.get("name")
    api_secret_key = "DzJNvBi24Htggyg5HpvDPpex6YAKIgbMNaRbPV5mImVUCM1ds3WMUR9PpcGM1wd6"
    querystring = {"title": video_name}

    url = "https://dev.vdocipher.com/api/videos"
    headers = {
        'Authorization': "Apisecret " + api_secret_key
    }
    response = requests.request("PUT", url, headers=headers, params=querystring)
    uploadInfo = response.json()
    clientPayload = uploadInfo['clientPayload']
    uploadLink = clientPayload['uploadLink']
    video_id = uploadInfo['videoId']
    
    
    filename = request.FILES.get("video")

    m = MultipartEncoder(fields=[
        ('x-amz-credential', clientPayload['x-amz-credential']),
        ('x-amz-algorithm', clientPayload['x-amz-algorithm']),
        ('x-amz-date', clientPayload['x-amz-date']),
        ('x-amz-signature', clientPayload['x-amz-signature']),
        ('key', clientPayload['key']),
        ('policy', clientPayload['policy']),
        ('success_action_status', '201'),
        ('success_action_redirect', ''),
        ('file', ('filename',filename, 'text/plain'))
        ])

    response = requests.post(
    uploadLink,
    data=m,
    headers={'Content-Type': m.content_type}
    )
    response.raise_for_status()
    return video_id


# if upload from server
    #filename = request.FILES.get("file")
    # m = MultipartEncoder(fields=[
    #     ('x-amz-credential', clientPayload['x-amz-credential']),
    #     ('x-amz-algorithm', clientPayload['x-amz-algorithm']),
    #     ('x-amz-date', clientPayload['x-amz-date']),
    #     ('x-amz-signature', clientPayload['x-amz-signature']),
    #     ('key', clientPayload['key']),
    #     ('policy', clientPayload['policy']),
    #     ('success_action_status', '201'),
    #     ('success_action_redirect', ''),
    #     ('file', ('filename', filename, 'text/plain'))
    # ])

    # response = requests.post(
    #     uploadLink,
    #     data=m,
    #     headers={'Content-Type': m.content_type}
    # )
