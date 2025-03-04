**24-08-06 scMicroC qc**
```shell
cd /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc

python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 Bio-scMicro-C-K562_R1_001.fastq.gz -f2 Bio-scMicro-C-K562_R2_001.fastq.gz -o ./Bio-scMicro-C-K562
python /mnt/hpc/home/xuxinran/microC/trim_index.py -a CTGTCTCTTATACA -f1 Bio-scMicro-C-K562_trim_1.fq -f2 Bio-scMicro-C-K562_trim_2.fq -o ./Bio-scMicro-C-K562

seqkit stat Bio-scMicro-C-K562_R1_001.fastq.gz  Bio-scMicro-C-K562_trim_1.fq  Bio-scMicro-C-K562_trim_index_1.fq

bwa mem -5SP -T0 -t100 /mnt/hpc/home/xuxinran/REF/hg19/Sequence/BWAIndex/genome.fa Bio-scMicro-C-K562_trim_index_1.fq Bio-scMicro-C-K562_trim_index_2.fq -o Bio-scMicro-C-K562_aligned.sam
pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in 100 --nproc-out 100 --chroms-path /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes Bio-scMicro-C-K562_aligned.sam > Bio-scMicro-C-K562_parsed.pairsam
pairtools sort --tmpdir ./tmp --nproc 100 Bio-scMicro-C-K562_parsed.pairsam > Bio-scMicro-C-K562_sorted.pairsam
pairtools dedup --nproc-in 100 --nproc-out 100 --mark-dups --max-mismatch 3 --backend cython --output-stats Bio-scMicro-C-K562_stats.txt --output Bio-scMicro-C-K562_dedup.pairsam Bio-scMicro-C-K562_sorted.pairsam
python3 /mnt/hpc/home/xuxinran/microC/Micro-C-main/get_qc.py -p Bio-scMicro-C-K562_stats.txt > Bio-scMicro-C-K562_qc.txt
```

**24-08-06 5次scMicroC比较**
1. clean read 汇总
```shell
cd /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 B_L003_R1_001.fastq.gz -f2 B_L003_R2_001.fastq.gz -o ./B_L003
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 B_L003_trim_1.fq -f2 B_L003_trim_2.fq -a CTGTCTCTTATACA -o ./B_L003
cd /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 C_L003_R1_001.fastq.gz -f2 C_L003_R2_001.fastq.gz -o ./C_L003
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 C_L003_trim_1.fq -f2 C_L003_trim_2.fq -a CTGTCTCTTATACA -o ./C_L003

cd /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 scMicro-ATAC-2x_S4_L001_R1_001.fastq.gz -f2 scMicro-ATAC-2x_S4_L001_R3_001.fastq.gz -o ./scMicro-ATAC-2x
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 scMicro-ATAC-2x_trim_1.fq -f2 scMicro-ATAC-2x_trim_2.fq -a CTGTCTCTTATACA -o ./scMicro-ATAC-2x
cd /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x
python /mnt/hpc/home/xuxinran/microC/trim_diffadapter.py -f1 scMicro-ATAC-12x_S8_L001_R1_001.fastq.gz -f2 scMicro-ATAC-12x_S8_L001_R3_001.fastq.gz -o ./scMicro-ATAC-12x
python /mnt/hpc/home/xuxinran/microC/trim_index.py -f1 scMicro-ATAC-12x_trim_1.fq -f2 scMicro-ATAC-12x_trim_2.fq -a CTGTCTCTTATACA -o ./scMicro-ATAC-12x


seqkit stat /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x/scMicro-ATAC-2x_S4_L001_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x/scMicro-ATAC-2x_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/2x/scMicro-ATAC-2x_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x/scMicro-ATAC-12x_S8_L001_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x/scMicro-ATAC-12x_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0327/scMicroC/bulk_data/12x/scMicro-ATAC-12x_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B/B_L003_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B/B_L003_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/B/B_L003_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C/C_L003_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C/C_L003_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0516_scMicroC/data/C/C_L003_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0724/scMicroC/clean_data/Bio-scMicro-C-K562_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0724/scMicroC/clean_data/Bio-scMicro-C-K562_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0724/scMicroC/clean_data/Bio-scMicro-C-K562_trim_read1N_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc/qc/2-Bio-scMicro-C-K562_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc/qc/2-Bio-scMicro-C-K562_trim_1.fq /mnt/hpc/home/xuxinran/microC/date/date_0806_scMicroCqc/qc/2-Bio-scMicro-C-K562_trim_index_1.fq
```

**24-08-20 MicroCRUN**
```shell
# 去index
## no生物素
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-CTCF-2_L7_G007 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-K27ac-2_L7_G028 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-4_L7_G092.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-4_L7_G092.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-CTCF-4_L7_G092 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-4_L7_G027.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-4_L7_G027.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/no-GM-K27ac-4_L7_G027 -i GATCGGAAGAGCA
## 生物素
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-2_L4_G029.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-2_L4_G029.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-CTCF-2_L4_G029 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-CTCF-4_L4_G042 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-K27ac-2_L4_G005 -i GATCGGAAGAGCA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-4_L4_G084.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-4_L4_G084.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0820_1micriC_2microRUN/microRUN/clean_data/bio-GM-K27ac-4_L4_G084 -i GATCGGAAGAGCA

# 去adapter
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-CTCF-2_L4_G029_trim_index_1.fq -f2 bio-GM-CTCF-2_L4_G029_trim_index_2.fq -o bio-GM-CTCF-2_L4_G029 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-CTCF-4_L4_G042_trim_index_1.fq -f2 bio-GM-CTCF-4_L4_G042_trim_index_2.fq -o bio-GM-CTCF-4_L4_G042 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-K27ac-2_L4_G005_trim_index_1.fq -f2 bio-GM-K27ac-2_L4_G005_trim_index_2.fq -o bio-GM-K27ac-2_L4_G005 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 bio-GM-K27ac-4_L4_G084_trim_index_1.fq -f2 bio-GM-K27ac-4_L4_G084_trim_index_2.fq -o bio-GM-K27ac-4_L4_G084 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-CTCF-2_L7_G007_trim_index_1.fq -f2 no-GM-CTCF-2_L7_G007_trim_index_2.fq -o no-GM-CTCF-2_L7_G007 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-CTCF-4_L7_G092_trim_index_1.fq -f2 no-GM-CTCF-4_L7_G092_trim_index_2.fq -o no-GM-CTCF-4_L7_G092 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-K27ac-2_L7_G028_trim_index_1.fq -f2 no-GM-K27ac-2_L7_G028_trim_index_2.fq -o no-GM-K27ac-2_L7_G028 -a CGCTCTTCCGATCT
python /mnt/hpc/home/xuxinran/code/microC/trim_read1N.py -f1 no-GM-K27ac-4_L7_G027_trim_index_1.fq -f2 no-GM-K27ac-4_L7_G027_trim_index_2.fq -o no-GM-K27ac-4_L7_G027 -a CGCTCTTCCGATCT

seqkit stat /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-2_L4_G029.R1.fastq.gz bio-GM-CTCF-2_L4_G029_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R1.fastq.gz bio-GM-CTCF-4_L4_G042_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R1.fastq.gz bio-GM-K27ac-2_L4_G005_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-4_L4_G084.R1.fastq.gz bio-GM-K27ac-4_L4_G084_trim_adapter_1.fq > bio-GM_seqkit.txt
seqkit stat /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R1.fastq.gz no-GM-CTCF-2_L7_G007_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-4_L7_G092.R1.fastq.gz no-GM-CTCF-4_L7_G092_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R1.fastq.gz no-GM-K27ac-2_L7_G028_trim_adapter_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-4_L7_G027.R1.fastq.gz no-GM-K27ac-4_L7_G027_trim_adapter_1.fq > no-GM_seqkit.txt

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-CTCF-2_L4_G029_trim_read1N_1.fq -2 ./clean_data/bio-GM-CTCF-2_L4_G029_trim_read1N_2.fq -p ./bio-GM-CTCF-2_L4_G029
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-CTCF-4_L4_G042_trim_read1N_1.fq -2 ./clean_data/bio-GM-CTCF-4_L4_G042_trim_read1N_2.fq -p ./bio-GM-CTCF-4_L4_G042
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-K27ac-2_L4_G005_trim_read1N_1.fq -2 ./clean_data/bio-GM-K27ac-2_L4_G005_trim_read1N_2.fq -p ./bio-GM-K27ac-2_L4_G005
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/bio-GM-K27ac-4_L4_G084_trim_read1N_1.fq -2 ./clean_data/bio-GM-K27ac-4_L4_G084_trim_read1N_1.fq -p ./bio-GM-K27ac-4_L4_G084
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-CTCF-2_L7_G007_trim_read1N_1.fq -2 ./clean_data/no-GM-CTCF-2_L7_G007_trim_read1N_2.fq -p ./no-GM-CTCF-2_L7_G007
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-CTCF-4_L7_G092_trim_read1N_1.fq -2 ./clean_data/no-GM-CTCF-4_L7_G092_trim_read1N_2.fq -p ./no-GM-CTCF-4_L7_G092
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-K27ac-2_L7_G028_trim_read1N_1.fq -2 ./clean_data/no-GM-K27ac-2_L7_G028_trim_read1N_2.fq -p ./no-GM-K27ac-2_L7_G028

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/no-GM-K27ac-4_L7_G027_trim_read1N_1.fq -2 ./clean_data/no-GM-K27ac-4_L7_G027_trim_read1N_2.fq -p ./no-GM-K27ac-4_L7_G027

## 饱和度
python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-CTCF-4_L4_G042.R2.fastq.gz -o bio-GM-CTCF-2_L4_G029

python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-bio-GM-MicroRUN/20240814_LH00524_0111_B22CFWYLT4/bio-GM-K27ac-2_L4_G005.R2.fastq.gz -o ./bio-GM-K27ac-2_L4_G005
python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-CTCF-2_L7_G007.R2.fastq.gz -o ./no-GM-CTCF-2_L7_G007
python /mnt/hpc/home/xuxinran/code/microC/microc-preseq.py -l 12 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-no-GM-MicroRUn/20240815_LH00308_0214_B22FCFCLT4/no-GM-K27ac-2_L7_G028.R2.fastq.gz -o ./no-GM-K27ac-2_L7_G028

```

