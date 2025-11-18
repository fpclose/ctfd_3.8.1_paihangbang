"""
CTFd-Paihangb Plugin
分赛道排行榜插件

Author: fpclose
Version: 1.0.0
Compatible: CTFd 3.8.1
"""

__version__ = "1.0.0"
__author__ = "fpclose"

from flask import Blueprint

def load(app):
    """
    插件加载入口
    """
    # 创建插件蓝图，注册静态文件和模板
    paihangb_bp = Blueprint(
        'ctfd_paihangb',
        __name__,
        template_folder='templates',
        static_folder='assets',
        static_url_path='/plugins/ctfd-paihangb/assets'
    )
    
    app.register_blueprint(paihangb_bp)
    
    # 导入并注册路由（API 和页面）
    from . import routes
    routes.register_routes(app)
    
    print("[ctfd-paihangb] 插件加载成功")
