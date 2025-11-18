"""
CTFd-Paihangb Plugin
分赛道排行榜插件

Author: fpclose
Version: 1.0.0
Compatible: CTFd 3.8.1
"""

__version__ = "1.0.2"
__author__ = "fpclose"

from flask import Blueprint, jsonify, request
import json

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
    
    # 添加 after_request 钩子来扩展 scoreboard API
    @app.after_request
    def add_school_to_scoreboard(response):
        """在 scoreboard API 响应中添加学校信息"""
        # 只处理 scoreboard API 请求
        if request.path == '/api/v1/scoreboard' and response.status_code == 200:
            try:
                data = json.loads(response.get_data(as_text=True))
                if data.get('success') and data.get('data'):
                    # 导入需要的模块
                    from CTFd.models import TeamFieldEntries, TeamFields
                    
                    # 获取学校字段
                    school_field = TeamFields.query.filter_by(name="学校名称").first()
                    track_field = TeamFields.query.filter_by(name="参与赛道").first()
                    
                    # 为每个队伍添加学校信息
                    for team in data['data']:
                        team_id = team.get('account_id')
                        
                        # 添加学校信息
                        team['school'] = ''
                        if school_field:
                            entry = TeamFieldEntries.query.filter_by(
                                team_id=team_id,
                                field_id=school_field.id
                            ).first()
                            if entry and entry.value:
                                team['school'] = entry.value
                        
                        # 添加赛道信息
                        team['track'] = ''
                        if track_field:
                            entry = TeamFieldEntries.query.filter_by(
                                team_id=team_id,
                                field_id=track_field.id
                            ).first()
                            if entry and entry.value:
                                team['track'] = entry.value
                    
                    # 更新响应
                    response.set_data(json.dumps(data))
            except Exception as e:
                print(f"[ctfd-paihangb] 添加学校信息失败: {e}")
        
        return response
    
    print("[ctfd-paihangb] 插件加载成功")
    print("[ctfd-paihangb] Scoreboard API 扩展已启用")
