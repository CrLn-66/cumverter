from flask import Flask, render_template, request, send_file, url_for
from flask_socketio import SocketIO, emit
import time  # Example for simulating progress
# ... other imports
import uuid
import os
import shutil
import rawpy
import imageio

upload_folder = os.getcwd() + "/uploads"
this = os.getcwd() + "/"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder 
socketio = SocketIO(app)
print(app.config['UPLOAD_FOLDER'])
# ... routes (index, convert)
def convert_and_emit_progress(uid, total_images, current_position, downloadlink):
    # ... perform conversion
        socketio.emit('progress', {'id': uid,'total_images': total_images, "cuurent": current_position, "dlurl": downloadlink}) # Simulate processing time
@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

def convert(folder, format, id, total):
    os.mkdir(os.path.join(this+"output/", id))
    for i, file in enumerate(os.listdir(folder)):
        print(file)
        filepath = os.path.join(folder, file) 
        socketio.emit('progress', {'id': id,'total_images': total, "current": i, "dlurl": "null"})
        a = rawpy.imread(filepath).postprocess()
        out = os.path.join(this+"output/", f"{id}/")
        imageio.imsave(f"{out}{i}.{format}", a)
    
    if total < 2:
        shutil.move(f"{out}0.{format}", this+"static/"+ f"0.{format}")
        urk = url_for('static', filename=f"0.{format}")
        print(urk)
        socketio.emit('progress', {'id': id,'total_images': total, "current": i+1, "dlurl": urk})
        return
    zip_files(id)
    socketio.emit('progress', {'id': id,'total_images': total, "current": i+1, "dlurl": url_for('static', filename=f"{id}.zip")})



@app.route('/convert', methods=['POST'])
def convertweb():
    if 'files' not in request.files:
        return "No files uploaded"

    files = request.files.getlist('files')
    output_format = request.form.get('format')
    total_images = len(files)
    # Start conversion in a background thread
    uid = str(uuid.uuid1())
    os.mkdir(app.config['UPLOAD_FOLDER'] + f"/{uid}")
    for i, file in enumerate(files):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'] + f"/{uid}", filename)
        file.save(filepath)
        
    convert(app.config['UPLOAD_FOLDER'] + f"/{uid}/", output_format, uid, total_images)
    return "Conversion started!"

@app.route('/')
def index():
    return render_template("index.html")

def zip_files(folder):
    shutil.make_archive(os.path.join(this, f"static/{folder}"), "zip", this +  f"output/{folder}")
if __name__ == '__main__':
    socketio.run(app, debug=True) 
