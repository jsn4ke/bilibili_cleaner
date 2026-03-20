# 快速使用指南

## 一键启动（推荐方式）

1. 激活虚拟环境（首次使用需要）：
```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

2. 获取Cookie（SESSDATA 和 bili_jct）：
   - 打开浏览器，登录B站
   - 按F12打开开发者工具
   - 切换到 Application 标签
   - 刷新页面，点击任意请求
   - 在 Cookies 中找到 SESSDATA 和 bili_jct
   - 将Cookie填入 config/config.yaml 文件

详细教程请查看 `获取Cookie指南.md`

3. 运行工具：

```bash
# 方式1：双击运行（推荐）
run.bat

# 方式2：交互式菜单（可选择单个功能）
venv\Scripts\python.exe bilibili_cleaner_onefile.py --config config/config.yaml

# 方式3：自动模式（直接执行一键清理全部）
venv\Scripts\python.exe bilibili_cleaner_onefile.py --auto --config config/config.yaml
```

## 功能说明

运行后会显示交互式菜单：

**菜单选项：**
1. 取消所有关注
2. 取消所有点赞
3. 清空所有收藏夹
4. 移除所有粉丝（可选）
5. 一键清理全部（按顺序）
0. 退出

**功能说明：**
- **取消关注：** 显示用户名并取消关注
- **取消点赞：** 显示视频标题并取消点赞
- **清空收藏夹：** 删除收藏夹中的所有内容
- **移除粉丝：** 移除粉丝（保留作为可选功能）

## 执行顺序

程序按固定顺序执行，确保：
- 先取消点赞
- 再清空收藏
- 最后移除粉丝

## 重要提示

⚠️ **所有删除操作不可恢复！**

建议：
- 先检查 config/config.yaml 中的 Cookie 是否正确
- 确认无误后再运行
- 如遇失败可重新运行继续清理
- 程序会自动重试失败的请求

## 常见问题

**Q: 提示登录验证失败？**
A: 检查SESSDATA是否正确，Cookie可能已过期，需要重新获取。

**Q: 部分操作失败？**
A: B站可能有频率限制，稍后重试即可。

**Q: 如何查看当前状态？**
A: 程序运行前会显示当前关注数、点赞数、粉丝数。

**Q: 收藏夹为空？**
A: 正常现象，表示收藏夹已经被清空。

**Q: 没有粉丝？**
A: 正常现象，表示账号没有粉丝需要移除。
