#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import time
import json
import requests
import argparse
import re
import subprocess
from urllib.parse import urlparse, unquote
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import random
import shutil
import sys

# 解析命令行参数
parser = argparse.ArgumentParser(description='下载资源文件')
parser.add_argument('--dry-run', action='store_true', help='测试模式，不实际保存文件')
parser.add_argument('--max-workers', type=int, default=5, help='并发下载的工作线程数量')
parser.add_argument('--clean-errors', action='store_true', help='清除之前记录的错误，重新尝试下载失败的资源')
parser.add_argument('--retry-all', action='store_true', help='重新下载所有资源，包括已下载的')
parser.add_argument('--verbose', action='store_true', help='显示详细输出')
parser.add_argument('--timeout', type=int, default=30, help='下载超时时间(秒)')
parser.add_argument('--skip-cert-verify', action='store_true', help='跳过SSL证书验证')
parser.add_argument('--no-git-clone', action='store_true', help='不使用git clone下载GitHub仓库')
parser.add_argument('--url-file', default='resource_list.txt', help='包含URL的文件 (txt或csv格式)')
parser.add_argument('--output-dir', default='downloads', help='下载文件的输出目录')
parser.add_argument('--delay', type=float, default=1, help='下载之间的延迟（秒）')
parser.add_argument('--random-delay', action='store_true', help='使用随机延迟(1-5秒)')
parser.add_argument('--retry', type=int, default=3, help='下载失败时的重试次数')
parser.add_argument('--skip-existing', action='store_true', help='跳过已经存在的文件')
parser.add_argument('--use-csv', action='store_true', help='强制使用CSV格式解析资源文件')
parser.add_argument('--category', type=str, help='只下载指定分类的资源')
args = parser.parse_args()

# 配置
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(ROOT_DIR, "data/resources.csv")
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "data/downloads")
LOG_FILE = os.path.join(ROOT_DIR, "data/download_log.json")
RESOURCE_FILE = os.path.join(ROOT_DIR, "data", args.url_file)
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", args.output_dir)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}
MAX_WORKERS = args.max_workers  # 并发下载数量

# GitHub仓库正则表达式
GITHUB_REPO_PATTERN = re.compile(r'https?://github\.com/([^/]+)/([^/]+)/?(\?.+)?$')
GITHUB_REPO_PAGE_PATTERN = re.compile(r'https?://github\.com/([^/]+)/([^/]+)/(tree|blob)/[^/]+/.*')
GITHUB_PAGE_PATTERN = re.compile(r'https?://(www\.)?github\.com/[^/]+/[^/]+')

# Git仓库标记
GIT_REPO_SUFFIX = "_git"

# 资源分类颜色 (用于终端彩色输出)
CATEGORY_COLORS = {
    "公开芯片SDK": "\033[1;32m",         # 绿色
    "FreeRTOS文档": "\033[1;34m",        # 蓝色
    "RISC-V框架相关文档": "\033[1;35m",  # 紫色
    "UWB的Rifa标准文档": "\033[1;33m",   # 黄色
    "其他行业相关文档": "\033[1;36m",    # 青色
    "一些领域相关paper": "\033[1;91m",   # 亮红色
    "default": "\033[0m"                # 默认
}

# 确保下载目录存在
if not args.dry_run:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_filename(resource_name, index):
    """生成文件名，替换空格为下划线"""
    # 移除引号
    name = resource_name.strip('"')
    # 替换空格为下划线，移除不合法的文件名字符
    safe_name = "".join([c if c.isalnum() or c in [' ', '.', '_', '-'] else '_' for c in name])
    safe_name = safe_name.replace(' ', '_')
    
    # 添加索引
    return f"{index}_{safe_name}"


def get_extension(url, resource_type):
    """根据URL和资源类型确定文件扩展名"""
    if resource_type.lower() == "pdf":
        return ".pdf"
    
    # 尝试从URL中提取扩展名
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    
    if ext:
        return ext
    
    # 默认扩展名
    if "html" in resource_type.lower():
        return ".html"
    else:
        return ".txt"


def is_github_repo(url):
    """判断URL是否是GitHub仓库"""
    if args.no_git_clone:
        return False
    
    # 检查是否是GitHub仓库主页
    repo_match = GITHUB_REPO_PATTERN.match(url)
    if repo_match:
        return True
    
    # 检查是否是GitHub仓库子页面
    repo_page_match = GITHUB_REPO_PAGE_PATTERN.match(url)
    if repo_page_match:
        # 构造仓库主页URL
        username = repo_page_match.group(1)
        repo_name = repo_page_match.group(2)
        return f"https://github.com/{username}/{repo_name}"
    
    # 特殊处理 README.md at branch - owner/repo 格式
    readme_match = re.match(r'https?://github\.com/([^/]+)/([^/]+)/blob/[^/]+/README\.md.*', url)
    if readme_match:
        username = readme_match.group(1)
        repo_name = readme_match.group(2)
        return f"https://github.com/{username}/{repo_name}"
    
    return False


