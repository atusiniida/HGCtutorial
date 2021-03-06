## HGCスパコンの並列化チュートリアル
[大腸菌次世代シーケンサーデータ](https://www.ncbi.nlm.nih.gov/sra/?term=SRR001666)を[大腸菌ゲノム](https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3)にbwaでmappingする処理をpython 及びUniva Grid Engineを用いて並列化する

#### directoryの作成、 codeのダウンロード
`mkdir bin`  
`mkdir package`  
`git clone  https://github.com/atusiniida/HGCtutorial.git`     

#### PATHを通す
`export PATH=${HOME}/bin:${PATH}`

~/.bashrc に書き込むことで次回ログイン時に自動設定される　  

`echo export PATH=\${HOME}/bin:\${PATH} >> ~/.bashrc`　

#### python3 設定
`export LD_LIBRARY_PATH=/usr/local/package/python/3.6.4/lib:${LD_LIBRARY_PATH}`  
`export PATH=/usr/local/package/python/3.6.4/bin:${PATH}`  

~/.bashrc に書き込むことで次回ログイン時に自動設定される  

`echo export LD_LIBRARY_PATH=/usr/local/package/python/3.6.4/lib:\${LD_LIBRARY_PATH} >> ~/.bashrc`  
`echo export PATH=/usr/local/package/python/3.6.4/bin:\${PATH} >> ~/.bashrc`

#### sratoolkit のインストール
https://www.ncbi.nlm.nih.gov/books/NBK242621/  

`cd package`  
`wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.9.0/sratoolkit.2.9.0-centos_linux64.tar.gz`
`tar xvzf sratoolkit.2.9.0-centos_linux64.tar.gz`  
`ln -s ~/package/sratoolkit.2.9.0-centos_linux64/bin/* ~/bin`  
`rm sratoolkit.2.9.0-centos_linux64.tar.gz`   
`cd ..`  

#### bwa　のインストール
`cd package`  
`wget -O bwa-0.7.12.tar.bz2 'http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.12.tar.bz2/download?use_mirror=jaist&r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fbio-bwa%2Ffiles%2F&use_mirror=jaist'`  
 `bzip2 -dc bwa-0.7.12.tar.bz2 | tar xvf -`  
 `cd bwa-0.7.12`  
 `make`  
 `cd ..`  
 `ln -s ~/package/bwa-0.7.12/bin/bwa ~/bin`   
 `rm bwa-0.7.12.tar.bz2`  
 `cd ..`

#### リードをdownload
`cd HGCtutorial`

以降HGCtutorialにて作業  

`prefetch SRR001666`  
`fastq-dump SRR001666`  
`mv SRR001666.fastq  read.fastq`  

#### リファレンスをdownload
`wget http://genome2d.molgenrug.nl/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna`  
`mkdir ref`  
`mv NC_000913.fna ref/reference.fa`  


#### インデックスファイルの作成  
`cd ref`  
`bwa index -p ecoli_index reference.fa`  
`cd ..`  

#### 最初の10000 read を取得　(1read = 4行）  
`head -40000 read.fastq > read10000.fastq`  

#### mapping  
`bwa mem ref/ecoli_index  read10000.fastq  > read10000.sam`  

または

`bwa aln ref/ecoli_index read10000.fastq > read10000.sai`  
`bwa samse ref/ecoli_index read10000.sai read10000.fastq > read10000.sam`


#### qsubでbwaをsubmit
`qsub code/bwa.sh  read10000 ref/ecoli_index`

#### read.fastqを10並列でmapping
`python code/paralellBwa.py  read.fastq 10 > read.sam`

#### paralellBwa.pyの中でやっていること  
1 fastqファイルを分割する。  
`python code/splitFastq.py read.fastq 10 tmp`

2 分割した各fastqファイルをインプットとしqsubでcode/bwa.shをなげる。  
`python code/qsubBwa.py tmp*.fastq`

3 1秒ごとにqstatし、jobが終わるまで待つ。  
`python code/wait4job2finish.py tmp`

4 終わったらoutputをまとめる。  
`python code/catSam.py tmp*.sam > read.sam`

pythonの中からshellのコマンドを実行するときはrun関数を使う。runCommand.pyを参照。  
`python code/runCommand.py pwd`

分割したファイルのprefixをプロセスIDにする事で、異なるプロセスでスクリプトを同時に投げた場合の干渉が防げる。

プロセス id の取得:  
　　import  os   
　　pid =  os.getpid()  
　　prefix = “tmp.”  + str(pid)  
　分割したファイル名:  
　　prefix + “.” + str(fileindex) + “.fastq”

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
　-l ljob 　(2週間）  
　-l sjob  　(8時間）
