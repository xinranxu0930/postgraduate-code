## 准备：安装R包
## 分析
```shell
python /mnt/hpc/home/xuxinran/DirectSeq/3_colco/trait8_colco.py -c chr1 -s + -o /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/colco -g /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/stability/gene_merge.bed --ASE /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/ASE/nano_merge_ASE_SNP.csv --m6A /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/m6A/nano_merge_m6A_SNP.csv --pseU /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/pseU/nano_merge_pseU_SNP.csv --stability /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/stability/nano_merge_stability_SNP.csv --isoform /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/isoform/nano_merge_isoform_SNP.csv --polyA /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/apa/nano_merge_polyA_SNP.csv --promoter /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/promoter/nano_merge_promoter_SNP.csv --tss /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/tss/nano_merge_tss_SNP.csv

# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/3_colco/run.sh
```