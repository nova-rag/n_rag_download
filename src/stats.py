#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime

# 配置
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(ROOT_DIR, "data/resources.csv")
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "data/downloads")
LOG_FILE = os.path.join(ROOT_DIR, "data/download_log.json")

def human_readable_size(size_bytes):
    """将字节数转换为人类可读的格式"""
    if size_bytes == 0:
        return "0 B"
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def print_divider(char='-', length=80):
    """打印分隔线"""
    print(char * length)

def main():
    # 检查日志文件是否存在
    if not os.path.exists(LOG_FILE):
        print("错误: 下载日志文件不存在，请先运行下载程序")
        return
    
    # 加载日志
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
    except Exception as e:
        print(f"无法读取日志文件: {e}")
        return
    
    downloaded_files = log_data.get("downloaded_files", [])
    errors = log_data.get("errors", {})
    last_updated = log_data.get("last_updated", 0)
    
    # 统计信息
    total_files = len(downloaded_files)
    error_count = len(errors)
    
    # 计算下载文件的总大小
    total_size = 0
    file_types = {}
    for filename in downloaded_files:
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            total_size += file_size
            
            # 统计文件类型
            ext = os.path.splitext(filename)[1].lower()
            if not ext:
                ext = "无扩展名"
            if ext in file_types:
                file_types[ext]["count"] += 1
                file_types[ext]["size"] += file_size
            else:
                file_types[ext] = {"count": 1, "size": file_size}
    
    # 打印统计信息
    print_divider("=")
    print(f"资源下载统计")
    print_divider("=")
    print(f"总资源数: {total_files + error_count}")
    print(f"已下载: {total_files}")
    print(f"下载失败: {error_count}")
    print(f"下载完成率: {total_files / (total_files + error_count) * 100:.2f}%")
    print(f"总大小: {human_readable_size(total_size)}")
    
    if last_updated > 0:
        last_updated_time = datetime.fromtimestamp(last_updated).strftime("%Y-%m-%d %H:%M:%S")
        print(f"最后更新时间: {last_updated_time}")
    
    # 打印文件类型统计
    print_divider()
    print("文件类型统计:")
    print("类型\t\t数量\t大小")
    for ext, data in sorted(file_types.items(), key=lambda x: x[1]["size"], reverse=True):
        ext_padded = ext + "\t" if len(ext) < 8 else ext
        print(f"{ext_padded}\t{data['count']}\t{human_readable_size(data['size'])}")
    
    # 打印错误信息
    if errors:
        print_divider()
        print(f"下载失败的资源 ({error_count}):")
        for index, error_info in errors.items():
            print(f"[{index}] {error_info['resource']}")
            print(f"  错误: {error_info['error']}")
    
    print_divider("=")

if __name__ == "__main__":
    main() 