**24-08-29 MicroCRUN**
```shell
# 去index
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-CTCF-8MCUT_L3_Q0060W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-CTCF-8MCUT_L3_Q0060W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-CTCF-8MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-1MCUT_L3_Q0056W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-1MCUT_L3_Q0056W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K4me3-1MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-4MCUT_L3_Q0058W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-4MCUT_L3_Q0058W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K4me3-4MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-10MCUT_L3_Q0061W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-10MCUT_L3_Q0061W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K4me3-10MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-2MCUT_L3_Q0057W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-2MCUT_L3_Q0057W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K27ac-2MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-6MCUT_L3_Q0059W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-6MCUT_L3_Q0059W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K27ac-6MCUT -i CTGTCTCTTATACACAT
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-10MCUT_L3_Q0062W0179.R1.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-10MCUT_L3_Q0062W0179.R2.fastq.gz -o /mnt/hpc/home/xuxinran/microC/date/date_0828/GM-H3K27ac-10MCUT -i CTGTCTCTTATACACAT

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-CTCF-8MCUT_trim_index_1.fq -2 ./clean_data/GM-CTCF-8MCUT_trim_index_2.fq -p ./GM-CTCF-8MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K27ac-10MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K27ac-10MCUT_trim_index_2.fq -p ./GM-H3K27ac-10MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K27ac-2MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K27ac-2MCUT_trim_index_2.fq -p ./GM-H3K27ac-2MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K27ac-6MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K27ac-6MCUT_trim_index_2.fq -p ./GM-H3K27ac-6MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K4me3-10MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K4me3-10MCUT_trim_index_2.fq -p ./GM-H3K4me3-10MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K4me3-1MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K4me3-1MCUT_trim_index_2.fq -p ./GM-H3K4me3-1MCUT --methods MicroRUN
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ./clean_data/GM-H3K4me3-4MCUT_trim_index_1.fq -2 ./clean_data/GM-H3K4me3-4MCUT_trim_index_2.fq -p ./GM-H3K4me3-4MCUT --methods MicroRUN

seqkit stat /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-CTCF-8MCUT_L3_Q0060W0179.R1.fastq.gz ./clean_data/GM-CTCF-8MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-1MCUT_L3_Q0056W0179.R1.fastq.gz ./clean_data/GM-H3K4me3-1MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-4MCUT_L3_Q0058W0179.R1.fastq.gz ./clean_data/GM-H3K4me3-4MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K4me3-10MCUT_L3_Q0061W0179.R1.fastq.gz ./clean_data/GM-H3K4me3-10MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-2MCUT_L3_Q0057W0179.R1.fastq.gz ./clean_data/GM-H3K27ac-2MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-6MCUT_L3_Q0059W0179.R1.fastq.gz ./clean_data/GM-H3K27ac-6MCUT_trim_index_1.fq /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-10MCUT_L3_Q0062W0179.R1.fastq.gz ./clean_data/GM-H3K27ac-10MCUT_trim_index_1.fq
```

**24-09-01**
```shell
# 一、rs3731239在microC的loop情况
## 


# 二、microRUN 和公共数据比较
## 1、下载数据
$prefetch -v SRR16356487 --max-size 50G # GSM5628869 HCT_GM12878_H3K27ac_Rep1
$prefetch -v SRR16356486 --max-size 50G # GSM5628870 HCT_GM12878_H3K27ac_Rep2
$prefetch -v SRR16356485 --max-size 50G # GSM5628871 HCT_GM12878_H3K27ac_Rep3
$prefetch -v SRR5831489 --max-size 50G # GSM2705041 GM HiChIP H3K27ac biological replicate 1
$prefetch -v SRR5831490 --max-size 50G # GSM2705042 GM HiChIP H3K27ac biological replicate 2
mv SRR16356487.sra HCT_GM12878_H3K27ac_Rep1.sra
mv SRR16356486.sra HCT_GM12878_H3K27ac_Rep2.sra
mv SRR16356485.sra HCT_GM12878_H3K27ac_Rep3.sra
mv SRR5831489.sra GM_HiChIP_H3K27ac_biological_replicate1.sra
mv SRR5831490.sra GM_HiChIP_H3K27ac_biological_replicate2.sra
fastq-dump --gzip --split-3 -O ./ HCT_GM12878_H3K27ac_Rep1.sra
fastq-dump --gzip --split-3 -O ./ HCT_GM12878_H3K27ac_Rep2.sra
fastq-dump --gzip --split-3 -O ./ HCT_GM12878_H3K27ac_Rep3.sra
fastq-dump --gzip --split-3 -O ./ GM_HiChIP_H3K27ac_biological_replicate1.sra
fastq-dump --gzip --split-3 -O ./ GM_HiChIP_H3K27ac_biological_replicate2.sra
cat HCT_GM12878_*_1.fastq.gz > HCT_GM12878_H3K27ac_1.fastq.gz
cat HCT_GM12878_*_2.fastq.gz > HCT_GM12878_H3K27ac_2.fastq.gz
cat GM_HiChIP_H3K27ac_biological_*_1.fastq.gz > GM_HiChIP_H3K27ac_biological_1.fastq.gz
cat GM_HiChIP_H3K27ac_biological_*_2.fastq.gz > GM_HiChIP_H3K27ac_biological_2.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-*.R1.fastq.gz > GM-H3K27ac.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240828_microCUT/GM-H3K27ac-*.R2.fastq.gz > GM-H3K27ac.R2.fastq.gz

## 2、去除index
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 GM-H3K27ac.R1.fastq.gz -f2 GM-H3K27ac.R2.fastq.gz -o ./GM-H3K27ac -i CTGTCTCTTATACACAT

## 3、QC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./GM_QC -t 100 -1 ./data/GM-H3K27ac_trim_index_1.fq -2 ./data/GM-H3K27ac_trim_index_2.fq -p ./GM_QC/GM-H3K27ac --methods MicroRUN --tmp
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./HCT_QC -t 100 -1 ./data/HCT_GM12878_H3K27ac_1.fastq.gz -2 ./data/HCT_GM12878_H3K27ac_2.fastq.gz -p ./HCT_QC/HCT_GM12878_H3K27ac --methods MicroRUN --tmp
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./HiChIP_QC -t 100 -1 ./data/GM_HiChIP_H3K27ac_biological_replicate2_1.fastq.gz -2 ./data/GM_HiChIP_H3K27ac_biological_replicate2_2.fastq.gz -p ./GM_HiChIP_H3K27ac_biological --methods MicroRUN

# fithichip
export PATH="/f/xinran/MicroC/HiC-Pro_3.1.0/bin/:$PATH"
bash /f/xinran/MicroC/HiChIP/FitHiChIP/FitHiChIP_HiCPro.sh -C /f/xinran/11111/GM_fithichip/config.txt
bash /f/xinran/MicroC/HiChIP/FitHiChIP/FitHiChIP_HiCPro.sh -C /f/xinran/11111/HCT_fithichip/config.txt
bash /f/xinran/MicroC/HiChIP/FitHiChIP/FitHiChIP_HiCPro.sh -C config.txt

# loop
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads 100 /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_mapped.pairs /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads 100 -r 5000,10000 --ignore-sparsity /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/GM_QC/GM-H3K27ac_hic.hiccups

java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads 100 /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_mapped.pairs /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads 100 -r 5000,10000 --ignore-sparsity /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_contact_map.hic /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HCT_QC/HCT_GM12878_H3K27ac_hic.hiccups

java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar pre --threads 100 /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_mapped.pairs /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_contact_map.hic /mnt/hpc/home/xuxinran/REF/hg19/hg19.chrom.sizes
java -Djava.awt.headless=true -jar /mnt/hpc/home/xuxinran/microC/Micro-C-main/juicertools.jar hiccups --cpu -f 0.1 --threads 100 -r 5000,10000 --ignore-sparsity /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_contact_map.hic /mnt/hpc/home/xuxinran/microC/date/date_0901/microRUN_analysis/HiChIP_QC/GM_HiChIP_H3K27ac_biological_hic.hiccups


```

