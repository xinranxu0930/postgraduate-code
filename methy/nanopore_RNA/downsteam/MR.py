# gene只能有._; 不能有别的字符
# esd命名的时候不要有别的字符
# epi和flist的表型 只能有.-

import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import seaborn as sns
from scipy.optimize import minimize_scalar
import argparse
import os
import pickle
from subprocess import call
import argparse

def bf_to_pvalue(bf, f, trait_type, N, s=None):
    """
    Calculate p-value from Bayes Factor for a SNP given other parameters.

    Parameters:
    - bf: Bayes Factor (not log)
    - f: minor allele frequency (MAF)
    - trait_type: 'quant' for quantitative trait or 'cc' for case-control
    - N: sample size
    - s: proportion of samples that are cases (required if trait_type is 'cc')

    Returns:
    - Estimated p-value
    """
    def Var_data(f, N):
        """Variance calculation for quantitative trait."""
        return 1 / (2 * N * f * (1 - f))
    def Var_data_cc(f, N, s):
        """Variance calculation for case-control data."""
        return 1 / (2 * N * f * (1 - f) * s * (1 - s))
    if trait_type == "quant":
        sd_prior = 0.15
        V = Var_data(f, N)
    else:
        sd_prior = 0.2
        V = Var_data_cc(f, N, s)
    r = sd_prior**2 / (sd_prior**2 + V)
    def objective(z):
        lABF = 0.5 * (np.log(1 - r) + (r * z**2))
        return abs(np.exp(lABF) - bf)
    # Find the z-score that minimizes the difference between calculated BF and given BF
    result = minimize_scalar(objective)
    z = abs(result.x)  # Take absolute value as z-score is always positive
    # Calculate p-value from z-score
    p = 2 * (1 - norm.cdf(z))
    return p

def getSE(A1_m6A, A1_A, A2_m6A, A2_A):
    alpha1_post = 1 + A1_m6A
    beta1_post = 1 + A1_A
    alpha2_post = 1 + A2_m6A
    beta2_post = 1 + A2_A
    var_A1 = alpha1_post * beta1_post / ((alpha1_post + beta1_post)^2 * (alpha1_post + beta1_post + 1))
    var_A2 = alpha2_post * beta2_post / ((alpha2_post + beta2_post)^2 * (alpha2_post + beta2_post + 1))
    SE = np.sqrt(var_A1 + var_A2)
    return SE

# stQTL求SE
def analyze_snp_stability_MannWhitneyU(A1_stability, A2_stability):
    total_count = len(A1_stability) + len(A2_stability)
    A1_count = len(A1_stability)
    A2_count = len(A2_stability)
    if (total_count < 10) or (A1_count == 0) or (A2_count == 0):
        return None,None
    stat, p_value = mannwhitneyu(A1_stability, A2_stability, alternative='two-sided')
    dominance = 0
    for x in A1_stability:
        for y in A2_stability:
            if x > y:
                dominance += 1
            elif x < y:
                dominance -= 1
    delta = dominance / (A1_count * A2_count)
    return p_value, delta

def bootstrap_delta_se(A1_stability, A2_stability, n_boot=100):
    A1_stability = eval(A1_stability)
    A2_stability = eval(A2_stability)
    delta_values = []
    for _ in range(n_boot):
        # 从原始数据中随机抽样
        A1_sample = np.random.choice(A1_stability, size=len(A1_stability), replace=True)
        A2_sample = np.random.choice(A2_stability, size=len(A2_stability), replace=True)
        # 计算 delta 值
        _, delta = analyze_snp_stability_MannWhitneyU(A1_sample, A2_sample)
        delta_values.append(delta)
    # 计算 SE
    se = np.std(delta_values)
    return se

