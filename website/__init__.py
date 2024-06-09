import os
from os import path
from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
DB_NAME = "database.db"
babel = Babel()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'anykey'
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
    app.config['BABEL_DEFAULT_LOCALE'] = 'eng'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(path.dirname(__file__), DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    db.init_app(app)
    babel.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        create_database(app)

    from website.views import MyMainView
    from .models import User, Tovar, Sklad, Cart, Order, Comment, Message, Point
    from website.admin_views.user_view import UserView
    from website.admin_views.tovar_view import TovarView
    from website.admin_views.comment_view import CommentView
    from website.admin_views.cart_view import CartView
    from website.admin_views.order_view import OrderView
    from website.admin_views.point_view import PointView
    from website.admin_views.message_view import MessageView
    from website.admin_views.sklad_view import SkladView
    from website.admin_views.image_view import ImageView
    
    admin = Admin(app, 'Tw1_comp', index_view=MyMainView(), template_mode='bootstrap4', url='/')
    admin.add_view(CommentView(Comment, db.session))
    admin.add_view(MessageView(Message, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(TovarView(Tovar, db.session))
    admin.add_view(OrderView(Order, db.session))
    admin.add_view(SkladView(Sklad, db.session))
    admin.add_view(CartView(Cart, db.session))
    admin.add_view(PointView(Point, db.session))
    admin.add_view(ImageView())
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    return app

def create_database(app):
    if not path.exists(f'website/{DB_NAME}'):
        with app.app_context():
            db.create_all()
        print('Created Database!')
