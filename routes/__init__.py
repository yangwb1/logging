from flask import Flask
from .asset_routes import bp as asset_bp
from .log_routes import bp as log_bp
from .search_routes import bp as search_bp
from .edit_routes import bp as edit_bp
from .grok_routes import bp as grok_bp

def register_blueprints(app: Flask):
    app.register_blueprint(asset_bp, url_prefix='/assets')
    app.register_blueprint(log_bp, url_prefix='/logs')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(edit_bp, url_prefix='/edit')
    app.register_blueprint(grok_bp, url_prefix='/grok')
