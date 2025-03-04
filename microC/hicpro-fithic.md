[GitHub - ay-lab/fithic: Fit-Hi-C is a tool for assigning statistical confidence estimates to chromosomal contact maps produced by genome-wide genome architecture assays such as Hi-C.](https://github.com/ay-lab/fithic)

## 安装

```Shell
mamba install -c bioconda fithic
mamba install -c bioconda samtools
mamba install -c conda-forge r-rcolorbrewer
mamba install -c conda-forge r-ggplot2
mamba install -c bioconda pysam
mamba install -c bioconda bowtie2
mamba install -c bioconda bx-python
mamba install -c conda-forge numpy
mamba install -c bioconda iced

## 安装HiC-Pro
git clone https://github.com/nservant/HiC-Pro.git

#修改config-install.txt

make configure
make install

```

## HiC-Pro

```Shell
cd /f/xinran/MicroC/fithic_call_loop/mcc_230327_230616

cp /f/xinran/MicroC/HiC-Pro_3.1.0/config-hicpro.txt
#修改config文件
/f/xinran/MicroC/HiC-Pro_3.1.0/bin/HiC-Pro -i /f/xinran/MicroC/fithic_call_loop/mcc_230327_230616/data/ -o ./hicpro_output -c /f/xinran/MicroC/fithic_call_loop/mcc_230327_230616/config-hicpro.txt
#这里要注意数据存放的文件夹，数据位于/h/xinran/call_loop/mcc_230327_230616/data/1-yo-po-mcc-merge/，但是这里要写/h/xinran/call_loop/mcc_230327_230616/data/
```

结果：

[HiC-Pro的使用 ｜ HiC辅助基因组组装（一）_hicpro结果invalid pairs_生信技术的博客-CSDN博客](https://blog.csdn.net/m0_49960764/article/details/118887684)

bowtie_results目录下共有三个文件夹：

- bwt2：存放合并后的bam文件和统计结果；

- bwt2_global：存放全局比对结果；

- bwt2_local：存放局部比对结果；

hic_results/data：存放valid pair reads及其他无效数据文件；

- allVaildPairs:合并后的Valid pairs数据

- DEPairs:Dangling end pairs数据

- DumpPairs:实际片段长度和理论片段长度不同的数据

- REPairs：酶切片段重新连接的pairs

- FiltePairs:基于min/max insert/fragment size过滤的pairs，MAPQ过低的pairs；

- SCPairs：片段自连的pairs

hic_results/matrix：存放不同分辨率矩阵文件；

- matrix:存放不同分辨率矩阵文件, 分为raw和iced文件，

- raw: 初始的关联矩阵iced:ice校正后的矩阵,供后续分析使用。

hic_results/pic：存放统计分析图片；

- plotHiCContactRanges_Example1.pdf有效互作中各类型比例图；

- plotHiCFragmentSize_Example1.pdf有效互作的片段大小分布图；

- plotMappingPairing_Example1.pd合并后双端比对过滤结果图；

hic_results/stats：存放统计表；

- LZ-3-15-1_allValidPairs.mergestat

    这个文件主要记录的是valid pairs中去除PCR duplication后，trans比对(比对到reference中不同序列)和cis比对(比对到reference中同一条序列)的情况。

    其中valid_interaction与xx.mRSstat文件中一致；valid_interaction_rmdup表示去除PCR duplication后的valid interaction。

    Valid interaction rmdup = Trans interaction + Cis interaction

- LZ-3-15-1.mpairstat

    这个文件主要记录的是reads对的情况，包括

    两端均未比对上的reads pair（Unmapped_pairs）：3980707 16.746

    只有一端比对上的reads pair(Pairs_with_singleton)：7666170 32.249

    低质量的reads pair（Low_qual_pairs）：0 0.0

    唯一比对reads pair(Unique_paired_alignments)：4945079 20.803

    Unique paired alignments用于后续分析

- LZ-3-15-1.mRSstat

    这个文件主要记录的是过滤掉的invalid Hi-C products，包括Dangling end pairs、Religation pairs、Self Cycle pairs、Dumped pairs等

- LZ-3-15-1_R1.mmapstat和LZ-3-15-1_R2.mmapstat

    它们记录了PE reads分开比对的结果。

    以R1.mmapstat文件为例：

    total_R1是总的R1 reads；

    mapped_R1有由两个部分组成，分别为：

    第一步 (HiCPro称为global alignment)比对上的reads pair(即global_R1)，

    第二步比对(HiCPro称为local alignment)比对上的reads对(即local_R1)。

    具体关系如下：

    Total reads = Unmapped pairs + Pairs with singleton + Low qual pairs + Unique paired alignments

```Shell
mkdir ./fithic_res/

python /f/xinran/MicroC/HiC-Pro_3.1.0/bin/utils/hicpro2fithic.py -i ./hicpro_output/hic_results/matrix/1-yo-po-mcc-merge/raw/20000/1-yo-po-mcc-merge_20000.matrix -b ./hicpro_output/hic_results/matrix/1-yo-po-mcc-merge/raw/20000/1-yo-po-mcc-merge_20000_abs.bed -s /f/xinran/MicroC/fithic_call_loop/mcc_230327_230616/hicpro_output/hic_results/matrix/1-yo-po-mcc-merge/iced/20000/1-yo-po-mcc-merge_20000_iced.matrix.biases -o ./fithic_res
```

## FitHiC
[hicpro脚本](https://www.jianshu.com/p/c69da38b39a3)

[使用FitHiC评估染色质交互作用的显著性-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/1557256)

```Shell
cd /f/xinran/MicroC/fithic_call_loop/mcc_230327_230616/fithic_res

zcat fithic.biases.gz | awk 'NF>=3'  > filtered.biases
gzip filtered.biases

fithic -f fithic.fragmentMappability.gz -i fithic.interactionCounts.gz -t filtered.biases.gz -o . -l 1-yo-po-mcc-merge -v -x intraOnly -r 20000
```

其中`zcat fithic.biases.gz | awk 'NF>=3'  > filtered.biases`的作用是将`fithic.biases.gz`中的空行去掉




