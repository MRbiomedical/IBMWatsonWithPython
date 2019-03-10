from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
import json

File = open("authen.json")
data = json.load(File)
apikey = data["apikey"]
link = data["url"]

speech_to_text = SpeechToTextV1(
    iam_apikey=apikey,
    url=link
)

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

myRecognizeCallback = MyRecognizeCallback()

with open(join(dirname(__file__), '', 'audio-file.flac'),
              'rb') as audio_file:
    audio_source = AudioSource(audio_file)
    speech_to_text.recognize_using_websocket(
        audio=audio_source,
        content_type='audio/flac',
        recognize_callback=myRecognizeCallback,
        model='en-US_BroadbandModel',
        keywords=['colorado', 'tornado', 'tornadoes'],
        keywords_threshold=0.5,
        max_alternatives=3)
