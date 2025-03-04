#!/bin/bash

# 打印帮助信息
usage() {
    echo "Usage: $0 <fastq1> <fastq2> <bowtie2_index> <output_prefix> <output_dir> <threads>"
    echo ""
    echo "Description:"
    echo "  This script processes ATAC-seq data through the following steps:"
    echo "    1. Bowtie2 alignment of paired-end FASTQ files."
    echo "    2. Sorting, deduplication, and indexing of BAM files using SAMtools."
    echo "    3. Peak calling using MACS2."
    exit 1
}

# 检查参数数量
if [ "$#" -ne 6 ]; then
    usage
fi

# 参数赋值
fastq1=$1
fastq2=$2
bowtie2_index=$3
output_prefix=$4
output_dir=$5
threads=$6

# 检查参数是否完整
if [ -z "$fastq1" ] || [ -z "$fastq2" ] || [ -z "$bowtie2_index" ] || [ -z "$output_prefix" ] || [ -z "$output_dir" ]; then
    usage
fi

# 创建或清空输出目录
mkdir -p "$output_dir"/"$output_prefix"_ATACseq

# 定义中间文件
raw_bam_file="${output_dir}/${output_prefix}.bam"
fixmate_bam_file="${output_dir}/${output_prefix}.fixmate.bam"
sort_bam_file="${output_dir}/${output_prefix}.sorted.bam"
dedup_bam="${output_dir}/${output_prefix}.sorted.dedup.bam"
peak_file="${output_dir}/${output_prefix}_peaks"

# 1. Bowtie2 比对
echo "Running Bowtie2 ..."
bowtie2 -p "$threads" -x "$bowtie2_index" -1 "$fastq1" -2 "$fastq2" | samtools sort -n -O bam -@ "$threads" -o - > "$raw_bam_file"
if [ $? -ne 0 ]; then
    echo "Bowtie2 alignment failed."
    exit 1
fi

# 2. SAMtools 排序
echo "Samtools fixmate..."
samtools fixmate -@ "$threads" -m "$raw_bam_file" "$fixmate_bam_file"
samtools sort -@ "$threads" -o "$sort_bam_file" "$fixmate_bam_file"
if [ $? -ne 0 ]; then
    echo "SAMtools sorting failed."
    exit 1
fi

# 3. SAMtools 去重
echo "Removing duplicates..."
samtools markdup -@ "$threads" -r "$sort_bam_file" "$dedup_bam"
if [ $? -ne 0 ]; then
    echo "SAMtools deduplication failed."
    exit 1
fi

# 4. SAMtools 构建索引
echo "Indexing BAM file..."
samtools index -@ "$threads" "$dedup_bam"
if [ $? -ne 0 ]; then
    echo "SAMtools indexing failed."
    exit 1
fi

# 5. MACS2 Call Peak
echo "Calling peaks with MACS2..."
mkdir -p "$output_dir"/Macs2_out
macs2 callpeak -t "$dedup_bam" -n "$output_prefix" --outdir "$output_dir"/Macs2_out -g hs
if [ $? -ne 0 ]; then
    echo "MACS2 peak calling failed."
    exit 1
fi

echo "Pipeline completed successfully. Results are in $output_dir/Macs2_out."