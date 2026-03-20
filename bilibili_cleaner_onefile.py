# -*- coding: utf-8 -*-
"""
B站账号清理工具 - 单文件版本
一键清理B站账号的工具
"""
import asyncio
import sys
import argparse
import requests
from pathlib import Path
from urllib.parse import urlencode


# ==================== BVID转AV号工具 ====================
def bvid_to_aid(bvid: str) -> int:
    """将BVID转换为AV号 - 使用bilibili_api库的转换"""
    try:
        sys.path.insert(0, 'venv/Lib/site-packages')
        from bilibili_api.utils.aid_bvid_transformer import bvid2aid
        return bvid2aid(bvid)
    except Exception as e:
        # 如果bilibili_api不可用，返回-1表示失败
        print(f"  BVID转换失败，将使用API获取AV号: {e}")
        return -1


# ==================== 配置加载 ====================
def load_config(config_path: str = "config/config.yaml"):
    """加载配置文件"""
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            sessdata = config.get('bilibili', {}).get('sessdata', '')
            bili_jct = config.get('bilibili', {}).get('bili_jct', '')
            uid = config.get('bilibili', {}).get('uid', 0)
            skip_verify = config.get('settings', {}).get('skip_verify', False)
            return sessdata, bili_jct, uid, skip_verify
    except Exception as e:
        print(f'加载配置失败: {e}')
        return None, None, None, False


