from flask_admin.contrib.sqla import ModelView


class OrderView(ModelView):
    column_display_pk = True
    
    column_list = ['id', 
                   'type', 
                   'nomerzakaza',
                   'track_number',  
                   'status', 
                   'tovar_name', 
                   'tovar_quantity', 
                   'fio',  
                   'email', 
                   'telephone', 
                   'country', 
                   'city', 
                   'receiving_point', 
                   'street', 
                   'house', 
                   'flat', 
                   'promocod',  
                   'price', 
                   'comment', 
                   'created_at']

    column_default_sort = ('created_at', True)
    column_sortable_list = ('id', 
                   'type', 
                   'nomerzakaza',
                   'track_number',  
                   'status', 
                   'tovar_name', 
                   'tovar_quantity', 
                   'fio',  
                   'email', 
                   'telephone', 
                   'country', 
                   'city', 
                   'receiving_point', 
                   'street', 
                   'house', 
                   'flat', 
                   'promocod',  
                   'price', 
                   'comment', 
                   'created_at')

    STATUS_TYPES = [
        (u'In processing', u'In processing'),
        (u'Assembled', u'Assembled'),
        (u'Sorted', u'Sorted'),
        (u'Paid for', u'Paid for'),
        
        (u'At the post office', u'At the post office'),
        
        (u'Refund', u'Refund'),
        (u'Cancelled', u'Cancelled'),
        (u'Delivered', u'Delivered'),
    ]
    
    form_choices = {
        'status': STATUS_TYPES,
    }


    can_delete = True
    can_create = True
    can_edit = True
    can_export = True
    export_max_rows = 500
    export_types = ['csv']
    
    
    column_searchable_list = ['street', 'country', 'city','fio', 'email', 'telephone']
    column_filters = ['id', 
                   'type', 
                   'nomerzakaza',
                   'track_number',  
                   'status', 
                   'tovar_name', 
                   'tovar_quantity', 
                   'fio',  
                   'email', 
                   'telephone', 
                   'country', 
                   'city', 
                   'receiving_point', 
                   'street', 
                   'house', 
                   'flat', 
                   'promocod',  
                   'price', 
                   'comment', 
                   'created_at']
    
    column_editable_list = ['track_number', 'status']
    
    
    create_modal = True
    edit_modal = True