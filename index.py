import json
from re import T
from flask import Flask, after_this_request, request, jsonify, make_response, send_from_directory
import os
import uuid
import shutil
import magic

from requests import Response

app = Flask(__name__, static_folder=os.path.dirname(os.getcwd()))

tmpdir = 'temp'
uploaddir = 'temp/upload'
downloaddir = 'temp/download'

os.makedirs(tmpdir, exist_ok=True)
os.makedirs(uploaddir, exist_ok=True)
os.makedirs(downloaddir, exist_ok=True)


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    tmpname = uuid.uuid4()
    args = request.args.to_dict()

    uploaded_filename = f'{uploaddir}/{tmpname}'
    downloaded_filename = f'{downloaddir}/{tmpname}'

    # @after_this_request
    # def remove_files(response):
    #     if os.path.exists(uploaded_filename):
    #         os.unlink(uploaded_filename)
    #     if os.path.exists(downloaded_filename):
    #         shutil.rmtree(downloaded_filename)
    #     return response

    if 'type' not in args:
        return make_response(jsonify({'message': 'You must inform "type"'}), 422)

    if args['type'] not in ['vocals', 'instrumental']:
        return make_response(jsonify({'message': 'You must inform "type" as "vocals" or "instrumental"'}), 422)

    uploaded_file.save(uploaded_filename)
    mime = magic.Magic(mime=True).from_file(uploaded_filename)
    if(not mime.startswith('audio/')):
        return make_response(jsonify({'message': 'You must upload an audio file'}), 422)

    os.system(
        f'spleeter separate -o {downloaddir} -p spleeter:2stems {uploaded_filename}')
    print(downloaded_filename)
    return send_from_directory(directory=f'{downloaded_filename}', path=('vocals.wav' if args['type'] == 'vocals' else 'accompaniment.wav'), as_attachment=True)


app.run(host='0.0.0.0')