# ==================== API请求工具 ====================
def api_request(method: str, url: str, sessdata: str, bili_jct: str, params: dict = None, data: dict = None, retry_count: int = 3) -> dict:
    """发送API请求（带重试）"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
        "Referer": "https://www.bilibili.com"
    }

    for attempt in range(retry_count):
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            else:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                post_data = urlencode(data, doseq=True)
                response = requests.post(url, headers=headers, data=post_data, timeout=30)

            try:
                return response.json()
            except:
                return {}

        except requests.exceptions.ConnectionError:
            if attempt < retry_count - 1:
                print(f"  连接失败，重试中... ({attempt + 1}/{retry_count})")
                asyncio.sleep(2)
            else:
                print(f"  连接失败，已重试{retry_count}次")
                return {}
        except requests.exceptions.Timeout:
            if attempt < retry_count - 1:
                print(f"  请求超时，重试中... ({attempt + 1}/{retry_count})")
                asyncio.sleep(2)
            else:
                print(f"  请求超时，已重试{retry_count}次")
                return {}
        except Exception as e:
            print(f"  请求异常: {e}")
            return {}

    return {}


# ==================== 关注管理 ====================
async def get_followings(sessdata: str, bili_jct: str, uid: int) -> list:
    """获取所有关注"""
    all_followings = []
    page = 1
    page_size = 50

    while True:
        url = "https://api.bilibili.com/x/relation/followings"
        params = {"vmid": uid, "pn": page, "ps": page_size}
        result = api_request("GET", url, sessdata, bili_jct, params=params)

        if result.get("code") == 0:
            data = result.get("data", {})
            list_data = data.get("list", [])
            all_followings.extend(list_data)
            if len(list_data) < page_size:
                break
        else:
            print(f"获取关注列表失败: {result.get('message', '未知错误')}")
            break

        page += 1
        await asyncio.sleep(0.3)

    return all_followings


async def unfollow_user(sessdata: str, bili_jct: str, target_mid: int) -> bool:
    """取消关注某个用户"""
    try:
        url = "https://api.bilibili.com/x/relation/modify"
        data = {
            "fid": str(target_mid),
            "act": "2",
            "csrf": bili_jct
        }
        result = api_request("POST", url, sessdata, bili_jct, data=data)
        return result.get("code", -1) == 0
    except Exception as e:
        print(f"  取消关注异常: {e}")
        return False


async def unfollow_all(sessdata: str, bili_jct: str, uid: int) -> dict:
    """取消所有关注"""
    followings = await get_followings(sessdata, bili_jct, uid)
    total = len(followings)

    if total == 0:
        print("没有关注的用户")
        return {"success": 0, "failed": 0}

    print(f"\n找到 {total} 个关注的用户，开始取消关注...")

    success_count = 0
    failed_count = 0

    for idx, user_info in enumerate(followings, 1):
        target_mid = user_info.get("mid", 0)
        name = user_info.get("uname", "未知用户")

        success = await unfollow_user(sessdata, bili_jct, target_mid)
        if success:
            success_count += 1
            print(f"[{idx}/{total}] [OK] 已取关: {name}")
        else:
            failed_count += 1
            print(f"[{idx}/{total}] [FAIL] 取关失败: {name}")

        await asyncio.sleep(0.5)

    return {"success": success_count, "failed": failed_count}


# ==================== 点赞管理 ====================
async def get_liked_videos(sessdata: str, bili_jct: str, uid: int) -> list:
    """获取所有点赞的视频"""
    all_liked = []
    page = 1
    page_size = 30

    while True:
        url = "https://api.bilibili.com/x/space/like/video"
        params = {"vmid": uid, "pn": page, "ps": page_size}
        result = api_request("GET", url, sessdata, bili_jct, params=params)

        if result.get("code") == 0:
            data = result.get("data", {})
            vlist = data if isinstance(data, list) else []
            if isinstance(data, dict):
                vlist = data.get("list", data.get("vlist", []))
            all_liked.extend(vlist)
            if len(vlist) < page_size:
                break
        else:
            print(f"获取点赞列表失败: {result.get('message', '未知错误')}")
            break

        page += 1
        await asyncio.sleep(0.5)

    return all_liked


async def unlike_video(sessdata: str, bili_jct: str, bvid: str, vid_info: dict = None) -> bool:
    """取消点赞某个视频"""
    try:
        # 直接从API返回的数据中获取aid
        aid = vid_info.get("aid") if vid_info else bvid_to_aid(bvid)
        url = "https://api.bilibili.com/x/web-interface/archive/like"
        # 添加csrf和csrf_token两个参数
        data = {
            "aid": aid,
            "like": 2,
            "csrf": bili_jct,
            "csrf_token": bili_jct
        }
        result = api_request("POST", url, sessdata, bili_jct, data=data)

        if result.get("code") == 0:
            title = vid_info.get("title", "未知") if vid_info else "未知"
            print(f"  [OK] 已取消点赞: {title}")
            return True
        else:
            title = vid_info.get("title", "未知") if vid_info else "未知"
            print(f"  [FAIL] 取消点赞失败: {result.get('message', '未知错误')} - {title}")
            return False
    except Exception as e:
        title = vid_info.get("title", "未知") if vid_info else "未知"
        print(f"  [FAIL] 取消点赞异常 {title}: {e}")
        return False


async def unlike_all(sessdata: str, bili_jct: str, uid: int) -> dict:
    """取消所有点赞"""
    videos = await get_liked_videos(sessdata, bili_jct, uid)
    total = len(videos)

    if total == 0:
        print("没有点赞的视频")
        return {"success": 0, "failed": 0}

    print(f"\n找到 {total} 个点赞的视频，开始取消点赞...")

    success_count = 0
    failed_count = 0

    for idx, vid_info in enumerate(videos, 1):
        bvid = vid_info.get("bvid", "")
        success = await unlike_video(sessdata, bili_jct, bvid, vid_info)
        if success:
            success_count += 1
        else:
            failed_count += 1
        print(f"[{idx}/{total}] 成功: {success_count}, 失败: {failed_count}")
        await asyncio.sleep(0.8)

    return {"success": success_count, "failed": failed_count}


# ==================== 收藏管理 ====================
async def get_favorites(sessdata: str, bili_jct: str, uid: int) -> list:
    """获取所有收藏夹"""
    url = "https://api.bilibili.com/x/v3/fav/folder/created/list-all"
    result = api_request("GET", url, sessdata, bili_jct, params={"up_mid": uid})
    if result.get("code") == 0:
        return result.get("data", {}).get("list", [])
    return []


async def get_fav_content(sessdata: str, bili_jct: str, media_id: int) -> list:
    """获取收藏夹所有内容"""
    all_content = []
    page = 1
    page_size = 20

    while True:
        url = "https://api.bilibili.com/x/v3/fav/resource/list"
        result = api_request("GET", url, sessdata, bili_jct, params={
            "media_id": media_id, "pn": page, "ps": page_size, "keyword": ""
        })

        if result.get("code") == 0:
            data = result.get("data", {})
            # 数据在 data.medias 字段中（info 字段包含的是文件夹元数据）
            content = data.get("medias", [])

            if content is None:
                content = []

            if not isinstance(content, list):
                print(f"  警告：内容格式异常，类型={type(content)}")
                content = []
            else:
                all_content.extend(content)
            if len(content) < page_size:
                break
        else:
            print(f"获取收藏夹内容失败: {result.get('message', '未知错误')}")
            break

        page += 1
        await asyncio.sleep(0.5)

    return all_content


async def delete_fav_item(sessdata: str, bili_jct: str, media_id: int, bvid: str, fav_info: dict = None) -> bool:
    """删除收藏项"""
    try:
        # 从API返回的数据中获取id (这个id实际上就是视频的aid)
        # 在收藏夹API返回中，id字段等于视频的aid
        aid = fav_info.get("id") if fav_info else bvid_to_aid(bvid)

        # 使用正确的API端点和参数格式
        # resources格式: "aid:2" 其中2表示视频类型
        url = "https://api.bilibili.com/x/v3/fav/resource/batch-del"
        data = {
            "media_id": str(media_id),     # 收藏夹ID
            "resources": f"{aid}:2",       # 资源格式: aid:type (2=视频)
            "csrf": bili_jct
        }
        result = api_request("POST", url, sessdata, bili_jct, data=data)

        if result.get("code") == 0:
            title = fav_info.get("title", "未知") if fav_info else "未知"
            print(f"  [OK] 已删除收藏: {title}")
            return True
        else:
            title = fav_info.get("title", "未知") if fav_info else "未知"
            print(f"  [FAIL] 删除收藏失败: {result.get('message', '未知错误')} - {title}")
            return False
    except Exception as e:
        title = fav_info.get("title", "未知") if fav_info else "未知"
        print(f"  [FAIL] 删除收藏异常 {title}: {e}")
        return False


async def clean_all_favorites(sessdata: str, bili_jct: str, uid: int) -> dict:
    """清空所有收藏夹"""
    try:
        favorites = await get_favorites(sessdata, bili_jct, uid)
    except Exception as e:
        print(f"[FAIL] 获取收藏夹失败: {e}")
        return {"success": 0, "failed": 0}

    if not favorites:
        print("没有收藏夹")
        return {"success": 0, "failed": 0}

    print(f"\n找到 {len(favorites)} 个收藏夹")

    total_success = 0
    total_failed = 0

    for fav in favorites:
        media_id = fav.get("id")
        title = fav.get("title", "未命名收藏夹")

        print(f"\n处理收藏夹: {title}")

        try:
            content = await get_fav_content(sessdata, bili_jct, media_id)
        except Exception as e:
            print(f"[FAIL] 获取收藏夹内容失败 ({title}): {e}")
            total_failed += 1
            continue

        total = len(content)

        if total == 0:
            print("  收藏夹为空")
            continue

        for idx, item in enumerate(content, 1):
            bvid = item.get("bvid")
            video_title = item.get("title", "未知标题")

            try:
                success = await delete_fav_item(sessdata, bili_jct, media_id, bvid, item)
                if success:
                    total_success += 1
                    print(f"  [{idx}/{total}] [OK] 已删除收藏: {video_title}")
                else:
                    total_failed += 1
                    print(f"  [{idx}/{total}] [FAIL] 删除收藏失败: {video_title}")
            except Exception as e:
                print(f"[FAIL] 删除收藏项异常 ({video_title}): {e}")
                total_failed += 1

            await asyncio.sleep(0.8)

    print(f"\n结果: {total_success} 成功, {total_failed} 失败")
    return {"success": total_success, "failed": total_failed}


# ==================== 粉丝管理 ====================
async def get_followers(sessdata: str, bili_jct: str, uid: int) -> list:
    """获取所有粉丝"""
    all_followers = []
    page = 1
    page_size = 50

    while True:
        url = "https://api.bilibili.com/x/relation/followers"
        result = api_request("GET", url, sessdata, bili_jct, params={
            "vmid": uid, "pn": page, "ps": page_size
        })

        if result.get("code") == 0:
            followers = result.get("data", {}).get("list", [])
            all_followers.extend(followers)
            if len(followers) < page_size:
                break
        else:
            print(f"获取粉丝失败: {result.get('message', '未知错误')}")
            break

        page += 1
        await asyncio.sleep(0.3)

    return all_followers


async def remove_follower(sessdata: str, bili_jct: str, follower_uid: int) -> bool:
    """移除某个粉丝"""
    url = "https://api.bilibili.com/x/relation/modify"
    data = {"fid": str(follower_uid), "act": "6", "csrf": bili_jct}
    result = api_request("POST", url, sessdata, bili_jct, data=data)
    return result.get("code", -1) == 0


async def remove_all_followers(sessdata: str, bili_jct: str, uid: int, add_to_blacklist: bool = False) -> dict:
    """移除所有粉丝"""
    followers = await get_followers(sessdata, bili_jct, uid)
    total = len(followers)

    if total == 0:
        print("没有粉丝")
        return {"success": 0, "failed": 0, "blocked": 0}

    print(f"\n找到 {total} 个粉丝，开始移除...")
    if add_to_blacklist:
        print("注意: 拉黑功能暂未实现")

    success_count = 0
    failed_count = 0

    for idx, follower in enumerate(followers, 1):
        follower_uid = follower.get('mid', 0)
        name = follower.get('name', '未知用户')

        success = await remove_follower(sessdata, bili_jct, follower_uid)
        if success:
            success_count += 1
            print(f"[{idx}/{total}] [OK] 已移除: {name}")
        else:
            failed_count += 1
            print(f"[{idx}/{total}] [FAIL] 移除失败: {name}")

        await asyncio.sleep(0.8)

    return {"success": success_count, "failed": failed_count, "blocked": 0}


# ==================== 统计信息 ====================
async def get_stats(sessdata: str, bili_jct: str, uid: int):
    """获取账号统计信息"""
    # 获取关注数
    url = "https://api.bilibili.com/x/relation/stat"
    result = api_request("GET", url, sessdata, bili_jct, params={"vmid": uid})
    if result.get("code") == 0:
        data = result.get("data", {})
        following = data.get('following', 0)
        follower = data.get('follower', 0)
        print(f"关注数: {following}")
        print(f"粉丝数: {follower}")
    else:
        print("获取统计信息失败")

    # 获取点赞数
    liked = await get_liked_videos(sessdata, bili_jct, uid)
    print(f"点赞数: {len(liked)}")


# ==================== 一键清理 ====================
async def clean_all_ordered(sessdata: str, bili_jct: str, uid: int):
    """一键清理全部（按顺序执行）"""
    print("\n" + "="*50)
    print("  一键清理全部（按顺序执行）")
    print("="*50)

    total_success = 0
    total_failed = 0

    # 1. 取消关注
    print("\n[步骤 1/3] 取消所有关注")
    result = await unfollow_all(sessdata, bili_jct, uid)
    total_success += result.get("success", 0)
    total_failed += result.get("failed", 0)
    print(f"  结果: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")

    # 2. 取消点赞
    print("\n[步骤 2/3] 取消所有点赞")
    result = await unlike_all(sessdata, bili_jct, uid)
    total_success += result.get("success", 0)
    total_failed += result.get("failed", 0)
    print(f"  结果: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")

    # 3. 清空收藏夹
    print("\n[步骤 3/3] 清空所有收藏夹")
    result = await clean_all_favorites(sessdata, bili_jct, uid)
    total_success += result.get("success", 0)
    total_failed += result.get("failed", 0)
    print(f"  结果: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")

    # 显示总结果
    print("\n" + "="*50)
    print("  清理完成")
    print("="*50)
    print(f"取消关注: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")
    print(f"取消点赞: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")
    print(f"清空收藏夹: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")
    print(f"总计: {total_success} 成功, {total_failed} 失败")


# ==================== 交互式菜单 ====================
async def show_menu(sessdata: str, bili_jct: str, uid: int):
    """显示交互式菜单"""
    while True:
        print("\n" + "="*50)
        print("  B站账号清理工具")
        print("="*50)
        print("\n请选择操作:")
        print("  1. 取消所有关注")
        print("  2. 取消所有点赞")
        print("  3. 清空所有收藏夹")
        print("  4. 移除所有粉丝")
        print("  5. 一键清理全部（按顺序）")
        print("  0. 退出")
        print("\n请输入选项编号 (1-5, 0): ", end="")

        try:
            choice = input()
        except (KeyboardInterrupt, EOFError):
            print("\n\n程序已退出")
            return

        if choice == "0":
            print("\n感谢使用，再见！")
            break
        elif choice == "1":
            print("\n开始取消所有关注...")
            result = await unfollow_all(sessdata, bili_jct, uid)
            print(f"\n结果: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")
        elif choice == "2":
            print("\n开始取消所有点赞...")
            result = await unlike_all(sessdata, bili_jct, uid)
            print(f"\n结果: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")
        elif choice == "3":
            print("\n开始清空所有收藏夹...")
            result = await clean_all_favorites(sessdata, bili_jct, uid)
            print(f"\n结果: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")
        elif choice == "4":
            print("\n开始移除所有粉丝...")
            result = await remove_all_followers(sessdata, bili_jct, uid)
            print(f"\n结果: {result.get('success', 0)} 成功, {result.get('failed', 0)} 失败")
        elif choice == "5":
            print("\n开始一键清理全部...")
            await clean_all_ordered(sessdata, bili_jct, uid)
        else:
            print("\n无效选项，请重新选择")


# ==================== 主程序 ====================
async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="B站账号清理工具 - 单文件版本")
    parser.add_argument("--sessdata", help="SESSDATA (不指定则从配置文件读取)")
    parser.add_argument("--bili-jct", help="bili_jct (不指定则从配置文件读取)")
    parser.add_argument("--auto", action="store_true", help="自动模式：直接执行一键清理全部")
    parser.add_argument("--config", help="配置文件路径 (默认: config/config.yaml)")
    args = parser.parse_args()

    # 加载配置
    config_path = args.config if args.config else "config/config.yaml"
    sessdata, bili_jct, uid, skip_verify = load_config(config_path)

    # 命令行参数覆盖
    if args.sessdata:
        sessdata = args.sessdata
    if args.bili_jct:
        bili_jct = args.bili_jct

    if not sessdata:
        print("错误: 必须指定SESSDATA或在配置文件中配置")
        return

    # 显示统计信息
    print("\n当前账号状态:")
    await get_stats(sessdata, bili_jct, uid)

    # 根据参数决定执行模式
    if args.auto:
        print("\n自动模式：执行一键清理全部...")
        await clean_all_ordered(sessdata, bili_jct, uid)
    else:
        await show_menu(sessdata, bili_jct, uid)


if __name__ == "__main__":
    asyncio.run(main())
