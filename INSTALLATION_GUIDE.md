# CTFd-Paihangb 插件安装指南

## 📋 概述

CTFd-Paihangb（排行榜）插件为 CTFd 3.8.1 提供了分赛道排行榜功能，并自动在默认排行榜中添加学校信息显示。

### 主要特性

- ✅ **默认排行榜增强**：自动在 `/scoreboard` 中显示学校信息
- ✅ **四大榜单**：总榜、新生榜、进阶榜、社会榜
- ✅ **学校信息显示**：排行榜中显示每个队伍的学校
- ✅ **赛道信息显示**：排行榜中显示每个队伍的参与赛道
- ✅ **一键切换**：快速切换不同赛道榜单
- ✅ **学校筛选**：按学校名称筛选团队
- ✅ **实时搜索**：支持队伍名称和学校名称搜索
- ✅ **美观界面**：排名徽章（🥇🥈🥉）、赛道彩色徽章
- ✅ **自动刷新**：每30秒自动更新数据
- ✅ **API 扩展**：自动为 scoreboard API 添加学校和赛道字段

## 🚀 快速开始

### 前置要求

⚠️ **重要**：本插件依赖以下插件，请按顺序安装：

1. **ctfd-user** - 提供用户自定义字段
   - 仓库：https://github.com/fpclose/ctfd_3.8.1_user
   
2. **ctfd-tuandui** - 提供团队赛道信息
   - 仓库：https://github.com/fpclose/ctfd_3.8.1_tuandui

### 安装步骤

```bash
# 1. 下载插件
cd /opt/CTFd/CTFd/plugins
git clone https://github.com/fpclose/ctfd_3.8.1_paihangbang.git ctfd-paihangb

# 2. 复制模板文件（可选，如果要修改默认排行榜样式）
cp ctfd-paihangb/scoreboard.html.example /opt/CTFd/CTFd/themes/core/templates/scoreboard.html

# 3. 重启 CTFd
cd /opt/CTFd
docker compose restart ctfd
```

## 🎯 功能说明

### 1. 默认排行榜增强

安装插件后，访问 `/scoreboard` 会自动显示学校信息：

| 排名 | 队伍名称 | **学校** | 得分 |
|------|---------|---------|------|
| 1 | Team A | 北京大学 | 1000 |
| 2 | Team B | 清华大学 | 900 |
| 3 | Team C | 复旦大学 | 800 |

**工作原理**：
- 插件使用 `after_request` 钩子
- 自动拦截 `/api/v1/scoreboard` API 请求
- 在响应中添加 `school` 和 `track` 字段
- 前端模板自动显示这些信息

### 2. 自定义排行榜页面

访问 `/scoreboard/custom` 查看完整功能的排行榜：

- **四大榜单切换**
- **学校筛选下拉框**
- **队伍/学校名称搜索**
- **赛道徽章显示**
- **排名徽章（🥇🥈🥉）**

### 3. API 扩展

插件自动扩展以下 API：

#### 原生 Scoreboard API（扩展）

```http
GET /api/v1/scoreboard
```

**扩展字段**：
```json
{
  "success": true,
  "data": [
    {
      "pos": 1,
      "account_id": 5,
      "name": "Team A",
      "score": 962,
      "school": "北京大学",        // 新增
      "track": "新生赛道"           // 新增
    }
  ]
}
```

#### 自定义 Scoreboard API

```http
GET /api/v1/scoreboard/data?track=新生赛道&school=北京大学
```

## 📖 使用指南

### 查看默认排行榜

1. 访问 `http://your-ctfd-url/scoreboard`
2. 查看所有队伍及其学校信息
3. 使用赛道切换按钮过滤队伍

### 查看自定义排行榜

1. 访问 `http://your-ctfd-url/scoreboard/custom`
2. 使用筛选器按学校过滤
3. 使用搜索框搜索队伍或学校
4. 点击重置按钮清除筛选

### 搜索功能