**24-09-01** 合并所有的young和old的数据 call loop、loopQTL 查看一端是promoter一端SNP的loop/valid pair
```shell
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240311/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240522_pool_microC_microCUT/old-po-Micro-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240521_LH00524_0040_A223YVLLT4/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240607_LH00308_0156_B223VFVLT4/old-po-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240611_LH00524_0057_A2253NYLT4/old-po-microc-rep5_L3_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-Micro-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240828_LH00308_0228_B22FM25LT4/old-po-microc-32/old-po-microc-32_L6_G041.R1.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/old_merge.R1.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240311/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240522_pool_microC_microCUT/old-po-Micro-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240521_LH00524_0040_A223YVLLT4/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240607_LH00308_0156_B223VFVLT4/old-po-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240615_rep_poolingMicroC/20240611_LH00524_0057_A2253NYLT4/old-po-microc-rep5_L3_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-Micro-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-43/20240828_LH00308_0228_B22FM25LT4/old-po-microc-32/old-po-microc-32_L6_G041.R2.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/old_merge.R2.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240716_microrun_microc/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240824_LH00524_0120_A22FLW7LT4/young-po-Micro-C-3ada-12_L6_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/Micro-C-young-pool14_L1_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/young-po-MicroC-rep31_L1_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/Micro-C-young-pool15_L4_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-Micro*.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240829_LH00524_0125_A22FLV3LT4/young-po-MicroC-rep32/young-po-MicroC-rep32_L1_G026.R1.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/young_merge.R1.fastq.gz

cat /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240530_poolingMicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240716_microrun_microc/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240819_microRUN_microC/ABFC20240368-39-41/202408-young-old-pool-MicroC/20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240824_LH00524_0120_A22FLW7LT4/young-po-Micro-C-3ada-12_L6_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/Micro-C-young-pool14_L1_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/young-po-MicroC-rep31_L1_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/Micro-C-young-pool15_L4_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-Micro*.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_240903_microC/ABFC20240368-44/20240829_LH00524_0125_A22FLV3LT4/young-po-MicroC-rep32/young-po-MicroC-rep32_L1_G026.R2.fastq.gz > /mnt/hpc/home/xuxinran/microC/date/date_0903/data/young_merge.R2.fastq.gz
 
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./young_loop -t 100 -1 ./data/young_merge.R1.fastq.gz -2 ./data/young_merge.R2.fastq.gz -p ./young_loop/young_merge --methods loop
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./old_loop -t 100 -1 ./data/old_merge.R1.fastq.gz -2 ./data/old_merge.R2.fastq.gz -p ./old_loop/old_merge --methods loop
```

**24-10-10** valid pair和细胞数目
```shell
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_R1_001.fastq.gz > scMicro5-GM-Tn5-bead_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_R2_001.fastq.gz > scMicro5-GM-Tn5-bead_R2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_I1_001.fastq.gz > scMicro5-GM-Tn5-bead_I1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*Tn5*_I2_001.fastq.gz > scMicro5-GM-Tn5-bead_I2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_R1_001.fastq.gz > scMicro5-GM_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_R2_001.fastq.gz > scMicro5-GM_R2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_I1_001.fastq.gz > scMicro5-GM_I1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241010_scMicroC/ABFC20240368-56/20240930_LH00308_0255_A22H7H5LT4/*_I2_001.fastq.gz > scMicro5-GM_I2_001.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 scMicro5-GM_R1_001.fastq.gz -f2 scMicro5-GM_R2_001.fastq.gz -o ../clean_data/scMicro5-GM -i CTGTCTCTTATACACATCTCCGAG
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 scMicro5-GM-Tn5-bead_R1_001.fastq.gz -f2 scMicro5-GM-Tn5-bead_R2_001.fastq.gz -o ../clean_data/scMicro5-GM-Tn5-bead -i CTGTCTCTTATACACATCTCCGAG

seqkit stat *R1_001.fastq.gz
seqkit stat *_trim_index_1.fq

## valid pair
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./qc -t 100 -1 ./clean_data/scMicro5-GM-Tn5-bead_trim_index_1.fq -2 ./clean_data/scMicro5-GM-Tn5-bead_trim_index_2.fq -p ./qc/scMicro5-GM-Tn5-bead --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./qc -t 100 -1 ./clean_data/scMicro5-GM_trim_index_1.fq -2 ./clean_data/scMicro5-GM_trim_index_2.fq -p ./qc/scMicro5-GM --methods MicroC

## 细胞数
mv scMicro5-GM-Tn5-bead_R1_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_R1_001.fastq.gz
mv scMicro5-GM-Tn5-bead_I1_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_I1_001.fastq.gz
mv scMicro5-GM-Tn5-bead_R2_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_R3_001.fastq.gz
mv scMicro5-GM-Tn5-bead_I2_001.fastq.gz scMicro5-GM-Tn5-bead_S1_L001_R2_001.fastq.gz
mv scMicro5-GM_R1_001.fastq.gz scMicro5-GM_S1_L001_R1_001.fastq.gz
mv scMicro5-GM_I1_001.fastq.gz scMicro5-GM_S1_L001_I1_001.fastq.gz
mv scMicro5-GM_R2_001.fastq.gz scMicro5-GM_S1_L001_R3_001.fastq.gz
mv scMicro5-GM_I2_001.fastq.gz scMicro5-GM_S1_L001_R2_001.fastq.gz
bash 1.sh scMicro5-GM 1>scMicro5-GM.txt 2>&1
bash 2.sh scMicro5-GM-Tn5-bead 1>scMicro5-GM-Tn5-bead.txt 2>&1
```

