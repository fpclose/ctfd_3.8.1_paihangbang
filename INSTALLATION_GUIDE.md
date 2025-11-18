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
├── __init__.py                          # 插件入口
├── config.json                          # 插件配置
├── routes.py                            # 路由和 API 端点
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

### 3. 自动功能

#### 自动刷新
- 每30秒自动请求最新数据
- 无需手动刷新页面
- 确保数据实时性

#### 自动排名
- 按总分从高到低排序
- 分数相同时按最后解题时间排序
- 动态计算，实时更新

## 🔧 技术实现

### API 接口

插件提供以下 API 端点：

#### 获取排行榜数据

```http
GET /api/scoreboard/data
```

**查询参数**：
- `track` (可选): 赛道筛选，可选值：`新生赛道`、`进阶赛道`、`社会赛道`
- `school` (可选): 学校筛选，填写学校名称

**响应示例**：
```json
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "team_id": 1,
      "team_name": "Team Alpha",
      "school": "北京大学",
      "track": "新生赛道",
      "score": 1000,
      "solve_count": 10,
      "last_solve": "2025-11-18T12:00:00"
    }
  ]
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

- **总榜**：蓝色主题
- **新生榜**：绿色主题
- **进阶榜**：青色主题
- **社会榜**：灰色主题

### 筛选器面板

```
┌──────────────────────────────────────────┐
│  🔍 筛选器                               │
│                                          │
│  学校：[下拉选择所有学校]                 │
│  搜索：[输入队伍名称]                     │
│  [重置筛选]                              │
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

### 排名徽章

- **第1名**：🥇 金色渐变
- **第2名**：🥈 银色渐变
- **第3名**：🥉 铜色渐变
- **其他**：灰色背景

### 赛道徽章

- **新生赛道**：绿色徽章 `badge-success`
- **进阶赛道**：青色徽章 `badge-info`
- **社会赛道**：灰色徽章 `badge-secondary`

## 📖 使用指南

### 访问排行榜

安装后访问以下地址：

```
http://your-ctfd-url/scoreboard/custom
```

或在 CTFd 导航栏添加链接（需要管理员配置）。

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

#### 4. 搜索队伍

1. 在搜索框输入队伍名称（支持模糊匹配）
2. 实时过滤显示结果
3. 保持当前的赛道和学校筛选

#### 5. 重置筛选

1. 点击"重置"按钮
2. 清除所有筛选条件
3. 返回当前榜单的完整列表

## 🔄 数据流程

```
用户访问页面
    ↓
加载初始数据（总榜）
    ↓
用户切换榜单/筛选
    ↓
AJAX 请求 API
    ↓
后端查询数据（带缓存）
    ↓
计算排名
    ↓
返回 JSON 数据
    ↓
前端渲染更新
    ↓
30秒后自动刷新
```

## 🐛 故障排除

### 问题 1：排行榜显示为空

**症状**：页面加载完成，但没有显示任何队伍

**可能原因**：
- ctfd-tuandui 插件未安装
- 团队没有填写"参与赛道"字段
- 数据库中没有团队数据

**解决方法**：

1. 确认前置插件已安装：
   ```bash
   ls -la /opt/CTFd/CTFd/plugins/ | grep -E "ctfd-user|ctfd-tuandui"
   ```

2. 检查团队赛道数据：
   ```sql
   SELECT t.id, t.name, tfe.value as track
   FROM teams t
   LEFT JOIN field_entries tfe ON t.id = tfe.team_id
   LEFT JOIN fields f ON tfe.field_id = f.id
   WHERE f.name = '参与赛道';
   ```

3. 查看插件加载状态：
   ```bash
   docker compose logs ctfd | grep "ctfd-paihangb"
   ```

### 问题 2：数据不刷新

**症状**：排行榜数据长时间不更新

**解决方法**：

1. 清除浏览器缓存：按 `Ctrl + Shift + R` 强制刷新

2. 清除服务器缓存：
   ```python
   # 在 CTFd Python 环境中执行
   from CTFd.cache import cache
   cache.clear()
   ```

3. 检查自动刷新功能：
   - 打开浏览器开发者工具（F12）
   - 查看 Console 标签是否有错误
   - 查看 Network 标签确认 API 请求

### 问题 3：样式显示异常

**症状**：页面布局混乱，样式不正确

