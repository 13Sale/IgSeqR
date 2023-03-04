def main():
    # argparse
    #  --input1, -i, -b, -fq, -R1
    #  --input2, -R2
    #  --out -o default: ./IgSeqR
    #  --cores -c default: os command (lookup)
    #  --unpaired, -u default: False
    #  --hisatRef, -x
    #  --igRef, -ir default: Generate
    #  --igChain, -ig default: Both
    #  --Verbosity, -v defualt: Warning

    # logging


    # process inputs:
    # - bam2fastq if needed
    # - hisat
    
    # 

def processInputs(cores, i1, i2, ref, sample, unpaired, out):
    if not os.path.exists(ref):
        print(f"Error: HISAT Reference file '{ref}' does not exist.")
        exit(1)

    if not os.path.exists(i1):
        print(f"Error: Input file '{i1}' does not exist.")
        exit(1)

    if not unpaired and i2 is not None:
        if '.fastq' not in i1 and '.fq' not in i1:
            print(f"Error: Input file '{i1}' does not contain a FASTQ file.")
            exit(1)

        if '.fastq' not in i2 and '.fq' not in i2:
            print(f"Error: Input file '{i2}' does not contain a FASTQ file.")
            exit(1)

        print("Paired-end FASTQ Provided...")
        hisatAlign(unpaired=unpaired, input1=i1, input2=i2, ref=ref, cores=cores)
    else:
        if '.bam' in i1:
            if not unpaired:
                print ("Paired-end BAM Provided...")
                bamToFastq(unpaired=unpaired, bam=i1, sample=sample, cores=cores, stage="raw")
                hisatAlign(unpaired=unpaired, input1=f"{out}FASTQ/_read1.raw.fastq.gz", input2=f"{out}FASTQ/{sample}_read1.raw.fastq.gz", ref=ref, cores=cores)
            else:
                print("Unpaired BAM Provided...")
                bamToFastq(unpaired=unpaired, bam=i1, sample=sample, cores=cores, stage="raw")
                hisatAlign(unpaired=unpaired, input1=f"./IgSeqR/FASTQ/{sample}.raw.fastq.gz", input2="", ref=ref, cores=cores)
        elif '.fastq' in i1 or '.fq' in i1:
            if unpaired:
                print("Unpaired FASTQ Provided...")
                hisatAlign(unpaired=unpaired, input1=i1, input2="", ref=ref, cores=cores)
            else:
                print("Error: Single input file '{i1}' does not contain a BAM file, for unpaired FASTQ analysis please use -U argument.")
                exit(1)
        else:
            print(f"Error: Input file '{i1}' does not contain an unpaired BAM or FASTQ file.")
            exit(1)

def bamToFastq(unpaired, bam, sample, cores, stage, out): 
    print("\n" + '{:=^100}'.format(' Converting BAM to FASTQ '))
    if stage == "raw":
        outDir = f"{out}FASTQ"
    else:
        outDir = f"{out}IG_READS"        

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    cmd = ("samtools", "fastq",
           "-@", cores, 
           "-N", 
           "-c", "6", 
           bam)

    if unpaired is False:
        cmd += ("-1", f"{outDir}/{sample}_read1.{stage}.fastq.gz", 
                "-2", f"{outDir}/{sample}_read2.{stage}.fastq.gz",
                "-0", f"{outDir}/{sample}_singleton.{stage}.fastq.gz")
    else: 
        cmd += ("-1", f"{outDir}/{sample}_read1.{stage}.fastq.gz")

    subprocess.check_call(cmd)


    # for hisat - example to call shell script 
    script_dir = os.path.dirname(os.path.abspath(__file__))
shell_script_path = os.path.join(script_dir, 'your_script.sh')
subprocess.run(['bash', shell_script_path])

if __name__ == __main__: 
    main()