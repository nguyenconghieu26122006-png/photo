import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Cấu hình thư mục lưu ảnh
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tạo thư mục uploads nếu chưa có
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kiểm tra xem có file trong request không
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        # Nếu người dùng không chọn file
        if file.filename == '':
            return redirect(request.url)
            
        # Nếu file hợp lệ thì lưu lại
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    # Lấy danh sách ảnh trong thư mục để hiển thị
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    # Sắp xếp ảnh mới nhất lên đầu (tùy chọn)
    images.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
    
    return render_template('index.html', images=images)

if __name__ == '__main__':
    # host='0.0.0.0' để các máy khác trong cùng mạng LAN có thể truy cập được
    app.run(debug=True, host='0.0.0.0', port=5000)