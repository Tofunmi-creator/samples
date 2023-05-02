import re
import requests
from bs4 import BeautifulSoup

class BookScrape:
    def __init__(self):
        self.url_main="https://books.toscrape.com/"
        self.topics=self.get_topic(self.url_main)
        print("To retrieve a list of books under a topic Press \'1\'. \nTo retrieve price of a book price \'2\'")
        op_no=int(input('Enter number here: '))
        if op_no==1:
            self.get_topic_list()
        elif op_no ==2:
            self.book_price()
        else:
            print('You have entered an invalid input')

    def url_content(self,url):
        try:
            html = requests.get( url ).content
        except:
            print("Failed Internet Connection")
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
    
    def get_topic_list(self):
        b_list={}
        count =1
        topic_count=[]       
        for i in self.topics:
            topic=i.text.strip()
            topic_count.append(count)
            print(str(count)+'. ',topic)    
            b_list[count]=[topic, i.find('a')['href']]
            count+=1

        print("Select serial no of topic to view book records")
        b=int(input('Enter number here: '))

        if b >=min(topic_count) and b <=max(topic_count):
            sel_url=self.url_main+b_list[b][1] 
            print("Find below list of books for ", b_list[b][0],"\n")
            
            books,_=self.get_list_pages(sel_url)
            print(books)    
        else: 
            print('Invalid Input')


    def get_price(self,url):
        tags=self.url_content(url).find('p', attrs={'class':'price_color'}).text    
        return tags
    

    def book_price(self):
        topic_input=input('enter name of topic: ')
        book_input=input('enter book title: ')


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
                print('Here are the prices of book(s) from your search input')
                for i in result:
                    print('The price of book \''+str(i[0])+'\' is '+str(i[1]))
            else:
                print('No item matching your book input')

        else:
            print('No item matching your topic input')


BookScrape()