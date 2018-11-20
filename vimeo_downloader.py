USER_AGENT = "Mozilla/5.0"
import subprocess
import sys
import re
import json

WGET_BASE = ['curl','-A',USER_AGENT,'-s','-o']

if 0==subprocess.call(['wget','--version']):
    QUIET_WGET = ['wget','-U',USER_AGENT,'-q','-O','-']
    TARGET_WGET = ['wget','-U',USER_AGENT,'-O']
elif 0==subprocess.call(['curl','--version']):
    QUIET_WGET = ['curl','-A',USER_AGENT,'-s']
    TARGET_WGET = ['curl','-A',USER_AGENT,'-o']
else:
    print("no downloader found")
    sys.exit(5)

vimeo_id = sys.argv[1]

xml = str(subprocess.check_output(QUIET_WGET+['http://vimeo.com/{}'.format(vimeo_id)]))

jsonstart = xml.find("window.vimeo.clip_page_config") + 32
jsonend = xml.find(";", jsonstart)

confurljson = xml[jsonstart:jsonend]

rep = confurljson.count("<")
for x in range(rep):
    start = confurljson.find("<")
    end = confurljson.find(">") + 1
    confurljson = confurljson[:start] + confurljson[end:]

confurljson = re.sub(".*clip_page_config[^{]*","",config_line)[:-1]
caption = re.sub(".*content=.","",caption_line)[:-2]

capstart = xml.find("og:title") + 18
capend = xml.find(">", capstart)

caption = xml[capstart:capend]

caption = caption.replace("\"", "")

myjson = json.loads(confurljson)

configurl = myjson['player']['config_url']

theconfig = subprocess.check_output(QUIET_WGET+[configurl])

configurl = configurl.replace("\\", "")

video_url_json = json.loads(theconfig)["request"]["files"]["progressive"]

res_url = {}
for v in video_url_json:
    print("available quality ",v['quality'])
    res_url[v['quality']] = v['url']

besturl = res_url[max(res_url)]
quality = max(res_url)
print("Chose {} as best resolution".format(v['quality']))

filename = "{}-{}-{}.flv".format(caption, quality, vimeo_id) 
filename = filename.replace("/","_")

subprocess.check_call(TARGET_WGET+[filename,besturl])
