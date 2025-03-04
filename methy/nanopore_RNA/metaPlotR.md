```shell
##下载
# 下载参考基因组
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz
tar -zxvf /f/xinran/REF/hg19/chromFa.tar.gz
# 下载扩展基因预测表
# 下载Bio::Perl
mamba install bioconda::perl-bioperl
mamba install bioconda::perl-app-cpanminus
find ~/mambaforge/* -name "Seq.pm"
export PERL5LIB=/f/xinran/mambaforge/pkgs/perl-bioperl-core-1.7.8-pl5321hdfd78af_1/lib/perl5/site_perl:$PERL5LIB
conda activate bioperl
conda install bioconda::bedtools
cpan Bio::Perl

##数据预处理
# 1、make_annot_bed.pl为转录组中的每个核苷酸创建主注释文件
perl /f/xinran/methy/M6A/metaPlotR/make_annot_bed.pl --genomeDir /f/xinran/REF/hg19/chroms_fa --genePred /f/xinran/methy/M6A/metaPlotR/ref/hg19_gencode_v19.genePred > hg19_annot.bed

# 2、使用sort命令对主注释文件进行排序：
sort -k1,1 -k2,2n hg19_annot.bed > hg19_annot.sorted.bed

# 3、size_of_cds_utrs.pl创建一个文件，对转录区域的开始和结束位置的转录组坐标进行编目（即5'UTR，CDS和3'UTR）。它以排序的主注释文件为输入（hg19_annot.sorted.bed），并输出一个区域注释文件。区域注释文件是确定查询位点与转录组特征（即转录起始位点、开始密码子、停止密码子和转录端）的距离所必需的。
perl /f/xinran/methy/M6A/metaPlotR/size_of_cds_utrs.pl --annot hg19_annot.sorted.bed > region_sizes.txt

# 4、annotate_bed_file.pl注释了用户提供的BED文件，其中包含相关地点的单核苷酸基因组坐标。它充当Bedtools Intersect的包装器，本质上用主注释文件（hg19_annot.sorted.bed）中的匹配行（即相同的坐标）标记用户提供的BED文件中的每一行。输出的文件称为注释查询文件。
perl /f/xinran/methy/M6A/metaPlotR/annotate_bed_file.pl --bed metaplotR.bed --bed2 /f/xinran/methy/M6A/metaPlotR/ref/hg19_annot.sorted.bed > annot.sorted.bed


# 5、rel_and_abs_dist_calc.pl标识用户提供的站点所在的转录区域，并将转录组坐标转换为元基因坐标。也就是说，发生在5'UTR中的站点的值从0到1，其中0和1分别代表5'UTR的5'和3'末端。同样，CDS中的站点的值从1到2，3'UTR从2到3。该脚本将注释查询fileannot_miclip.cims.bed和区域注释文件utr_cds_ends.txt作为输入。输出的距离测量文件包含绘制元基因所需的所有值。
perl /f/xinran/methy/M6A/metaPlotR/rel_and_abs_dist_calc.pl --bed annot.sorted.bed --regions /f/xinran/methy/M6A/metaPlotR/ref/region_sizes.txt > o.dist.measures.txt

Rscript /f/xinran/methy/M6A/metaPlotR/metaPlot.R --dist o.dist.measures.txt --name old --od ./
```



```shell
sort -k1,1 -k2,2n m5C.bed > nano_merge_m5C_all_metaPlotR.sorted.bed

perl /f/xinran/methy/M6A/metaPlotR/annotate_bed_file.pl --bed nano_merge_m5C_all_metaPlotR.sorted.bed --bed2 /f/xinran/methy/M6A/metaPlotR/ref/hg19_annot.sorted.bed > annot_m5C_all.bed

perl /f/xinran/methy/M6A/metaPlotR/rel_and_abs_dist_calc.pl --bed annot_m5C_all.bed --regions /f/xinran/methy/M6A/metaPlotR/ref/region_sizes.txt > nano_merge_m5C.dist.measures.all.txt

Rscript /f/xinran/methy/M6A/metaPlotR/metaPlot.R --dist nano_merge_m5C.dist.measures.all.txt --name m5C  --od ./
```