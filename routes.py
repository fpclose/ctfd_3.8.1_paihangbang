"""
路由处理，提供分赛道排行榜 API 和页面
"""

import json
from flask import Blueprint, jsonify, render_template
from flask_restx import Api, Namespace, Resource

from CTFd.utils.decorators.visibility import check_score_visibility
from CTFd.models import Fields, FieldEntries, db
from .scores import (
    get_all_standings,
    get_new_standings,
    get_upper_standings,
    get_social_standings
)


def format_standings(standings):
    """
    格式化排行榜数据为 JSON
    """
    response = []
    for rank, team in enumerate(standings, start=1):
        response.append({
            "rank": rank,
            "team_id": team.account_id,
            "team_name": team.name,
            "score": float(team.score) if team.score else 0.0
        })
    return response


def register_routes(app):
    """
    注册排行榜 API 路由
    """
    # 创建 API 蓝图
    api_bp = Blueprint("ctfd_paihangb_api", __name__, url_prefix="/api/v1")
    api = Api(api_bp, version="v1", title="CTFd Paihangbang API", doc=False)
    
    # 创建命名空间
    top10_namespace = Namespace('top10', description="分赛道排行榜 API")
    
    @top10_namespace.route('/leaderboards')
    class Top10Leaderboards(Resource):
        @check_score_visibility
        def get(self):
            """
            获取四个赛道的前10名队伍信息
            """
            try:
                all_standings = get_all_standings(count=10)
                new_standings = get_new_standings(count=10)
                upper_standings = get_upper_standings(count=10)
                social_standings = get_social_standings(count=10)
                
                response = {
                    "all": format_standings(all_standings),
                    "new": format_standings(new_standings),
                    "upper": format_standings(upper_standings),
                    "social": format_standings(social_standings)
                }
                
                return {"success": True, "data": response}, 200
            
            except Exception as e:
                return {"success": False, "message": str(e)}, 500
    
    # 注册命名空间
    api.add_namespace(top10_namespace, "/top10")
    
    # 添加获取赛道团队 ID 的路由（用于前端筛选）
    @api_bp.route('/teams/track/<string:track_name>')
    @check_score_visibility
    def get_track_teams(track_name):
        """
        获取指定赛道的所有团队 ID
        """
        try:
            # 查找"参与赛道"字段
            track_field = Fields.query.filter_by(name="参与赛道", type="team").first()
            if not track_field:
                print(f"[ctfd-paihangb] 未找到'参与赛道'字段")
                return jsonify({"success": True, "data": []})
            
            print(f"[ctfd-paihangb] 找到'参与赛道'字段，ID: {track_field.id}")
            
            # 查找该赛道的所有团队
            # 数据库中存储的是 JSON 格式的值，如 "新生赛道"
            all_entries = FieldEntries.query.filter_by(field_id=track_field.id).all()
            
            team_ids = []
            for entry in all_entries:
                try:
                    # 解析 JSON 值
                    value = json.loads(entry.value) if entry.value else ""
                    print(f"[ctfd-paihangb] 团队 {entry.team_id} 的赛道值: {value}")
                    
                    if value == track_name:
                        team_ids.append(entry.team_id)
                except json.JSONDecodeError:
                    # 如果不是 JSON，直接比较
                    if entry.value == track_name:
                        team_ids.append(entry.team_id)
            
            print(f"[ctfd-paihangb] 赛道 '{track_name}' 的团队 ID: {team_ids}")
            
            return jsonify({"success": True, "data": team_ids})
        
        except Exception as e:
            print(f"[ctfd-paihangb] 错误: {str(e)}")
            return jsonify({"success": False, "message": str(e)}), 500
    
    # 注册蓝图
    app.register_blueprint(api_bp)
    
    # 创建页面路由蓝图
    page_bp = Blueprint(
        "ctfd_paihangb_pages",
        __name__,
        template_folder="templates",
        static_folder="assets",
        url_prefix="/scoreboard"
    )
    
    @page_bp.route('/custom')
    @check_score_visibility
    def custom_scoreboard():
        """
        自定义排行榜页面
        """
        # 获取所有学校列表
        school_field = Fields.query.filter_by(name="学校名称", type="team").first()
        schools = []
        
        if school_field:
            entries = FieldEntries.query.filter_by(field_id=school_field.id).all()
            schools_set = set()
            for entry in entries:
                if entry.value:
                    try:
                        value = json.loads(entry.value) if isinstance(entry.value, str) and entry.value.startswith('"') else entry.value
                        if value and value.strip():
                            schools_set.add(value.strip())
                    except:
                        if entry.value.strip():
                            schools_set.add(entry.value.strip())
            
            schools = sorted(list(schools_set))
        
        return render_template('scoreboard/custom_scoreboard.html', schools=schools)
    
    # 注册页面蓝图
    app.register_blueprint(page_bp)
    
    print("[ctfd-paihangb] 路由注册成功")
    print("[ctfd-paihangb] 页面地址: /scoreboard/custom")
    print("[ctfd-paihangb] API 地址: /api/v1/top10/leaderboards")
    print("[ctfd-paihangb] API 地址: /api/v1/teams/track/<track_name>")
