#!/usr/bin/env python

"""
通过命令行参数执行 Cool-Tools 的 Loop Calling (dot-calling) 分析。

该脚本加载一个 .cool 文件和一个 'expected' 数据文件，
使用 Hiccups 论文中描述的标准 kernels 来识别染色质环，
并将结果保存到指定的输出文件中。

示例用法:
python run_loop_calling.py my_data.1kb.cool my_expected.1kb.tsv my_loops.tsv --max-loci-separation 3000000 -n 16
"""

import pandas as pd
import cooler
import cooltools
import cooltools.lib.numutils
import argparse # 导入 argparse 库
import sys # 用于在出错时退出

# 打印正在使用的 cooltools 版本以供参考
print(f"Using cooltools version: {cooltools.__version__}")

def main():
    """主执行函数"""
    # ======================================================
    # 1. 设置命令行参数解析
    # ======================================================
    parser = argparse.ArgumentParser(
        description="使用 cooltools.api.dotfinder.dots 进行 Loop Calling。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助文本格式
    )
    
    # --- 位置参数 (必需) ---
    parser.add_argument(
        "cool_path",
        type=str,
        help="输入的 .cool 文件路径。"
    )
    parser.add_argument(
        "expected_path",
        type=str,
        help="输入的 'expected' 数据文件路径 (TSV 格式)。"
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="用于保存 loop calling 结果的输出文件路径 (TSV 格式)。"
    )

    # --- 可选参数 ---
    parser.add_argument(
        "--max-loci-separation",
        type=int,
        default=2000000,
        help="考虑的位点间最大基因组分离距离（单位：bp）。\n默认值: 2,000,000"
    )
    parser.add_argument(
        "-n", "--nproc",
        type=int,
        default=8,
        help="用于并行计算的进程数。\n注意：请根据你的机器核心数设置一个合理的值。\n默认值: 8"
    )
    
    # 解析传入的参数
    args = parser.parse_args()

    ## ======================================================
    ## 2. 准备 Kernels 和参数
    ## ======================================================
    print("\n--- 配置参数 ---")
    print(f"Cooler file: {args.cool_path}")
    print(f"Expected file: {args.expected_path}")
    print(f"Output file: {args.output_path}")
    print(f"Max loci separation: {args.max_loci_separation:,} bp")
    print(f"Number of processes: {args.nproc}")
    print("---------------------\n")
    
    # 使用标准的 hiccups kernels 配置
    KERNELS = {
        "donut": cooltools.lib.numutils.get_kernel(w=7, p=2, ktype="donut"),
        "vertical": cooltools.lib.numutils.get_kernel(w=7, p=1, ktype="vertical"),
        "horizontal": cooltools.lib.numutils.get_kernel(w=7, p=1, ktype="horizontal"),
        "lowleft": cooltools.lib.numutils.get_kernel(w=7, p=1, ktype="lowleft"),
    }

    ## ======================================================
    ## 3. 执行 Loop Calling
    ## ======================================================
    
    # 加载 cooler 文件
    try:
        clr = cooler.Cooler(args.cool_path)
    except Exception as e:
        print(f"错误: 无法加载 .cool 文件 '{args.cool_path}'.")
        print(f"详细信息: {e}")
        sys.exit(1)

    # 加载 expected 文件
    try:
        expected_df = pd.read_csv(args.expected_path, sep="\t")
    except FileNotFoundError:
        print(f"错误: 'expected' 文件未找到 '{args.expected_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取 'expected' 文件时出错: {e}")
        print("请确保你的 'expected' 文件是一个正确的制表符分隔 (TSV) 文件。")
        sys.exit(1)

    # 调用 cooltools 的核心 dots 函数
    print("开始 Loop Calling...")
    dot_calls_df = cooltools.api.dotfinder.dots(
        clr,
        expected=expected_df,
        kernels=KERNELS,
        max_loci_separation=args.max_loci_separation,
        nproc=args.nproc,
    )

    # 保存结果
    try:
        dot_calls_df.to_csv(args.output_path, sep="\t", index=False)
    except Exception as e:
        print(f"错误: 保存结果到 '{args.output_path}' 时失败。")
        print(f"详细信息: {e}")
        sys.exit(1)


    print("\n✅ Done!")
    print(f"Loops 结果已成功保存到: {args.output_path}")

# ======================================================
# 脚本执行入口点
# ======================================================
if __name__ == "__main__":
    main()