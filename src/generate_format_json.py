#!/usr/bin/env python3
"""
根据downloaded_resources_info.json生成format_data_info.json
增加clean_path字段，表示清理后的文件路径
如果是目录，则遍历查找有价值的文件（PDF、JSON、CSV、MD等），并将每个文件生成独立的条目
"""

import os
import json
import glob
import argparse
import shutil
from pathlib import Path
from collections import defaultdict

# 基础配置
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_INPUT_FILE = os.path.join(ROOT_DIR, "data/downloaded_resources_info.json")
DEFAULT_OUTPUT_FILE = os.path.join(ROOT_DIR, "data/format_data_info.json")
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "data/downloads")
CLEANED_DIR = os.path.join(ROOT_DIR, "data/cleaned_data")

# 支持的文件类型
SUPPORTED_EXTENSIONS = [
    '.pdf',   # PDF文档
    '.json',  # JSON文件
    '.csv',   # CSV文件
    '.md',    # Markdown文件
    '.txt',   # 文本文件
    '.rst',   # ReStructuredText文件
    '.yaml', '.yml',  # YAML文件
    '.xml',   # XML文件
    '.html', '.htm',  # HTML文件
    '.doc', '.docx',  # Word文档
    '.xls', '.xlsx',  # Excel文件
    '.ppt', '.pptx',  # PowerPoint文件
]

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='生成带有清理路径的资源JSON信息文件')
    parser.add_argument('--input', '-i', help='输入JSON文件路径', default=DEFAULT_INPUT_FILE)
    parser.add_argument('--output', '-o', help='输出JSON文件路径', default=DEFAULT_OUTPUT_FILE)
    parser.add_argument('--verbose', '-v', help='显示详细输出', action='store_true')
    parser.add_argument('--extensions', '-e', help='指定要包含的文件扩展名，用逗号分隔，例如：pdf,json,md', default=None)
    args = parser.parse_args()
    return args

def ensure_dir(directory):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)

def get_supported_extensions(custom_extensions=None):
    """获取支持的文件扩展名列表"""
    if custom_extensions:
        # 处理用户指定的扩展名
        exts = [ext.strip().lower() for ext in custom_extensions.split(',')]
        # 确保所有扩展名都以.开头
        exts = ['.' + ext if not ext.startswith('.') else ext for ext in exts]
        return exts
    return SUPPORTED_EXTENSIONS

def find_valuable_files(directory, extensions=None):
    """在目录中查找指定类型的文件"""
    extensions = extensions or SUPPORTED_EXTENSIONS
    valuable_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in extensions:
                valuable_files.append(os.path.join(root, file))
    
    return valuable_files

def get_file_type(filename):
    """获取文件类型"""
    file_ext = os.path.splitext(filename)[1].lower()
    
    # 映射扩展名到更友好的描述
    ext_to_type = {
        '.pdf': 'PDF文档',
        '.json': 'JSON文件',
        '.csv': 'CSV文件',
        '.md': 'Markdown文件',
        '.txt': '文本文件',
        '.rst': 'ReStructuredText文件',
        '.yaml': 'YAML文件', 
        '.yml': 'YAML文件',
        '.xml': 'XML文件',
        '.html': 'HTML文件', 
        '.htm': 'HTML文件',
        '.doc': 'Word文档', 
        '.docx': 'Word文档',
        '.xls': 'Excel文件', 
        '.xlsx': 'Excel文件',
        '.ppt': 'PowerPoint文件', 
        '.pptx': 'PowerPoint文件',
    }
    
    return ext_to_type.get(file_ext, '未知文件类型')

