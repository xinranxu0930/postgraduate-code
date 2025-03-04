# 前期须知

**1、SNP文件**

提前准备snp的txt文件，header可以不一样，但是顺序要一样
- 有genotype，plink后将frq文件整理为标准格式

```shell
plink --bfile /mnt/hpc/home/xuxinran/huvec_genotype/huvec_imputed --freq --out /mnt/hpc/home/xuxinran/huvec_genotype/allele_frequencies
awk -F'\t' 'NR==1 || $NF > 0.05' /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt > /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite_005.txt
```
- 没有genotype，用对应的SNP vcf注释文件整理为标准格式
|CHR|pos|SNP|A1|A2|MAF|

| CHR | pos | SNP | A1 | A2 | MAF |
| :-: | :-: | :-: | :-: | :-: | :-: |
| chr1 | 16002228 | rs72704715 | C | G | 0.01923 |

<span style="color:red;">A1是minor(effect) A2是major MAF是A1的频率，也可以认为是EAF</span>

# 所有前期处理
## fast5 2 pod5
```shell
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5

pod5 convert fast5 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/20240202-zhaolin-RNA-2/old/fast5_pass/*.fast5 --strict --output old_2_pass.pod5
```

## basecall
```shell
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/basecall

## old1
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_1_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m6A_DRACH@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_1_calls_m6A.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m5C@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_1_calls_m5C.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_inosine_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_1_calls_I.bam

## old2
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_2_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m6A_DRACH@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_2_calls_m6A.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m5C@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_2_calls_m5C.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_inosine_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > old_2_calls_I.bam

## yo1
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_1_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m6A_DRACH@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_1_calls_m6A.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m5C@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_1_calls_m5C.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_1_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_inosine_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_1_calls_I.bam

## yo2
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_pseU@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_2_calls_pseU.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m6A_DRACH@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_2_calls_m6A.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_m5C@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_2_calls_m5C.bam
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_2_pass.pod5 --modified-bases-models /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0_inosine_m6A@v1 --reference /mnt/hpc/home/xuxinran/REF/hg19/hg19.fa --mm2-opts "-x splice -k 14" --modified-bases-threshold 0.7 --estimate-poly-a -x cuda:all > yo_2_calls_I.bam

## all
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_1_pass.pod5 --emit-fastq -x cuda:all > ../fastq/all/old_1_calls_all.fastq
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/old_2_pass.pod5 --emit-fastq -x cuda:all > ../fastq/all/old_2_calls_all.fastq
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_1_pass.pod5 --emit-fastq -x cuda:all > ../fastq/all/yo_1_calls_all.fastq
/mnt/hpc/home/xuxinran/DirectSeq/dorado-0.8.1-linux-x64/bin/dorado basecaller /mnt/hpc/home/xuxinran/DirectSeq/dorado_model/rna004_130bps_hac@v5.1.0 /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/pod5/yo_2_pass.pod5 --emit-fastq -x cuda:all > ../fastq/all/yo_2_calls_all.fastq
cd ../fastq/all
cat *_calls_all.fastq > nano_merge_calls_all.fastq

```
## 两种bam 2 fastq
```shell
## bam2fastq
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A
samtools fastq -T "MM,ML" -@ 100 -0 old_1_calls_m6A.fastq ../../basecall/old_1_calls_m6A.bam
samtools fastq -T "MM,ML" -@ 100 -0 old_2_calls_m6A.fastq ../../basecall/old_2_calls_m6A.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_1_calls_m6A.fastq ../../basecall/yo_1_calls_m6A.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_2_calls_m6A.fastq ../../basecall/yo_2_calls_m6A.bam
cat *_calls_m6A.fastq > nano_merge_calls_m6A.fastq

cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/pseU
samtools fastq -T "MM,ML" -@ 100 -0 old_1_calls_pseU.fastq ../../basecall/old_1_calls_pseU.bam
samtools fastq -T "MM,ML" -@ 100 -0 old_2_calls_pseU.fastq ../../basecall/old_2_calls_pseU.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_1_calls_pseU.fastq ../../basecall/yo_1_calls_pseU.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_2_calls_pseU.fastq ../../basecall/yo_2_calls_pseU.bam
cat *_calls_pseU.fastq > nano_merge_calls_pseU.fastq

cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m5C
samtools fastq -T "MM,ML" -@ 100 -0 old_1_calls_m5C.fastq ../../basecall/old_1_calls_m5C.bam
samtools fastq -T "MM,ML" -@ 100 -0 old_2_calls_m5C.fastq ../../basecall/old_2_calls_m5C.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_1_calls_m5C.fastq ../../basecall/yo_1_calls_m5C.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_2_calls_m5C.fastq ../../basecall/yo_2_calls_m5C.bam
cat *_calls_m5C.fastq > nano_merge_calls_m5C.fastq

cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/I
samtools fastq -T "MM,ML" -@ 100 -0 old_1_calls_I.fastq ../../basecall/old_1_calls_I.bam
samtools fastq -T "MM,ML" -@ 100 -0 old_2_calls_I.fastq ../../basecall/old_2_calls_I.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_1_calls_I.fastq ../../basecall/yo_1_calls_I.bam
samtools fastq -T "MM,ML" -@ 100 -0 yo_2_calls_I.fastq ../../basecall/yo_2_calls_I.bam
cat *_calls_I.fastq > nano_merge_calls_I.fastq
```

