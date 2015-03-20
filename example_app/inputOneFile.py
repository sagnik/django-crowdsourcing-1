import sqlite3 as lite
import sys
import glob
import os
import json
from nltk.tokenize import sent_tokenize
import shutil

insrtcmd1="SELECT id FROM crowdsourcing_question ORDER BY id DESC LIMIT 1"
insrtcmd2="SELECT id FROM crowdsourcing_survey ORDER BY id DESC LIMIT 1"
jsonfile=sys.argv[1]
imagefile=sys.argv[1].replace('jsons','images')[:-4]+"png"
print jsonfile,imagefile
if not os.path.exists(jsonfile) or not os.path.exists(imagefile):
	print "hurum!"
	sys.exit(1)
try:
	cont=json.load(open(jsonfile,"r"))
except:
	print "json could not be loaded"
 
try:
	con = lite.connect('dev.db')
	with con:
		cur = con.cursor()    
		cur.execute(insrtcmd1)
		qid=cur.fetchone()[0]
		cur=con.cursor()
		cur.execute(insrtcmd2)
		survey_id=cur.fetchone()[0]
   		surveyid=str(survey_id+1)
		print "question id",qid,"survey_id",survey_id
		#insert info from
		captions=[]
		mentions=[]
		imagetexts=[]
		try: 
			mentions=['mention_sentence_'+str(i)+": "+x for i,x in enumerate(sent_tokenize(cont['Mention'][0]))]
		except KeyError:
			print "mentions not found"
		try:
			captions=['caption_sentence_'+str(i)+": "+x for i,x in enumerate(sent_tokenize(cont['Caption']))]
		except KeyError:
			print "captions not found"
		try:
			imagetexts=['imgtext_element_'+str(i)+": "+x['Text'] for i,x in enumerate(cont['ImageText'])]
		except KeyError:
			print "image texts not found"
						
		tnm="crowdsourcing_question"
		allquestions=imagetexts+captions+mentions
		options="abscissa label\nabscissa value\nordinate label \nordinate value\n legend \n dataset\nmetric \n method"
		slugvalue="figure"+surveyid
		insrtcmd='INSERT INTO '+"crowdsourcing_survey"+' VALUES("'+surveyid+'","'+slugvalue+'","'\
		+slugvalue+'","'+""+\
		'","'+""+'","'+""+'","'+'0'+'","'+'0'+'","'+'0'+'","'+'1'+'","'+"1"+'","'+'1'+'","'\
		+'2015-03-18 18:56:53'+'","'+'2015-03-18'+'","'+''+'","'+'0'+'","'+'1'+'","'+''+'","'+''+'","'+'2'+'","'+''+'","'+''+'","'\
		''+'")'
		cur.execute(insrtcmd)
		
		#input the figure
		cur=con.cursor() 
		index=0
		imgname=imagefile.split("/")[-1]
		insrtcmd='INSERT INTO '+tnm+' VALUES("'+str(qid+1)+'","'+surveyid+'","'+'question'+str(index)+'","'+''+\
		'","'+''+\
		'","'+'question'+str(index)+'","'+"<img src='/media/img/"+imgname+"'>"+'","'+""+'","'+'0'+'","'+str(index)\
		+'","'+'bool'+'","'+'1'+'","'+""+'","'+""+'","'\
		+'1'+'","'+'0'+'")'
		print insrtcmd
		cur.execute(insrtcmd)
		shutil.copy(imagefile,'/home/szr163/django-crowdsourcing-1/example_app/example_app/media/img/')
		#insrtcmd='INSERT INTO '+tnm+' VALUES('
		qid+=1
		for index,question in enumerate(allquestions):
			insrtcmd='INSERT INTO '+tnm+' VALUES("'+str(qid+1)+'","'+surveyid+'","'+'question'+str(index+1)+'","'+question+\
			'","'+"<p><b>"+question+"</b></p>"+\
			'","'+'question'+str(index+1)+'","'+""+'","'+""+'","'+'0'+'","'+str(index+1)+'","'+'select'+'","'+'1'+'","'+options+'","'+""+'","'\
			+'1'+'","'+'0'+'")'
			print insrtcmd
			qid+=1
			cur.execute(insrtcmd)
except lite.Error, e:
	print "Error %s: "% e.args[0]
	sys.exit(1)


    
finally:
	if con:
		con.close()
