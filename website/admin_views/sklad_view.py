from flask_admin.contrib.sqla import ModelView


class SkladView(ModelView):
    column_display_pk = True

    can_delete = True
    can_create = True
    can_edit = True
    can_export = True