# Scripting

## Architecture :
![alt text](Architecture.png)

## Transfer files :

**predict.csv**
```csv
description
" She is also a Ronald D. Asmus Policy ..."
" He is a member of the AICPA and ..."
" Dr. Aster has held teaching and ..."
" He runs a boutique design studio ..."
" He focuses on cloud security, identity ..."
[...]
````

**results.csv**
```csv
description,job_id
" She is also a Ronald D. Asmus Policy ...",5
" He is a member of the AICPA and ...",4
" Dr. Aster has held teaching and ...";5
" He runs a boutique design studio ...",2
" He focuses on cloud security, identity ...",10
[...]
````


## AWS Installation :
If you want to change FIFO, Buckets ... names, make sure ton re-configure scripts
- Create **S3 buckets** with default encryption enabled :
  - ```predict-bucket-big-data-6```
  - ```results-bucket-big-data-6```
- Create **FIFO SQS** queues with default configuration :
  - ```StartPredicting.fifo```
  - ```SendResults.fifo```
- Create 1 **EC2 instance** with default configuration
