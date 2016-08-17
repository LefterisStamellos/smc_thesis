###### process data in participants' answers in such a way that they can be used to run wilcoxon statistical tests
import pandas as pd, numpy as np, os, json, csv

#load json with participants' answers into a dictionary
with open('answers.json') as data_file:    
    data = json.load(data_file)

# initialize empty answers dictionary
#
# structure of dictionary to contain all answers:
# answers = {'clfr':
#               { 'all': 
#                   { 'similarity': [A(P0),A(P1)...,A(P24)],
#                     'substitutability': [A(P0),A(P1)...,A(P24)],
#                     'appreciation': [A(P0),A(P1)...,A(P24)]}}}
#                 'composers': ...
#                   .
#                   .
#                   .
#                 'train_over5':...}}
#           {'rand':
#               { 'all': 
#                   { 'similarity': [A(P0),A(P1)...,A(P24)],
#                     'substitutability': [A(P0),A(P1)...,A(P24)],
#                     'appreciation': [A(P0),A(P1)...,A(P24)]}}}
#                 'composers': ...
#                   .
#                   .
#                   .
#                 'trained  over 5':...}}}
# 
# where A(P0) to A(P24) the aggregate of answers for participants 0 to 24
#
# labels = ['strong_disagree','disagree','neutral','agree','strong_agree'] are mapped to numbers 1 to 5

questions = ['similarity','substitutability','appreciation']
labels = ['strong_disagree','disagree','neutral','agree','strong_agree']
types = ['clfr','rand']
categories = ['all','composers','non composers','drummers','non drummers','not trained','trained under 5','trained over 5']
answers = {}

dict_typ = {}
for category in categories:
    dict_typ[category] = {questions[0]:25*[0],questions[1]:25*[0],questions[2]:25*[0]}
answers['clfr'] = dict_typ

dict_typ = {}
for category in categories:
    dict_typ[category] = {questions[0]:25*[0],questions[1]:25*[0],questions[2]:25*[0]}
answers['rand'] = dict_typ

# Fill dictionary for all participants: answers['clfr']['all'] and answers['rand']['all']
for key,value in data.items():
    if key!='step1':
        if (int(key[4:]) < 12):
            for (k,v) in value.items():
                for q in questions:
                    ipdb.set_trace()
                    answers['clfr']['all'][q][int(k)] += labels.index(v[questions.index(q)])+1
        else:
            for (k,v) in value.items():
                for q in questions:
                    ipdb.set_trace()
                    answers['rand']['all'][q][int(k)] += labels.index(v[questions.index(q)])+1

for key,value in data.items():
    if key!='step1':
        if (int(key[4:]) < 12):
            for k,v in value.items():
                if data['step1'][k][0] == 'yes_compose':
                    for q in questions:
                        answers['clfr']['composers'][q][int(k)] += labels.index(v[questions.index(q)])+1
                else:
                    for q in questions:
                        answers['clfr']['non composers'][q][int(k)] += labels.index(v[questions.index(q)])+1

                if data['step1'][k][1] == 'yes_drums':
                    for q in questions:
                        answers['clfr']['drummers'][q][int(k)] += labels.index(v[questions.index(q)])+1
                else:
                    for q in questions:
                        answers['clfr']['non drummers'][q][int(k)] += labels.index(v[questions.index(q)])+1
                
                if data['step1'][k][2] == 'no_train':
                    for q in questions:
                        answers['clfr']['not trained'][q][int(k)] += labels.index(v[questions.index(q)])+1
                elif data['step1'][k][2] == 'train_under5':
                    for q in questions:
                        answers['clfr']['trained under 5'][q][int(k)] += labels.index(v[questions.index(q)])+1
                else:
                    for q in questions:
                        answers['clfr']['trained over 5'][q][int(k)] += labels.index(v[questions.index(q)])+1
                        
        else:
            for k,v in value.items():
                if data['step1'][k][0] == 'yes_compose':
                    for q in questions:
                        answers['rand']['composers'][q][int(k)] += labels.index(v[questions.index(q)])+1
                else:
                    for q in questions:
                        answers['rand']['non composers'][q][int(k)] += labels.index(v[questions.index(q)])+1

                if data['step1'][k][1] == 'yes_drums':
                    for q in questions:
                        answers['rand']['drummers'][q][int(k)] += labels.index(v[questions.index(q)])+1
                else:
                    for q in questions:
                        answers['rand']['non drummers'][q][int(k)] += labels.index(v[questions.index(q)])+1
                
                if data['step1'][k][2] == 'no_train':
                    for q in questions:
                        answers['rand']['not trained'][q][int(k)] += labels.index(v[questions.index(q)])+1
                elif data['step1'][k][2] == 'train_under5':
                    for q in questions:
                        answers['rand']['trained under 5'][q][int(k)] += labels.index(v[questions.index(q)])+1
                else:
                    for q in questions:
                        answers['rand']['trained over 5'][q][int(k)] += labels.index(v[questions.index(q)])+1


for typ in types:
    for category in categories:
        for question in questions:
            answers[typ][category][question] = filter(lambda a: a != 0, answers[typ][category][question])

#load json with participants' answers into a dictionary
with open('answers_curated.json','w') as data_file:    
    json.dump(answers,data_file)