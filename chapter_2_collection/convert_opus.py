'''
================================================ 
##            VOICEBOOK REPOSITORY            ##      
================================================ 

repository name: voicebook 
repository version: 1.0 
repository link: https://github.com/jim-schwoebel/voicebook 
author: Jim Schwoebel 
author contact: js@neurolex.co 
description: a book and repo to get you started programming voice applications in Python - 10 chapters and 200+ scripts. 
license category: opensource 
license: Apache 2.0 license 
organization name: NeuroLex Laboratories, Inc. 
location: Seattle, WA 
website: https://neurolex.ai 
release date: 2018-09-28 

This code (voicebook) is hereby released under a Apache 2.0 license license. 

For more information, check out the license terms below. 

================================================ 
##               LICENSE TERMS                ##      
================================================ 

Copyright 2018 NeuroLex Laboratories, Inc. 

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 

     http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License. 

================================================ 
##               SERVICE STATEMENT            ##        
================================================ 

If you are using the code written for a larger project, we are 
happy to consult with you and help you with deployment. Our team 
has >10 world experts in Kafka distributed architectures, microservices 
built on top of Node.js / Python / Docker, and applying machine learning to 
model speech and text data. 

We have helped a wide variety of enterprises - small businesses, 
researchers, enterprises, and/or independent developers. 

If you would like to work with us let us know @ js@neurolex.co. 

================================================ 
##               CONVERT_OPUS.PY              ##    
================================================ 

Quick script to collect some audio files in .wav format, 
then transcode these audio files into .OPUS format, and then
compress all the files in the folder into a .zip file. 

Compressing to .OPUS format is lossy and takes up about
15% of the size a .wav file would take up on the CPU.

Compared to .FLAC, 50% vs. 15% storage reduction.

OPUS is commonly used on cell data to take up minimal volume.

I suggest recording in .FLAC if possible to reduce potential for signal loss.
FLAC is also a bit more portable in terms of FFmpeg and file conversion software.
'''
import shutil, os, ffmpy 

def zipdir(folder, delete):
    # ziph is zipfile handle
    shutil.make_archive(folder, 'zip', folder)
    if delete == True:
        shutil.rmtree(folder)

def convert_opus(opusdir):
    curdir=os.getcwd()
    listdir=os.listdir()
    removedfiles=list()
    for i in range(len(listdir)):
        if listdir[i][-4:]!='opus':
            # get new file names 
            file=listdir[i]
            newfile=file[0:-4]+'.opus'
            # copy file to opus encoding folder 
            shutil.copy(curdir+'/'+file, opusdir+'/'+file)
            os.chdir(opusdir)
            # encode with opus codec 
            os.system('opusenc %s %s'%(file,newfile))
            shutil.copy(opusdir+'/'+newfile, curdir+'/'+newfile)
            # delete files in opus folder 
            os.remove(file)
            os.remove(newfile)
            # delete .wav file in original dir 
            os.chdir(curdir)
            os.remove(file)
            removedfiles.append(file)
    return removedfiles 

# get 10 files recorded in 'recordings' folder in current directory
# record them if the folder doesn't exist 
hostdir=os.getcwd()
opusdir=hostdir+'/opustools'
if 'recordings' not in os.listdir():
    os.system('python3 ps_record.py')

# change to directory of recordings to compress all files in directory 
os.chdir(hostdir+'/recordings')
convert_opus(opusdir)

# change back to main directory and compress files, delete main folder 
os.chdir(hostdir)
zipdir('recordings', True)
