```shell
## 1、筛选flag=0
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/0_bam_flag_filter.py -b nano_merge_calls_m5C_sorted_mod_map.bam -p ./nano_merge_m5C -t 10 -m strand
samtools index -@ 10 nano_merge_m5C_calls_sorted_map0.bam
samtools index -@ 10 nano_merge_m5C_calls_sorted_map16.bam

## 2、获取甲基化位点和read的对应关系
python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/1_pileup_read.py -o ./nano_merge -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam/m5C/nano_merge_m5C_calls_sorted_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/1_pileup_read.py -o ./nano_merge -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam/m5C/nano_merge_m5C_calls_sorted_map16.bam -t 10 -s - --motif

## 3、获取甲基化位点结果；read的pkl文件(base质量筛选)
python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/2_get_m5C_read.py -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m5C/nano_merge_map0.bam -f nano_merge_read_m5C_pos_f_tmp.txt -o ./nano_merge -c chr1 -s +
# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/run2.sh

## 4、合并结果、检查base、分析motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/3_mergeMODres.py -o ./nano_merge -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --metaPlotR

## 5、获取qtl位点结果
python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/4_get_m5Cqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m5C/nano_merge_map0.bam -p ./nano_merge -m /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/m5C/nano_merge_m5C_sites.csv -r /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/m5C/nano_merge_m5C_read_tmp_f.pkl -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes --snp_info /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/snp_info_singlesite.txt --snp_info /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/snp_info_singlesite.txt
# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/run4.sh

## 6、合并SNP位点情况；fisher
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m5C -o ./nano_merge --qqplot
```