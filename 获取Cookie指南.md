# 获取B站SESSDATA详细指南

## 方法1：Chrome/Edge 浏览器（最常用）

### 步骤：

1. **打开B站并登录**
   - 访问 https://www.bilibili.com/
   - 点击右上角登录

2. **打开开发者工具**
   - 按键盘 `F12`
   - 或者：右键点击页面 → 选择「检查」

3. **切换到 Application 标签**
   - 点击顶部的 `Application` 标签
   - 或者 `应用程序` 标签

4. **找到 Cookies**
   - 左侧菜单展开 `Storage`（存储）
   - 点击 `Cookies` → 点击 `https://www.bilibili.com`

5. **复制 SESSDATA**
   - 在右侧列表中找到 `SESSDATA`
   - 双击 `Value` 列的值
   - 或者选中后按 Ctrl+C 复制

```
┌────────────────────────────────────────────┐
│ Cookies │ https://www.bilibili.com      │
├────────────────────────────────────────────┤
│ Name     │ Value                        │
├────────────────────────────────────────────┤
│ SESSDATA │ a1b2c3d4e5f6g7h8i9... ← 复制这个值
│ bili_jct │ abc123def456               │
│ DedeUserID │ 123456789               │
└────────────────────────────────────────────┘
```

---

## 方法2：Chrome/Edge - 快捷方式

1. 访问 https://www.bilibili.com/ 并登录
2. 按 `F12` 打开开发者工具
3. 按以下快捷键：
   - Windows: `Ctrl + Shift + P`
   - Mac: `Cmd + Shift + P`
4. 输入 `cookie` 选择「Show Cookies」
5. 找到 SESSDATA 复制

---

## 方法3：FireFox 浏览器

1. **打开B站并登录**
   - 访问 https://www.bilibili.com/

2. **打开开发者工具**
   - 按 `F12`

3. **切换到 Storage 标签**
   - 如果没有 Storage 标签：
     - 点击右上角 `...` 按钮
     - 选择 `获取更多工具` → `Web 开发者工具`
     - 切换到 `存储` 标签

4. **找到 Cookies**
   - 左侧 `Cookies` → `https://www.bilibili.com`
   - 找到 `SESSDATA` 复制

---

## 方法4：最简单 - 使用浏览器插件

安装「EditThisCookie」或「Cookie-Editor」插件：

1. 打开 https://www.bilibili.com/ 并登录
2. 点击浏览器工具栏的插件图标
3. 找到 `SESSDATA` 复制其值

---

## 验证是否正确

SESSDATA 通常是这样的格式：
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0...
```

长度在 100-200 字符之间。

---

## 如果找不到怎么办？

### 检查以下几点：

1. **确保已登录B站**
   - 检查右上角是否显示你的头像

2. **刷新页面**
   - 按 `F5` 刷新后再查看

3. **检查域名**
   - 确保是 `https://www.bilibili.com` 不是其他域名

4. **清空Cookie后重新登录**
   - 打开开发者工具 → Application → Cookies
   - 右键 → Clear
   - 重新登录B站

---

## 获取后如何使用？

复制 SESSDATA 后，运行：

```bash
python src/bilibili_cleaner/main.py --sessdata "这里粘贴你的SESSDATA"
```

或者双击 `run.bat`，粘贴即可。