**24-10-23**
```shell
# 去除index
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 SRR27586278_1.fastq.gz -f2 SRR27586278_3.fastq.gz -o ./deindex/SRR27586278 -i CTGTCTCTTATACACATCT
seqkit stat -j 20 SRR27586278_1.fastq.gz ./deindex/SRR27586278_trim_index_1.fq

flash SRR27586278_trim_index_1.fq  SRR27586278_trim_index_2.fq --min-overlap 10 --max-mismatch-density 0.25 -t 60 --output-prefix="SRR27586278" --output-directory="./flash"
fastqc ./flash/SRR27586278.extendedFrags.fastq -o ./fastqc -t 20

mv ../SRR27586278_1.fastq.gz SRR27586278_S1_L001_R1_001.fastq.gz
mv ../SRR27586278_2.fastq.gz SRR27586278_S1_L001_R2_001.fastq.gz
mv ../SRR27586278_3.fastq.gz SRR27586278_S1_L001_R3_001.fastq.gz

/mnt/hpc/home/xuxinran/softward/cellranger-atac-2.1.0/bin/cellranger-atac count --id=SRR27586278 --localcores=100 --reference=/mnt/hpc/home/xuxinran/REF/hg19/hg19-scATAC-reference-sources/hg19 --fastqs=. --sample=SRR27586278

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o . -t 110 -1 ./deindex/SRR27586278_trim_index_1.fq -2 ./deindex/SRR27586278_trim_index_2.fq -p ./qc/scMicro5-GM-Tn5-bead --methods MicroC

# 统计细胞数
python /mnt/hpc/home/xuxinran/code/microC/count_validPair_barcode.py -p /mnt/hpc/home/xuxinran/microC/date/date_1023/qc/scMicro5-GM-Tn5-bead_mapped.pairs -b /mnt/hpc/home/xuxinran/microC/date/date_1023/scdata/SRR27586278_S1_L001_R2_001.fastq.gz -o ./SRR27586278
umi_tools whitelist --stdin=SRR27586278_validpair.fastq --bc-pattern=CCCCCCCCCCCCCCCCCCCCCCCCNNNNNNNNNNNNNNNNNNNNNNNN --log2stderr > whitelist.txt
awk -F '\t' '{
    gsub(/,/, " ", $4)
    sum = $3
    n = split($4, arr, " ")
    for (i = 1; i <= n; i++) {
        sum += arr[i]
    }
    print $0, sum
}' OFS='\t' /mnt/hpc/home/xuxinran/microC/date/date_1023/whitelist.txt > /mnt/hpc/home/xuxinran/microC/date/date_1023/SRR27586278_barcode_read.txt
```

**24-10-28**
```shell
## 首先去掉polyA部分
python /mnt/hpc/home/xuxinran/microC/date/date_1028/trim1.py

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ScMicroC-GM12878-PolyA_trim_1.fq -2 ScMicroC-GM12878-PolyA_trim_2.fq -p ScMicroC-GM12878 --methods MicroC
cp /mnt/hpc/home/xuxinran/microC/data/xueqi_241028_scMicroC/ABFC20240368-75/20241024_LH00524_0172_B22H7GGLT4/ScMicroC-GM12878-PolyA_S9_L002_R1_001.fastq.gz ./
cp /mnt/hpc/home/xuxinran/microC/data/xueqi_241028_scMicroC/ABFC20240368-75/20241024_LH00524_0172_B22H7GGLT4/ScMicroC-GM12878-PolyA_S9_L002_I1_001.fastq.gz ScMicroC-GM12878-PolyA_S9_L002_R2_001.fastq.gz
cp /mnt/hpc/home/xuxinran/microC/data/xueqi_241028_scMicroC/ABFC20240368-75/20241024_LH00524_0172_B22H7GGLT4/ScMicroC-GM12878-PolyA_S9_L002_R2_001.fastq.gz ScMicroC-GM12878-PolyA_S9_L002_R3_001.fastq.gz
cp /mnt/hpc/home/xuxinran/microC/data/xueqi_241028_scMicroC/ABFC20240368-75/20241024_LH00524_0172_B22H7GGLT4/ScMicroC-GM12878-PolyA_S9_L002_I2_001.fastq.gz ScMicroC-GM12878-PolyA_S9_L002_I1_001.fastq.gz

pairtools split --nproc-in 50 --nproc-out 50 --output-pairs ScMicroC-GM12878_mapped.pairs --output-sam ScMicroC-GM12878_unsorted.bam ScMicroC-GM12878_dedup.pairsam

# 筛选出所有非valid pair的read，检查在chrom上的分布情况
/mnt/hpc/home/xuxinran/microC/date/date_1028/get_unvalidpair_bam.ipynb
samtools sort -o sorted_unvalidpair.bam unvalidpair.bam
samtools idxstats sorted_unvalidpair.bam > ScMicroC-GM12878_unvalidpair.txt
/mnt/hpc/home/xuxinran/microC/date/date_1028/chrom_coverage.ipynb

# 统计细胞数量
python /mnt/hpc/home/xuxinran/code/microC/count_validPair_barcode.py -p ScMicroC-GM12878_mapped.pairs -b ./sc/ScMicroC-GM12878-PolyA_S9_L002_R1_001.fastq.gz -o ./ScMicroC-GM12878 -b_n 16 -u_n 12
umi_tools whitelist --stdin=ScMicroC-GM12878_validpair.fastq --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNNNN --log2stderr --method reads --error-correct-threshold > whitelist.txt

awk -F '\t' '{
    gsub(/,/, " ", $4)
    sum = $3
    n = split($4, arr, " ")
    for (i = 1; i <= n; i++) {
        sum += arr[i]
    }
    print $0, sum
}' OFS='\t' /mnt/hpc/home/xuxinran/microC/date/date_1028/whitelist.txt > /mnt/hpc/home/xuxinran/microC/date/date_1028/ScMicroC-GM12878-PolyA_barcode_read.txt

```

**补23-11-07**
```shell
## 首先去掉polyA部分
cd /mnt/hpc/home/xuxinran/microC/date/date_1121
python /mnt/hpc/home/xuxinran/code/microC/trim_polyA.py

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 scMicroC-GM-1-polyA_trim_1.fq -2 scMicroC-GM-1-polyA_trim_2.fq -p scMicroC-GM-1-polyA --methods MicroC

# 统计细胞数量
python /mnt/hpc/home/xuxinran/code/microC/count_validPair_barcode.py -p scMicroC-GM-1-polyA_mapped.pairs -b End-3x-1_R2_001.fastq.gz -o ./End-3x-1
umi_tools whitelist --stdin=End-3x-1_validpair.fastq --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNNNNNNNNNNNNNNNN --log2stderr > whitelist.txt

awk -F '\t' '{
    gsub(/,/, " ", $4)
    sum = $3
    n = split($4, arr, " ")
    for (i = 1; i <= n; i++) {
        sum += arr[i]
    }
    print $0, sum
}' OFS='\t' /mnt/hpc/home/xuxinran/microC/date/date_1107/whitelist.txt > /mnt/hpc/home/xuxinran/microC/date/date_1107/End-3x-1_barcode_read.txt
```

**24-11-02**
```shell
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_241102_microC/ABFC20240368-61/20241011_LH00308_0260_A22H5NWLT4/GM12878-Micro-C/GM12878-Micro-C_L1_G042.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_241102_microC/ABFC20240368-61/20241011_LH00308_0260_A22H5NWLT4/GM12878-Micro-C/GM12878-Micro-C_L1_G042.R2.fastq.gz -p GM12878-Micro-C_L1 --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_241102_microC/ABFC20240368-61/20241013_LH00308_0262_B22H55JLT4/GM12878-Micro-C/GM12878-Micro-C_L7_G042.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_241102_microC/ABFC20240368-61/20241013_LH00308_0262_B22H55JLT4/GM12878-Micro-C/GM12878-Micro-C_L7_G042.R2.fastq.gz -p GM12878-Micro-C_L7 --methods MicroC
```


**24-11-21**
```shell
cd /mnt/hpc/home/xuxinran/microC/date/date_1107

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 End-3x-1_R1_001.fastq.gz -2 End-3x-1_R3_001.fastq.gz -p End-3x-1 --methods MicroC

# 统计细胞数量
python /mnt/hpc/home/xuxinran/code/microC/count_validPair_barcode.py -p scMicroC-GM-1-polyA_mapped.pairs -b /mnt/hpc/home/xuxinran/microC/data/xueqi_241121_scMicroC/ABFC20240368-94/20241117_LH00308_0291_A22JKFCLT4/scMicroC-GM-1-polyA_S8_L002_R1_001.fastq.gz -o scMicroC-GM-1-polyA -b_n 16 -u_n 12
umi_tools whitelist --stdin=scMicroC-GM-1-polyA_validpair.fastq --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNNNN --log2stderr --method reads > whitelist.txt

awk -F '\t' '{
    gsub(/,/, " ", $4)
    sum = $3
    n = split($4, arr, " ")
    for (i = 1; i <= n; i++) {
        sum += arr[i]
    }
    print $0, sum
}' OFS='\t' whitelist.txt > scMicroC-GM-1-polyA_barcode_read.txt

```

