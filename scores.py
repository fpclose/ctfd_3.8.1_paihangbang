"""
分数计算和排行榜数据获取模块
基于 CTFd 原生排行榜系统
"""

from sqlalchemy.sql.expression import union_all
from sqlalchemy import func

from CTFd.cache import cache
from CTFd.models import db, Teams, Solves, Awards, Challenges, TeamFieldEntries, TeamFields
from CTFd.utils.dates import unix_time_to_utc
from CTFd.utils import get_config
from CTFd.utils.modes import get_model


def get_scores(admin=False):
    """
    计算所有团队的分数
    包括 Solves 和 Awards
    """
    scores = (
        db.session.query(
            Solves.account_id.label("account_id"),
            db.func.sum(Challenges.value).label("score"),
            db.func.max(Solves.id).label("id"),
            db.func.max(Solves.date).label("date"),
        )
        .join(Challenges)
        .filter(Challenges.value != 0)
        .group_by(Solves.account_id)
    )

    awards = (
        db.session.query(
            Awards.account_id.label("account_id"),
            db.func.sum(Awards.value).label("score"),
            db.func.max(Awards.id).label("id"),
            db.func.max(Awards.date).label("date"),
        )
        .filter(Awards.value != 0)
        .group_by(Awards.account_id)
    )

    # 冻结时间过滤
    freeze = get_config("freeze")
    if not admin and freeze:
        scores = scores.filter(Solves.date < unix_time_to_utc(freeze))
        awards = awards.filter(Awards.date < unix_time_to_utc(freeze))

    # 合并 solves 和 awards
    results = union_all(scores, awards).alias("results")

    # 按团队 ID 汇总分数
    sumscores = (
        db.session.query(
            results.columns.account_id,
            db.func.sum(results.columns.score).label("score"),
            db.func.max(results.columns.id).label("id"),
            db.func.max(results.columns.date).label("date"),
        )
        .group_by(results.columns.account_id)
        .subquery()
    )

    return sumscores


@cache.memoize(timeout=60)
def get_track_team_ids(track_name):
    """
    获取指定赛道的所有团队 ID
    
    Args:
        track_name: 赛道名称（新生赛道、进阶赛道、社会赛道）
    """
    team_ids = []
    
    # 查找"参与赛道"字段
    track_field = TeamFields.query.filter_by(name="参与赛道").first()
    if not track_field:
        return team_ids
    
    # 查找该赛道的所有团队
    teams = TeamFieldEntries.query.filter_by(
        field_id=track_field.id
    ).filter(
        TeamFieldEntries.value == track_name
    ).all()
    
    for team in teams:
        team_ids.append(team.team_id)
    
    return team_ids


@cache.memoize(timeout=60)
def get_standings(track=None, count=None, admin=False):
    """
    获取排行榜数据
    
    Args:
        track: 赛道筛选（None=全部, 新生赛道, 进阶赛道, 社会赛道）
        count: 限制返回数量
        admin: 是否管理员视图
    
    Returns:
        排行榜数据列表
    """
    Model = get_model()
    sumscores = get_scores(admin)
    
    # 构建基础查询
    if admin:
        standings_query = (
            db.session.query(
                Model.id.label("account_id"),
                Model.name.label("name"),
                Model.hidden,
                Model.banned,
                sumscores.columns.score,
            )
            .join(sumscores, Model.id == sumscores.columns.account_id)
            .order_by(sumscores.columns.score.desc(), sumscores.columns.id)
        )
    else:
        standings_query = (
            db.session.query(
                Model.id.label("account_id"),
                Model.name.label("name"),
                sumscores.columns.score,
            )
            .join(sumscores, Model.id == sumscores.columns.account_id)
            .filter(Model.banned == False, Model.hidden == False)
            .order_by(sumscores.columns.score.desc(), sumscores.columns.id)
        )
    
    # 赛道过滤
    if track:
        team_ids = get_track_team_ids(track)
        if team_ids:
            standings_query = standings_query.filter(Model.id.in_(team_ids))
        else:
            # 如果没有找到该赛道的团队，返回空列表
            return []
    
    # 限制数量
    if count:
        standings = standings_query.limit(count).all()
    else:
        standings = standings_query.all()
    
    return standings


@cache.memoize(timeout=60)
def get_all_standings(count=None, admin=False):
    """获取总榜"""
    return get_standings(track=None, count=count, admin=admin)


@cache.memoize(timeout=60)
def get_new_standings(count=None, admin=False):
    """获取新生榜"""
    return get_standings(track="新生赛道", count=count, admin=admin)


@cache.memoize(timeout=60)
def get_upper_standings(count=None, admin=False):
    """获取进阶榜"""
    return get_standings(track="进阶赛道", count=count, admin=admin)


@cache.memoize(timeout=60)
def get_social_standings(count=None, admin=False):
    """获取社会榜"""
    return get_standings(track="社会赛道", count=count, admin=admin)

