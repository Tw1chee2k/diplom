import bcrypt
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired, Email, Length
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash, generate_password_hash

class UserView(ModelView):
    column_display_pk = True
    column_list = ['id', 'type', 'email', 'password', 'nickname']
    column_default_sort = ('nickname', True)
    column_sortable_list = ('id', 'type', 'email', 'password', 'nickname')
    
    can_delete = True
    can_create = True
    can_edit = True
    can_export = True
    
    export_max_rows = 500
    export_types = ['csv']
    
    form_args = {
        'nickname': dict(label='nick', validators = [DataRequired()]),
        'email': dict(label='email', validators = [Email()])
    }
    
    AVAILABLE_USER_TYPES = [
        (u'Admin', u'Admin'),
        (u'User', u'User'),
    ]
    
    form_choices = {
        'type': AVAILABLE_USER_TYPES,
    }
    
    column_descriptions = dict(
        nickname='Main nickname'
    )
    
    column_exclude_list = ['password']
    column_searchable_list = ['email', 'nickname']
    column_filters = ['id','email', 'nickname']
    column_editable_list = ['email', 'nickname', 'type']
    
    create_modal = True
    edit_modal = True
    
    def on_model_change(self, view, model, is_created):
        model.password = generate_password_hash(model.password)
        
        
    # form_excluded_columns = ['nickname']