**27-11-27**
```shell
# GM-scMicroC-readN2N 普通
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/1_S9_L003_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/2_S10_L003_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/3_S11_L003_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/4_S12_L003_R1_001.fastq.gz > S12_L003_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/1_S9_L003_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/2_S10_L003_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/3_S11_L003_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-01/20241122_LH00708_0023_A22JJYKLT4/4_S12_L003_R2_001.fastq.gz > S12_L003_R2_001.fastq.gz
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -i CTGTCTCTTATACA -f1 S12_L003_R1_001.fastq.gz -f2 S12_L003_R2_001.fastq.gz -o ./S12_L003
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ../clean/S12_L003_trim_index_1.fq -2 ../clean/S12_L003_trim_index_2.fq -p S12_L003 --methods MicroC


# scMicroC-GM-2-400bpup GM-scMicroC-1-400bpup Young-po-scMicroC-polyA polyA
# 去掉polyAQC
python /mnt/hpc/home/xuxinran/code/microC/trim_polyA.py -i AGATCGGAAGAGCACAC -o ./Young-po-scMicroC-polyA -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-02/20241122_LH00708_0022_B22JFVHLT4/Young-po-scMicroC-polyA_S58_L003_R1_001.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-02/20241122_LH00708_0022_B22JFVHLT4/Young-po-scMicroC-polyA_S58_L003_R2_001.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/trim_polyA.py -i AGATCGGAAGAGCACAC -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-04/20241122_LH00708_0022_B22JFVHLT4/GM-scMicroC-1-400bpup_S55_L003_R1_001.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-04/20241122_LH00708_0022_B22JFVHLT4/GM-scMicroC-1-400bpup_S55_L003_R2_001.fastq.gz -o GM-scMicroC-1-400bpup

python /mnt/hpc/home/xuxinran/code/microC/trim_polyA.py -i AGATCGGAAGAGCACAC -f1 /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-04/20241122_LH00708_0022_B22JFVHLT4/scMicroC-GM-2-400bpup_S56_L003_R1_001.fastq.gz -f2 /mnt/hpc/home/xuxinran/microC/data/xueqi_241127_scMicroC/ABFC20241429-04/20241122_LH00708_0022_B22JFVHLT4/scMicroC-GM-2-400bpup_S56_L003_R2_001.fastq.gz -o scMicroC-GM-2-400bpup

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ../clean/GM-scMicroC-1-400bpup_trim_1.fq -2 ../clean/GM-scMicroC-1-400bpup_trim_2.fq -p GM-scMicroC-1-400bpup --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ../clean/scMicroC-GM-2-400bpup_trim_1.fq -2 ../clean/scMicroC-GM-2-400bpup_trim_2.fq -p scMicroC-GM-2-400bpup --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 ../clean/Young-po-scMicroC-polyA_trim_1.fq -2 ../clean/Young-po-scMicroC-polyA_trim_2.fq -p Young-po-scMicroC-polyA --methods MicroC

```

**27-12-14 HiC**
```shell
cd /mnt/hpc/home/xuxinran/microC/date/date_1213_hic_yxf

python /mnt/hpc/home/xuxinran/microC/HiC-Pro_3.1.0/bin/utils/digest_genome.py -r hindiii -o contig.HindIII.txt /mnt/hpc/home/xuxinran/REF/hg38/hg38.fa

/mnt/hpc/home/xuxinran/microC/HiC-Pro_3.1.0/bin/HiC-Pro --input /mnt/hpc/home/xuxinran/microC/date/date_1213_hic_yxf/data/ --output hicpro_output --conf config-hicpro.txt -s proc_hic

mkdir old_fithic_res yo_fithic_res

python /mnt/hpc/home/xuxinran/microC/HiC-Pro_3.1.0/bin/utils/hicpro2fithic.py -i ./hicpro_output/hic_results/matrix/HUVEC-Old/raw/20000/HUVEC-Old_20000.matrix -b ./hicpro_output/hic_results/matrix/HUVEC-Old/raw/20000/HUVEC-Old_20000_abs.bed -s ./hicpro_output/hic_results/matrix/HUVEC-Old/iced/20000/HUVEC-Old_20000_iced.matrix.biases -o ./fithic_res

python /mnt/hpc/home/xuxinran/microC/HiC-Pro_3.1.0/bin/utils/hicpro2fithic.py -i ./hicpro_output/hic_results/matrix/HUVEC-Young/raw/20000/HUVEC-Young_20000.matrix -b ./hicpro_output/hic_results/matrix/HUVEC-Young/raw/20000/HUVEC-Young_20000_abs.bed -s ./hicpro_output/hic_results/matrix/HUVEC-Young/iced/20000/HUVEC-Young_20000_iced.matrix.biases -o ./yo_fithic_res

cd old_fithic_res
zcat fithic.biases.gz | awk 'NF>=3'  > filtered.biases
gzip filtered.biases
fithic -f fithic.fragmentMappability.gz -i fithic.interactionCounts.gz -t filtered.biases.gz -o . -l HUVEC-Old -v -x All -r 20000

cd ../yo_fithic_res
zcat fithic.biases.gz | awk 'NF>=3'  > filtered.biases
gzip filtered.biases
fithic -f fithic.fragmentMappability.gz -i fithic.interactionCounts.gz -t filtered.biases.gz -o . -l HUVEC-Young -v -x All -r 20000

```


