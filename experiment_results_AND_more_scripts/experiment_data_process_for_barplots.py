###### process data in participants' answers in such a way that they can be used to plot bar plots

import pandas as pd, numpy as np, os, json, csv

#load json with participants' answers into a dictionary
with open('answers.json') as data_file:    
    data = json.load(data_file)

questions = ['similarity','substitutability','appreciation']
labels = ['strong_disagree','disagree','neutral','agree','strong_agree']
types = ['clfr','rand']
categories = ['all','composers','non composers','drummers','non drummers','not trained','trained under 5','trained over 5']
counter = {}

for category in categories:
    tmp = {}
    for typ in types:
        tmp[typ] = {questions[0]:5*[0],questions[1]:5*[0],questions[2]:5*[0]}
    counter[category] = tmp

for key,value in data.items():
    if key!='step1':
        for k,v in value.items():
            if (int(key[4:]) < 12):
                for q in questions:
                    counter['all']['clfr'][q][labels.index(v[questions.index(q)])]+=1
            else:
                for q in questions:
                    counter['all']['rand'][q][labels.index(v[questions.index(q)])]+=1

for key,value in data.items():
    if key!='step1':
        if (int(key[4:]) < 12):
            for k,v in value.items():
                if data['step1'][k][0] == 'yes_compose':
                    for q in questions:
                        counter['composers']['clfr'][q][labels.index(v[questions.index(q)])]+=1
                else:
                    for q in questions:
                        counter['non composers']['clfr'][q][labels.index(v[questions.index(q)])]+=1

                if data['step1'][k][1] == 'yes_drums':
                    for q in questions:
                        counter['drummers']['clfr'][q][labels.index(v[questions.index(q)])]+=1
                else:
                    for q in questions:
                        counter['non drummers']['clfr'][q][labels.index(v[questions.index(q)])]+=1
                
                if data['step1'][k][2] == 'no_train':
                    for q in questions:
                        counter['not trained']['clfr'][q][labels.index(v[questions.index(q)])]+=1
                elif data['step1'][k][2] == 'train_under5':
                    for q in questions:
                        counter['trained under 5']['clfr'][q][labels.index(v[questions.index(q)])]+=1
                else:
                    for q in questions:
                        counter['trained over 5']['clfr'][q][labels.index(v[questions.index(q)])]+=1
                        
        else:
            for k,v in value.items():
                if data['step1'][k][0] == 'yes_compose':
                    for q in questions:
                        counter['composers']['rand'][q][labels.index(v[questions.index(q)])]+=1
                else:
                    for q in questions:
                        counter['non composers']['rand'][q][labels.index(v[questions.index(q)])]+=1

                if data['step1'][k][1] == 'yes_drums':
                    for q in questions:
                        counter['drummers']['rand'][q][labels.index(v[questions.index(q)])]+=1
                else:
                    for q in questions:
                        counter['non drummers']['rand'][q][labels.index(v[questions.index(q)])]+=1
                
                if data['step1'][k][2] == 'no_train':
                    for q in questions:
                        counter['not trained']['rand'][q][labels.index(v[questions.index(q)])]+=1
                elif data['step1'][k][2] == 'train_under5':
                    for q in questions:
                        counter['trained under 5']['rand'][q][labels.index(v[questions.index(q)])]+=1
                else:
                    for q in questions:
                        counter['trained over 5']['rand'][q][labels.index(v[questions.index(q)])]+=1

#load json with participants' answers into a dictionary
with open('answers_for_barplots.json','w') as data_file:    
    json.dump(counter,data_file)