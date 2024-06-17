
# rsRNAfinder
rsRNAfinder identifies and annotates ribosomal RNA-derived small RNAs (rsRNAs), categorizing them into three series: rRF-5, rRF-3, and rRF-i. It provides comprehensive information of identifed rsRNAs including rsRNA category, expression, size, and parent rRNA details (such as locus and strand). Implemented using Python and Bash, rsRNAfinder utilizes the snakemake workflow management system. The source code can be found at [https://github.com/rebminso/rsRNAfinder.git](https://github.com/rebminso/rsRNAfinder.git) and is open source and compatible with multiple platforms. Installation instructions are provided below.

![workflow_rrf](https://github.com/rebminso/rsRNAfinder/assets/85422585/7a0c61f5-b5b4-4266-8cac-4480aa7b2e9d)


### Depth indented listing of files
```bash this
rsRNA/
├── config
│   ├── config.yaml
│   ├── environment.yml
├── data
│   ├── Feature_table
│   ├── Genome
│   ├── store
│   │   └── rRNA_AT.bed
│   └── trimmed
│       └── test
│           └── test_trimmed.fq
├── myscript
│   ├── build_genome_file.py
│   ├── csv_to_html.py
│   ├── filtered_sam.py
│   ├── filter_rrf_identifier.py
│   ├── pyplot.py
│   ├── rnafold2.py
│   ├── rnafold.py
│   ├── rrf_identifier.py
│   └── rRNA_stat.py
├── rules
│   ├── classification.smk
│   ├── default_smk
│   │   ├── alignment_default.smk
│   │   └── artificial_genome_default.smk
│   └── User_defined
│       ├── alignment.smk
│       └── artificial_genome.smk
└── snakefile
```
## USAGE of rsRNA
### 1. Deploy workflow

The repository can be downloaded with all the additional dependencies handled by snakemake, provided that snakemake is fully installed and available.

```bash
    git clone https://github.com/rebminso/rsRNAfinder.git
    cd rsRNAfinder
```
The repository has a primary directory named &quot;rsRNAfinder&quot; with several
subfolders. The important files are named “data” and “config.” The config file is the configuration file that is modified to configure the workflow as per the needs, whereas the data file allows you to load your input data.

### 2. Install Snakemake
Snakemake can best be installed through the [Mamba package manager](https://github.com/mamba-org/mamba). The latest version of snakemake==7.20.0 is required to run the workflow. The installation instructions for snakemake can be found in their [documentation](https://snakemake.readthedocs.io/en/stable/), but briefly, if conda and mamba are already installed, snakemake can be installed with the following command:

```bash
    conda activate base
    conda env create -f config/environment.yml
    conda activate rsRNA
```
OR

Manually install the following dependencies to create an environment and load packages through the command line as shown below:
```bash
    conda activate base
    conda create -n rsRNA python=3.7 --no-default-packages
    conda activate rsRNA
    pip install snakemake==7.20.0
    conda install -c bioconda bedtools
    pip install seaborn
    conda install -c conda-forge matplotlib
    conda install -c bioconda segemehl==0.2.0 
    conda install -c bioconda samtools
    conda install -c conda-forge biopython
    conda install -c bioconda viennarna

```


### 3. Configure workflow
The configuration of the workflow can be altered by modifying the `config/config.yaml` file, following the explainations provided in the file. 	

1. If Arabidopsis thaliana is to be used as the reference genome, no alteration in the config file will be required. 
 	
- A folder containing trimmed FASTQ files can be added to the `data/trimmed/` directory, with the input fastq filename required to be in the format of {xyz}_trimmed.fq, such as `SRR2354321_trimmed.fq`. The `Search strategy` in the config file is to be set to `Default`. 

Flank length, minimum and maximum rRFs sequence length, maximum number of mismatches in the alignment, and maximum RPM threshold for rRFs can be changed according to requirements in the config file. 

2. If a different genome is desired, the config file will need to be modified.

- A folder containing trimmed FASTQ files is to be added to the `data/trimmed/` directory.
- It should be noted that the input fastq file format must be in the {xyz}_trimmed.fq format, for example, `SRR2354321_trimmed.fq`.
- The FASTA sequence of the desired reference genome is to be added to `data/Genome/`.
- The genome feature table in .txt format is to be added to `data/Feature_table/`.

It should be noted that the feature table and reference genome must be from NCBI. Once all three types of files are added to their respective directories, the changes in the `config/config.yaml` file must be performed, with the setting specified.
- Search strategy: `Host`
- genome_fasta: `path/of/genome/file`
- species_NCBI_feature_table: `path/of/NCBI/feature/table/ofthe/genome/ofinterest`

Further changes to the flank length, minimum and maximum rRFs sequence length, the maximum number of mismatches in the alignment, and the maximum RPM threshold for rRFs can be made in the config file as required. Please ensure that the headers in the genome file are correctly formatted. Specifically, each fasta header for genomic sequences should begin with >chr[Num]. Meanwhile, headers for mitochondrial and plastid sequences should be written as 'chrMt' and 'chrPt,' respectively.

### 4. Run workflow
The workflow can be executed after proper configuration and deployment, with the current working directory set to `~./rsRNAfinder/`. To run, the following command should be executed:

```bash
    snakemake --cores 8 -q
```
The `--dryrun` or `-n` option allows you to see the scheduling plan, including the assigned priorities. The main Snakefile in the `~./rsRNAfinder/` directory will be automatically detected by snakemake and all the steps will be executed. Number of cores can also be increased. 

## Results
The `intermediate/` and `result/` directories will be generated in the current working directory, with the intermediate directory containing the intermediate files generated during processing and the results directory containing the output files. A separate folder will be created for each input sample and stored inside a directory named after the input reference genome.

At the end of the process, the result directory will contain several files, including:

a).	A `.csv` file with information on the rRF findings, including details on the respective rRNAs, such as length, sequence, raw and normalized counts, gene start and end, and genomic start and end positions of rRFs. This file will contain columns of following information:

| **Columns**     | **Description**      | 
| ------------- | ------------  |
| Category    | class of rRFs based on the mapping position of the read on the genome.|
| rRNA_info    | general rRNA information such as parental coordinates and chromosome number.|
|Gene_Start| coordinate where the first base of the read maps to with respect to the gene. |
|Gene End | coordinate where the last base of the read maps to with respect to the gene.|
|Sequence | mapped nucleotide sequence.|
|Length|length of the mapped bases|
|Genomic Start|coordinate where the first base of the read maps to with respect to the genomic position.|
|Genomic End |coordinate where the first base of the read maps to with respect to the genomic position. |
|Difference |sum of total number of mismatches, insertions, and differences in the mapped sequence.|
|RPM| ratio of the reads supporting the rRFs to the total number of small RNA sequences.|
|Seq_count| count of each unique sequence mapping to each genomic locus. |
|count| count of reads mapping exactly to the same genomic locus with some differences allowed.|

b).	`.html`: This presents the data on a webpage. The abundant rRFs from individual genomic locations are considered and the count of all mapped reads is kept in the creation of the HTML file from the above CSV file with an additional column of dot-bracket notation. The reads supporting the rRFs are divided by the total number of single sRNA seq and then multiplying with 1 million to normalize the rRF abundance to RPM.  
![html](https://github.com/rebminso/rsRNAfinder/assets/85422585/597ffab0-b797-4be9-8318-a10f1f36659e)


c).	A `.tsv` file with two columns showing the count of occurrence of each rRF class in the sample.
|  Column  |  Description  |
|----------|---------------|
|  rRF category  | total count of each category of rRFs |

d).	An eight-column file for abundance statistics summarizes the most abundant rRFs in all rRNA.

