
## 获取gencode promoter
```Shell
# TSS转promoter
awk 'BEGIN{OFS=FS="\t"}{
    if($6 == "+") {
        start = $2 - 2000;
        end = $3 + 500;
    } else if($6 == "-") {
        start = $2 - 500;
        end = $3 + 2000;
    }
    if(start < 0) start = 0;  # 确保起始位置不小于0
    print $1, start, end, $4, $5, $6, $7, $8;
}' /mnt/hpc/home/xuxinran/REF/hg19/Hs_EPDnew_006_hg19.bed > promoter_expanded.bed

sort -k1,1 -k2,2n promoter_expanded.bed > promoter_expanded_sorted.bed

bedtools merge -i promoter_expanded_sorted.bed -s -c 4,5,6 -o collapse > promoter_merge.bed

awk 'BEGIN{OFS="\t"} {$5 = 0; print}' promoter_merge.bed > temp_promoter_merge.bed

awk 'BEGIN{OFS="\t"} {
    split($6, strand, ",");
    $6 = strand[1];
    print
}' temp_promoter_merge.bed > promoter_final.bed

rm temp_promoter_merge.bed *expanded*

# 获取read-promoter的关系
python /mnt/hpc/home/xuxinran/DirectSeq/nanopuqtl/1_read2promoter.py

# 识别qtl
python /mnt/hpc/home/xuxinran/DirectSeq/nanopuqtl/2_get_puqtl.py -c chr1 -b /mnt/hpc/home/xuxinran/DirectSeq/data/zhaolin_240206/240201-zhaolin-RNA-merge/v0.7.2/bam/m6A/nano_merge_map0.bam -p ./nano_merge -s + --geno_size /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes -t 20 -f nano_merge_overlap_uniq.bed --snp_info /mnt/hpc/home/xuxinran/DirectSeq/refData_prepartCode/snp_info_singlesite.txt
#实际运行 /mnt/hpc/home/xuxinran/DirectSeq/nanopuqtl/run2.sh

python /mnt/hpc/home/xuxinran/DirectSeq/sharedCode/merge_trait_SNP_res.py -t promoter -o ./nano_merge --qqplot
```



