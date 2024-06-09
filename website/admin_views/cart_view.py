from flask_admin.contrib.sqla import ModelView


class CartView(ModelView):
    column_display_pk = True

    column_list = ['id', 'user_email', 'tovar_name', 'quantity', 'price']
    column_default_sort = ('id', True)
    column_sortable_list = ('id', 'user_email', 'tovar_name', 'quantity', 'price')

    can_delete = True
    can_create = True
    can_edit = True
    can_export = True
    export_max_rows = 500
    export_types = ['csv']
    
    column_searchable_list = ['user_email', 'tovar_name']
    column_filters = ['user_email', 'tovar_name']
    column_editable_list = ['quantity']
    
    create_modal = True
    edit_modal = True