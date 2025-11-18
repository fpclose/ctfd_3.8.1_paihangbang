"""
CTFd-Paihangb Plugin
分赛道排行榜插件

Author: fpclose
Version: 1.0.0
Compatible: CTFd 3.8.1
"""

__version__ = "1.0.0"
__author__ = "fpclose"

def load(app):
    """
    插件加载入口
    """
    # 导入并注册路由（API）
    from . import routes
    routes.register_routes(app)
    
    print("[ctfd-paihangb] 插件加载成功")