def load_and_filter_qtl(qtl_file,qtl_type,work_dir, gene_bed_file, apa_bed_file, isoform_bed_file, pu_bed_File):
    if qtl_type == "stQTL":
        qtl_data = pd.read_csv(qtl_file)
        qtl_data['se'] = qtl_data.apply(lambda row: bootstrap_delta_se(row['A1_STscore_l'], row['A2_STscore_l']), axis=1)
        new_names = {'pvalue': f'{qtl_type}_pvalue', 'se': f'{qtl_type}_se', 'Beta': f'{qtl_type}_Beta'}
        qtl_data = qtl_data.rename(columns=new_names)
        qtl_data = qtl_data[["chrom","strand","snp_pos","rsID","A1","A2","EAF",f"{qtl_type}_Beta",f"{qtl_type}_pvalue",f"{qtl_type}_se"]]
        qtl_data['rsID'] = qtl_data.apply(lambda row: f"{row['chrom']}:{str(row['snp_pos'])}" if row['rsID'] == "." else row['rsID'], axis=1)
    elif qtl_type in ['m6AQTL','pseUQTL','m5CQTL','inosineQTL']:
        qtl_data = pd.read_csv(qtl_file)
        qtl_data['Pvalue'] = qtl_data.apply(lambda row: bf_to_pvalue(row['BayesFactor'], row['EAF'], "quant", 104), axis=1)
        qtl_data['se'] = qtl_data.apply(lambda row: getSE(row.iloc[10], row.iloc[8], row.iloc[11], row.iloc[9]), axis=1)
        qtl_data = qtl_data.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 17, 18, 19]]
        qtl_data.columns = ["chrom","strand","snp_pos",f"{qtl_type}_mod_pos","rsID","A1","A2","EAF",f"{qtl_type}_Beta",f"{qtl_type}_pvalue",f"{qtl_type}_se"]
        qtl_data['rsID'] = qtl_data.apply(lambda row: f"{row['chrom']}:{str(row['snp_pos'])}" if row['rsID'] == "." else row['rsID'], axis=1)
    else:
        qtl_data = pd.read_csv(qtl_file)
        qtl_data['Pvalue'] = qtl_data.apply(lambda row: bf_to_pvalue(row['BayesFactor'], row['EAF'], "quant", 104), axis=1)
        qtl_data['se'] = qtl_data.apply(lambda row: getSE(row.iloc[7], row.iloc[9], row.iloc[8], row.iloc[10]), axis=1)
        qtl_data = qtl_data.iloc[:, [0,1,2,3,4,5,6,11,15,16,17]]
        qtl_data.columns = ["chrom","strand","snp_pos","rsID","A1","A2","EAF",f"{qtl_type}_id",f"{qtl_type}_Beta",f"{qtl_type}_pvalue",f"{qtl_type}_se"]
        qtl_data["clean_id"] = qtl_data[f"{qtl_type}_id"].astype(str).str.replace(r'[^a-zA-Z0-9]', '', regex=True)
        qtl_data['rsID'] = qtl_data.apply(lambda row: f"{row['chrom']}:{str(row['snp_pos'])}" if row['rsID'] == "." else row['rsID'], axis=1)
    qtl_data_copy = qtl_data.copy()
    save_esi(qtl_data_copy, qtl_type)
    qtl_data_copy = qtl_data.copy()
    save_esd(qtl_data_copy, qtl_type)
    qtl_data_copy = qtl_data.copy()
    save_epi_flist(qtl_data_copy, qtl_type, work_dir, gene_bed_file, apa_bed_file, isoform_bed_file, pu_bed_File)

# 整个数据集中所有的SNP：1    rs1001  0   744055  A   G   0.23
def save_esi(df, qtl_type):
    df['chrom'] = df['chrom'].str.replace('chr', '', regex=False)
    df['LD_pos'] = 0
    res_df = df[["chrom","rsID","LD_pos","snp_pos","A1","A2","EAF"]]
    res_df.to_csv(f'{qtl_type}.esi', index=False, sep="\t", header=False)

