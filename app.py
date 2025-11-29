import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Cần thiết để hiện thông báo lỗi/thành công

# Cấu hình thư mục gốc
BASE_UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Tạo thư mục gốc nếu chưa có
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    # Xử lý tạo Album mới
    if request.method == 'POST':
        album_name = request.form.get('album_name')
        if album_name:
            # Tạo tên thư mục an toàn (bỏ ký tự đặc biệt)
            safe_name = secure_filename(album_name)
            new_album_path = os.path.join(BASE_UPLOAD_FOLDER, safe_name)
            if not os.path.exists(new_album_path):
                os.makedirs(new_album_path)
            return redirect(url_for('view_album', album_name=safe_name))

    # Lấy danh sách các album hiện có (là các thư mục con)
    albums = [f for f in os.listdir(BASE_UPLOAD_FOLDER) if os.path.isdir(os.path.join(BASE_UPLOAD_FOLDER, f))]
    return render_template('home.html', albums=albums)

@app.route('/album/<album_name>', methods=['GET', 'POST'])
def view_album(album_name):
    album_path = os.path.join(BASE_UPLOAD_FOLDER, album_name)
    
    # Nếu album không tồn tại thì quay về trang chủ
    if not os.path.exists(album_path):
        return redirect(url_for('home'))

    # Xử lý Upload nhiều file
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        
        files = request.files.getlist('files[]') # Lấy danh sách nhiều file
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(album_path, filename))
        
        return redirect(url_for('view_album', album_name=album_name))

    # Lấy danh sách ảnh trong album
    images = os.listdir(album_path)
    # Sắp xếp ảnh mới nhất lên đầu
    images.sort(key=lambda x: os.path.getmtime(os.path.join(album_path, x)), reverse=True)
    
    return render_template('album_view.html', album_name=album_name, images=images)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)