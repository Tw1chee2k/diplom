from flask_admin.contrib.sqla import ModelView


class PointView(ModelView):
    column_display_pk = True

    column_list = ['id', 'city', 'street', 'number']
    column_default_sort = ('id', True)
    column_sortable_list = ('id', 'city', 'street', 'number')


    can_delete = True
    can_create = True
    can_edit = True
    can_export = True    
    export_max_rows = 500
    export_types = ['csv']
    
    column_searchable_list = ['street', 'number', 'city',]
    column_filters = ['street', 'number', 'city']
    column_editable_list = ['street', 'number', 'city']
    
    create_modal = True
    edit_modal = True