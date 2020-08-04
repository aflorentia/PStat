import pandas as pd

import hello
import database as db
import plots
import csvFiles


def main():

#---|      Step1 : Download the Files  |--------
#---------------------------------------------

    hello.download_files()


#--|  Step2 :  Create and Initialise my Database   |-------
#---------------------------------------------

    conn=db.create_connection()
    c=conn.cursor()
    db.create_db(c,conn)
    db.table_key(c,conn)                                                        #Anatrexe stin database =>  foreignKeys




#----|  Step3 : Initialise my tracking lists ==> 
#       these lists will keep the necessary records  =>
#       which plots will be drawn by using these lists  |-----
#-------------------------------------------------

    year=[]
    tt=[]
    transport=[]
    country=[]

#----|  Step4 : Proccess excel files one by one |-----
#-------------------------------------------------

    book=['2011','2012','2013','2014','2015']                                       #lista gia tin anatrexei twn excell

    for b in range (5) :
        month3=[]
        temp=0
        for s in range(2,12,3) :

            sheet=s
            df=pd.read_excel('text'+book[b]+'.xls',sheet_name=sheet,index_col=None,header=None)

            df.columns=['NO','COUNTRY','AIR','RAILWAY','SEA','ROAD','TOTAL']
            df=df.drop(columns=['NO'])
            df=df.dropna(thresh=6)
            df=df.set_index('COUNTRY')
            df=df.drop(index='of which:')
            df=df[['AIR','RAILWAY','SEA','ROAD','TOTAL']].astype('int')
            df=df.sort_values(by=['TOTAL'],ascending=False)


            i,j =df.shape       #diamensions
            i,j=i-1,j-1





#=======================================================================================================================
#--------------------------           |         By 3 Months           |       ------------------------------------------
#=======================================================================================================================
            temp=df.iloc[0,j]-temp
            month3.append(temp.tolist())                                        #    month3.append(temp)        ANAFORA
            temp=df.iloc[0,j]


        year.append(month3)
        db.update_month(conn,c,month3,b)

        print("By Year List",year)
        print("By 3Months List",month3)


#=======================================================================================================================
#--------------------------      |         PerYear|Total            |       --------------------------------------------
#=======================================================================================================================

        total=df.iloc[0,j]
        tt.append(total)

        total=total.tolist()
        db.update_year(conn,c,total,b)


        #print(total)
        #print(df.loc[df['TOTAL']==max(df['TOTAL'])])

#=======================================================================================================================
#------------------------------        |           Top5           |         --------------------------------------------
#=======================================================================================================================

        top=df.drop(index='TOTAL ARRIVALS').head(5)
        top=top.iloc[:,j]

        country.append(top)

        countries=top.index.tolist()
        db.update_top(conn,c,countries,b)

        #print(countries)
        #print(top)

#=======================================================================================================================
#--------------------------             |         Transportation           |            --------------------------------
#=======================================================================================================================

        tr=df.iloc[0,0:4]
        tr=tr.tolist()
        db.update_trans(conn,c,tr,b)

        transport.append(tr)                                                        # krataw lista gia ka8e etos => plot

#        print(transport)

#=======================================================================================================================
#==============================            |       TESTING     AREA      |           ===================================
#=======================================================================================================================

    #db.select_from(c,'month')

#=======================================================================================================================
#==============================================         |PLOTS|            =============================================
#=======================================================================================================================
    '''''
#        plots.plot_top(top,book,b)                                 #ektipwsi gia ka8e etos =>   parapono   &    allages
    top=pd.concat(country,keys=['2011','2012','2013','2014','2015'])                      #εναια εκτύπωση
    plots.plot_top(top,book,b)
    plots.plot_rail(transport)
    plots.plot_year(tt,book)    
    plots.plot_month3(year)
    plots.plt.show()
    '''
#=======================================================================================================================
#========================================        |Database Elements|            ========================================
#=======================================================================================================================


#    db.select_all(c)

    csvFiles.write(c)
    conn.close()



if __name__ == '__main__':
    main()