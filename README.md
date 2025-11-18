# CTFd-Paihangb Plugin

CTFd 3.8.1 分赛道排行榜插件

## 📋 插件简介

`ctfd-paihangb` 是一个用于 CTFd 3.8.1 的分赛道排行榜插件。该插件根据团队的参与赛道将排行榜分为不同的榜单，并支持灵活的筛选功能。

**作者**：fpclose  
**版本**：1.0.0  
**兼容**：CTFd 3.8.1  
**依赖**：ctfd-tuandui 插件（用于获取团队赛道信息）

## ✨ 功能特性

### 四大榜单

1. **总榜** - 显示所有团队的排名
2. **新生榜** - 只显示新生赛道的团队
3. **进阶榜** - 只显示进阶赛道的团队
4. **社会榜** - 只显示社会赛道的团队

### 核心功能

- ✅ **一键切换** - 通过按钮快速切换不同榜单
- ✅ **学校筛选** - 按学校名称筛选团队
- ✅ **实时搜索** - 根据队伍名称实时过滤
- ✅ **自动排名** - 按分数和解题时间自动排序
- ✅ **美观界面** - 渐变色设计，响应式布局
- ✅ **自动刷新** - 每30秒自动更新数据
- ✅ **排名徽章** - 前三名特殊显示（金银铜牌）

## 🎨 界面展示

### 榜单切换

```
┌─────────────────────────────────────────────────────┐
│  [🏆 总榜]  [🎓 新生榜]  [🚀 进阶榜]  [👥 社会榜]   │
└─────────────────────────────────────────────────────┘
```

### 筛选器

```
┌──────────────────────────────────────────┐
│  🔍 筛选器                               │
│                                          │
│  学校：[下拉选择]                         │
│  搜索：[队伍名称]                         │
│  [重置]                                  │
└──────────────────────────────────────────┘
```

### 排行榜表格

```
┌──────┬────────────┬────────────┬──────────┬────────┬──────┐
│ 排名 │ 队伍名称    │ 学校       │ 赛道     │ 解题数 │ 总分 │
├──────┼────────────┼────────────┼──────────┼────────┼──────┤
│  🥇  │ Team A     │ 北京大学   │ 新生赛道 │   10   │ 1000 │
│  🥈  │ Team B     │ 清华大学   │ 进阶赛道 │    8   │  900 │
│  🥉  │ Team C     │ 复旦大学   │ 新生赛道 │    7   │  800 │
│   4  │ Team D     │ 上海交大   │ 社会赛道 │    6   │  700 │
└──────┴────────────┴────────────┴──────────┴────────┴──────┘
```

## 📂 文件结构

```
/opt/CTFd/CTFd/plugins/ctfd-paihangb/
├── __init__.py                          # 插件入口
├── config.json                          # 插件配置
├── routes.py                            # 路由和数据处理
├── README.md                            # 本文件
├── install.sh                           # 一键安装脚本
├── templates/
│   └── scoreboard/
│       └── custom_scoreboard.html       # 排行榜页面模板
└── assets/
    ├── css/
    │   └── scoreboard.css               # 样式文件
    └── js/
        └── scoreboard.js                # 前端交互逻辑
```

## 🚀 安装方法

### 前置要求

⚠️ **重要**：本插件依赖 `ctfd-tuandui` 插件提供的团队赛道信息

