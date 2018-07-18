hadoop jar /opt/cloudera/parcels/CDH-5.11.1-1.cdh5.11.1.p0.4/lib/hadoop-mapreduce/hadoop-streaming.jar \
-D mapreduce.job.reduces=1 \
-files hdfs://dumbo/user/lz1714/project/python_code/incid_mapper1.py,hdfs://dumbo/user/lz1714/project/python_code/incid_reducer1.py \
-mapper "python incid_mapper1.py" \
-reducer "python incid_reducer1.py" \
-input /user/lz1714/project/NYC.csv \
-output /user/lz1714/project/output

hadoop jar /opt/cloudera/parcels/CDH-5.11.1-1.cdh5.11.1.p0.4/lib/hadoop-mapreduce/hadoop-streaming.jar \
-D mapreduce.job.reduces=1 \
-files hdfs://dumbo/user/lz1714/project/python_code/incid_mapper2.py \
-mapper "python incid_mapper2.py" \
-input /user/lz1714/project/output/part-00000 \
-output /user/lz1714/project/output_final
