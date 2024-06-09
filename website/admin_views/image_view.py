from flask_admin.contrib.fileadmin import FileAdmin
import os
from urllib.parse import quote, unquote

class ImageView(FileAdmin):
    def __init__(self, *args, **kwargs):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__name__), 'website', 'static'))
        image_folder = os.path.join(base_path, 'img')

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        
        super(ImageView, self).__init__(image_folder, '/static/img/', name='Images')