**24-12-14 合并所有old和young的pool HUVEC数据 call loop call loopqtl**
```shell
cd /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL
cat /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/13-old-po-Micro-C-rep6/13-old-po-Micro-C-rep6_S54_L002_R1_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/14-old-po-Micro-C-rep7/14-old-po-Micro-C-rep7_S55_L002_R1_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202211-young5G-old1G-poolmicroc/old-micro-po/old-micro-po_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202212-po-micro-yo-old-rep1-jiace/old-micro-po-jiace/old-micro-po_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202212-po-micro-yo-old-rep2-5G/old-po-MC-rep2/old-po-MC-rep2_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202301-po-micro-yo-old-rep2-jiace/2-old-po-MC-rep2/2-old-po-MC-rep2_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C17_L1_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C18_L1_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C19_L1_G044.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C20_L1_G051.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C21_L1_G092.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C22_L1_G007.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C16_L4_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C17_L3_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C18_L7_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C19_L3_G044.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C20_L3_G051.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C21_L3_G092.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C22_L3_G007.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-microc-31_L4_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-microc-32_L7_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-microc-rep5_L3_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240611_LH00524_0057_A2253NYLT4_2/old-po-microc-rep5_L3_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240617_LH00524_0061_A223V5VLT4_2/old-po-Micro-C17_L2_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240617_LH00524_0061_A223V5VLT4_2/old-po-Micro-C18_L2_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-31_L4_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-32_L6_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-51_L6_Q0181W0181.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-52_L4_Q0063W0181.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-16/20240310_LH00234_0100_B223CYWLT4/old-po-microc-rep5_L8_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-16/20240310_LH00234_0100_B223CYWLT4/old-po-microc-rep6_L3_G044.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240521_LH00524_0040_A223YVLLT4/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-Micro-C19_L1_G044.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-MicroC-rep33_L2_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-MicroC-rep34_L2_G032.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C16_L6_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C17_L4_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C18_L4_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C22_L4_G007.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-microc-31_L6_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-microc-32_L5_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-microc-rep5_L5_G060.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-rep33_L3_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-rep34_L3_G032.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/old-po-microc-32/old-po-microc-32_L6_G041.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old_20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-rep33_L2_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old_20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-rep34_L2_G032.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-20240517_LH00524_0038_A223VNVLT4/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345/20230810_AH3MCTDSX7_U1275_TJYKDXWXQ-20230810/old-pool-Micro-C/old-pool-Micro-C_S131_L001_R1_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345/20230812_AHHMCYDSX7_U1275_TJYKDXWXQ-20230812/old-po-Micro-C-rep4/old-po-Micro-C-rep4_S90_L002_R1_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345/20230812_AHHMCYDSX7_U1275_TJYKDXWXQ-20230812/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S91_L002_R1_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345-jiace/20230820_AH2FCYDSX7_U1275_TJYKDXWXQ-20230820/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S29_L001_R1_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345-jiace/20230820_AH2FCYDSX7_U1275_TJYKDXWXQ-20230820/old-pool-Micro-C/old-pool-Micro-C_S28_L001_R1_001.fastq.gz > old-pool-MicroC_R1_001.fastq.gz

cat /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/13-old-po-Micro-C-rep6/13-old-po-Micro-C-rep6_S54_L002_R2_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/14-old-po-Micro-C-rep7/14-old-po-Micro-C-rep7_S55_L002_R2_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202211-young5G-old1G-poolmicroc/old-micro-po/old-micro-po_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202212-po-micro-yo-old-rep1-jiace/old-micro-po-jiace/old-micro-po_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202212-po-micro-yo-old-rep2-5G/old-po-MC-rep2/old-po-MC-rep2_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202301-po-micro-yo-old-rep2-jiace/2-old-po-MC-rep2/2-old-po-MC-rep2_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C17_L1_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C18_L1_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C19_L1_G044.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C20_L1_G051.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C21_L1_G092.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202405-old-pool-MicroC/20240514_LH00308_0135_A223Y5HLT4/old-po-Micro-C22_L1_G007.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C16_L4_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C17_L3_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C18_L7_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C19_L3_G044.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C20_L3_G051.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C21_L3_G092.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-Micro-C22_L3_G007.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-microc-31_L4_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-microc-32_L7_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/old-po-microc-rep5_L3_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240611_LH00524_0057_A2253NYLT4_2/old-po-microc-rep5_L3_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240617_LH00524_0061_A223V5VLT4_2/old-po-Micro-C17_L2_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240617_LH00524_0061_A223V5VLT4_2/old-po-Micro-C18_L2_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-31_L4_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-32_L6_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-51_L6_Q0181W0181.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-15/20240307_LH00234_0098_B22HMKVLT3/old-po-microc-52_L4_Q0063W0181.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-16/20240310_LH00234_0100_B223CYWLT4/old-po-microc-rep5_L8_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240311-old-pool-Micro-C/LBFC20201487-16/20240310_LH00234_0100_B223CYWLT4/old-po-microc-rep6_L3_G044.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/20240521_LH00524_0040_A223YVLLT4/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-Micro-C19_L1_G044.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-MicroC-rep33_L2_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240823_LH00308_0222_A22FM35LT4/old-po-MicroC-rep34_L2_G032.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C16_L6_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C17_L4_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C18_L4_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-Micro-C22_L4_G007.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-microc-31_L6_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-microc-32_L5_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240825_LH00308_0224_B22F3CWLT3/old-po-microc-rep5_L5_G060.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-rep33_L3_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/20240827_LH00524_0122_A22FLWVLT4/old-po-MicroC-rep34_L3_G032.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/ABFC20240368-43/old-po-microc-32/old-po-microc-32_L6_G041.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old_20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-rep33_L2_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old_20240816_LH00524_0113_A22FCFFLT4/old-po-MicroC-rep34_L2_G032.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-20240517_LH00524_0038_A223VNVLT4/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345/20230810_AH3MCTDSX7_U1275_TJYKDXWXQ-20230810/old-pool-Micro-C/old-pool-Micro-C_S131_L001_R2_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345/20230812_AHHMCYDSX7_U1275_TJYKDXWXQ-20230812/old-po-Micro-C-rep4/old-po-Micro-C-rep4_S90_L002_R2_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345/20230812_AHHMCYDSX7_U1275_TJYKDXWXQ-20230812/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S91_L002_R2_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345-jiace/20230820_AH2FCYDSX7_U1275_TJYKDXWXQ-20230820/old-po-Micro-C-rep5/old-po-Micro-C-rep5_S29_L001_R2_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/old-pool-MicroC/old-pool-Micro-C-rep345-jiace/20230820_AH2FCYDSX7_U1275_TJYKDXWXQ-20230820/old-pool-Micro-C/old-pool-Micro-C_S28_L001_R2_001.fastq.gz > old-pool-MicroC_R2_001.fastq.gz

cat /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/12-y-po-Micro-C-rep4/12-y-po-Micro-C-rep4_S53_L002_R1_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202207-4-Micro-c-y-re1/4-Micro-c-y-re1/4-Micro-c-y-re1_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202209-2_young_Micro_c_rep1/2_young_Micro_c_rep1/2_young_Micro_c_rep1_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202211-young5G-old1G-poolmicroc/yo-micro-po_1/yo-micro-po_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202212-po-micro-yo-old-rep1-jiace/yo-micro-po-jiace/yo-micro-po_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202212-po-micro-yo-old-rep2-5G/yo-po-MC-rep2/yo-po-MC-rep2_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202301-po-micro-yo-old-rep2-jiace/1-yo-po-MC-rep2/1-yo-po-MC-rep2_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/20240607_LH00308_0156_B223VFVLT4/Micro-C-young-pool14_L4_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool14_L4_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool15_L4_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240723_LH00524_0089_A227VMVLT4/young-po-Micro-C-1ada-11_L8_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240723_LH00524_0089_A227VMVLT4/young-po-Micro-C-3ada-12_L8_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240726_LH00308_0195_A22CGLHLT4/young-po-Micro-C-1ada-11_L1_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240726_LH00308_0195_A22CGLHLT4/young-po-Micro-C-3ada-12_L4_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407-k562-stop-after/ABFC20240368-23/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-1ada-11_L3_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407-k562-stop-after/ABFC20240368-23/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-3ada-12_L3_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-pool14_L2_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-pool15_L2_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-pool14_L1_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-pool15_L1_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool14_L4_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool15_L4_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240824_LH00524_0120_A22FLW7LT4/young-po-Micro-C-3ada-12_L6_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/Micro-C-young-pool14_L1_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/young-po-MicroC-rep31_L1_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/Micro-C-young-pool15_L4_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-Micro-C-1ada-11_L4_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-MicroC-rep32_L4_G026.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240829_LH00524_0125_A22FLV3LT4/young-po-MicroC-rep32_L1_G026.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/y-po-Micro-c-rep3-cheapbio/y-po-Micro-c-rep3/y-po-Micro-c-rep3_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/y-po-Micro-c-rep3-cheapbio-jiace/y-po-Micro-c-rep3/y-po-Micro-c-rep3_1.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/young_20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-rep31_L2_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/young_20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-rep32_L2_G026.R1.fastq.gz > yo-pool-MicroC_R1_001.fastq.gz


cat /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/12-y-po-Micro-C-rep4/12-y-po-Micro-C-rep4_S53_L002_R2_001.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202207-4-Micro-c-y-re1/4-Micro-c-y-re1/4-Micro-c-y-re1_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202209-2_young_Micro_c_rep1/2_young_Micro_c_rep1/2_young_Micro_c_rep1_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202211-young5G-old1G-poolmicroc/yo-micro-po_1/yo-micro-po_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202212-po-micro-yo-old-rep1-jiace/yo-micro-po-jiace/yo-micro-po_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202212-po-micro-yo-old-rep2-5G/yo-po-MC-rep2/yo-po-MC-rep2_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202301-po-micro-yo-old-rep2-jiace/1-yo-po-MC-rep2/1-yo-po-MC-rep2_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/20240607_LH00308_0156_B223VFVLT4/Micro-C-young-pool14_L4_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool14_L4_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202406-pool-young-old-Micro-C-jiace_buce/ABFC20240368-09/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool15_L4_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240723_LH00524_0089_A227VMVLT4/young-po-Micro-C-1ada-11_L8_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240723_LH00524_0089_A227VMVLT4/young-po-Micro-C-3ada-12_L8_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240726_LH00308_0195_A22CGLHLT4/young-po-Micro-C-1ada-11_L1_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407_y_po_jiace/ABFC20240368-28/20240726_LH00308_0195_A22CGLHLT4/young-po-Micro-C-3ada-12_L4_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407-k562-stop-after/ABFC20240368-23/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-1ada-11_L3_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/202407-k562-stop-after/ABFC20240368-23/20240713_LH00524_0079_A227VLYLT4/young-po-Micro-C-3ada-12_L3_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-pool14_L2_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240517_LH00524_0038_A223VNVLT4/Micro-C-young-pool15_L2_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-pool14_L1_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240520_LH00308_0139_B223Y7CLT4/Micro-C-young-pool15_L1_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool14_L4_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/20240607_LH00308_0156_B223VFVLT4_2/Micro-C-young-pool15_L4_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240824_LH00524_0120_A22FLW7LT4/young-po-Micro-C-3ada-12_L6_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/Micro-C-young-pool14_L1_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0226_A22FM3TLT4/young-po-MicroC-rep31_L1_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/Micro-C-young-pool15_L4_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-Micro-C-1ada-11_L4_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240826_LH00308_0227_B22FLWFLT4/young-po-MicroC-rep32_L4_G026.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/ABFC20240368-44/20240829_LH00524_0125_A22FLV3LT4/young-po-MicroC-rep32_L1_G026.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/y-po-Micro-c-rep3-cheapbio/y-po-Micro-c-rep3/y-po-Micro-c-rep3_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/y-po-Micro-c-rep3-cheapbio-jiace/y-po-Micro-c-rep3/y-po-Micro-c-rep3_2.clean.fq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/young_20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-rep31_L2_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/wangxueqi/MicroC_pool_young_old/pool-Micro-C/young-pool-MicroC/young_20240816_LH00524_0113_A22FCFFLT4/young-po-MicroC-rep32_L2_G026.R2.fastq.gz > yo-pool-MicroC_R2_001.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 120 -1 old-pool-MicroC_R1_001.fastq.gz -2 old-pool-MicroC_R2_001.fastq.gz -p old-pool-MicroC --methods loop
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 120 -1 yo-pool-MicroC_R1_001.fastq.gz -2 yo-pool-MicroC_R2_001.fastq.gz -p yo-pool-MicroC --methods loop

sambamba sort -t 100 -o old-pool-MicroC.sorted.bam old-pool-MicroC_unsorted.bam
sambamba sort -t 100 -o yo-pool-MicroC.sorted.bam yo-pool-MicroC_unsorted.bam

bash old_qtl.sh
bash yo_qtl.sh
```

