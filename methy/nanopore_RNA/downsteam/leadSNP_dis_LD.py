import pandas as pd
from subprocess import call,run
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
import pickle
import re
import argparse

def load_and_filter_qtl(qtl_file,qtl_type):
    if qtl_type == "stQTL":
        cols_to_read = ["chrom","strand","snp_pos_1base","rsID","pvalue"]
        qtl_data = pd.read_csv(qtl_file, usecols=cols_to_read)
        qtl_filtered = qtl_data[qtl_data['pvalue'] < 0.05]
        qtl_filtered['s'] = qtl_filtered['snp_pos_1base']-1
        qtl_filtered['e'] = qtl_filtered['snp_pos_1base']+1
        return qtl_filtered[['chrom', 's', 'e', 'rsID', 'pvalue', 'strand']]
    else:
        cols_to_read = ["chrom","strand","snp_pos_1base","rsID","BayesFactor"]
        qtl_data = pd.read_csv(qtl_file, usecols=cols_to_read)
        qtl_filtered = qtl_data[qtl_data['BayesFactor'] > 3]
        qtl_filtered['s'] = qtl_filtered['snp_pos_1base']-1
        qtl_filtered['e'] = qtl_filtered['snp_pos_1base']+1
        return qtl_filtered[['chrom', 's', 'e', 'rsID', 'BayesFactor', 'strand']] # chrom   start   end   name   score   strand

def get_lead_qtl(qtl_genes_bed,qtl_type):
    qtl_genes = pd.read_csv(qtl_genes_bed, sep='\t', header=None,usecols=[0,1,3,4,9])
    if qtl_type == "stQTL":
        qtl_genes.columns = ['chrom', 'snp_pos', 'rsID', 'pvalue', 'geneID']
        qtl_genes['snp_pos'] = qtl_genes['snp_pos']+1
        lead_qtls = qtl_genes.loc[qtl_genes.groupby('geneID')['pvalue'].idxmin()]
    else:
        qtl_genes.columns = ['chrom', 'snp_pos', 'rsID', 'BF', 'geneID']
        qtl_genes['snp_pos'] = qtl_genes['snp_pos']+1
        # 对每个基因（geneID）分组，保留BayesFactor（BF）最大的那个QTL
        lead_qtls = qtl_genes.loc[qtl_genes.groupby('geneID')['BF'].idxmax()]
    return lead_qtls

