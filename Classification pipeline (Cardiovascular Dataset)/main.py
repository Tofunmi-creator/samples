
import pandas as pd
import numpy as np
import smtplib
from os.path import basename
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.metrics import confusion_matrix
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

file= "cardio.csv"


class file_process:
    def __init__(self, file):
        self.data=file
        self.preprocess()

    def readfile(self):
        return pd.read_csv(self.data)


    def preprocess(self):
        f=self.readfile()
        f=f[(f['ap_lo']<500) & (f['ap_lo']>30)]
        f=f[(f['ap_hi']<250) & (f['ap_hi']>50)]

        data_smok=f[f['smoke']==1]
        data_smok=data_smok.sample(n=6053)
        data_nsmok=f[f['smoke']==0]
        data_nsmok=data_nsmok.sample(n=6053)
        f=pd.concat([data_smok,data_nsmok])
        f=f.sample(frac=1)

        f['bmi']=(f['weight']/(f['height']**2))**(1/2)
        f=f.drop(columns=['age'])

        f_min_max=[f.ap_lo.max(), f.ap_lo.min(),f.ap_hi.max(),f.ap_hi.min()]
        sm_unq= sorted(f['smoke'].unique())
        n_rows=f.id.count()
        self.trans_data=f
        self.trans_data.to_csv('clean_file.csv')
        return len(f.columns), sm_unq, n_rows, f_min_max, f
      

    def data_explore(self, clean_file):
        tabl=pd.read_csv(clean_file)
        corr= np.corrcoef(tabl.height,tabl.weight)
        count_smoker= tabl[tabl['smoke']==1]['smoke'].count()
        with open('explor_info.txt', 'a') as exp_data:
            exp_data.write('\ncorrelation coefficient between height & weight for dataset is {}\n'.format(corr[0,1]))
            exp_data.write('Number of Smokers in dataset equals {}\n'.format(round(count_smoker,4)))
            exp_data.write('Find in folder images of exploration data for relevant columns\n')
        exp_data.close()
        feature=['height','weight',	'ap_hi','ap_lo','cholesterol']
        for i in feature:
            tabl.boxplot(i,'smoke')
            plt.title(i+' VS Smoke')
            plt.savefig('{}.png'.format(i))
        return tabl,  tabl.id.count() 
    




    def model_training(self, test_size=0.3):
         
         cat_feature=self.trans_data[['gender','cholesterol']]
         num_feature=self.trans_data[['bmi']]
         Label=self.trans_data['smoke']        
         
         X_train, X_test, y_train, y_test = train_test_split\
         (np.concatenate((cat_feature,num_feature),axis=1),Label, test_size=test_size)
         logreg=LogisticRegression()
         self.model=logreg.fit(X_train,y_train)
         y_pred=self.model.predict(X_test)
         score=logreg.score(X_test,y_test)
         cm=confusion_matrix(y_test, y_pred)
         with open('explor_info.txt', 'a') as train_data:
            train_data.write("\nModel Score with a test split of {} is {}".format(test_size,score))
            train_data.write("\nModel confusion matrix is {}".format(cm))
         train_data.close()
         return score, self.model
    
    def model_infer(self):
        """gender_feat (int): Values: 1 or 2. Input value for Gender; 1 for Male & 2 for Female
           cholest_feat(int): Input value between 1 & 3 for cholesterol
           height_feat(int): Enter your height in cm 
           weight_feat(int): Enter your weight in kg """
        gender_feat= 1
        cholest_feat= 3
        height_feat= 170
        weight_feat=90
        cat_feature=[[int(gender_feat),int(cholest_feat)]]
        bmi_feat= [[((int(weight_feat)/(int(height_feat)**2))**(1/2))]]
        
        infer_feat=np.concatenate((cat_feature,bmi_feat),axis=1)
        y_infer=self.model.predict(infer_feat)
        with open('explor_info.txt', 'a') as infer_data:
            infer_data.write('\n')
            infer_data.write("Prediction for your input data is {}, smoker and non-smoker represented by 0 & 1 respectively".format(y_infer))
        infer_data.close()
        return y_infer
        

    def email_opr(self, mailing_list, ml_files):
        from_addr = 'johncaul2@gmail.com'
        to_addr = mailing_list
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] =   ", ".join(to_addr) 
        msg['Subject'] = 'ML Process complete, Please view the files below'

        body = "Hello Everyone! This is test i like"
        files = ml_files
        msg.attach(MIMEText(body, 'plain'))
       

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)


        smtp_server = smtplib.SMTP('smtp.gmail.com', 587) #Specify Gmail Mail server

        smtp_server.ehlo() #Send mandatory 'hello' message to SMTP server

        smtp_server.starttls() #Start TLS Encryption as we're not using SSL.

        #Login to gmail: Account | Password
        smtp_server.login('******', '****')

        text = msg.as_string()

        #Compile email: From, To, Email body
        smtp_server.sendmail(from_addr, to_addr, text)
        smtp_server.quit()
        


