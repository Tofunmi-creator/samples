from django.shortcuts import render
import re
import requests
from bs4 import BeautifulSoup
from .forms import bookinfo, topicsn
from django.contrib import messages

class BookScrape:
    def __init__(self):
        self.url_main="https://books.toscrape.com/"
        self.topics=self.get_topic(self.url_main) 
        
    def url_content(self,url):
        html = requests.get( url ).content
        html_parse=BeautifulSoup(html,'html.parser')
        return html_parse

    def get_list_pages(self,url):        
        def get_list(url):           
            tags= self.url_content(url).findAll('h3')       
            return tags        
        count=2
        url_list=get_list(url)
        tag_pages=[]
        tag_pages+=url_list  
        while url_list !=[]:
                url2=url.replace("index.html",'page-'+str(count)+'.html')
                url_list=get_list(url2)
                tag_pages+=url_list       
                count+=1
        books=""
        book_ref=[]
        for i in tag_pages:        
            books+=str(i.find('a')['title'])+'\n'
            book_ref.append(i)
        return books, book_ref

    def get_topic(self,url):      
        tags=self.url_content(url).find('ul', attrs={'class':"nav nav-list"}).find('ul').find_all('li')       
        return tags 

    def get_topic_text(self):
        b_list=[]            
        for i in self.topics:
            b_list.append(i.text.strip())
        return b_list

    def get_topic_list(self,b):                  
        b_list={}
        count =1
        topic_count=[]       
        for i in self.topics:
            topic=i.text.strip()
            topic_count.append(count)              
            b_list[count]=[topic, i.find('a')['href']]
            count+=1          
        b=int(b)
        
        if b >=min(topic_count) and b <=max(topic_count):
            sel_url=self.url_main+b_list[b][1] 
            topic_search=b_list[b][0]            
            books,_=self.get_list_pages(sel_url)     
        return books,topic_search

    def get_price(self,url):
        tags=self.url_content(url).find('p', attrs={'class':'price_color'}).text    
        return tags 

    def book_price(self, topic_input, book_input):                
        topic_search={}
        for i in self.topics:
            topic=str(i.text.strip())
            if topic_input.lower() in topic.lower():
                topic_search[topic]=i.find('a')['href']
        if topic_search !={}:
            result=[]
            for topic, link in topic_search.items():
                s_url=self.url_main+link
                books, book_ref=self.get_list_pages(s_url)
                books=books.split('\n')
                for book, ref in zip(books,book_ref):
                    if book_input.lower() in book.lower():
                        j= re.sub('\../',"",ref.find('a')['href'])
                        j="https://books.toscrape.com/catalogue/"+j
                        price=self.get_price(j)
                        result.append([book,price])            
            if result !=[]:
                msg=""
            else:
                msg='No item matching your book input'
        else:
            msg='No item matching your topic input'
            result=[]
        return result, msg


def home(request):
    return render(request, 'home.html',{})

def bookprice(request):
    result=""
    form=bookinfo(request.POST)
    if request.method=="POST":
        if form.is_valid():
            topic_entry=request.POST['topic']
            book_entry=request.POST['book_name']
            result,msg=BookScrape().book_price(topic_entry,book_entry)
            if msg=="":
                pass
            else:    
                messages.success(request, (msg))
    return render(request, 'bookprice.html',{'form':form,'result':result})

def booklist(request):
    form = topicsn(request.POST)
    books=""
    topic_search=""
    topic_list=BookScrape().get_topic_text()
    if request.method =="POST":
        
        if request.POST.getlist('books'):
            if form.is_valid():  
                s_no=request.POST['topic_sn']                
                books,topic_search=BookScrape().get_topic_list(s_no)
                
                books=books.split('\n')              
    return render(request, 'booklist.html',{'books':books, 'form':form,'topic_search':topic_search,'topic_list':topic_list})
