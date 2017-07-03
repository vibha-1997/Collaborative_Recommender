import pandas as pd
import numpy as np
import csv
import json
from math import sqrt
import math


df2=pd.read_csv('newfile.csv')

def similarity_score(user1,user2):
    both_viewed={}
    for col in df2[df2['u_id']==user1].ix[:,df2.columns!='u_id']:
        
        if math.isnan(df2.loc[df2['u_id']==user1,col].item())==False:
                       
            if math.isnan(df2.loc[df2['u_id']==user2,col].item())==False:
                both_viewed[col]=1

    if len(both_viewed)==0:
        return 0
    

    sum_of_eclidean_distance=[]

    for col in df2[df2['u_id']==user1].ix[:,df2.columns!='u_id']:
        if math.isnan(df2.loc[df2['u_id']==user1,col].item())==False:
            if math.isnan(df2.loc[df2['u_id']==user2,col].item())==False:                
                sum_of_eclidean_distance.append(pow(df2.loc[df2['u_id']==user1,col].item() - df2.loc[df2['u_id']==user2,col].item(),2))
    sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

    return 1/(1+sqrt(sum_of_eclidean_distance))

def pearson_correlation(user1,user2):
    both_rated={}
    #getting both rated items
    for col in df2[df2['u_id']==user1].ix[:,df2.columns!='u_id']:
        
        if math.isnan(df2.loc[df2['u_id']==user1,col].item())==False:
                       
            if math.isnan(df2.loc[df2['u_id']==user2,col].item())==False:
                both_rated[col]=1
    number_of_ratings=len(both_rated)

    if len(both_rated)==0:
        return 0
    #Adding all prefrences of the two users
    user1_prefrence_sum=sum([df2.loc[df2['u_id']==user1,ele].item() for ele in both_rated])
    user2_prefrence_sum=sum([df2.loc[df2['u_id']==user2,ele].item() for ele in both_rated])



    #adding squared values
    user1_prefrence_sum_square=sum([pow(df2.loc[df2['u_id']==user1,ele].item(),2) for ele in both_rated])
    user2_prefrence_sum_square=sum([pow(df2.loc[df2['u_id']==user2,ele].item(),2) for ele in both_rated])


    product_sum_of_users=sum([df2.loc[df2['u_id']==user1,ele].item()*df2.loc[df2['u_id']==user2,ele].item() for ele in both_rated])

    #Calculation of pearson score
    nm=product_sum_of_users-(user1_prefrence_sum * user2_prefrence_sum/number_of_ratings)
    dn=sqrt((user1_prefrence_sum_square-pow(user1_prefrence_sum,2)/number_of_ratings)*(user2_prefrence_sum_square-pow(user2_prefrence_sum,2)/number_of_ratings))

   
    if dn==0:
        
        return 0
    else:
        r=float(nm)/dn
        return r

def user_recommendations(user):
    totals={}
    simSums={}
    rankings=[]
    recommendations_list=[]
    
    for other in df2['u_id']:
        
        if other==user:
            continue
        else:
            
            sim=pearson_correlation(user,other)
            print other
            if sim<=0:
                continue
            for col in df2[df2['u_id']==other].ix[:,df2.columns!='u_id']:
                if math.isnan(df2.loc[df2['u_id']==other,col].item())==False:
                    if math.isnan(df2.loc[df2['u_id']==user,col].item())==True or (df2.loc[df2['u_id']==user,col].item())==0:
                        totals.setdefault(col,0)
                        totals[col]+=df2.loc[df2['u_id']==other,col].item()*sim
                        simSums.setdefault(col,0)
                        simSums[col]+=sim
                    
    print sim
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    print rankings
    

    recommendations_list=[recommend_item for score,recommend_item in rankings]
    return recommendations_list[:3]

                    
                    



    
    

    

    
                        
                

            
