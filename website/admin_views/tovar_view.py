import os
from flask import url_for
from markupsafe import Markup
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from wtforms import validators

file_path = os.path.abspath(os.path.dirname(__name__))

class TovarView(ModelView):
    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'type': 'Type',
        'name': 'Name',
        'count': 'Count',
        'cost': 'Cost',
        'status': 'Status',
        'color': 'Color',
        'size': 'Size',
        'material': 'Material',
        'base': 'Base',
        'info': 'Info',
        'sklad_id': 'Sklad_id',
    }
    column_list = ['id', 'type', 'name', 'count', 'cost', 'status', 'color', 'size', 'material', 'base', 'info', 'img_name','sklad_id']
    column_default_sort = ('id', True)
    column_sortable_list = ['id', 'type', 'name', 'count', 'cost', 'status', 'color', 'size', 'material', 'base', 'info', 'img_name','sklad_id']

    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    export_max_rows = 500
    export_types = ['csv']

    form_args = {
        'name': dict(label='NAIMENOVANIE', validators=[validators.DataRequired()]),
    }

    TYPE_TYPES = [
        (u'Mat', u'Mat'),
        (u'Game sleeve', u'Game sleeve'),
        (u'Keyboard', u'Keyboard'),
        (u'Headphones', u'Headphones'),
        (u'Mouse', u'Mouse'),
    ]
    STATUS_TYPES = [
        (u'Soon', u'Soon'),
        (u'In stoke', u'In stoke'),
        (u'Sold', u'Sold'),
    ]
    COST_TYPES = [
        (u'29.99', u'29.99'),
        (u'39.99', u'39.99'),
    ]
    COLOR_TYPES = [
        (u'Pixel art', u'Pixel art'),
        (u'Black', u'Black'),
        (u'White', u'White'),
        (u'Anime', u'Anime'),
    ]
    SIZE_TYPES = [
        (u'450x400mm', u'450x400mm'),
        (u'900x400mm', u'900x400mm'),
    ]
    THICKNESS_TYPES = [
        (u'4mm', u'4mm'),
    ]
    MATERIAL_TYPES = [
        (u'Cloth', u'Cloth'),
    ]
    BASE_TYPES = [
        (u'Eco-friendly Rubber', u'Eco-friendly Rubber'),
    ]
    INFO_TYPES = [
        (u'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', u'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.'),
        (u'A samurai has no purpose, only a path... This mat will fit perfectly and decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!', u'A samurai has no purpose, only a path... This mat will fit perfectly и decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!'),
    ]

    form_choices = {
        'type': TYPE_TYPES,
        'status': STATUS_TYPES,
        'cost': COST_TYPES,
        'color': COLOR_TYPES,
        'size': SIZE_TYPES,
        'thickness': THICKNESS_TYPES,
        'material': MATERIAL_TYPES,
        'base': BASE_TYPES,
        'info': INFO_TYPES,
    }

    column_descriptions = dict(
        name='First and Last name'
    )

    column_searchable_list = ['name', 'type','img_name']
    column_filters = ['status', 'type']
    column_editable_list = ['cost', 'status', 'count', 'img_name']

    create_modal = True
    edit_modal = True

    form_excluded_columns = ['id']



    def create_form(self, obj=None):
        return super(TovarView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(TovarView, self).edit_form(obj)    