请确保已安装：
1. [ctfd-user](https://github.com/fpclose/ctfd_3.8.1_user)
2. [ctfd-tuandui](https://github.com/fpclose/ctfd_3.8.1_tuandui)

### 方法一：使用一键安装脚本（推荐）

```bash
# 下载安装脚本
wget https://raw.githubusercontent.com/fpclose/ctfd_3.8.1_paihangb/main/install.sh

# 添加执行权限
chmod +x install.sh

# 运行安装（需要 root 或 sudo 权限）
sudo ./install.sh
```

### 方法二：手动安装

```bash
# 克隆仓库
cd /opt/CTFd/CTFd/plugins/
git clone https://github.com/fpclose/ctfd_3.8.1_paihangb.git ctfd-paihangb

# 重启 CTFd
cd /opt/CTFd && docker compose restart ctfd
```

## 📖 使用说明

### 访问排行榜

安装后，访问以下地址查看自定义排行榜：

```
http://your-ctfd-url/scoreboard/custom
```

### 操作说明

#### 1. 切换榜单

点击顶部的按钮快速切换不同榜单：
- **总榜** - 显示所有团队
- **新生榜** - 只显示新生赛道团队
- **进阶榜** - 只显示进阶赛道团队
- **社会榜** - 只显示社会赛道团队

#### 2. 使用筛选器

点击"筛选器"展开筛选选项：
- **学校筛选** - 从下拉菜单选择特定学校
- **搜索框** - 输入队伍名称进行实时搜索
- **重置按钮** - 清除所有筛选条件

#### 3. 查看详情

- 点击队伍名称可以跳转到该队伍的详情页
- 排名前三的队伍会显示特殊的金银铜徽章
- 不同赛道的队伍会显示不同颜色的徽章

## 🔧 技术实现

### 1. 数据获取与缓存

```python
@cache.memoize(timeout=60)
def get_scoreboard_data(track=None, school=None):
    """获取排行榜数据，60秒缓存"""
    # 查询团队
    # 计算分数
    # 排序
    return scoreboard
```

### 2. API 接口

```
GET /api/scoreboard/data?track=新生赛道&school=北京大学
```

返回 JSON 格式的排行榜数据：
```json
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "team_id": 1,
      "team_name": "Team A",
      "school": "北京大学",
      "track": "新生赛道",
      "score": 1000,
      "solve_count": 10,
      "last_solve": "2025-11-16T12:00:00"
    }
  ]
}
```

### 3. 前端交互

- **Vue.js 风格** - 数据驱动的界面更新
- **AJAX 异步加载** - 不刷新页面更新数据
- **本地过滤** - 搜索功能在前端进行，响应更快
- **自动刷新** - 每30秒自动请求最新数据

### 4. 排名规则

1. **主要排序** - 按总分从高到低
2. **次要排序** - 分数相同时，按最后解题时间从早到晚
3. **动态计算** - 每次请求时实时计算，确保准确性

## 🎨 样式设计

### 颜色方案

- **总榜按钮** - 蓝色（#007bff）
- **新生赛道** - 绿色徽章（#28a745）
- **进阶赛道** - 青色徽章（#17a2b8）
- **社会赛道** - 灰色徽章（#6c757d）

### 排名徽章

- **第1名** - 金色渐变（金牌）
- **第2名** - 银色渐变（银牌）
- **第3名** - 铜色渐变（铜牌）
- **其他** - 灰色背景

### 响应式设计

- 桌面端：完整显示所有列
- 平板端：隐藏部分列
- 手机端：按钮纵向排列，表格横向滚动

## 🔄 与原版排行榜的区别

### 原版 CTFd 排行榜

- 只有一个总榜
- 无法按赛道筛选
- 无法按学校筛选
- 样式较为简单

### ctfd-paihangb 插件

- ✅ 四个独立榜单（总榜、新生榜、进阶榜、社会榜）
- ✅ 按赛道一键切换
- ✅ 按学校筛选
- ✅ 实时搜索队伍
- ✅ 美观的渐变设计
- ✅ 前三名特殊显示
- ✅ 自动刷新数据

## 📊 使用场景

### 场景 1：查看新生榜

```
用户操作：点击"新生榜"按钮
系统响应：
  - 只显示参与赛道为"新生赛道"的团队
  - 自动重新排名
  - 更新队伍数量显示
```

### 场景 2：筛选特定学校

```
用户操作：
  1. 选择榜单（如进阶榜）
  2. 在学校下拉框选择"北京大学"
  
系统响应：
  - 显示进阶赛道 + 北京大学的所有团队
  - 在这些团队中进行排名
```

### 场景 3：搜索特定队伍

```
用户操作：在搜索框输入"dragon"

系统响应：
  - 实时过滤包含"dragon"的队伍名称
  - 保持当前的赛道和学校筛选
  - 即时更新显示结果
```

## 🐛 故障排除

### 问题 1：排行榜显示为空

**症状**：页面加载完成，但没有显示任何队伍

**可能原因**：
- ctfd-tuandui 插件未安装
- 团队没有填写参与赛道信息

**解决方法**：
1. 确认 ctfd-tuandui 插件已安装并加载
2. 检查数据库中是否有团队赛道数据：
```sql
SELECT t.name, tfe.value 
FROM teams t 
JOIN field_entries tfe ON t.id = tfe.team_id 
JOIN fields f ON tfe.field_id = f.id 
WHERE f.name = '参与赛道';
```

### 问题 2：数据不刷新

**症状**：排行榜数据不更新

**解决方法**：
1. 清除浏览器缓存（Ctrl + F5）
2. 清除服务器缓存：
```python
from CTFd.cache import cache
cache.clear()
```

### 问题 3：样式显示异常

**症状**：页面布局混乱，样式不正确

**解决方法**：
1. 检查 CSS 文件是否正确加载
2. 清除浏览器缓存
3. 检查浏览器控制台是否有错误

### 问题 4：API 请求失败

**症状**：浏览器控制台显示 404 或 500 错误

**解决方法**：
1. 检查插件是否正确加载：
```bash
docker compose logs ctfd | grep "ctfd-paihangb"
```
2. 确认路由已注册
3. 查看 CTFd 日志中的错误信息

## 🔄 卸载

### 保留数据卸载

```bash
# 删除插件目录
rm -rf /opt/CTFd/CTFd/plugins/ctfd-paihangb

# 重启 CTFd
cd /opt/CTFd && docker compose restart ctfd
```

**注意**：插件不修改数据库，不需要删除任何数据

## 📝 更新日志

### v1.0.0 (2025-11-16)

- ✨ 初始版本发布
- ✅ 支持四大榜单切换
- ✅ 支持学校筛选
- ✅ 支持实时搜索
- ✅ 美观的界面设计
- ✅ 响应式布局
- ✅ 自动刷新功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👤 作者

**fpclose**

- GitHub: [@fpclose](https://github.com/fpclose)
- 项目地址：
  - ctfd-paihangb: [https://github.com/fpclose/ctfd_3.8.1_paihangb](https://github.com/fpclose/ctfd_3.8.1_paihangb)
  - ctfd-user: [https://github.com/fpclose/ctfd_3.8.1_user](https://github.com/fpclose/ctfd_3.8.1_user)
  - ctfd-tuandui: [https://github.com/fpclose/ctfd_3.8.1_tuandui](https://github.com/fpclose/ctfd_3.8.1_tuandui)

## 🙏 致谢

感谢 CTFd 项目：[https://github.com/CTFd/CTFd](https://github.com/CTFd/CTFd)

## 📚 相关文档

- [ctfd-user 插件](https://github.com/fpclose/ctfd_3.8.1_user) - 用户信息定制插件（前置依赖）
- [ctfd-tuandui 插件](https://github.com/fpclose/ctfd_3.8.1_tuandui) - 团队信息定制插件（前置依赖）

---

**如果这个插件对你有帮助，请给个 ⭐ Star！**