# 每个表型对应的SNP：Chr    SNP Bp  A1  A2  Freq    Beta    se  p
def save_esd(df, qtl_type):
    df['chrom'] = df['chrom'].str.replace('chr', '', regex=False)
    if qtl_type in ['m6AQTL','pseUQTL','m5CQTL','inosineQTL']:
        df['mod_id'] = df['chrom'] + "X" + df[f"{qtl_type}_mod_pos"].astype(str)
        dfs = df.groupby('mod_id')
        for name, group in dfs:
            res_df = group[["chrom","rsID","snp_pos","A1","A2","EAF",f"{qtl_type}_Beta",f"{qtl_type}_se",f"{qtl_type}_pvalue"]]
            res_df.columns = ["Chr","SNP","Bp","A1","A2","Freq","Beta","se","p"]
            res_df.to_csv(f'{qtl_type}{name}.esd', index=False, sep="\t")
    if qtl_type in ['puQTL','3aQTL','irQTL']:
        dfs = df.groupby("clean_id")
        for name, group in dfs:
            res_df = group[["chrom","rsID","snp_pos","A1","A2","EAF",f"{qtl_type}_Beta",f"{qtl_type}_se",f"{qtl_type}_pvalue"]]
            res_df.columns = ["Chr","SNP","Bp","A1","A2","Freq","Beta","se","p"]
            res_df.to_csv(f'{qtl_type}{name}.esd', index=False, sep="\t")

