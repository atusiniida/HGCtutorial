

cd UGEtutorial

### リードをダウウンロード

wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR001/SRR001666/SRR001666.sra


### SRAをfastaqにコンバートするプログラムを用意  

wget http://ftp-private.ncbi.nlm.nih.gov/sra/sdk/2.1.16/sratoolkit.2.1.16-centos_linux64.tar.gz  
tar xvzf sratoolkit.2.1.16-centos_linux64.tar.gz  
sratoolkit.2.1.16-centos_linux64/bin/fastq-dump  


### SRAをfastaqにコンバート  

sratoolkit.2.1.16-centos_linux64/bin/fastq-dump SRR001666.sra  
mv SRR001666.fastq read.fastq  

### リファレンスをダウンロード  
wget http://genome2d.molgenrug.nl/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna  

mkdir ref  
mv NC_000913.fna ref/reference.fa  

### bwa を取得  
wget -O bwa-0.7.12.tar.bz2 'http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.12.tar.bz2/download?use_mirror=jaist&r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fbio-bwa%2Ffiles%2F&use_mirror=jaist'  
 bzip2 -dc bwa-0.7.12.tar.bz2 | tar xvf -  
 cd bwa-0.7.12  
 make  
 cd ..  

### bwa のPATHをとおす  
export PATH=$HOME/UGEtutorial/bwa-0.7.12:$PATH  
setenv PATH  $HOME/UGEtutorial/bwa-0.7.12:$PATH  (tcshの場合）  
printenv  PATH  

https://qiita.com/Naggi-Goishi/items/2c49ea50602ea80bf015  


### インデックスファイルの作成  
cd ref  
bwa index -p ecoli_index reference.fa  
cd ..  

### 最初の10000 read を取得　(1read = 4行）  
head -40000 read.fastq > read10000.fastq  

###mapping  
bwa mem ref/ecoli_index  read10000.fastq  > test.sam  

http://cell-innovation.nig.ac.jp/wiki/tiki-index.php?page=SAMtools  


### qsub  よくつかうオプション
https://supcom.hgc.jp/japanese/utili_info/manual/uge.html  


ジョブIDの指定  
-N  job_Id  

メモリの制限  
-l s_vmem=XG,mem_req=XG  

Current working Dirで実行（outfile errfileがCurrent working Dirにでる）  
-cwd  

outfile X errfile Y の指定  
-o X -e Y  

キューの設定 (defaultは2日間jobがおわらないとkillされる）  
-l ljob 　（2週間）  
-l sjob  (8時間）  