**25-01-07 Droplet Hi-C**
```shell
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250107_DropletHi-C/ABFC20241429-25/20250103_LH00524_0222_A22KGMLLT4/*R1_001.fastq.gz > A_L001_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250107_DropletHi-C/ABFC20241429-25/20250103_LH00524_0222_A22KGMLLT4/*R2_001.fastq.gz > A_L001_R2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250107_DropletHi-C/ABFC20241429-25/20250103_LH00524_0222_A22KGMLLT4/*I2_001.fastq.gz > A_L001_I2_001.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 A_L001_R1_001.fastq.gz -f2 A_L001_R2_001.fastq.gz -o A_L001 -i CTGTCTCTTATACACATCTCCGAG
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 A_L001_trim_index_1.fq -2 A_L001_trim_index_2.fq -p ./A --methods MicroC


python /mnt/hpc/home/xuxinran/code/microC/count_validPair_barcode.py -p A_mapped.pairs -b A_L001_I2_001.fastq.gz -o ./A
umi_tools whitelist --stdin=A_validpair.fastq --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNNNNNNNNNNNNNNNN --log2stderr > whitelist.txt
awk -F '\t' '{
    gsub(/,/, " ", $4)
    sum = $3
    n = split($4, arr, " ")
    for (i = 1; i <= n; i++) {
        sum += arr[i]
    }
    print $0, sum
}' OFS='\t' whitelist.txt > A_barcode_read.txt


fastqc -t 4 -o fastqc A_L001_trim_index_1.fq
```

**25-01-07 Droplet Hi-C**
```shell
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250114_DropletHi-C-rep/ABFC20241429-31/20250111_LH00708_0061_A22KGGLLT4/*R1_001.fastq.gz > A_L001_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250114_DropletHi-C-rep/ABFC20241429-31/20250111_LH00708_0061_A22KGGLLT4/*R2_001.fastq.gz > A_L001_R2_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250114_DropletHi-C-rep/ABFC20241429-31/20250111_LH00708_0061_A22KGGLLT4/*I2_001.fastq.gz > A_L001_I2_001.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 A_L001_R1_001.fastq.gz -f2 A_L001_R2_001.fastq.gz -o A_L001 -i CTGTCTCTTATACACATCTCCGAG -l 75
mkdir fastqc
fastqc -t 20 -o fastqc A_L001_trim_index_1.fq
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 100 -1 A_L001_trim_index_1.fq -2 A_L001_trim_index_2.fq -p ./A --methods MicroC

```


**25-01-07 merge pooling call loop and loopqtl;merge MCC**
```shell
## MCC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh_hg38.py -o ./ -t 100 -1 /mnt/hpc/home/xuxinran/microC/data/xueqi_250211_MCC_merge/MCC_po_merge.R1.fastq.gz -2 /mnt/hpc/home/xuxinran/microC/data/xueqi_250211_MCC_merge/MCC_po_merge.R2.fastq.gz -p ./MCC_po_merge --methods loop
bash MCC_po_merge_run.sh

## microC old
cat /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/old-pool-MicroC_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250116_LH00524_0231_A22KCWFLT4/old-po-Micro-C16/old-po-Micro-C16_L1_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250120_LH00308_0342_A22TCHWLT3/old-po-Micro-C16/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/old-po-Micro-C16/old-po-Micro-C16_L3_G048.R1.fastq.gz > old-po-Micro.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/old-pool-MicroC_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250116_LH00524_0231_A22KCWFLT4/old-po-Micro-C16/old-po-Micro-C16_L1_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250120_LH00308_0342_A22TCHWLT3/old-po-Micro-C16/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/old-po-Micro-C16/old-po-Micro-C16_L3_G048.R2.fastq.gz > old-po-Micro.R2.fastq.gz

## microC young
cat /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/yo-pool-MicroC_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L3_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L3_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0074_B22JWFMLT3/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L5_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250118_LH00524_0234_B22KF7CLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L2_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC6/y-po-MicroC6_L3_G042.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC7/y-po-MicroC7_L3_G028.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC21/y-po-MicroC21_L3_G092.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC22/y-po-MicroC22_L3_G007.R1.fastq.gz > yo-po-Micro.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/yo-pool-MicroC_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L3_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L3_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0074_B22JWFMLT3/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L5_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250118_LH00524_0234_B22KF7CLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L2_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC6/y-po-MicroC6_L3_G042.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC7/y-po-MicroC7_L3_G028.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC21/y-po-MicroC21_L3_G092.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC22/y-po-MicroC22_L3_G007.R2.fastq.gz > yo-po-Micro.R2.fastq.gz

## microC all
cat /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/old-pool-MicroC_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/yo-pool-MicroC_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250116_LH00524_0231_A22KCWFLT4/old-po-Micro-C16/old-po-Micro-C16_L1_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250120_LH00308_0342_A22TCHWLT3/old-po-Micro-C16/old-po-Micro-C16_L2_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L3_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L3_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0074_B22JWFMLT3/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/old-po-Micro-C16/old-po-Micro-C16_L3_G048.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L5_G001.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250118_LH00524_0234_B22KF7CLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L2_G025.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC6/y-po-MicroC6_L3_G042.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC7/y-po-MicroC7_L3_G028.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC21/y-po-MicroC21_L3_G092.R1.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC22/y-po-MicroC22_L3_G007.R1.fastq.gz > m-po-Micro.R1.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/old-pool-MicroC_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/date/date_1214_callQTL/yo-pool-MicroC_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250116_LH00524_0231_A22KCWFLT4/old-po-Micro-C16/old-po-Micro-C16_L1_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/20250120_LH00308_0342_A22TCHWLT3/old-po-Micro-C16/old-po-Micro-C16_L2_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L3_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250124_LH00524_0238_B22KJ7YLT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L3_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0073_A22K3MJLT3/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/ABFC20241429-41/20250127_LH00708_0074_B22JWFMLT3/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/old-po-Micro-C16/old-po-Micro-C16_L3_G048.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool14/Micro-C-young-pool14_L3_G084.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250114_LH00308_0337_B22KGL7LT4/Micro-C-young-pool15/Micro-C-young-pool15_L3_G005.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L5_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250115_LH00708_0065_A22KGN7LT4/young-po-Micro-C-3ada-12/young-po-Micro-C-3ada-12_L5_G001.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace3/ABFC20241429-33/20250118_LH00524_0234_B22KF7CLT4/young-po-Micro-C-1ada-11/young-po-Micro-C-1ada-11_L2_G025.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC6/y-po-MicroC6_L3_G042.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC7/y-po-MicroC7_L3_G028.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC21/y-po-MicroC21_L3_G092.R2.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250209_poolingmicroC_rep/date_250205_young_po_MicroC_jiace2/ABFC20241429-44/20250124_LH00524_0238_B22KJ7YLT4/y-po-MicroC22/y-po-MicroC22_L3_G007.R2.fastq.gz > m-po-Micro.R2.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh_hg38.py -o ./ -t 110 -1 old-po-Micro.R1.fastq.gz -2 old-po-Micro.R2.fastq.gz -p ./old-po-Micro --methods loop
bash old-po-Micro_run.sh

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh_hg38.py -o ./ -t 110 -1 yo-po-Micro.R1.fastq.gz -2 yo-po-Micro.R2.fastq.gz -p ./young-po-Micro --methods loop
bash young-po-Micro_run.sh

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh_hg38.py -o ./ -t 110 -1 m-po-Micro.R1.fastq.gz -2 m-po-Micro.R2.fastq.gz -p ./merge-po-Micro --methods loop
bash merge-po-Micro_run.sh

```

