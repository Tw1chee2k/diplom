from flask_admin.contrib.sqla import ModelView
from wtforms import form, StringField, IntegerField
from wtforms.validators import DataRequired, Length


class CommentView(ModelView):
    column_display_pk = True
    form_columns = ['text', 'user_id', 'tovar_id', 'created_at']

    
    column_list = ['id', 'text', 'user_id', 'tovar_id', 'created_at']
    column_default_sort = ('created_at', True)
    column_sortable_list = ('id', 'text', 'user_id', 'tovar_id', 'created_at')
    can_delete = True
    can_create = True
    can_edit = True
    can_export = True
    
    export_max_rows = 500
    export_types = ['csv']
    
    column_searchable_list = ['text', 'user_id', 'tovar_id']
    column_filters = ['text', 'user_id', 'tovar_id']
    
    column_editable_list = ['text']
    
    create_modal = True
    edit_modal = True
