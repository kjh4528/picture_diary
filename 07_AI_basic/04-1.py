import fal_client
from dotenv import load_dotenv

load_dotenv()


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

result = fal_client.subscribe(
    'fal-ai/kling-video/v2/master/image-to-video',
    arguments={
        'prompt': 'static shot, gentle smile, subtle breathing, cinematic lighting',
        'image_url' : 'https://www.fitpetmall.com/wp-content/uploads/2023/10/shutterstock_1844153299-1024x683-1.png',
        'duration':'5'
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)

print(result['video']['url'])
