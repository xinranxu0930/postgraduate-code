#!/bin/bash

# 参数
input_dir=""
bowtie2_index=""
output_dir=""
threads=4
script_path="/mnt/hpc/home/xuxinran/code/ATACseq.sh"
partition="cpuPartition"   # 分区，默认值为 cpuPartition
node="cpu09"               # 默认节点

# 打印帮助信息
usage() {
    echo "Usage: $0 -i <input_dir> -x <bowtie2_index> -o <output_dir> [-t <threads>] [-p <partition>] [-n <node>] [-l <log_dir>]"
    echo ""
    echo "Description:"
    echo "  This script submits Slurm jobs for all paired R1.fastq.gz and R2.fastq.gz files in the input directory."
    echo ""
    echo "Required arguments:"
    echo "  -i <input_dir>        Directory containing input FASTQ files."
    echo "  -x <bowtie2_index>    Path to the Bowtie2 index."
    echo "  -o <output_dir>       Directory to save output files."
    echo ""
    echo "Optional arguments:"
    echo "  -t <threads>          Number of threads for each job (default: 4)."
    echo "  -n <node>             The node to run the job (default: cpu09)."
    exit 1
}

# 解析参数
while getopts ":i:x:o:t:p:n:l:" opt; do
    case $opt in
        i) input_dir="$OPTARG" ;;
        x) bowtie2_index="$OPTARG" ;;
        o) output_dir="$OPTARG" ;;
        t) threads="$OPTARG" ;;
        p) partition="$OPTARG" ;;
        n) node="$OPTARG" ;;
        l) log_dir="$OPTARG" ;;
        *) usage ;;
    esac
done

# 检查参数是否完整
if [ -z "$input_dir" ] || [ -z "$bowtie2_index" ] || [ -z "$output_dir" ]; then
    usage
fi

# 自动设置分区
if [[ "$partition" == *"cpu"* ]]; then
    partition="cpuPartition"
elif [[ "$partition" == *"gpu"* ]]; then
    partition="gpu"
else
    echo "Error: Please specify a valid partition (e.g., 'cpu01' or 'gpu02')."
    exit 1
fi

# 创建输出目录（如果不存在）
mkdir -p "$output_dir"
log_dir="${output_dir}/slurm_log"
mkdir "$log_dir"

# 遍历所有成对的 FASTQ 文件
for fastq1 in "$input_dir"/*R1.fastq.gz; do
    # 自动匹配 R2 文件（匹配 _R1 或 .R1 后缀）
    fastq2="${fastq1/_R1.fastq.gz/_R2.fastq.gz}"
    fastq2="${fastq2/.R1.fastq.gz/.R2.fastq.gz}"
    
    # 检查 R2 文件是否存在
    if [ ! -f "$fastq2" ]; then
        echo "Warning: Skipping $fastq1 because paired R2 file not found."
        continue
    fi

    # 提取文件前缀作为输出前缀
    base_name=$(basename "$fastq1" .R1.fastq.gz)
    base_name="${base_name/.R1/}"
    output_prefix="$base_name"

    # 定义 Slurm 作业脚本内容
    slurm_script="$output_dir/${output_prefix}.slurm"
    cat <<EOF > "$slurm_script"
#!/bin/bash
#SBATCH --job-name=${output_prefix}
#SBATCH --partition=$partition
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=$threads
#SBATCH --error=$log_dir/${output_prefix}_%j.err
#SBATCH --output=$log_dir/${output_prefix}_%j.out
#SBATCH -w $node

bash $script_path "$fastq1" "$fastq2" "$bowtie2_index" "$output_prefix" "$output_dir" "$threads"
EOF

    # 提交 Slurm 作业
    sbatch "$slurm_script"
    echo "Submitted job for: $fastq1 and $fastq2"
done

echo "All jobs have been submitted."