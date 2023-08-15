import pandas as pd
from sqlalchemy import create_engine, text
from tkinter import *
from tkinter import messagebox



engine = create_engine('postgresql://postgres:1234@localhost/new')

root=Tk()

welcome=Label(root, text="Welcome to E-wallet services", background="purple",font=('Helvetica', 25, 'italic'), padx=5)
welcome.grid(row=0, column=0, columnspan=2, sticky=N+E+W+S)
s_frame=LabelFrame(root, text="Sign into your account", padx=10,pady=10)
s_frame.grid(row=1, column=1, columnspan=2,padx=10)

e_lab=Label(s_frame, text="Enter your email: ", anchor=E)
e_lab.grid(row=0, column=0)
p_lab=Label(s_frame, text="Enter your password: ", anchor=E)
p_lab.grid(row=1, column=0)
e_entry=Entry(s_frame, width=50)
e_entry.grid(row=0, column=1)
p_entry=Entry(s_frame, width=50)
p_entry.grid(row=1, column=1)
create_label=Label(root, text="Click \"Open account\" button to create a new account")
create_label.grid(row=2, column=0, columnspan=2)





class user:
    def __init__(self):        
        engine = create_engine('postgresql://postgres:1234@localhost/new')

        

    def create_acct(self):
        n_acct=Toplevel()
        name_l=Label(n_acct, text="Enter your name: ")
        name_l.grid(row=0, column=0, pady=10)
        email_l=Label(n_acct, text="Enter your email: ")
        email_l.grid(row=1,column=0)
        password_l=Label(n_acct, text="Enter your password: ")
        password_l.grid(row=2,column=0)


        name_e=Entry(n_acct, width=50)
        name_e.grid(row=0, column=1, pady=10)
        email_e=Entry(n_acct, width=50)
        email_e.grid(row=1,column=1)
        password_e=Entry(n_acct, width=50)
        password_e.grid(row=2,column=1)
       
        def acct_act():
            name=name_e.get()
            email=email_e.get()
            password=password_e.get()
        
            extract_id = "SELECT concat('BK','_00', (select MAX(id)+1 from users))"        
            
            engine = create_engine('postgresql://postgres:1234@localhost/new')
            with engine.connect() as conn:                   
                self.acct_id =[*conn.execute(extract_id)][0][0] 

                new_user= "INSERT INTO users(acct_id, name,email,password) VALUES (\'{}\',\'{}\',\'{}\',\'{}\')".format(self.acct_id, name,email,password)
                new_id="select distinct last_value(acct_id) over() from users"      
                conn.execute(new_user)
                new_id=[*conn.execute(new_id)][0][0]
            
                user_table="CREATE TABLE  {} (trans_type varchar, amount integer, trans_date TIMESTAMP)".format(new_id)      
        
                conn.execute(user_table)
                first_trans="INSERT INTO {} (amount, trans_date) VALUES (0, now())".format(new_id)
                conn.execute(first_trans)
            messagebox.showinfo("New account alert","You have succesfully created an account"+"\n"+"Your account ID is "+str(new_id))

        acct_bt=Button(n_acct, text="Create account", command=acct_act)  
        acct_bt.grid(row=3, column=0, columnspan=2)

    def fund_acct(self):
       # acct_id=input("enter identification number")
             
        funds=  int(self.fd_entry.get())
        engine = create_engine('postgresql://postgres:1234@localhost/new')
        with engine.connect() as conn:
            balance="select distinct last_value(amount) over()+{} from {}".format(funds,self.acct_id)
            new_bal=[*conn.execute(balance)][0][0]
            trans="INSERT INTO {} VALUES ('credit',{},now())".format(self.acct_id, new_bal)
            conn.execute(trans)
        messagebox.showinfo("Transaction",'Transaction completed')

    def check_bal(self):
        
        with engine.connect() as conn:
            bal="select distinct last_value(amount) over() from {}".format(self.acct_id)
            bal=[*conn.execute(bal)][0][0]
        Label(self.land_page, text="Your account balance is  ₦{}".format(bal)).grid(row=2,column=0)
        
        
    
    def transfer_fund(self):
        receipt_id=self.tf_entry.get()
        user_search= 'SELECT name FROM users WHERE acct_id = \'{}\''.format(receipt_id)
        with engine.connect() as conn:
            r_name=[*conn.execute(user_search)][0][0]
            resp = messagebox.askyesno("Receiver's Info", "Receiver'name is "+ str(r_name)+"\nDo you want to continue the transaction?")
            if resp==1:
                funds=int(self.tf_fund_entry.get())
                balance="select distinct last_value(amount) over()-{} from {}".format(funds,self.acct_id)
                new_bal=[*conn.execute(balance)][0][0]
                trans="INSERT INTO {} VALUES ('debit',{},now())".format(self.acct_id, new_bal)
                conn.execute(trans)
                credit_receipt= "INSERT INTO {} VALUES ('credit', (SELECT distinct last_value(amount) over()+{} from {}),now())".format(receipt_id,funds,receipt_id)
                conn.execute(credit_receipt)
                messagebox.showinfo("Transaction","Transaction Completed Successfully!")
            else:
                pass
    
    def sign_in(self):
         
        global e_entry
        global p_entry
        global new1
        email= e_entry.get()
        password=p_entry.get()
        
        if email=="" or password=="":
            messagebox.showinfo("Error","Email or Password fields cannot be empty!")
            
        else:  
            engine = create_engine('postgresql://postgres:1234@localhost/new') 
            with engine.connect() as conn:
                try:
                    em_pd_check='SELECT password FROM users WHERE email=\'{}\''.format(email)
                    em_pd_check=[*conn.execute(em_pd_check)][0][0]
                    if em_pd_check == password:                
                        get_id= 'SELECT acct_id from users WHERE email=\'{}\''.format(email)
                        self.acct_id=[*conn.execute(get_id)][0][0]
                        acct_name ='SELECT name from users WHERE acct_id =\'{}\''.format(self.acct_id)
                        self.acct_name=[*conn.execute(acct_name)][0][0]              
                except IndexError:
                    pne_error=messagebox.showinfo("Error","Wrong email and password combination!")
                    self.acct_id=""
                except NameError:
                    pne_error=messagebox.showinfo("Error","Wrong email and password combination!")
                    self.acct_id=""
                except AttributeError:
                    pne_error=messagebox.showinfo("Error","Wrong email and password combination!")
                    self.acct_id=""

                
                            
            
            if self.acct_id != "":
                self.land_page=Toplevel()
                self.land_page.geometry("500x400")
                l_wel=Label(self.land_page, text="Welcome to your wallet account "+str(self.acct_name) +"\nYour account id: "+str(self.acct_id), font=('Arial', 20))
                l_wel.grid(row=0,column=0)

                ck_bal=Button(self.land_page, text="Check balance", command=self.check_bal)
                ck_bal.grid(row=1,column=0)

                #Funding account frame
                fd_frame=LabelFrame(self.land_page, text="Fund your account", padx=10)
                fd_frame.grid(row=3, column=0, columnspan=2, padx=10)
                fd_label=Label(fd_frame, text="Enter amount: ")
                fd_label.grid(row=0, column=0)
                self.fd_entry=Entry(fd_frame, width=50)
                self.fd_entry.grid(row=0, column=1)
                fd_acct=Button(fd_frame, text="Deposit", command=self.fund_acct)
                fd_acct.grid(row=1,column=1)

                #Transfer funds frame
                tf_frame=LabelFrame(self.land_page, text="Enter transfer details ", padx=10)
                tf_frame.grid(row=4, column=0, columnspan=2, padx=10)
                tf_label=Label(tf_frame, text="Enter receiver's Bank ID: ")
                tf_label.grid(row=0, column=0)
                self.tf_entry=Entry(tf_frame, width=50)
                self.tf_entry.grid(row=0, column=1)

                tf_fund=Label(tf_frame, text="Enter amount: ")
                tf_fund.grid(row=1, column=0)
                self.tf_fund_entry=Entry(tf_frame, width=50)
                self.tf_fund_entry.grid(row=1, column=1)


                tf_acct=Button(tf_frame, text="Transfer", command=self.transfer_fund)
                tf_acct.grid(row=2,column=1)

                lg_bt=Button(self.land_page, text="Sign out",padx=100, command= self.log_out)
                lg_bt.grid(row=5,column=0, columnspan=2)
            else:
                pass
        return self.acct_id

    def log_out(self):
        self.land_page.destroy()
        print(log_var[self.acct_id], "log out Successfully!")
        del log_var[self.acct_id]
       
  
      

def log_in():
    try:
        with engine.connect() as conn:
            id= 'SELECT acct_id from users WHERE email=\'{}\''.format(e_entry.get()) 
            global acct_log       
            acct_log=[*conn.execute(id)][0][0]
        
        global log_var
        log_var=globals()
        
        log_var[acct_log] =user()
        print(log_var[acct_log], "created")
        try:
            log_var[acct_log].sign_in()
            print( log_var[acct_log], "logged in Successfully!")
        except AttributeError:
            del log_var[acct_log]
            pass
    except IndexError:
        pne_error=messagebox.showinfo("Error","Wrong email and password combination!")

    
   

def create_acc():
    user().create_acct()



sign_bt=Button(s_frame, text="Sign in", padx=130,command=log_in)
sign_bt.grid(row=2,column=0, columnspan=2,pady=(10,0))

create_bt=Button(root, text="Open account",  command=create_acc)
create_bt.grid(row=3,column=0, columnspan=2,pady=(5,10))



root.mainloop()
