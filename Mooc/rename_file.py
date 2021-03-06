import os

print(os.path.curdir)
path = 'Mooc/数据结构__数据结构__浙江大学/{1}--课程'
for i, dirs, j in os.walk(path):
    for f in j:
        if f.endswith('flv') and not f.endswith('.flv'):
            print(i, f)
            os.rename(i+'/'+f, i+'/'+f.replace('flv', '.flv'))
            # raise ValueError