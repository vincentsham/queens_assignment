import requests
from bs4 import BeautifulSoup
import pickle
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
from threading import Thread
import time
sys.setrecursionlimit(10000)
 
 
class StackOverflowQuestions():
    def __init__(self,type):
            self.BASE_URL = 'https://stackoverflow.com/search'
            self.SORT = '?tab='+type
            self.TAG = '&q=%5bandroid%5d'
            self.CREATED = '%20created%3a2020-01..2020-02'
            self.TYPE = '%20is%3aquestion'
            self.q_no = 10
            self.NUM_ANSWERS = 10
            self.headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
            }
            self.page = '&page=1&pagesize=10'
            self.page_url = self.BASE_URL + self.SORT + self.TAG + self.CREATED + self.TYPE + self.page
            self.questions = []
            self.filename = './'+type+'.pkl'
            
 
    def crawl_pages(self):
        q_no = 0
        questions = []
        now = datetime.now()
        last_month = now - relativedelta(months=1)
        self.CREATED = '%20created%3a'+str(last_month.year)\
        +"-"+str(last_month.month).zfill(2)+'..'\
        +str(now.year)+"-"+str(now.month).zfill(2)
        
        self.page_url = self.BASE_URL + self.SORT + self.TAG + self.CREATED + self.TYPE + self.page
        # print(self.page_url)
        try:
            source_code = requests.get(self.page_url, stream=True).text
            soup = BeautifulSoup(source_code, 'html.parser')
            for link in soup.find_all('a', {'class': 'question-hyperlink'}):
                q = {}
                if q_no == self.q_no:
                    break
                url = 'http://stackoverflow.com/' + link.get('href')
                q['q_url'] = url
                title = link.get_text()
                if "[duplicate]" in title:
                    continue
                q['q'] = title
                self.parse_question(url, title,q)
                questions.append(q)
                q_no += 1 
            self.validation(questions)
        except (KeyboardInterrupt, EOFError, SystemExit):
            pass
 
 
    def parse_question(self,url, title,q):
        import time
        start_time = time.time()
        page = requests.get(url, stream=True)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print("--- %s seconds ---" % (time.time() - start_time))
        question = soup.find('div',class_="postcell").find('div', class_='post-text')
        vote = soup.find('div', class_="js-vote-count").text
        q['v'] = vote
        date = soup.find('div', class_="owner").find('span', class_="relativetime")
        q['date'] = (datetime.strptime(date['title'][:-1], "%Y-%m-%d %H:%M:%S")-relativedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        
        if question is not None:
            answers = soup.find_all('div', class_='answercell')
            end = len(answers)
            if end > self.NUM_ANSWERS:
                end = self.NUM_ANSWERS
            q['content'] = question
            q['a'] = []
            for i in range(0, end):
                answer = answers[i].find('div', class_='post-text')
                # print("===>")
                q['a'].append(answer)
                # print(answer)
        return
    
    def write(self,filename=None):
        if filename != None: 
            self.filename = filename
        with open(self.filename, 'wb') as f:
            pickle.dump(self.questions, f)
      
    
    def read(self,filename=None):
        if filename != None: 
            self.filename = filename
        with open(self.filename , 'rb') as f:
            load = pickle.load(f)
            self.validation(load)
                
    def validation(self,questions):
        if (len(questions)==10):
            for i in range(len(questions)):
                if questions[i]['q'] == "":    
                    return
            self.questions = questions
        
            
class MyThread(Thread):
    def __init__(self,funs):
        Thread.__init__(self,daemon=True)
        self.funs = funs
        self.running = True

    def run(self):
        while self.running:
            for f in self.funs:
                try:
                    f()
                except:
                    print("Error:on crawling")
                    pass
            time.sleep(60)
    def stop(self):
        self.running = False

