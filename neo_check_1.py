import subprocess
import re
import argparse
import os
import sys
sys.path.insert(0,os.getcwd())

frmt = '.ts'
from urlREGEX import URL_REGEX


parser = argparse.ArgumentParser(description='Finding Key...')
parser.add_argument('-f','--file', help='Provide filename with .m3u8 extension ', default='',required=True)
parser.add_argument('-t','--test',help='Test download for 2 files',default='Y',required=False)
parser.add_argument('-s','--start',help='startindex',default=0,required=False)
parser.add_argument('-T','--tsfile',help='to_mp4?',default=1,required=True)

args = vars(parser.parse_args())

#args = {'file':'chunklist_w438396826_b1348000_sleng.m3u8','start':0,'test':'Y',}

#define head and tail of the file
with open(args['file']) as f:
    head=f.readlines()[:10]
with open(args['file']) as f:
    tail=f.readlines()[-10:]

def get_key_url():
    key_url=re.findall(URL_REGEX,str(head))
    key_url = key_url[0][:-3]
    return key_url

key_file =  re.sub(r'\?.*',"",re.sub(r'https.*.smil\/',"",get_key_url()))

##############################
def save_key():
    if not (re.match(r'.*\.m3u8$',args['file'])):
        print('.m3u8 file does not exist...')
    else:       
        ## save key file only if does not exist already
        if not (os.path.isfile(key_file)):
            print('\n\n\tdownload {}'.format(key_file))
            os.system("aria2c " + get_key_url())
        else:
            print('{} {}'.format(u"\u2713",key_file))


##############################

base_url =  re.sub(r'/key_.*.m3u8key.*',"/",get_key_url())
media = [line.strip() for line in open(args['file']) if line.strip()[0] != '#' and line.strip() != '']
media_url = [base_url+m for m in media]

print("\n" , "FROM 0"," TO ",len(media)-1,"\n\n")
print ("\n","testing = ",args['test'])

if(args['test'] in ['y','Y']):
    to_down = range(2)
else:
    to_down = range(len(media_url))

for i in to_down:
    #filename = re.sub(r'https.*.smil\/',"",url)
    filename=media[i]
    if not (os.path.isfile(filename)):
        print('\n\t{} downloading {}'.format(u'\u2713',filename))
        os.system('aria2c -x 6 ' + media_url[i])

    else:
        print('{} {}'.format(u"\u2713",filename))


#####################
def fwrite(fname,content):
    with open(fname,'w') as f:
        f.write(content)

with open(args['file']) as f:
    lines = f.readlines()

save_key()
fwrite('key_url.txt',get_key_url())
playlist = 'playlist_'+ args['file']
fwrite(playlist,re.sub(URL_REGEX,key_file,"".join(lines)))


if(3>1):
    cmd = ['ffmpeg','-i',playlist,'-c','copy',args['tsfile']+'.TS']
    print('executing --> {}'.format(cmd))
    # after you have .ts combined files
    os.system(' '.join(cmd))

if(0>1):
    print("\n\nConverting to mp4...")
    os.system('sh ./sa_2.sh')




