
"""
@author: Ye
"""
import datetime
import tweepy,csv

EnglishList=('high school diploma','')
EmptyList=()
CompleteList=(EnglishList,EmptyList)

today=datetime.date.today()

#authentication
CONSUMER_KEY=""
CONSUMER_SECRET=""
OAUTH_TOKEN=""
OAUTH_TOKEN_SECRET=""

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True,parser=tweepy.parsers.\
                   JSONParser())
                   
#global var
tweetsPerQuery=100

def download(Keyword,SinceDate,UntilDate):
    
    #set up parameters
    q=Keyword
    MaxId=None
    tweetCount=0
    iterationCount=0
    
    #create txt file title and column name
    filename='Q='+q.replace(' ','')+'_'+'UntilDate='+UntilDate+'.txt'
    columnName=['creationDate','text','tweetID','userID','userLocation',\
    'userTimeZone','RT-Count']
    contentList=[]
    
    #download data and write to txt file
    with open(filename,'w',encoding='utf-8',newline='') as fout:
        cout=csv.writer(fout,delimiter='\t')
        cout.writerow(columnName)
        
        #collect tweet
        while True:
            print('---start iteration',iterationCount+1, 'current tweetCount is',\
            tweetCount,'---')
            
            if MaxId is None:
                search_result=api.search(q=q,count=tweetsPerQuery,\
                until=UntilDate,since=SinceDate)
            else:
                search_result=api.search(q=q,count=tweetsPerQuery,\
                until=UntilDate,since=SinceDate,max_id=MaxId)
                
            #process tweets returned, append to contentlist
            for tweets in search_result['statuses']:
                userLocation='N/A'
                userTimeZone='N/A'
                
                if tweets['user']['location']:
                    userLocation=tweets['user']['location']
                if tweets['user']['time_zone'] is not None:
                    userTimeZone=tweets['user']['time_zone']
    
                tempTuple=(tweets['created_at'],tweets['text'].\
                replace('\n',' '),str(tweets['id']),tweets['user']['id_str'],\
                userLocation,userTimeZone,str(tweets['retweet_count']))
                
                contentList.append(tempTuple) #list of tuple
            
            if tweetCount%500==0:
                cout.writerows(contentList)
                contentList=[]
    
            #update count
            tweetCount+=len(search_result['statuses'])
        
            #determine stopping condition
            if len(search_result['statuses'])==0 \
            or 'next_results' not in search_result['search_metadata']:
                cout.writerows(contentList)
                summary=['summary: keyword={} date={} tweetCount={}'.\
                format(q,SinceDate,tweetCount)]
                cout.writerow(summary)
                print("stop search")
                if 'next_results' not in search_result['search_metadata']:
                    print('next_results field unavailable')
                break
            
            #prepare for the next iteration
            MaxId=search_result['search_metadata']['next_results'].split('?max_id=')\
            [1].split('&q')[0]
            iterationCount+=1

for List in CompleteList:
    for Keyword in List:
        for Count in range(7):
            UntilDate=str(datetime.date.today()- datetime.timedelta(days=Count))
            SinceDate=str(datetime.date.today()- datetime.timedelta(days=Count+1))
            summary='Retrieve data for {} on {}'.format(Keyword,UntilDate)
            print(summary)
            download(Keyword,SinceDate,UntilDate)