The toolkit has several integrated libraries for quick visualization of the output from each sample. These plots will provide a better representation of the distribution of the results, including a [pie plot](https://drive.google.com/file/d/14IytEnGqT0xtO4c6GagGpOnDsEGf3Dwe/view), [bar plot](https://drive.google.com/file/d/18qPxfGAdOv85YZzMxoQp3vO8XE2gomiz/view), and two [box](https://drive.google.com/file/d/133PqGHTAt91ipc2BP2ldv2yxeRoGKsST/view) [plots](https://drive.google.com/file/d/1uNu-iISuWUWTEyGv0EpQmktVHtchxh4k/view).  

![result](https://github.com/rebminso/rsRNAfinder/assets/85422585/1816295e-977b-44bb-8cd3-922d1daa0bac)
Above figure shows (A) Barplot displaying the length distribution within different categories of rRFs.(B)  Pie chart providing a comprehensive view of the overall distribution of rRF categories (C) Boxplot representing average abundance of different rRNA classes across distinct categories of rRFs. (D) Boxplot illustrating the average abundance of nuclear, chloroplast, and mitochondrial rRNAs for each category of rRFs 

## Test run
**Download and configure rsRNA**
```bash
  git clone https://github.com/rebminso/rsRNAfinder.git
  unzip rsRNAfinder
  cd rsRNAfinder
  conda activate base
  conda env create -f config/environment.yml
  conda activate rsRNA

```

### **An example using a default genome i.e. *Arabidopisis thaliana***

**Download Input and Genome file**
- A test folder containing an input file is provided in `data/trimmed/` directory.
```bash
  gunzip data/trimmed/test/*
```

- Genome file is already provided in `data/Genome/` directory.
```bash
  gunzip data/Genome/*
```

**Run the following command to run test sample:**

```bash
  snakemake --cores 8 -q
```
-q can be replaced with -npr to perform a dry-run.

### **An example using any other genome** 
**Download Input and Genome file of interest**
```bash
cd data/trimmed
mkdir newfq
cd newfq
fastq-dump SRR24973537
cd ../../Genome/
wget https://ftp.ncbi.nlm.nih.gov/genomes/refseq/plant/Brassica_rapa/latest_assembly_versions/GCF_000309985.2_CAAS_Brap_v3.01/GCF_000309985.2_CAAS_Brap_v3.01_genomic.fna.gz
gunzip *
mv GCF_000309985.2_CAAS_Brap_v3.01_genomic.fna brap_ref.fna
```
- Genome fasta header should start with '>chr[Num]'. Mitochondrial and plastid fasta headers also should be as chrMt & chrPt respectively.

**Download Feature table file of interest**
```bash
cd ../
mkdir Feature_table
cd Feature_table
wget https://ftp.ncbi.nlm.nih.gov/genomes/refseq/plant/Brassica_rapa/latest_assembly_versions/GCF_000309985.2_CAAS_Brap_v3.01/GCF_000309985.2_CAAS_Brap_v3.01_feature_table.txt.gz
gunzip *
mv GCF_000309985.2_CAAS_Brap_v3.01_feature_table.txt Brap.txt
```


**Changes the Config file**

```bash
reference_genome:
  Search_strategy: "Host"
  genome_fasta: "data/Genome/brap_ref.fna"
  species_NCBI_feature_table: "data/Feature_table/Brap.txt"
  ```
Return to the rsRNAfinder directory and execute the following command to run the test sample:
```bash
  snakemake --cores 8 -q
```
-q can be replaced with -npr to perform a dry-run.

## FAQs

#### 1.  error while loading shared libraries: libncurses.so.5: cannot open shared object file:

`sudo ln -s /usr/lib64/libncurses.so.6 /usr/lib64/libncurses.so.5`


#### 2. IncompleteFilesException: The files below seem to be incomplete.

`snakemake --cores 8 -q --ri`

#### 3. Automate removal of SAM file 
Change `"intermediate/SAM/{name}/{dir}/{sample}/{sample}_trimmed.sam"` to ` temp("intermediate/SAM/{name}/{dir}/{sample}/{sample}_trimmed.sam") ` in `rsRNAfinder/rules/default_smk/alignment_default.smk` file.


## Authors

- [@GarimaKalakoti](https://github.com/rebminso)
- gkalakoti@nipgr.ac.in

If you have any questions, bug reports, or suggestions, please contact:

**Dr. Shailesh Kumar**  
Staff Scientist, Bioinformatics Laboratory #202  
National Institute of Plant Genome Research (NIPGR), New Delhi  
Email: [shailesh@nipgr.ac.in](mailto:shailesh@nipgr.ac.in)

