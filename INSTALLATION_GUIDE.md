# CTFd-Paihangb 插件安装指南

## 📋 概述

CTFd-Paihangb（排行榜）插件为 CTFd 3.8.1 提供了分赛道排行榜功能，支持按赛道和学校进行筛选，提供更丰富的排行榜查看体验。

### 主要特性

- ✅ **四大榜单**：总榜、新生榜、进阶榜、社会榜
- ✅ **一键切换**：快速切换不同赛道榜单
- ✅ **学校筛选**：按学校名称筛选团队
- ✅ **实时搜索**：根据队伍名称实时过滤
- ✅ **自动排名**：按分数和解题时间自动排序
- ✅ **美观界面**：渐变色设计，响应式布局
- ✅ **自动刷新**：每30秒自动更新数据
- ✅ **排名徽章**：前三名特殊显示（金银铜牌）

## 🚀 快速开始

### 前置要求

⚠️ **重要**：本插件依赖以下插件，请按顺序安装：

1. **ctfd-user** - 提供用户自定义字段
   - 仓库：https://github.com/fpclose/ctfd_3.8.1_user
   
2. **ctfd-tuandui** - 提供团队赛道信息
   - 仓库：https://github.com/fpclose/ctfd_3.8.1_tuandui

### 方法一：使用安装脚本（推荐）

```bash
# 1. 下载插件
cd /opt/CTFd/CTFd/plugins
git clone https://github.com/fpclose/ctfd_3.8.1_paihangbang.git ctfd-paihangb

# 2. 运行安装脚本
cd ctfd-paihangb
chmod +x install.sh
sudo ./install.sh
```

### 方法二：手动安装

```bash
# 1. 克隆仓库到插件目录
cd /opt/CTFd/CTFd/plugins
git clone https://github.com/fpclose/ctfd_3.8.1_paihangbang.git ctfd-paihangb

# 2. 重启 CTFd
cd /opt/CTFd
docker compose restart ctfd
# 或者如果使用 systemd
sudo systemctl restart ctfd
```

## 📁 文件结构

```
ctfd-paihangb/
├── __init__.py                          # 插件入口，注册 Blueprint
├── config.json                          # 插件配置
├── routes.py                            # 路由和 API 端点（包含页面路由）
├── scores.py                            # 分数计算逻辑
├── install.sh                           # 安装脚本
├── templates/
│   └── scoreboard/
│       └── custom_scoreboard.html       # 排行榜页面模板
├── assets/
│   ├── css/
│   │   └── scoreboard.css               # 样式文件
│   └── js/
│       └── scoreboard.js                # 前端交互逻辑
├── README.md                            # 插件说明
└── INSTALLATION_GUIDE.md                # 本文档
```

## 🎯 功能说明

### 1. 四大榜单

#### 总榜
- 显示所有参赛团队
- 按总分排名
- 不做任何筛选

#### 新生榜
- 只显示"新生赛道"的团队
- 独立排名系统
- 适用于新生组别

#### 进阶榜
- 只显示"进阶赛道"的团队
- 独立排名系统
- 适用于高年级组别

#### 社会榜
- 只显示"社会赛道"的团队
- 独立排名系统
- 适用于社会人员组别

### 2. 筛选功能

#### 学校筛选
- 从下拉菜单选择特定学校
- 自动列出所有参赛学校
- 可与赛道筛选组合使用

#### 搜索功能
- 实时搜索队伍名称
- 前端过滤，响应迅速
- 支持模糊匹配

## 🔧 技术实现

### 页面路由

```python
# 访问地址
GET /scoreboard/custom

# 返回排行榜页面，包含学校列表数据
```

### API 接口

#### 1. 获取前10名排行榜数据

```http
GET /api/v1/top10/leaderboards
```

**响应示例**：
```json
{
  "success": true,
  "data": {
    "all": [...],
    "new": [...],
    "upper": [...],
    "social": [...]
  }
}
```

#### 2. 获取指定赛道的团队 ID

```http
GET /api/v1/teams/track/<track_name>
```

**参数**：
- `track_name`: 赛道名称（新生赛道/进阶赛道/社会赛道）

**响应示例**：
```json
{
  "success": true,
  "data": [1, 2, 3, 4, 5]
}
```

### 数据缓存

- **缓存时间**：60秒
- **缓存策略**：基于参数的 memoization
- **性能优化**：减少数据库查询次数

### 排名规则

1. **主要排序**：总分从高到低
2. **次要排序**：分数相同时，最后解题时间从早到晚
3. **实时计算**：每次请求时动态计算排名

## 🎨 界面设计

### 榜单切换按钮