**解决方法**：

1. 检查 CSS 文件加载：
   - 打开开发者工具 → Network 标签
   - 刷新页面
   - 查找 `scoreboard.css` 是否成功加载（状态码 200）

2. 清除浏览器缓存并强制刷新

3. 检查文件权限：
   ```bash
   ls -la /opt/CTFd/CTFd/plugins/ctfd-paihangb/assets/
   ```

### 问题 4：API 请求失败

**症状**：浏览器控制台显示 404 或 500 错误

**解决方法**：

1. 检查路由注册：
   ```bash
   docker compose logs ctfd | grep "route"
   ```

2. 验证 API 端点：
   ```bash
   curl http://localhost:8000/api/scoreboard/data
   ```

3. 查看详细错误日志：
   ```bash
   docker compose logs ctfd -f
   ```

### 问题 5：筛选功能不工作

**症状**：选择学校或赛道后没有反应

**解决方法**：

1. 检查 JavaScript 错误：
   - F12 → Console 标签
   - 查看是否有错误信息

2. 验证数据格式：
   - 确保团队的"学校名称"和"参与赛道"字段格式正确
   - 字段值应与预期完全匹配

3. 检查 JS 文件加载：
   ```bash
   ls -la /opt/CTFd/CTFd/plugins/ctfd-paihangb/assets/js/
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
   ```bash
   cd /opt/CTFd/CTFd/plugins
   git clone https://github.com/fpclose/ctfd_3.8.1_user.git ctfd-user
   cd ctfd-user && sudo ./install.sh
   ```

2. **第二步**：安装 ctfd-tuandui
   ```bash
   cd /opt/CTFd/CTFd/plugins
   git clone https://github.com/fpclose/ctfd_3.8.1_tuandui.git ctfd-tuandui
   cd ctfd-tuandui && sudo ./install.sh
   ```

3. **第三步**：安装 ctfd-paihangb
   ```bash
   cd /opt/CTFd/CTFd/plugins
   git clone https://github.com/fpclose/ctfd_3.8.1_paihangbang.git ctfd-paihangb
   cd ctfd-paihangb && sudo ./install.sh
   ```

4. **第四步**：重启 CTFd
   ```bash
   cd /opt/CTFd
   docker compose restart ctfd
   ```

## 🎨 自定义配置

### 修改刷新间隔

编辑 `assets/js/scoreboard.js`：

```javascript
// 默认 30 秒
const REFRESH_INTERVAL = 30000;

// 修改为 60 秒
const REFRESH_INTERVAL = 60000;
```

### 修改缓存时间

编辑 `routes.py`：

```python
# 默认 60 秒
@cache.memoize(timeout=60)

# 修改为 120 秒
@cache.memoize(timeout=120)
```

### 自定义颜色方案

编辑 `assets/css/scoreboard.css`，修改对应的颜色值。

### 添加自定义赛道

如果需要支持新的赛道类型：

1. 在 ctfd-tuandui 插件中添加赛道选项
2. 在本插件的前端代码中添加对应按钮
3. 重启 CTFd

## 📊 使用场景

### 场景 1：查看新生榜

```
目的：查看新生组的排名情况
操作：点击"新生榜"按钮
结果：只显示新生赛道的团队，按分数排名
```

### 场景 2：查看某学校在进阶榜的排名

```
操作步骤：
  1. 点击"进阶榜"按钮
  2. 展开筛选器
  3. 选择目标学校
  
结果：显示该学校在进阶赛道的所有队伍及排名
```

### 场景 3：搜索特定队伍

```
操作：在搜索框输入队伍名称关键词
结果：实时过滤显示匹配的队伍
```

## 📚 相关文档

- [ctfd-user 插件](https://github.com/fpclose/ctfd_3.8.1_user)
- [ctfd-tuandui 插件](https://github.com/fpclose/ctfd_3.8.1_tuandui)
- [CTFd 官方文档](https://docs.ctfd.io/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目基于 MIT 许可证开源。

## 📮 联系方式

- GitHub Issues: https://github.com/fpclose/ctfd_3.8.1_paihangbang/issues
- 维护者: fpclose

---

**版本**: 1.0.0  
**兼容**: CTFd 3.8.1  
**依赖**: ctfd-user, ctfd-tuandui  
**最后更新**: 2025-11-18
