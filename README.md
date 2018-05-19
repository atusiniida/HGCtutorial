## HGCスパコンの並列化チュートリアル
大腸菌次世代シーケンサーデータを大腸菌ゲノムにbwaでmappingするプロセスをpython 及びUniva Grid Engineを用いて並列化する

#### working directoryの作成
>mkdir HGCtutorial
cd HGCtutorial  

#### SRAからシーケンスデータをdownloadするプログラムを用意  
>wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.9.0/sratoolkit.2.9.0-centos_linux64.tar.gz
tar xvzf sratoolkit.2.9.0-centos_linux64.tar.gz
sratoolkit.2.9.0-centos_linux64/bin/fastq-dump  


#### リードをdownload
>sratoolkit.2.9.0-centos_linux64/bin/prefetch SRR001666  
sratoolkit.2.9.0-centos_linux64/bin/fastq-dump SRR001666  
mv  SRR001666.fastq  read.fastq  

#### リファレンスをdownload  
>wget　http://genome2d.molgenrug.nl/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna  
mkdir ref  
mv NC_000913.fna ref/reference.fa  

#### bwaをdownload  
>wget -O bwa-0.7.12.tar.bz2 'http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.12.tar.bz2/download?use_mirror=jaist&r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fbio-bwa%2Ffiles%2F&use_mirror=jaist'  
 bzip2 -dc bwa-0.7.12.tar.bz2 | tar xvf -  
 cd bwa-0.7.12  
 make  
 cd ..  

#### bwaのPATHをとおす  
>export PATH=$HOME/UGEtutorial/bwa-0.7.12:$PATH    
printenv  PATH  

#### インデックスファイルの作成  
>cd ref  
bwa index -p ecoli_index reference.fa  
cd ..  

#### 最初の10000 read を取得　(1read = 4行）  
>head -40000 read.fastq > read10000.fastq  

#### mapping  
>bwa mem ref/ecoli_index  read10000.fastq  > read10000.sam  

または

>bwa-0.7.12/bwa aln ref/ecoli_index read10000.fastq > read10000.sai  
bwa-0.7.12/bwa samse ref/ecoli_index read10000.sai read10000.fastq > read10000.sam


#### python3 設定
>export LD_LIBRARY_PATH=/usr/local/package/python/3.6.4/lib:${LD_LIBRARY_PATH}  
export PATH=/usr/local/package/python/3.6.4/bin:${PATH}  

~/.bashrc に書き込むことで次回ログイン時に自動設定される

>echo ‘export LD_LIBRARY_PATH=/usr/local/package/python/3.6.4/lib:${LD_LIBRARY_PATH} ‘ >> ~/.bashrc  
echo ‘LD_LIBRARY_PATH=/usr/local/package/python/3.6.4/lib:${LD_LIBRARY_PATH}’  >> ~/.  

#### 並列化scriptをdownload
>wget https://raw.githubusercontent.com/atusiniida/HGCtutorial/master/bwa.sh  
wget https://raw.githubusercontent.com/atusiniida/HGCtutorial/master/paralellBwa.py  


#### read.fastqを10並列でmapping

>python paralellBwa.py  read.fastq 10 > read.sam

やっていること
1 fastqファイルに分割する。

プロセス id の取得:  
import  os   
pid =  os.getpid()  
prefix = “tmp.”  + str(pid)  

分割したファイル名:  
prefix + “.” + str(fileindex) + “.fastq”

2 qsubでbwa.shをなげる。  
3 qstat でjobが終わってるかをみる。  
4 終わったらoutputをまとめる。

#### qsub  よくつかうオプション
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