# minimap 添加mod tag
```shell
## minimap2
minimap2 -ax splice -ub -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/nano_merge_calls_m6A.fastq | samtools sort -@ 100 -O BAM -o nano_merge_calls_m6A_sorted.bam
samtools index -@ 20 nano_merge_calls_m6A_sorted.bam

minimap2 -ax splice -ub -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m5C/nano_merge_calls_m5C.fastq | samtools sort -@ 100 -O BAM -o nano_merge_calls_m5C_sorted.bam
samtools index -@ 20 nano_merge_calls_m5C_sorted.bam

minimap2 -ax splice -ub -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/pseU/nano_merge_calls_pseU.fastq | samtools sort -@ 100 -O BAM -o nano_merge_calls_pseU_sorted.bam
samtools index -@ 20 nano_merge_calls_pseU_sorted.bam

minimap2 -ax splice -ub -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/I/nano_merge_calls_I.fastq | samtools sort -@ 100 -O BAM -o nano_merge_calls_I_sorted.bam
samtools index -@ 20 nano_merge_calls_I_sorted.bam

minimap2 -ax splice -ub -k14 -t 100 /mnt/hpc/home/xuxinran/REF/hg19/DirectSeq/hg19_dna.min /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/all/nano_merge_calls_all.fastq | samtools sort -@ 100 -O BAM -o nano_merge_calls_all_sorted.bam
samtools index -@ 20 nano_merge_calls_all_sorted.bam
python /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/0_bam_flag_filter.py -b nano_merge_calls_all_sorted.bam -p ./nano_merge_all -t 10 -m all
samtools index -@ 10 nano_merge_all_calls_sorted_map0.bam
samtools index -@ 10 nano_merge_all_calls_sorted_map16.bam
samtools index -@ 10 nano_merge_all_calls_sorted_map.bam


## 添加mod tag
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam
python /mnt/hpc/home/xuxinran/DirectSeq/nanom6Aqtl/00_add_modification_tag.py -f /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/nano_merge_calls_m6A.fastq -b nano_merge_calls_m6A_sorted.bam -t 20
samtools index -@ 20 nano_merge_calls_m6A_sorted_mod_map.bam

python /mnt/hpc/home/xuxinran/DirectSeq/nanopseUqtl/00_add_modification_tag.py -f /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/pseU/nano_merge_calls_pseU.fastq -b nano_merge_calls_pseU_sorted.bam -t 20
samtools index -@ 20 nano_merge_calls_pseU_sorted_mod_map.bam

python /mnt/hpc/home/xuxinran/DirectSeq/nanom5Cqtl/00_add_modification_tag.py -f /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m5C/nano_merge_calls_m5C.fastq -b nano_merge_calls_m5C_sorted.bam -t 20
samtools index -@ 20 nano_merge_calls_m5C_sorted_mod_map.bam

python /mnt/hpc/home/xuxinran/DirectSeq/nanoIqtl/00_add_modification_tag.py -f /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/I/nano_merge_calls_I.fastq -b nano_merge_calls_I_sorted.bam -t 20
samtools index -@ 20 nano_merge_calls_I_sorted_mod_map.bam

rm nano_merge_calls_pseU_sorted.bam*
rm nano_merge_calls_m6A_sorted.bam*
rm nano_merge_calls_I_sorted.bam*
rm nano_merge_calls_m5C_sorted.bam*
```

# 数据量统计
```shell
# map情况 17981994
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam/all
samtools flagstat nano_merge_calls_sorted_map.bam
# read数量 base数量
cd /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A
seqkit stat /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/nano_merge_calls_m6A.fastq
# duplication
# 数据质量
NanoPlot --fastq /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/fastq/m6A/nano_merge_calls_m6A.fastq -o fastq-plots --maxlength 500000 -t 20 --plots hex dot
# 平均测序量
samtools depth -a /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.8.1/bam/all/nano_merge_calls_sorted_map.bam > depth.txt
awk '$3 > 0 {sum+=$3; count++} END {print sum/count}' depth.txt
rm depth.txt
```