def git_clone_repo(url, filepath):
    """使用git clone下载GitHub仓库"""
    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 构造git clone命令
        cmd = ["git", "clone", "--depth=1", url, filepath]
        
        # 执行git clone
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 检查结果
        if result.returncode != 0:
            raise Exception(f"Git clone失败: {result.stderr}")
        
        return True, None
    except Exception as e:
        return False, str(e)


def download_resource(index, resource_data, downloaded_files, errors):
    """下载单个资源"""
    # 判断资源数据格式
    if isinstance(resource_data, tuple) or isinstance(resource_data, list):
        # CSV格式：[URL, 文件名, 资源类型, 来源, 分类]
        if len(resource_data) >= 5:
            url, custom_filename, resource_type = resource_data[0], resource_data[1], resource_data[2]
            source = resource_data[3] if len(resource_data) > 3 else ""
            category = resource_data[4] if len(resource_data) > 4 else ""
            resource_name = custom_filename
        elif len(resource_data) >= 3:
            url, custom_filename, resource_type = resource_data[0], resource_data[1], resource_data[2]
            source = resource_data[3] if len(resource_data) > 3 else ""
            category = ""
            resource_name = custom_filename
        elif len(resource_data) == 2:
            url, custom_filename = resource_data
            resource_type = ""
            source = ""
            category = ""
            resource_name = custom_filename
        else:
            url = resource_data[0]
            custom_filename = ""
            resource_type = ""
            source = ""
            category = ""
            resource_name = url
    else:
        # 纯文本格式：URL
        url = resource_data
        custom_filename = ""
        resource_type = ""
        source = ""
        category = ""
        resource_name = url
    
    # 如果指定了分类过滤且当前资源不属于该分类，则跳过
    if args.category and category and args.category.lower() != category.lower():
        if args.verbose:
            print(f"跳过 [{index}] {resource_name} - 不属于分类 '{args.category}'")
        return False, None, "已跳过"
    
    # 生成文件名
    if custom_filename:
        # 使用自定义文件名
        safe_name = "".join([c if c.isalnum() or c in [' ', '.', '_', '-'] else '_' for c in custom_filename])
        safe_name = safe_name.replace(' ', '_')
        base_filename = f"{index}_{safe_name}"
    else:
        base_filename = get_filename(resource_name, index)
    
    # 确定扩展名
    if resource_type:
        ext = get_extension(url, resource_type)
    else:
        # 尝试从URL中提取扩展名
        path = urlparse(url).path
        ext = os.path.splitext(path)[1]
        if not ext:
            ext = ".html"  # 默认为HTML
    
    filename = f"{base_filename}{ext}"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 检查是否已下载且不是重试模式
    if filename in downloaded_files and not args.retry_all:
        if args.verbose:
            print(f"已跳过 [{index}] {resource_name} - 文件已存在")
        return False, None, "已跳过"
    
    # 获取分类的彩色标记
    color_start = CATEGORY_COLORS.get(category, CATEGORY_COLORS["default"])
    color_end = "\033[0m"  # 重置颜色
    
    # 显示下载信息，带有分类标记
    category_display = f" [{color_start}{category}{color_end}]" if category else ""
    
    # 检查是否是GitHub仓库
    github_repo_url = is_github_repo(url)
    if github_repo_url:
        if github_repo_url is True:
            github_repo_url = url
        
        print(f"检测到GitHub仓库 [{index}]{category_display} {resource_name}...")
        
        # 目录名使用仓库名或自定义文件名
        if custom_filename:
            repo_name = safe_name
        else:
            repo_name = os.path.basename(urlparse(github_repo_url).path)
            if not repo_name:
                repo_name = resource_name.replace(' ', '_')
        
        # 设置git仓库路径
        git_repo_path = os.path.join(OUTPUT_DIR, f"{index}_{repo_name}{GIT_REPO_SUFFIX}")
        
        # 在非测试模式下下载
        if not args.dry_run:
            success, error = git_clone_repo(github_repo_url, git_repo_path)
            if success:
                print(f"  成功克隆仓库: {github_repo_url} 到 {git_repo_path}")
                return True, None, "成功"
            else:
                errors[str(index)] = {
                    "resource": resource_name,
                    "url": url,
                    "error": f"Git clone失败: {error}"
                }
                print(f"  失败: Git clone失败: {error}")
                
                # 尝试普通下载
                print(f"  尝试普通下载...")
        else:
            print(f"  测试模式: 仓库将克隆到 {git_repo_path}")
            return True, None, "成功"
    
    # 普通下载
    try:
        if not github_repo_url:
            print(f"下载中 [{index}] {resource_name}...")
        
        # 根据不同类型处理不同的下载方式
        if args.skip_cert_verify:
            response = requests.get(url, headers=HEADERS, timeout=args.timeout, verify=False)
        else:
            response = requests.get(url, headers=HEADERS, timeout=args.timeout)
        
        # 检查响应状态
        if response.status_code != 200:
            error_msg = f"HTTP错误: {response.status_code}"
            errors[str(index)] = {
                "resource": resource_name,
                "url": url,
                "error": error_msg
            }
            print(f"  失败: {error_msg}")
            return False, error_msg, "失败"
        
        # 在非测试模式下保存内容
        if not args.dry_run:
            with open(filepath, 'wb') as f:
                f.write(response.content)
        
        print(f"  成功: {filename}")
        return True, None, "成功"
        
    except Exception as e:
        error_msg = str(e)
        errors[str(index)] = {
            "resource": resource_name,
            "url": url,
            "error": error_msg
        }
        print(f"  失败: {error_msg}")
        return False, error_msg, "失败"