```
┌─────────────────────────────────────────────────────┐
│  [🏆 总榜]  [🎓 新生榜]  [🚀 进阶榜]  [👥 社会榜]   │
└─────────────────────────────────────────────────────┘
```

### 响应式设计

- **桌面端**：完整显示所有列
- **平板端**：隐藏部分列
- **手机端**：按钮纵向排列，表格横向滚动

## 📖 使用指南

### 访问排行榜

安装后访问以下地址：

```
http://your-ctfd-url/scoreboard/custom
```

### 操作步骤

#### 1. 查看总榜

1. 访问排行榜页面
2. 默认显示总榜
3. 查看所有团队排名

#### 2. 切换赛道榜单

1. 点击顶部按钮（新生榜/进阶榜/社会榜）
2. 自动筛选对应赛道的团队
3. 重新计算排名

#### 3. 按学校筛选

1. 点击"筛选器"展开筛选面板
2. 在"学校"下拉框选择目标学校
3. 自动过滤显示结果

## 🐛 故障排除

### 问题 1：页面无法访问（404 错误）

**症状**：访问 `/scoreboard/custom` 显示 404

**可能原因**：
- 插件未正确加载
- 路由未注册

**解决方法**：

1. 检查插件加载状态：
   ```bash
   docker compose logs ctfd | grep "ctfd-paihangb"
   ```
   
   应该看到：
   ```
   [ctfd-paihangb] 插件加载成功
   [ctfd-paihangb] 路由注册成功
   [ctfd-paihangb] 页面地址: /scoreboard/custom
   ```

2. 重启 CTFd：
   ```bash
   cd /opt/CTFd
   docker compose restart ctfd
   ```

### 问题 2：排行榜显示为空

**症状**：页面加载完成，但没有显示任何队伍

**可能原因**：
- ctfd-tuandui 插件未安装
- 团队没有填写"参与赛道"字段

**解决方法**：

1. 确认前置插件已安装
2. 检查团队赛道数据
3. 查看插件加载状态

### 问题 3：样式显示异常

**症状**：页面布局混乱，样式不正确

**解决方法**：

1. 检查 CSS 文件加载：
   - 打开开发者工具 → Network 标签
   - 查找 `scoreboard.css` 是否成功加载

2. 清除浏览器缓存并强制刷新（Ctrl + Shift + R）

### 问题 4：学校下拉框为空

**症状**：筛选器中的学校下拉框没有选项

**可能原因**：
- 团队没有填写"学校名称"字段
- ctfd-tuandui 插件未正确配置

**解决方法**：

1. 确保团队已填写"学校名称"字段
2. 检查数据库中的字段数据：
   ```sql
   SELECT t.name, fe.value 
   FROM teams t
   JOIN field_entries fe ON t.id = fe.team_id
   JOIN fields f ON fe.field_id = f.id
   WHERE f.name = '学校名称';
   ```

## 🔗 依赖关系

### 插件依赖链

```
ctfd-paihangb (本插件)
    ↓ 依赖
ctfd-tuandui (团队插件)
    ↓ 依赖
ctfd-user (用户插件)
```

### 安装顺序

**必须按照以下顺序安装**：

1. **第一步**：安装 ctfd-user
2. **第二步**：安装 ctfd-tuandui
3. **第三步**：安装 ctfd-paihangb
4. **第四步**：重启 CTFd

## 📚 相关文档

- [ctfd-user 插件](https://github.com/fpclose/ctfd_3.8.1_user)
- [ctfd-tuandui 插件](https://github.com/fpclose/ctfd_3.8.1_tuandui)
- [CTFd 官方文档](https://docs.ctfd.io/)

## 🔄 更新日志

### v1.0.1 (2025-11-18)

- 🐛 **修复页面路由缺失**：添加 `/scoreboard/custom` 页面路由
- ✨ **添加 Blueprint 注册**：支持模板和静态文件
- 🎨 **修复 Bootstrap 5 兼容性**：更新模板语法
- 📊 **添加学校列表获取**：自动获取并传递学校列表到模板
- 📝 **完善文档**：更新安装指南和故障排除

### v1.0.0 (2025-11-16)

- ✨ 初始版本发布
- ✅ 支持四大榜单切换
- ✅ 支持学校筛选
- ✅ 支持实时搜索

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目基于 MIT 许可证开源。

## 📮 联系方式

- GitHub Issues: https://github.com/fpclose/ctfd_3.8.1_paihangbang/issues
- 维护者: fpclose

---

**版本**: 1.0.1  
**兼容**: CTFd 3.8.1  
**依赖**: ctfd-user, ctfd-tuandui  
**最后更新**: 2025-11-18
