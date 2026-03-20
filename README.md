# Bilibili Account Cleaner

一键清理B站账号的工具 - 帮你快速清空点赞、收藏和粉丝。

## 功能特性

- ✅ 取消所有关注（显示用户名）
- ✅ 取消所有视频点赞（显示视频标题）
- ✅ 清空所有收藏夹
- ✅ 移除所有粉丝（可选功能）
- ✅ 一键清理全部（按顺序执行：关注 → 点赞 → 收藏）
- ✅ 交互式菜单（可单独选择功能）
- ✅ 自动错误处理和重试机制

## 快速开始

### 方式1：直接运行（推荐）

1. 编辑 `config/config.yaml`，填入你的Cookie
2. 双击 `run.bat` 运行

### 方式2：命令行

**Windows:**
```bash
# 交互式菜单（可选择单个功能）
venv\Scripts\python.exe bilibili_cleaner_onefile.py --config config/config.yaml

# 自动模式：直接执行一键清理全部
venv\Scripts\python.exe bilibili_cleaner_onefile.py --auto --config config/config.yaml
```

**Linux/Mac:**
```bash
# 交互式菜单
venv/bin/python bilibili_cleaner_onefile.py --config config/config.yaml

# 自动模式
venv/bin/python bilibili_cleaner_onefile.py --auto --config config/config.yaml
```

## 虚拟环境 (venv) 使用说明

本项目使用 Python 虚拟环境 (`venv`) 来隔离项目依赖，避免与系统 Python 环境冲突。

### 创建虚拟环境

如果 `venv` 目录不存在，请先创建：

**Windows:**
```bash
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

### 安装依赖

创建虚拟环境后，使用 `requirements.txt` 安装项目依赖：

**Windows:**
```bash
venv\Scripts\pip install -r requirements.txt
```

**Linux/Mac:**
```bash
venv/bin/pip install -r requirements.txt
```

### 激活虚拟环境（可选）

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

激活后可以直接使用 `python` 命令，无需指定完整路径：
```bash
python bilibili_cleaner_onefile.py --auto
```

### 退出虚拟环境

```bash
deactivate
```

## 配置Cookie

**快速配置：**

1. 复制 `config/config.yaml.example` 为 `config/config.yaml`
2. 编辑 `config/config.yaml` 文件，填入你的账号信息

```yaml
bilibili:
  # SESSDATA: 必需，用于身份验证的Cookie
  # 获取方式：见下面的详细教程
  sessdata: "your_sessdata_here"

  # bili_jct: 必需，CSRF令牌
  bili_jct: "your_bili_jct_here"

  # uid: 必需，您的B站用户ID
  # 获取方式：访问 https://space.bilibili.com/ 后URL中的数字
  uid: 12345678

settings:
  # 是否跳过确认提示（谨慎使用）
  skip_verify: false
```

### 获取Cookie的方法

1. 打开浏览器，登录 [B站](https://www.bilibili.com/)
2. 按 `F12` 打开开发者工具
3. 点击 `Application` 标签
4. 左侧：Cookies → https://www.bilibili.com
5. 找到 `SESSDATA` 和 `bili_jct`，复制填入配置文件

详细教程请查看 `获取Cookie指南.md`

## 清理结果

工具会按顺序执行以下操作：

1. **步骤 1/3: 取消所有点赞** - 遍历所有点赞的视频并取消点赞
2. **步骤 2/3: 清空所有收藏夹** - 遍历所有收藏夹并删除其中的内容
3. **步骤 3/3: 移除所有粉丝** - 遍历所有粉丝并移除（可选拉黑）

完成后显示汇总结果。

## 注意事项

⚠️ **重要提示：**

1. 所有删除操作**不可恢复**，请谨慎操作
2. 建议先备份数据再进行清理
3. B站可能有频率限制，程序已添加延迟和重试机制
4. 如果遇到失败，可以重新运行继续清理
5. 程序使用API直接操作，确保Cookie正确

## 文件说明

```
talk/
├── venv/                      # Python虚拟环境
├── bilibili_cleaner_onefile.py  # 单文件主程序
├── run.bat                    # Windows快捷启动脚本
├── .gitignore                 # Git忽略文件配置
├── config/
│   ├── config.yaml            # 配置文件（Cookie填在这里，不提交到git）
│   └── config.yaml.example   # 配置文件模板
├── QUICKSTART.md              # 快速使用指南
├── README.md                 # 本说明文档
└── 获取Cookie指南.md         # Cookie获取详细教程
```

## 依赖库

依赖项已定义在 `requirements.txt` 文件中：

- `bilibili-api` - B站API辅助库（BVID/AV号转换）
- `requests` - HTTP请求
- `pyyaml` - 配置文件解析

## 许可证

MIT License

## 免责声明

本工具仅供个人学习和研究使用，使用者需自行承担使用本工具产生的风险和责任。请遵守B站用户协议和服务条款。