def process_resources(input_file, verbose=False, custom_extensions=None):
    """处理资源信息，生成带有clean_path的新资源列表"""
    try:
        # 读取输入JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            resources = json.load(f)
        
        if verbose:
            print(f"已读取 {len(resources)} 个资源")
        
        # 确保清理数据目录存在
        ensure_dir(CLEANED_DIR)
        
        # 获取支持的文件扩展名
        supported_extensions = get_supported_extensions(custom_extensions)
        if verbose:
            print(f"支持的文件类型: {', '.join(supported_extensions)}")
        
        # 处理后的资源列表
        processed_resources = []
        
        # 统计信息
        stats = {
            "total": len(resources),
            "dirs": 0,
            "files": 0,
            "by_type": defaultdict(int),
            "other": 0
        }
        
        # 处理每个资源
        for resource in resources:
            # 获取原始路径
            path = resource.get("path", "")
            
            # 跳过没有路径的资源
            if not path:
                if verbose:
                    print(f"跳过无路径资源: {resource.get('filename', '未知')}")
                continue
            
            # 构建完整路径
            full_path = os.path.join(ROOT_DIR, path)
            
            # 检查路径是否是目录
            if os.path.isdir(full_path):
                stats["dirs"] += 1
                
                # 是目录，查找所有有价值的文件
                if verbose:
                    print(f"处理目录: {path}")
                
                valuable_files = find_valuable_files(full_path, supported_extensions)
                
                if not valuable_files:
                    # 没有找到有价值的文件，创建一个默认条目
                    repo_name = os.path.basename(path)
                    clean_dir = os.path.join(CLEANED_DIR, repo_name)
                    ensure_dir(clean_dir)
                    
                    resource_copy = resource.copy()
                    resource_copy["clean_path"] = os.path.join("data/cleaned_data", repo_name)
                    processed_resources.append(resource_copy)
                    stats["other"] += 1
                    
                    if verbose:
                        print(f"  没有找到有价值的文件，创建了默认条目: {resource_copy['clean_path']}")
                else:
                    # 找到有价值的文件，为每个文件创建一个条目
                    repo_name = os.path.basename(path)
                    clean_dir = os.path.join(CLEANED_DIR, repo_name)
                    ensure_dir(clean_dir)
                    
                    for valuable_file in valuable_files:
                        # 计算相对于仓库根目录的路径
                        rel_path = os.path.relpath(valuable_file, full_path)
                        file_name = os.path.basename(valuable_file)
                        file_ext = os.path.splitext(file_name)[1].lower()
                        
                        # 创建目标路径
                        dest_path = os.path.join(clean_dir, file_name)
                        rel_dest_path = os.path.join("data/cleaned_data", repo_name, file_name)
                        
                        # 复制文件（如果不存在）
                        if not os.path.exists(dest_path):
                            try:
                                shutil.copy2(valuable_file, dest_path)
                                if verbose:
                                    print(f"  复制文件: {valuable_file} -> {dest_path}")
                            except Exception as e:
                                print(f"  复制文件失败: {valuable_file} -> {dest_path}: {str(e)}")
                                continue
                        
                        # 创建新的资源条目
                        resource_copy = resource.copy()
                        resource_copy["filename"] = f"{resource['filename']} - {file_name}"
                        resource_copy["clean_path"] = rel_dest_path
                        resource_copy["file_type"] = get_file_type(file_name)
                        processed_resources.append(resource_copy)
                        stats["by_type"][file_ext] = stats["by_type"].get(file_ext, 0) + 1
                        
                        if verbose:
                            print(f"  创建文件条目: {resource_copy['clean_path']} ({file_ext})")
            else:
                stats["files"] += 1
                
                # 是文件，创建对应的clean_path
                if verbose:
                    print(f"处理文件: {path}")
                
                # 获取文件名和扩展名
                filename = os.path.basename(path)
                file_dir = os.path.dirname(path)
                file_ext = os.path.splitext(filename)[1].lower()
                
                # 构建清理后的路径
                clean_path = os.path.join("data/cleaned_data", filename)
                
                # 如果是支持的文件类型，复制到clean_data目录
                if file_ext in supported_extensions:
                    dest_path = os.path.join(CLEANED_DIR, filename)
                    if not os.path.exists(dest_path):
                        try:
                            shutil.copy2(full_path, dest_path)
                            if verbose:
                                print(f"  复制文件: {full_path} -> {dest_path}")
                        except Exception as e:
                            print(f"  复制文件失败: {full_path} -> {dest_path}: {str(e)}")
                    
                    stats["by_type"][file_ext] = stats["by_type"].get(file_ext, 0) + 1
                
                # 创建新的资源条目
                resource_copy = resource.copy()
                resource_copy["clean_path"] = clean_path
                resource_copy["file_type"] = get_file_type(filename)
                processed_resources.append(resource_copy)
                
                if verbose:
                    print(f"  创建条目: {resource_copy['clean_path']}")
        
        return processed_resources, stats
    
    except Exception as e:
        print(f"处理资源时出错: {e}")
        import traceback
        traceback.print_exc()
        return [], {"total": 0, "dirs": 0, "files": 0, "by_type": {}, "other": 0}

def save_to_json(resources, output_file):
    """将资源信息保存为JSON文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resources, f, ensure_ascii=False, indent=2)
        print(f"成功! 已将 {len(resources)} 个资源信息写入: {output_file}")
        return True
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始生成带有清理路径的资源JSON信息文件...")
    
    # 解析命令行参数
    args = parse_args()
    input_file = args.input
    output_file = args.output
    verbose = args.verbose
    custom_extensions = args.extensions
    
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    
    # 处理资源
    resources, stats = process_resources(input_file, verbose, custom_extensions)
    
    # 打印统计信息
    print(f"\n处理统计:")
    print(f"总共处理: {stats['total']} 个资源")
    print(f"目录数量: {stats['dirs']} 个")
    print(f"文件数量: {stats['files']} 个")
    
    print(f"按文件类型统计:")
    for ext, count in stats["by_type"].items():
        print(f"  {ext}: {count} 个文件")
    
    print(f"其他条目: {stats['other']} 个")
    print(f"生成条目总数: {len(resources)} 个")
    
    # 保存JSON文件
    if resources:
        save_to_json(resources, output_file)
    else:
        print("没有找到有效的资源，未生成输出文件")

if __name__ == "__main__":
    main() 