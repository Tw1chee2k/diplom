from flask_admin.contrib.sqla import ModelView


class MessageView(ModelView):
    column_display_pk = True
    form_columns = ['text', 'user_email', 'created_at', 'category']
    column_list = ['id', 'text', 'user_email', 'created_at', 'category']
    column_default_sort = ('created_at', True)
    column_sortable_list = ('id', 'text', 'user_email', 'created_at', 'category')

    TEXT_TYPES = [
        (u'added to the processing', u'added to the processing'),
        (u'assembled', u'assembled'),
        (u'sorted', u' sorted'),
        (u'paid for', u'paid for'),
        
        (u'at the post office', u'at the post office'),
        
        (u'refund', u'refund'),
        (u'cancelled', u'cancelled'),
        (u'delivered', u'delivered'),
    ]
    
    form_choices = {
        'text': TEXT_TYPES,
    }

    can_delete = True
    can_create = True
    can_edit = True
    can_export = True
    export_max_rows = 500
    export_types = ['csv']
    
    
    column_searchable_list = ['text']
    column_filters = ['text', 'created_at']
    column_editable_list = ['text', 'category']
    
    
    create_modal = True
    edit_modal = True