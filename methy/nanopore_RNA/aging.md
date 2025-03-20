## m6A分析流程
```shell
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/aging/m6A

## 0、比对获取bam文件
cat /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/old_1_calls_m6A.fastq /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/old_2_calls_m6A.fastq > nano_old_calls_m6A.fastq
cat /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/yo_1_calls_m6A.fastq /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/yo_2_calls_m6A.fastq > nano_yo_calls_m6A.fastq

minimap2 -ax splice -ub -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min nano_old_calls_m6A.fastq | samtools sort -@ 100 -O BAM -o nano_old_calls_m6A_sorted.bam
samtools index -@ 20 nano_old_calls_m6A_sorted.bam

minimap2 -ax splice -ub -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min nano_yo_calls_m6A.fastq | samtools sort -@ 100 -O BAM -o nano_yo_calls_m6A_sorted.bam
samtools index -@ 20 nano_yo_calls_m6A_sorted.bam

python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/00_add_modification_tag.py -f nano_old_calls_m6A.fastq -b nano_old_calls_m6A_sorted.bam -t 20
samtools index -@ 20 nano_old_calls_m6A_sorted_mod_map.bam

python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/00_add_modification_tag.py -f nano_yo_calls_m6A.fastq -b nano_yo_calls_m6A_sorted.bam -t 20
samtools index -@ 20 nano_yo_calls_m6A_sorted_mod_map.bam

python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/0_bam_flag_filter.py -b nano_old_calls_m6A_sorted_mod_map.bam -p ./nano_old -t 10 -m all
samtools index -@ 10 nano_old_calls_sorted_map0.bam
samtools index -@ 10 nano_old_calls_sorted_map16.bam
samtools index -@ 10 nano_old_calls_sorted_map.bam

python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/0_bam_flag_filter.py -b nano_yo_calls_m6A_sorted_mod_map.bam -p ./nano_yo -t 10 -m all
samtools index -@ 10 nano_yo_calls_sorted_map0.bam
samtools index -@ 10 nano_yo_calls_sorted_map16.bam
samtools index -@ 10 nano_yo_calls_sorted_map.bam

rm nano_old_calls_m6A_sorted.bam* nano_old_calls_m6A_sorted_mod_map.bam* nano_yo_calls_m6A_sorted.bam* nano_yo_calls_m6A_sorted_mod_map.bam*


## 1、获取甲基化位点和read的对应关系
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./nano_old -b nano_old_calls_sorted_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./nano_old -b nano_old_calls_sorted_map16.bam -t 10 -s - --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./nano_yo -b nano_yo_calls_sorted_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./nano_yo -b nano_yo_calls_sorted_map16.bam -t 10 -s - --motif

## 3、获取甲基化位点结果；read的pkl文件(base质量筛选)
bash /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/aging/m6A/run2.sh

## 4、合并结果、检查base、分析motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/3_mergeMODres.py -o ./nano_old -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/3_mergeMODres.py -o ./nano_yo -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa

## 5、获取qtl位点结果
# 实际运行
bash /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/aging/m6A/run4.sh

## 6、合并SNP位点情况
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m6A -o ./nano_old
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m6A -o ./nano_yo






# young downsample再call qtl
# old: 4,174,410 yo: 13,691,545
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/aging/m6A/downsample

samtools view -@ 20 -s 42.30 -b ../nano_yo_calls_sorted_map.bam -o nano_yo_ds_calls_sorted_map.bam
samtools index nano_yo_ds_calls_sorted_map.bam
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/0_bam_flag_filter.py -b nano_yo_ds_calls_sorted_map.bam -p ./nano_yo_ds -t 10 -m strand
samtools index -@ 10 nano_yo_ds_calls_sorted_map0.bam
samtools index -@ 10 nano_yo_ds_calls_sorted_map16.bam

python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./nano_yo_ds -b nano_yo_ds_calls_sorted_map0.bam -t 10 -s + --motif
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/1_pileup_read.py -o ./nano_yo_ds -b nano_yo_ds_calls_sorted_map16.bam -t 10 -s - --motif

bash run2.sh

python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/3_mergeMODres.py -o ./nano_yo_ds -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa

bash run4.sh

## 6、合并SNP位点情况
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m6A -o ./nano_yo_ds

```


## 其他7种QTL分析流程
```shell
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_pseU_1.sh
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_m5C_1.sh
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_i_1.sh
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_trans4_1.sh

# APA
/mnt/hpc/home/xuxinran/DirectSeq/nano3aqtl/1_read2apadb.ipynb
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_apa_2.sh
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t apa -o ./old
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t apa -o ./young

# isoform
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_isoform_2.sh
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t isoform -o ./old
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t isoform -o ./young

# promoter
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_promoter_2.sh
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t promoter -o ./old
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t promoter -o ./young

# st
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_st_3.sh



# pseU
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_pseU_2.sh
python /mnt/hpc/home/xuxinran/DirectSeq/nanopseUqtl/3_mergeMODres.py -o ./old -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
python /mnt/hpc/home/xuxinran/DirectSeq/nanopseUqtl/3_mergeMODres.py -o ./young -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_pseU_4.sh
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t pseU -o ./old
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t pseU -o ./young

# m5C
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_m5C_2.sh
python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/3_mergeMODres.py -o ./old -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/3_mergeMODres.py -o ./young -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_m5C_4.sh
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m5C -o ./old
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t m5C -o ./young

# i
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_i_2.sh
python /mnt/hpc/home/xuxinran/DirectSeq/nanoIqtl/3_mergeMODres.py -o ./old -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
python /mnt/hpc/home/xuxinran/DirectSeq/nanoIqtl/3_mergeMODres.py -o ./young -f /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa
bash /mnt/hpc/home/xuxinran/DirectSeq/6_aging/run_i_4.sh
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t i -o ./old
python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t i -o ./young
```