def analyze_leadQTL_distance(qtl_file_1, qtl_file_2, qtl1, qtl2, gene_bed_file, chrom_size_file, work_dir, bim_dict, bfile_path):
    # 设置工作目录
    os.chdir(work_dir)
    # Step 1: 读取并筛选QTL summary数据
    qtl_filtered_1 = load_and_filter_qtl(qtl_file_1,qtl1)
    qtl_filtered_2 = load_and_filter_qtl(qtl_file_2,qtl2)
    # 保存为BED文件
    qtl_filtered_1.to_csv(f'{qtl1}.bed', sep='\t', header=False, index=False)
    qtl_filtered_2.to_csv(f'{qtl2}.bed', sep='\t', header=False, index=False)
    # Step 2: 排序BED文件
    call(f"sort -t, -k1,1V -k2,2n {qtl1}.bed > {qtl1}_sorted.bed",shell=True)
    call(f"sort -t, -k1,1V -k2,2n {qtl2}.bed > {qtl2}_sorted.bed",shell=True)
    # Step 3: 使用bedtools intersect找出QTL所在的基因
    call(f"bedtools intersect -a {qtl1}_sorted.bed -b {gene_bed_file} -g {chrom_size_file} -wa -wb -s -sorted > {qtl1}_gene.bed",shell=True)
    call(f"bedtools intersect -a {qtl2}_sorted.bed -b {gene_bed_file} -g {chrom_size_file} -wa -wb -s -sorted > {qtl2}_gene.bed",shell=True)
    # Step 4: 读取QTL和基因信息并找到每个基因的lead QTL
    lead_qtls_1 = get_lead_qtl(f'{qtl1}_gene.bed',qtl1)
    lead_qtls_2 = get_lead_qtl(f'{qtl2}_gene.bed',qtl2)
    lead_qtls_1 = lead_qtls_1.rename(columns={'rsID': 'rsID_1', 'snp_pos': 'snp_pos_1'})
    lead_qtls_2 = lead_qtls_2.rename(columns={'rsID': 'rsID_2', 'snp_pos': 'snp_pos_2'})
    merged_qtls = pd.merge(lead_qtls_1, lead_qtls_2[['geneID', 'rsID_2', 'snp_pos_2']], on='geneID', how='inner')
    # Step 5: 计算两个lead QTL之间的距离
    merged_qtls['dis'] = abs(merged_qtls['snp_pos_2'] - merged_qtls['snp_pos_1'])
    # 创建新的列 dis_group 根据预设的区间来划分 dis
    bins = [0, 10, 100, 1000, 10000, 100000]  # 设置区间
    labels = ['0', '10', '100', '1000', '10000']
    merged_qtls['dis_group'] = pd.cut(merged_qtls['dis'], bins=bins, labels=labels, right=False)
    # 设置绘图样式
    sns.set(style="whitegrid")
    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    sns.countplot(data=merged_qtls, x='dis_group', color='skyblue', edgecolor='black',width=0.4)
    # 添加标题和标签
    # plt.title('Distribution of Lead SNP Distance by Range', fontsize=16)
    plt.xlabel(f'Distance Range Between {qtl1} and {qtl2} (bp)', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    # 调整布局
    plt.tight_layout()
    # 保存图表为PDF
    plt.savefig(f'{qtl1}_{qtl2}_leaddis.pdf')
    # 检查是否包含 "rs"
    mask_rsID_1 = merged_qtls['rsID_1'].str.contains('rs', na=False)
    mask_rsID_2 = merged_qtls['rsID_2'].str.contains('rs', na=False)
    # 将 snp_pos_1 和 snp_pos_2 列转换为字符串类型
    merged_qtls['snp_pos_1'] = merged_qtls['snp_pos_1'].astype(str)
    merged_qtls['snp_pos_2'] = merged_qtls['snp_pos_2'].astype(str)
    # 使用位置信息替换不包含 "rs" 的值
    merged_qtls.loc[~mask_rsID_1, 'rsID_1'] = merged_qtls.loc[~mask_rsID_1, 'chrom'].str.replace('ch', '') + "_" + merged_qtls.loc[~mask_rsID_1, 'snp_pos_1'].str[2:]
    merged_qtls.loc[~mask_rsID_2, 'rsID_2'] = merged_qtls.loc[~mask_rsID_2, 'chrom'].str.replace('ch', '') + "_" + merged_qtls.loc[~mask_rsID_2, 'snp_pos_2'].str[2:]
    # 替换rsID为bim中的SNP name
    merged_qtls['rsID_1'] = merged_qtls['rsID_1'].map(bim_dict)
    merged_qtls['rsID_2'] = merged_qtls['rsID_2'].map(bim_dict)
    merged_qtls = merged_qtls.dropna(subset=['rsID_1', 'rsID_2'])
    merged_qtls = merged_qtls.reset_index(drop=True)
    res_df = add_ld_to_dataframe(merged_qtls, bfile_path)
    res_df.to_csv(f'{qtl1}_{qtl2}_LD.csv', index=False)

def run_plink_ld(bfile_path, rs1, rs2):
    if rs1 == rs2:
        return 1, 1
    else:
        command = [
                'plink',
                '--bfile', bfile_path,
                '--ld', rs1, rs2
            ]
        res = run(command, capture_output=True, text=True, check=True)
        filtered_ld_list = extract_r_sq_d(res.stdout)
        r2 ,d = filtered_ld_list[0][0], filtered_ld_list[0][1]
        return r2 ,d

def extract_r_sq_d(plink_output):
    r_sq_d_list = []
    pattern = r"R-sq = (.*)\s+D' = (.*)\n\n"  # 匹配R-sq和D'的正则表达式
    matches = re.findall(pattern, plink_output)
    for match in matches:
        r_sq = float(match[0])
        d = float(match[1])
        r_sq_d_list.append((r_sq, d))
    filtered_ld_list = filter_ld_results(r_sq_d_list)
    return filtered_ld_list


def filter_ld_results(r_sq_d_list, low_threshold=0.2, high_threshold=0.8):
    if len(r_sq_d_list) == 1:  # 如果只有一个结果，则直接保留
        return r_sq_d_list
    filtered_ld_list = []
    for r_sq, d in r_sq_d_list:
        if r_sq < low_threshold and d < low_threshold:
            continue  # 剔除R-sq和D'都很小的结果
        elif r_sq > high_threshold and d > high_threshold:
            filtered_ld_list.append((r_sq, d))  # 保留R-sq和D'都很大的结果
        elif (r_sq > low_threshold and d < low_threshold) or (r_sq < low_threshold and d > low_threshold):
            continue  # 剔除R-sq和D'一个大一个小的结果
        else:
            filtered_ld_list.append((r_sq, d)) # 保留其他结果
    if len(filtered_ld_list) > 0:
        return filtered_ld_list
    else:
        # 如果所有结果都被剔除，则选择一个相对合理的结果
        reasonable_result = None
        for r_sq, d in r_sq_d_list:
            if reasonable_result is None:
                reasonable_result = (r_sq, d)
            elif abs(r_sq - d) < abs(reasonable_result[0] - reasonable_result[1]):  # 选择R-sq和D'差异最小的结果
                reasonable_result = (r_sq, d)
        return [reasonable_result]

def add_ld_to_dataframe(res1_df, bfile_path):
    r2_list = []
    d_list = []
    for index, row in res1_df.iterrows():
        rs1 = row['rsID_1']
        rs2 = row['rsID_2']
        r2, d = run_plink_ld(bfile_path, rs1, rs2)
        r2_list.append(r2)
        d_list.append(d)
    res1_df['R_sq'] = r2_list
    res1_df['D'] = d_list
    return res1_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--chrom_size_file", type=str, help="chrom size file")
    parser.add_argument("-d","--work_dir", type=str, help="work directory")
    parser.add_argument("--geno", type=str, help="genotype file name")
    parser.add_argument("--gff", type=str, help="gff bed file")
    parser.add_argument("-b","--bim_dict", type=str, help="bim_dict.pkl file path")
    parser.add_argument("--qf1", type=str, help="QTL1 full summary statistics file")
    parser.add_argument("--q1", type=str, help="QTL1 type")
    parser.add_argument("--qf2", type=str, help="QTL2 full summary statistics file")
    parser.add_argument("--q2", type=str, help="QTL2 type")
    args = parser.parse_args()

    with open(args.bim_dict, 'rb') as f:
        bim_dict = pickle.load(f)
    analyze_leadQTL_distance(args.qf1, args.qf2, args.q1, args.q2, args.gff, args.chrom_size_file, args.work_dir, bim_dict, args.geno)