def load_log():
    """加载下载日志"""
    if args.dry_run or not os.path.exists(LOG_FILE):
        return {"downloaded_files": [], "errors": {}}
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
            
            # 如果是清理错误模式，清空错误记录
            if args.clean_errors:
                log_data["errors"] = {}
                
            # 如果是重试所有，清空下载记录
            if args.retry_all:
                log_data["downloaded_files"] = []
                
            return log_data
    except:
        return {"downloaded_files": [], "errors": {}}


def save_log(downloaded_files, errors):
    """保存下载日志"""
    if args.dry_run:
        return
        
    log_data = {
        "downloaded_files": downloaded_files,
        "errors": errors,
        "last_updated": time.time()
    }
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def check_git_installed():
    """检查是否安装了git"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def is_git_installed():
    """检查Git是否已安装"""
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False


def is_github_page(url):
    """检查URL是否是GitHub页面"""
    return GITHUB_PAGE_PATTERN.match(url) is not None


def get_filename_from_url(url, content_disposition=None):
    """从URL或Content-Disposition中提取文件名"""
    filename = None
    
    # 尝试从Content-Disposition中提取
    if content_disposition:
        matches = re.findall(r'filename=(?:\"?)([^;\"]*)(?:\"?)', content_disposition)
        if matches:
            filename = matches[0].strip()
    
    # 如果没有找到，从URL中提取
    if not filename:
        path = urlparse(url).path
        filename = unquote(os.path.basename(path))
    
    # 如果文件名为空，使用URL的哈希值
    if not filename or filename == '':
        filename = f"resource_{hash(url) % 10000}.html"
    
    # 如果是GitHub仓库，添加后缀标识
    if is_github_repo(url) and not args.no_git_clone:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 2:
            repo_owner = path_parts[0]
            repo_name = path_parts[1]
            filename = f"{repo_owner}_{repo_name}{GIT_REPO_SUFFIX}"
    
    return filename


def sanitize_filename(filename):
    """清理文件名，移除非法字符"""
    # 替换Windows/Unix系统中的非法字符
    illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'
    sanitized = re.sub(illegal_chars, '_', filename)
    
    # 限制文件名长度
    if len(sanitized) > 200:
        base, ext = os.path.splitext(sanitized)
        sanitized = base[:195] + ext
    
    return sanitized


def is_csv_file(file_path):
    """判断文件是否为CSV格式"""
    if args.use_csv:
        return True
    
    # 根据文件扩展名判断
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.csv':
        return True
    
    # 尝试读取文件内容判断
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            # 如果第一行包含逗号且不以#开头，可能是CSV
            if ',' in first_line and not first_line.startswith('#'):
                # 检查逗号数量，通常CSV至少有一个逗号
                return first_line.count(',') >= 1
    except:
        pass
    
    return False


def load_resources():
    """加载资源列表"""
    if not os.path.exists(RESOURCE_FILE):
        print(f"错误: 资源文件 {RESOURCE_FILE} 不存在")
        sys.exit(1)
    
    try:
        # 判断文件格式
        if is_csv_file(RESOURCE_FILE):
            print(f"以CSV格式读取文件: {RESOURCE_FILE}")
            return load_csv_resources(RESOURCE_FILE)
        else:
            print(f"以纯文本格式读取文件: {RESOURCE_FILE}")
            return load_text_resources(RESOURCE_FILE)
    except Exception as e:
        print(f"读取资源文件时出错: {e}")
        sys.exit(1)


def load_text_resources(file_path):
    """从文本文件中读取资源URL列表"""
    with open(file_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    return urls


def load_csv_resources(file_path):
    """从CSV文件中读取资源列表"""
    resources = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        # 尝试自动检测分隔符
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        
        # 如果第一行是标题行，跳过
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        
        reader = csv.reader(csvfile, dialect)
        
        # 如果有标题行，跳过
        if has_header:
            next(reader)
        
        for row in reader:
            # 跳过空行和注释行
            if not row or (row[0].startswith('#')):
                continue
            
            # 确保至少有URL
            if len(row) >= 1:
                resources.append(row)
    
    return resources


def download_resource_from_url(url, index, total):
    """下载单个资源URL"""
    # 创建session以维持连接
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # 获取文件名
    try:
        head_response = session.head(url, timeout=args.timeout)
        content_disposition = head_response.headers.get('Content-Disposition')
    except:
        content_disposition = None
    
    filename = get_filename_from_url(url, content_disposition)
    filename = sanitize_filename(filename)
    
    # 输出路径
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    # 如果是GitHub仓库且启用了git clone功能
    if is_github_repo(url) and not args.no_git_clone:
        if os.path.exists(output_path) and args.skip_existing:
            if args.verbose:
                print(f"[{index}/{total}] 跳过已存在的仓库: {filename}")
            return True, filename, "已跳过"
        
        if args.verbose:
            print(f"[{index}/{total}] 克隆仓库: {url} -> {filename}")
        
        # 如果目录已存在，先删除
        if os.path.exists(output_path):
            if os.path.isdir(output_path):
                shutil.rmtree(output_path)
            else:
                os.remove(output_path)
        
        success, message = git_clone_repo(url, output_path)
        return success, filename, message
    
    # 标准下载流程
    if os.path.exists(output_path) and args.skip_existing:
        if args.verbose:
            print(f"[{index}/{total}] 跳过已存在的文件: {filename}")
        return True, filename, "已跳过"
    
    if args.verbose:
        print(f"[{index}/{total}] 下载: {url} -> {filename}")
    
    # 重试机制
    for attempt in range(args.retry + 1):
        try:
            response = session.get(url, stream=True, timeout=args.timeout)
            response.raise_for_status()
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            
            # 使用tqdm显示进度条
            with open(output_path, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                disable=not args.verbose
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
            
            return True, filename, "已下载"
        
        except requests.HTTPError as e:
            error_message = f"HTTP错误: {e.response.status_code}"
        except requests.ConnectionError:
            error_message = "连接错误"
        except requests.Timeout:
            error_message = "请求超时"
        except Exception as e:
            error_message = f"下载错误: {str(e)}"
        
        # 如果不是最后一次尝试，则重试
        if attempt < args.retry:
            wait_time = 2 ** attempt  # 指数退避
            print(f"下载失败，将在 {wait_time} 秒后重试... ({attempt+1}/{args.retry})")
            time.sleep(wait_time)
        else:
            print(f"下载 {url} 失败: {error_message}")
            return False, filename, error_message


def get_category_statistics(resources):
    """获取各个分类的统计信息"""
    categories = {}
    
    for resource in resources:
        if isinstance(resource, (list, tuple)) and len(resource) >= 5:
            category = resource[4]
            if category:
                categories[category] = categories.get(category, 0) + 1
    
    return categories


def main():
    if args.dry_run:
        print("测试模式: 文件不会被实际保存")
    
    if args.skip_cert_verify:
        # 禁用SSL证书验证的警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print("警告: 已禁用SSL证书验证")
    
    # 检查git是否安装
    if not args.no_git_clone and not check_git_installed():
        print("警告: 未检测到git命令，将无法克隆GitHub仓库。只能普通下载GitHub页面。")
        print("如需使用git clone功能，请安装git: https://git-scm.com/downloads")
        print("或者使用 --no-git-clone 参数禁用git clone功能")
        args.no_git_clone = True
    
    # 加载日志
    log_data = load_log()
    downloaded_files = log_data.get("downloaded_files", [])
    errors = log_data.get("errors", {})
    
    # 读取资源列表
    resources = load_resources()
    
    # 如果指定了分类过滤，计算过滤后的资源数量
    filtered_count = len(resources)
    if args.category:
        filtered_count = sum(1 for r in resources 
                           if isinstance(r, (list, tuple)) and 
                           len(r) >= 5 and 
                           r[4].lower() == args.category.lower())
        print(f"找到 {filtered_count} 个属于分类 '{args.category}' 的资源（共 {len(resources)} 个资源）")
    else:
        print(f"找到 {len(resources)} 个资源")
        
        # 显示各分类的统计信息
        categories = get_category_statistics(resources)
        if categories:
            print("资源分类统计:")
            for category, count in categories.items():
                color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["default"])
                print(f"  {color}{category}{CATEGORY_COLORS['default']}: {count} 个")
    
    if args.clean_errors:
        print("已清除错误记录，将重试先前失败的下载")
    
    if args.retry_all:
        print("重新下载所有资源，包括已下载的")
    
    # 统计变量
    success_count = 0
    error_count = 0
    skip_count = 0
    github_count = 0
    category_stats = {}
    
    # 使用线程池进行并发下载
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        
        # 提交下载任务
        for i, resource in enumerate(resources, 1):
            # 下载资源
            future = executor.submit(download_resource, i, resource, downloaded_files, errors)
            futures.append((i, future))
        
        # 处理GitHub仓库计数及分类统计
        for resource in resources:
            # GitHub仓库计数
            url = resource[0] if isinstance(resource, (list, tuple)) else resource
            if is_github_repo(url) and not args.no_git_clone:
                github_count += 1
                
            # 分类统计
            if isinstance(resource, (list, tuple)) and len(resource) >= 5:
                category = resource[4]
                if category:
                    if args.category and category.lower() != args.category.lower():
                        continue
                    category_stats[category] = category_stats.get(category, {"total": 0, "success": 0, "error": 0, "skip": 0})
                    category_stats[category]["total"] += 1
        
        # 收集结果
        for i, future in futures:
            try:
                success, error_msg, status = future.result()
                
                # 更新分类统计
                resource = resources[i-1]  # 索引从1开始，所以这里减1
                category = ""
                if isinstance(resource, (list, tuple)) and len(resource) >= 5:
                    category = resource[4]
                
                if success:
                    if status == "已跳过":
                        skip_count += 1
                        if category:
                            category_stats[category]["skip"] += 1
                    else:
                        success_count += 1
                        if category:
                            category_stats[category]["success"] += 1
                else:
                    error_count += 1
                    if category:
                        category_stats[category]["error"] += 1
                        
            except Exception as e:
                print(f"任务执行异常 [{i}]: {e}")
                error_count += 1
                if args.verbose:
                    import traceback
                    traceback.print_exc()
    
    # 保存日志
    save_log(downloaded_files, errors)
    
    # 输出统计信息
    print("\n下载统计:")
    print(f"成功: {success_count}")
    print(f"失败: {error_count}")
    print(f"跳过: {skip_count}")
    
    if github_count > 0:
        github_mode = "标准下载" if args.no_git_clone else "Git克隆"
        print(f"其中GitHub仓库: {github_count} (处理方式: {github_mode})")
        
    total_count = success_count + error_count + skip_count
    
    # 如果有分类，显示分类统计
    if category_stats:
        print("\n分类下载统计:")
        for category, stats in category_stats.items():
            color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["default"])
            category_display = f"{color}{category}{CATEGORY_COLORS['default']}"
            total = stats["total"]
            success = stats["success"]
            error = stats["error"]
            skip = stats["skip"]
            print(f"  {category_display}: 成功 {success}, 失败 {error}, 跳过 {skip}, 总计 {total}")
    
    if args.category:
        print(f"\n总计: {total_count}/{filtered_count} 个属于分类 '{args.category}' 的资源")
    else:
        print(f"\n总计: {total_count}/{len(resources)} 个资源")
    
    # 输出错误信息
    if errors:
        print("\n错误详情:")
        for index, error_info in errors.items():
            resource_name = error_info.get("resource", "未知资源")
            error = error_info.get("error", "未知错误")
            print(f"[{index}] {resource_name}: {error}")
        
        # 提示用户
        print("\n提示: 使用 --skip-cert-verify 选项可能解决SSL证书问题")
        print("     使用 --clean-errors 选项可以重试失败的下载")
        print("     使用 --retry-all 选项可以重新下载所有资源")


if __name__ == "__main__":
    print("开始下载资源...")
    main()
    print("下载完成!") 