**支持搜索**：
- 队伍名称
- 学校名称

**示例**：
- 搜索"北京"：显示所有北京的学校
- 搜索"Team"：显示所有包含 Team 的队伍

## 🐛 故障排除

### 问题 1：默认排行榜不显示学校信息

**症状**：`/scoreboard` 页面不显示学校列

**解决方法**：

1. 确认插件已加载：
   ```bash
   docker compose logs ctfd | grep "ctfd-paihangb"
   ```
   
   应该看到：
   ```
   [ctfd-paihangb] 插件加载成功
   [ctfd-paihangb] Scoreboard API 扩展已启用
   ```

2. 测试 API：
   ```bash
   curl http://localhost:8000/api/v1/scoreboard | jq '.data[0]'
   ```
   
   应该包含 `school` 和 `track` 字段

3. 清除浏览器缓存：按 `Ctrl + Shift + R`

### 问题 2：学校信息显示"未填写"

**原因**：团队没有填写"学校名称"字段

**解决方法**：
1. 在 Admin → Teams → [队伍] → Fields 中填写
2. 确保字段名称为"学校名称"

### 问题 3：筛选功能不工作

**解决方法**：
1. 清除浏览器缓存
2. 检查浏览器控制台错误（F12）
3. 确认插件所有文件已正确安装

## 🔧 高级配置

### 修改默认排行榜模板

如果需要自定义默认排行榜样式：

```bash
# 1. 复制示例模板
cp /opt/CTFd/CTFd/plugins/ctfd-paihangb/scoreboard.html.example \
   /opt/CTFd/CTFd/themes/core/templates/scoreboard.html

# 2. 编辑模板
vim /opt/CTFd/CTFd/themes/core/templates/scoreboard.html

# 3. 重启 CTFd
docker compose restart ctfd
```

### 禁用 API 扩展

如果只想使用自定义排行榜而不修改默认排行榜：

编辑 `__init__.py`，注释掉 `@app.after_request` 装饰器部分。

## 🔄 更新日志

### v1.0.3 (2025-11-18)

- ✨ **添加 API 扩展**：自动为 `/api/v1/scoreboard` 添加学校和赛道字段
- 🎨 **修改默认排行榜模板**：在 `/scoreboard` 中显示学校信息
- 🔍 **增强搜索功能**：支持同时搜索队伍名称和学校名称
- 📝 **更新文档**：添加 API 扩展和默认排行榜说明
- 🐛 **修复筛选问题**：优化筛选逻辑

### v1.0.2 (2025-11-18)

- ✨ 添加学校和赛道信息显示
- 🎨 添加排名徽章和赛道徽章

### v1.0.1 (2025-11-18)

- 🐛 修复页面路由缺失

### v1.0.0 (2025-11-16)

- ✨ 初始版本发布

## 📚 API 参考

### 扩展的 Scoreboard API

```javascript
// GET /api/v1/scoreboard
{
  "success": true,
  "data": [
    {
      "pos": 1,
      "account_id": 5,
      "account_url": "/teams/5",
      "account_type": "team",
      "name": "Team A",
      "score": 962,
      "bracket_id": null,
      "bracket_name": null,
      "school": "北京大学",     // 插件添加
      "track": "新生赛道",       // 插件添加
      "members": [...]
    }
  ]
}
```

### 自定义 Scoreboard Data API

```javascript
// GET /api/v1/scoreboard/data?track=新生赛道&school=北京大学
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "team_id": 5,
      "team_name": "Team A",
      "school": "北京大学",
      "track": "新生赛道",
      "score": 962.0
    }
  ]
}
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目基于 MIT 许可证开源。

## 📮 联系方式

- GitHub Issues: https://github.com/fpclose/ctfd_3.8.1_paihangbang/issues
- 维护者: fpclose

---

**版本**: 1.0.3  
**兼容**: CTFd 3.8.1  
**依赖**: ctfd-user, ctfd-tuandui  
**最后更新**: 2025-11-18