# epi: 每个表型的信息：1    probe1001   0   924243  Gene01  +
# flist epi的基础上加上esd的路径
def save_epi_flist(df, qtl_type, work_dir,gene_bed_file,apa_bed_file,isoform_bed_file,pu_bed_file):
    if qtl_type in ['m6AQTL','pseUQTL','m5CQTL','inosineQTL']:
        df['s'] = df[f"{qtl_type}_mod_pos"].astype(int)-1
        df['e'] = df[f"{qtl_type}_mod_pos"].astype(int)+1
        df['score'] = 0
        df['mod_id'] = df['chrom'].astype(str) + df[f"{qtl_type}_mod_pos"].astype(str)
        bed_df = df[["chrom","s","e","mod_id","score","strand"]]
        bed_df = bed_df.drop_duplicates(keep="first")
        bed_df.to_csv(f'{qtl_type}_tmp.bed', sep='\t', index=False, header=False)
        call(f"bedtools intersect -a {qtl_type}_tmp.bed -b {gene_bed_file} -wa -wb -s > {qtl_type}_gene.bed", shell=True)
        gene_df = pd.read_csv(f'{qtl_type}_gene.bed', sep='\t', header=None, usecols=[0,1,3,5,9])
        gene_df.columns = ["chrom","mod_pos","mod_id","strand","gene_id"]
        gene_df['mod_pos'] = gene_df['mod_pos'] +1
        gene_df['gene_id'] = gene_df['gene_id'].astype(str).str.replace(",", ';', regex=True)
        gene_df["name"] = gene_df['chrom']+"-"+gene_df['mod_pos'].astype(str) # 表型名字：修饰位点
        gene_df['chrom'] = gene_df['chrom'].str.replace('chr', '', regex=False)
        gene_df["LD_pos"] = 0
        res_df = gene_df[["chrom","name","LD_pos","mod_pos","gene_id","strand"]]
        call(f"rm {qtl_type}_tmp.bed", shell=True)
        flist_df = res_df.copy()
        flist_df['clean_name'] = flist_df['name'].str.replace("-", "X").str.translate(str.maketrans("", "", "chr"))
        flist_df['PathOfEsd'] = f'{work_dir}/{qtl_type}' + flist_df['clean_name'].astype(str) + '.esd'
        del flist_df['clean_name']
        flist_df.columns = ["Chr","ProbeID","GeneticDistance","ProbeBp","Gene","Orientation",'PathOfEsd']
        flist_df.to_csv(f'{qtl_type}.flist', sep='\t', index=False)
    elif qtl_type == "stQTL":
        df['s'] = df["snp_pos"].astype(int)-1
        df['e'] = df["snp_pos"].astype(int)+1
        df['score'] = 0
        df['rsID'] = df.apply(lambda row: f"{row['chrom']}:{str(row['snp_pos'])}" if row['rsID'] == "." else row['rsID'], axis=1)
        bed_df = df[["chrom","s","e","rsID","score","strand"]]
        bed_df.to_csv(f'{qtl_type}_tmp.bed', sep='\t', index=False, header=False)
        call(f"bedtools intersect -a {qtl_type}_tmp.bed -b {gene_bed_file} -wa -wb -s > {qtl_type}_gene.bed", shell=True)
        gene_df = pd.read_csv(f'{qtl_type}_gene.bed', sep='\t', header=None, usecols=[3,7,9])
        gene_df.columns = ["rsID","gene_start","gene_id"]
        qtl_data = pd.merge(qtl_data, gene_df, on="rsID", how="left")
        # make esd
        qtl_data['chrom'] = qtl_data['chrom'].str.replace('chr', '', regex=False)
        dfs = qtl_data.groupby('gene_id')
        for name, group in dfs:
            res_df = group[["chrom","rsID","snp_pos","A1","A2","EAF",f"{qtl_type}_Beta",f"{qtl_type}_se",f"{qtl_type}_pvalue"]]
            res_df.columns = ["Chr","SNP","Bp","A1","A2","Freq","Beta","se","p"]
            res_df.to_csv(f'{qtl_type}_{name}.esd', index=False, sep="\t")
        # make epi
        qtl_data["LD_pos"] = 0
        res_df = qtl_data[["chrom","rsID","LD_pos","gene_start","gene_id","strand"]]
        call(f"rm {qtl_type}_tmp.bed", shell=True)
        # make flist
        flist_df = res_df.copy()
        flist_df['PathOfEsd'] = f'{work_dir}/{qtl_type}_'+ flist_df['gene_id'] +'.esd'
        flist_df.columns = ["Chr","ProbeID","GeneticDistance","ProbeBp","Gene","Orientation",'PathOfEsd']
        flist_df.to_csv(f'{qtl_type}.flist', sep='\t', index=False)
    elif qtl_type == "3aQTL":
        call(f"bedtools intersect -a {apa_bed_file} -b {gene_bed_file} -wa -wb -s > apa_gene.bed",shell=True)
        apa_df = pd.read_csv("apa_gene.bed",sep="\t",header=None,usecols=[0,1,3,5,13],names=["chrom","apa_s","apa_id","strand","gene_id"])
        apa_df = apa_df[apa_df['apa_id'].isin(df[f"{qtl_type}_id"])]
        apa_df['apa_id'] = apa_df['apa_id'].astype(str).str.replace(r'[^a-zA-Z0-9.-]', '-', regex=True)
        apa_df['gene_id'] = apa_df['gene_id'].astype(str).str.replace(",", ';', regex=True)
        apa_df['chrom'] = apa_df['chrom'].str.replace('chr', '', regex=False)
        apa_df['LD_pos'] = 0
        res_df = apa_df[["chrom","apa_id","LD_pos","apa_s","gene_id","strand"]]
        call(f"rm apa_gene.bed",shell=True)
        flist_df = res_df.copy()
        flist_df['clean_id'] = flist_df['apa_id'].astype(str).str.replace(r'[^a-zA-Z0-9]', '', regex=True)
        flist_df['PathOfEsd'] = f'{work_dir}/{qtl_type}'+ flist_df['clean_id'] +'.esd'
        del flist_df['clean_id']
        flist_df.columns = ["Chr","ProbeID","GeneticDistance","ProbeBp","Gene","Orientation",'PathOfEsd']
        flist_df.to_csv(f'{qtl_type}.flist', sep='\t', index=False)
    elif qtl_type == "irQTL":
        call(f"bedtools intersect -a {isoform_bed_file} -b {gene_bed_file} -wa -wb -s > isoform_gene.bed",shell=True)
        isoform_df = pd.read_csv("isoform_gene.bed",sep="\t",header=None,usecols=[0,1,3,5,15],names=["chrom","isoform_s","isoform_id","strand","gene_id"])
        isoform_df = isoform_df.drop_duplicates(subset=['isoform_id'], keep='first')
        isoform_df = isoform_df[isoform_df['isoform_id'].isin(df[f"{qtl_type}_id"])]
        isoform_df['isoform_id'] = isoform_df['isoform_id'].astype(str).str.replace(r'[^a-zA-Z0-9.-]', '-', regex=True)
        isoform_df['gene_id'] = isoform_df['gene_id'].astype(str).str.replace(",", ';', regex=True)
        isoform_df['chrom'] = isoform_df['chrom'].str.replace('chr', '', regex=False)
        isoform_df['LD_pos'] = 0
        res_df = isoform_df[["chrom","isoform_id","LD_pos","isoform_s","gene_id","strand"]]
        call(f"rm isoform_gene.bed",shell=True)
        flist_df = res_df.copy()
        flist_df['clean_id'] = flist_df['isoform_id'].astype(str).str.replace(r'[^a-zA-Z0-9]', '', regex=True)
        flist_df['PathOfEsd'] = f'{work_dir}/{qtl_type}'+ flist_df['clean_id'] +'.esd'
        del flist_df['clean_id']
        flist_df.columns = ["Chr","ProbeID","GeneticDistance","ProbeBp","Gene","Orientation",'PathOfEsd']
        flist_df.to_csv(f'{qtl_type}.flist', sep='\t', index=False)
    else:
        call(f"bedtools intersect -a {pu_bed_file} -b {gene_bed_file} -wa -wb -s > promoter_gene.bed",shell=True)
        pu_df = pd.read_csv("promoter_gene.bed",sep="\t",header=None,usecols=[0,1,3,5,9],names=["chrom","pu_s","pu_id","strand","gene_id"])
        pu_df = pu_df.drop_duplicates(subset=['pu_id'], keep='first')
        pu_df = pu_df[pu_df['pu_id'].isin(df[f"{qtl_type}_id"])]
        pu_df['pu_id'] = pu_df['pu_id'].astype(str).str.replace(r'[^a-zA-Z0-9.-]', '-', regex=True)
        pu_df['gene_id'] = pu_df['gene_id'].astype(str).str.replace(",", ';', regex=True)
        pu_df['chrom'] = pu_df['chrom'].str.replace('chr', '', regex=False)
        pu_df['LD_pos'] = 0
        res_df = pu_df[["chrom","pu_id","LD_pos","pu_s","gene_id","strand"]]
        call(f"rm promoter_gene.bed",shell=True)
        flist_df = res_df.copy()
        flist_df['clean_id'] = flist_df['pu_id'].astype(str).str.replace(r'[^a-zA-Z0-9]', '', regex=True)
        flist_df['PathOfEsd'] = f'{work_dir}/{qtl_type}'+ flist_df['clean_id'] +'.esd'
        del flist_df['clean_id']
        flist_df.columns = ["Chr","ProbeID","GeneticDistance","ProbeBp","Gene","Orientation",'PathOfEsd']
        flist_df.to_csv(f'{qtl_type}.flist', sep='\t', index=False)
    res_df.to_csv(f'{qtl_type}.epi', sep='\t', index=False, header=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--qtl_type", type=str, help="qtl type")
    args = parser.parse_args()

    work_dir = f"/mnt/hpc/home/xuxinran/DirectSeq/8_downsteam/MR/{args.qtl_type}"
    os.chdir(work_dir)
    gene_bed_file = "/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/stqtl/gene_merge.bed"
    apa_bed_file = "/mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/hg19.apadb_v2_final.sorted.bed"
    isoform_bed_file = "/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/irqtl/nano_merge.annotated_transcripts.bed"
    pu_bed_File = "/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/puqtl/promoter_final.bed"

    qtl_dict = {
        'inosineQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/Iqtl/nano_merge_I_summary.csv',
        'puQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/puqtl/nano_merge_promoter_summary.csv',
        'm6AQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/m6Aqtl/nano_merge_m6A_summary.csv',
        'pseUQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/pseUqtl/nano_merge_pseU_summary.csv',
        'm5CQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/m5Cqtl/nano_merge_m5C_summary.csv',
        'stQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/stqtl/nano_merge_stability_summary.csv',
        '3aQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/3aqtl/nano_merge_APA_summary.csv',
        'irQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/irqtl/nano_merge_isoform_summary.csv'
    }

    load_and_filter_qtl(qtl_dict[args.qtl_type],args.qtl_type,work_dir, gene_bed_file, apa_bed_file, isoform_bed_file, pu_bed_File)