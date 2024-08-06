```shell
## 1、筛选flag=0
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/0_bam_flag_filter.py -b nano_merge_calls_m6A_sorted_mod_map.bam -p ./nano_merge -t 10 -m strand
samtools index -@ 10 nano_merge_map0.bam
samtools index -@ 10 nano_merge_map16.bam

## 2、获取甲基化位点和read的对应关系
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -p ./nano_merge -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -p ./nano_merge -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map16.bam -t 10 -s - --motif

## 3、获取甲基化位点结果；read的pkl文件(base质量筛选)
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/2_get_m6A_read.py -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -f nano_merge_read_m6A_pos_f_motif_tmp.txt -p ./nano_merge -c chr1 -s +
# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/run2.sh

## 4、合并结果、检查base、分析motif
/mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/3_merge_motif.ipynb

## 5、获取qtl位点结果
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/4_get_m6Aqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -m /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/m6A/nano_merge_m6A_sites.csv -r /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/m6A/nano_merge_m6A_read_tmp_f.pkl -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes --snp_info /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt

# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/run4.sh

## 6、合并genome位点情况；fisher
/mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/5_fdr.ipynb
rm *_haplotype_chr*_tmp.csv *_read_m6A_pos_*_tmp.txt *_sorted_map16.bam* *_sorted_map0.bam* *_m6A_read_tmp_*.pkl
```