**250224 单细胞microC QC和刘超QC**
```shell
## scMicroC
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250224_scMicroC/ABFC20241429-57/20250219_LH00708_0085_B22KFHHLT4/scMicroC-GM-250209-1_S29_L001_R1_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250224_scMicroC/ABFC20241429-57/20250219_LH00708_0085_B22KFHHLT4/scMicroC-GM-250209-2_S30_L001_R1_001.fastq.gz > scMicroC-GM_R1_001.fastq.gz
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250224_scMicroC/ABFC20241429-57/20250219_LH00708_0085_B22KFHHLT4/scMicroC-GM-250209-1_S29_L001_R2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250224_scMicroC/ABFC20241429-57/20250219_LH00708_0085_B22KFHHLT4/scMicroC-GM-250209-2_S30_L001_R2_001.fastq.gz > scMicroC-GM_R2_001.fastq.gz

python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 scMicroC-GM_R1_001.fastq.gz -f2 scMicroC-GM_R2_001.fastq.gz -o scMicroC-GM -i AGATCGGAAGAGCACACGTCTGAA

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 110 -1 scMicroC-GM_trim_index_1.fq -2 scMicroC-GM_trim_index_2.fq -p scMicroC-GM --methods MicroC
cat /mnt/hpc/home/xuxinran/microC/data/xueqi_250224_scMicroC/ABFC20241429-57/20250219_LH00708_0085_B22KFHHLT4/scMicroC-GM-250209-1_S29_L001_I2_001.fastq.gz /mnt/hpc/home/xuxinran/microC/data/xueqi_250224_scMicroC/ABFC20241429-57/20250219_LH00708_0085_B22KFHHLT4/scMicroC-GM-250209-2_S30_L001_I2_001.fastq.gz > scMicroC-GM_I2_001.fastq.gz
python /mnt/hpc/home/xuxinran/code/microC/count_validPair_barcode.py -p scMicroC-GM_mapped.pairs -b scMicroC-GM_I2_001.fastq.gz -o ./scMicroC-GM
umi_tools whitelist --stdin=scMicroC-GM_validpair.fastq --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNNNNNNNNNNNNNNNN --log2stderr > whitelist.txt
awk -F '\t' '{
    gsub(/,/, " ", $4)
    sum = $3
    n = split($4, arr, " ")
    for (i = 1; i <= n; i++) {
        sum += arr[i]
    }
    print $0, sum
}' OFS='\t' whitelist.txt > scMicroC-GM_read.txt

## 空间HiC用microC方法质控
python /mnt/hpc/home/xuxinran/microC/date/date_0224_hic/trim.py -f1 /mnt/hpc/home/xuxinran/microC/date/date_0224_hic/ANNO_XS01KF2024010377_PM-XS01KF2024010377-60/Rawdata/THICS/THICS_R1.fq.gz -f2 /mnt/hpc/home/xuxinran/microC/date/date_0224_hic/ANNO_XS01KF2024010377_PM-XS01KF2024010377-60/Rawdata/THICS/THICS_R2.fq.gz -o THICS
python /mnt/hpc/home/xuxinran/microC/date/date_0224_hic/trim.py -f1 /mnt/hpc/home/xuxinran/microC/date/date_0224_hic/ANNO_XS01KF2024010377_PM-XS01KF2024010377-60/Rawdata/TNCS/TNCS_R1.fq.gz -f2 /mnt/hpc/home/xuxinran/microC/date/date_0224_hic/ANNO_XS01KF2024010377_PM-XS01KF2024010377-60/Rawdata/TNCS/TNCS_R2.fq.gz -o TNCS

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 110 -1 THICS_trim_1.fq -2 THICS_trim_2.fq -p THICS --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 110 -1 TNCS_trim_1.fq -2 TNCS_trim_2.fq -p TNCS --methods MicroC

flash THICS_trim_1.fq THICS_trim_2.fq --min-overlap 7 --max-mismatch-density 0.25 -t 60 --output-prefix="THICS" --output-directory="./flash"

flash TNCS_trim_1.fq TNCS_trim_2.fq --min-overlap 7 --max-mismatch-density 0.25 -t 60 --output-prefix="TNCS" --output-directory="./flash"
```

**250226 scMicroC**
```shell
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 GM-2-scM-300up-250211_R1_001.fastq.gz -f2 GM-2-scM-300up-250211_R2_001.fastq.gz -o GM-2-scM-300up-250211 -i AGATCGGAAGAGCACACGTCTGAA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 GM-2-scMicroC-250210_R1_001.fastq.gz -f2 GM-2-scMicroC-250210_R2_001.fastq.gz -o GM-2-scMicroC-250210 -i AGATCGGAAGAGCACACGTCTGAA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 scM-GM-300bp-250211_R1_001.fastq.gz -f2 scM-GM-300bp-250211_R2_001.fastq.gz -o scM-GM-300bp-250211 -i AGATCGGAAGAGCACACGTCTGAA
python /mnt/hpc/home/xuxinran/code/microC/trim_index.py -f1 scMicroC-GM-250209_R1_001.fastq.gz -f2 scMicroC-GM-250209_R2_001.fastq.gz -o scMicroC-GM-250209 -i AGATCGGAAGAGCACACGTCTGAA

python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 110 -1 GM-2-scM-300up-250211_trim_index_1.fq -2 GM-2-scM-300up-250211_trim_index_2.fq -p GM-2-scM-300up-250211 --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 110 -1 GM-2-scMicroC-250210_trim_index_1.fq -2 GM-2-scMicroC-250210_trim_index_2.fq -p GM-2-scMicroC-250210 --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 110 -1 scM-GM-300bp-250211_trim_index_1.fq -2 scM-GM-300bp-250211_trim_index_2.fq -p scM-GM-300bp-250211 --methods MicroC
python /mnt/hpc/home/xuxinran/code/microC/print_QCsh.py -o ./ -t 110 -1 scMicroC-GM-250209_trim_index_1.fq -2 scMicroC-GM-250209_trim_index_2.fq -p scMicroC-GM-250209 --methods MicroC


```