import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.optimize import minimize_scalar
import argparse
import os
import pickle

def pi0est(pvalues, lambda_seq=np.arange(0.05, 0.95, 0.05), pi0_method="bootstrap"):
    m = len(pvalues)
    pi0 = min(1, np.mean(pvalues >= lambda_seq[-1]) / (1 - lambda_seq[-1]))
    if pi0_method == "bootstrap":
        mse = np.zeros_like(lambda_seq)
        for i, lambda_val in enumerate(lambda_seq):
            pi0_boot = np.mean(pvalues >= lambda_val) / (1 - lambda_val)
            mse[i] = np.mean((pi0_boot - pi0)**2)
        pi0 = min(1, np.mean(pvalues >= lambda_seq[np.argmin(mse)]) / (1 - lambda_seq[np.argmin(mse)]))
    return {"pi0": pi0}

def bootstrap_pi1_ci(pvalues, N=100, ci_percent=0.8, pi0_method="bootstrap"):
    lambda_seq = np.arange(0.05, 0.95, 0.05)
    def pi1_bootstrap(pvalues, pi0_method):
        p_samples = np.random.choice(pvalues, size=len(pvalues), replace=True)
        pi0_result = pi0est(p_samples, lambda_seq=lambda_seq, pi0_method=pi0_method)
        pi1_samples = 1 - pi0_result["pi0"]
        return pi1_samples
    pvalues = pvalues[~np.isnan(pvalues)]
    pi0_result = pi0est(pvalues, lambda_seq=lambda_seq, pi0_method=pi0_method)
    pi1_hat = 1 - pi0_result["pi0"]
    if N > 0:
        pi1_samples = [pi1_bootstrap(pvalues, pi0_method) for _ in range(N)]
        ci = np.percentile(pi1_samples, [(50-ci_percent/2*100), (50+ci_percent/2*100)])
    else:
        ci = np.array([pi1_hat, pi1_hat])
    result = {"ci_min": ci[0], "pi1": pi1_hat, "ci_max": ci[1]}
    return result

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

def load_and_filter_qtl(qtl_file,qtl_type):
    if qtl_type == "stQTL":
        cols_to_read = ["chrom","strand","snp_pos_1base","rsID","pvalue"]
        qtl_data = pd.read_csv(qtl_file, usecols=cols_to_read)
    else:
        cols_to_read = ["chrom","strand","snp_pos_1base","rsID","EAF","BayesFactor"]
        qtl_data = pd.read_csv(qtl_file, usecols=cols_to_read)
        qtl_data['pvalue'] = qtl_data.apply(lambda row: bf_to_pvalue(row['BayesFactor'], row['EAF'], "quant", 104), axis=1)
    qtl_data = qtl_data.loc[qtl_data.groupby(["chrom","strand","snp_pos_1base","rsID"])['pvalue'].idxmin()]
    # 修改列名
    qtl_data = qtl_data[["chrom","strand","snp_pos_1base","rsID","pvalue"]]
    qtl_data.columns = ["chrom","strand","snp_pos_1base","rsID",f"{qtl_type}_pvalue"]
    return qtl_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--base_qtl_type", type=str, help="base qtl type")
    parser.add_argument("-d","--work_dir", type=str, help="work directory")
    args = parser.parse_args()

    os.chdir(args.work_dir)
    # 主函数
    qtl_dict = {
        'inosine-QTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/Iqtl/nano_merge_I_summary.csv',
        'puQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/puqtl/nano_merge_promoter_summary.csv',
        'm6A-QTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/m6Aqtl/nano_merge_m6A_summary.csv',
        'pseU-QTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/pseUqtl/nano_merge_pseU_summary.csv',
        'm5C-QTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/m5Cqtl/nano_merge_m5C_summary.csv',
        'stQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/stqtl/nano_merge_stability_summary.csv',
        '3aQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/3aqtl/nano_merge_APA_summary.csv',
        'irQTL':'/mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/irqtl/nano_merge_isoform_summary.csv'
    }


    base_qtl_file = qtl_dict[args.base_qtl_type]
    merged_df = load_and_filter_qtl(base_qtl_file, args.base_qtl_type)

    for other_qtl_type, other_qtl_file in qtl_dict.items():
        if other_qtl_type == args.base_qtl_type:
            continue
        other_df = load_and_filter_qtl(other_qtl_file, other_qtl_type)
        merged_df = pd.merge(merged_df, other_df, on= ["chrom", "strand", "snp_pos_1base", "rsID"], how='left')

    all_res_dict = {}
    for i in qtl_dict.items():
        if i[0] == args.base_qtl_type:
            continue
        other_qtl_type = i[0]
        process_df = merged_df[[f"{args.base_qtl_type}_pvalue", f"{other_qtl_type}_pvalue"]].dropna()
        res_dict = {"all" : bootstrap_pi1_ci(np.array(merged_df[f"{other_qtl_type}_pvalue"]))}
        process_df_001 = process_df[process_df[f"{args.base_qtl_type}_pvalue"] < 0.01]
        res_dict["001"] = bootstrap_pi1_ci(np.array(process_df_001[f"{other_qtl_type}_pvalue"]))
        process_df_0001 = process_df[process_df[f"{args.base_qtl_type}_pvalue"] < 0.001]
        res_dict["0001"] = bootstrap_pi1_ci(np.array(process_df_0001[f"{other_qtl_type}_pvalue"]))
        process_df_00001 = process_df[process_df[f"{args.base_qtl_type}_pvalue"] < 0.0001]
        res_dict["00001"] = bootstrap_pi1_ci(np.array(process_df_00001[f"{other_qtl_type}_pvalue"]))
        all_res_dict[other_qtl_type] = res_dict

    with open(f'{args.base_qtl_type}_dict.pkl', 'wb') as f:
        pickle.dump(all_res_dict, f)
