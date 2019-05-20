import boto3
import botocore
import numpy as np
from scipy.stats import pearsonr

s3 = boto3.resource('s3')

def bucket_list():
    for bucket in s3.buckets.all():
        print(bucket.name)

def upload():
    data = open("명제석.txt", "rb")
    s3.Bucket("azizcloudcomputing").put_object(Key="명제석.txt", Body=data)
def download(name):
    try:
        for i in name:
            s3.Bucket("azizcloudcomputing").download_file(i+".txt", "downloadede.txt")
            with open("downloadede.txt", encoding="utf8") as f1:
                targetfile = 'download.txt'
                with open(targetfile, 'a', encoding='utf8') as f2:
                    for line in f1:
                        line = line.replace(" ","")
                        f2.write(line + '\n')


    except botocore.exceptions.ClientError as e:
        print("The error")

def recommend(name):
    me = name[len(name)-1]
    list = []
    try:
        with open("download.txt","r",encoding='utf8') as f1:
            for line in f1:
                tmplist = []
                tmp = line.split(',')
                for i in tmp:
                    i = i.replace("\n","")
                    tmplist.append(int(i))
                print(tmplist)
                list.append(np.array(tmplist))

        for i in range(0,len(list)-1):
            corr = pearsonr(list[i], list[len(list)-1])
            print(name[i] + " and " + name[len(list)-1] + " : " ,corr)
    except botocore.exceptions.ClientError as e:
        print("The error")

name = ["고석빈","구경민","정예원","강경민","김소민","명제석"]
# download(name)
recommend(name)

# bucket_list()
# upload()
# download()