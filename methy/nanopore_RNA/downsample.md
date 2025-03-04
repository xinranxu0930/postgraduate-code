```shell
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/model_checking_downsample

# 下采样
samtools view -@ 20 -s 42.75 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam/m6A/nano_merge_calls_m6A_sorted_mod_map.bam -o 75_m6A_sorted_mod_map.bam # 75%
samtools view -@ 20 -s 42.50 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam/m6A/nano_merge_calls_m6A_sorted_mod_map.bam -o 50_m6A_sorted_mod_map.bam # 50%
samtools view -@ 20 -s 42.25 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam/m6A/nano_merge_calls_m6A_sorted_mod_map.bam -o 25_m6A_sorted_mod_map.bam # 25%
samtools index 75_m6A_sorted_mod_map.bam
samtools index 50_m6A_sorted_mod_map.bam
samtools index 25_m6A_sorted_mod_map.bam

python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/0_bam_flag_filter.py -b 75_m6A_sorted_mod_map.bam -p ./75_m6A -t 10 -m strand
samtools index -@ 10 75_m6A_calls_sorted_map16.bam
samtools index -@ 10 75_m6A_calls_sorted_map0.bam
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/0_bam_flag_filter.py -b 50_m6A_sorted_mod_map.bam -p ./50_m6A -t 10 -m strand
samtools index -@ 10 50_m6A_calls_sorted_map16.bam
samtools index -@ 10 50_m6A_calls_sorted_map0.bam
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/0_bam_flag_filter.py -b 25_m6A_sorted_mod_map.bam -p ./25_m6A -t 10 -m strand
samtools index -@ 10 25_m6A_calls_sorted_map16.bam
samtools index -@ 10 25_m6A_calls_sorted_map0.bam

# call m6A
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./75_m6A -b ./bam/75_m6A_calls_sorted_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./75_m6A -b ./bam/75_m6A_calls_sorted_map16.bam -t 10 -s - --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./50_m6A -b ./bam/50_m6A_calls_sorted_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./50_m6A -b ./bam/50_m6A_calls_sorted_map16.bam -t 10 -s - --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./25_m6A -b ./bam/25_m6A_calls_sorted_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./25_m6A -b ./bam/25_m6A_calls_sorted_map16.bam -t 10 -s - --motif

## 3、获取甲基化位点结果；read的pkl文件(base质量筛选)
bash /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/aging/m6A/run2.sh

## 4、合并结果、检查base、分析motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/3_mergeMODres.py -o ./75 -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/3_mergeMODres.py -o ./50 -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/3_mergeMODres.py -o ./25 -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa

## 5、获取qtl位点结果
# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/aging/m6A/run4.sh

## 6、合并SNP位点情况
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m6A -o ./75
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m6A -o ./50
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m6A -o ./25

```