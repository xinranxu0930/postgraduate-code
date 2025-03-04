import pandas as pd
import mappy as mp
import argparse
import random


def generate_unique_umi(existing_umis,length=24):
    # max read num:281474976710656
    # 生成一个新的UMI
    bases = ['A', 'T', 'C', 'G']
    while True:
        umi = ''.join(random.choice(bases) for _ in range(length))
        if umi not in existing_umis:
            existing_umis.add(umi)
            return umi, existing_umis

def generate_quality_scores(length=24):
    # 生成对应长度的高质量值，每个碱基的 Phred 质量分数在 30 到 40 之间
    quality_scores = ''.join(chr(random.randint(63, 73)) for _ in range(length))
    return quality_scores

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check scMicroC cell count")
    parser.add_argument("-p", "--pairs", type=str, required=True, help="mapped.pairs file path")
    parser.add_argument("-b", "--barcode", type=str, required=True, help="barcode fastq file path")
    parser.add_argument("-o", "--output", type=str, help="output and pre path")
    parser.add_argument("-b_n", "--barcode_num", type=int, default=0, help="split N bp barcode in fastq")
    parser.add_argument("-u_n", "--umi_num", type=int, default=0, help="split N bp UMI in fastq")
    args = parser.parse_args()

    res_fastq = open(f"{args.output}_validpair.fastq", "w")
    num = args.barcode_num + args.umi_num

    valid_pair_readID_set = set(pd.read_csv(args.pairs, usecols=[0], names=['readID'], comment="#", sep="\t")['readID'])
    existing_umis = set()
    for read in mp.fastx_read(args.barcode, read_comment=True):
        read_name, comment = read[0], read[-1][1:]
        seq, qual = read[1], read[2]

        if read_name in valid_pair_readID_set:
            if num == 0:
                umi, existing_umis = generate_unique_umi(existing_umis)
                seq = seq + umi
                qual = qual + generate_quality_scores()
                res_fastq.write(f"@{read_name} 1{comment}\n{seq}\n+\n{qual}\n")
            else:
                res_fastq.write(f"@{read_name} 1{comment}\n{seq[:num]}\n+\n{qual[:num]}\n")

    res_fastq.close()