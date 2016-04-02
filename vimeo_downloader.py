#!/usr/bin/python2.7
USER_AGENT = "Mozilla/5.0"
import subprocess
import sys
import re
import json
vimeo_id = sys.argv[1]
try:
    subprocess.call(['wget','-U',USER_AGENT,'-q','-O','XML','http://vimeo.com/'+vimeo_id])
    xml = subprocess.check_output(['wget','-U',USER_AGENT,'-q','-O','-','http://vimeo.com/'+vimeo_id])
except:
    print "download of video page failed"
    sys.exit(1)
xml = xml.split("\n")
for l in xml:
    if "clip_page_config" in l:
        config_line = l
    if 'meta property="og:title' in l:
        caption_line = l
confurljson = re.sub(".*clip_page_config[^{]*","",config_line)[:-1]
caption = re.sub(".*content=.","",caption_line)[:-2]
try:
    myjson = json.loads(confurljson)
except ValueError:
    print "no valid json found in clip_page_config"
    print confurljson
    sys.exit(4)
try:
    configurl = myjson['player']['config_url']
except KeyError:
    print "json for player embedding unexpected"
    sys.exit(3)
try:
    theconfig = subprocess.check_output(['wget','-U',USER_AGENT,'-q','-O','-',configurl])
except:
    print "download of player configuration failed"
    sys.exit(1)
try:
    video_url_json = json.loads(theconfig)["request"]["files"]["progressive"]
except KeyError:
    print "unexpected player configuration json format"
    sys.exit(3)
except ValueError:
    print "no valid json found in player configuration"
    sys.exit(4)
res_url = {}
for v in video_url_json:
    try:
        print "available quality ",v['quality']
        res_url[v['quality']] = v['url']
    except KeyError:
        print "unexpected player configuration json format"
        sys.exit(3)
besturl = res_url[max(res_url)]
quality = max(res_url)
print "chose ",v['quality']," as best resolution"

filename=caption+"-("+quality+"-"+vimeo_id+").flv"
try:
    subprocess.check_call(['wget','-U',USER_AGENT,'-O',filename,besturl])
except:
    print "download of video failed"
    sys.exit(2)
sys.exit(0)
