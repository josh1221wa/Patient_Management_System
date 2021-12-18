import csv
import matplotlib.pyplot as plt
import pickle
import pyqrcode
import cv2
import pyzbar.pyzbar as pyzbar
import os
import time


def convertor(n): #changes string date to the following date
    dd=n[0:2]
    mm=n[3:5]
    yy=n[6:]
    if dd=="30" and mm in ["04","06","09","11"]:
        dd="01"
        mm=str(int(mm)+1)
    elif dd=="31" and mm in ["01","03","05","07","08","10"]:
        dd="01"
        mm=str(int(mm)+1)
    elif dd=="28" and mm=="02":
        if int(yy)%4==0 or int(yy)%400==0:  #checks wether year is a leap year
            dd="29"
        else:
            dd="01"
            mm="03"
    elif dd=="29" and mm=="02":
        dd="01"
        mm="03"
    elif dd=="31" and mm=="12":
        dd="01"
        mm="01"
        yy=int(yy)+1
    else:
        dd1=str(int(dd)+1)
        dd="0"*(2-len(dd1))+dd1
    return dd+'-'+mm+'-'+yy


def addhospital():  #adds a hospital to Hospital.csv
    name=input("Enter hospital name: ")
    place=input("Enter hospital place: ")
    num_beds=input("Enter number of beds available: ") #number of beds decrease as number of patients increase
    while True:
        owner=input("Enter wether Private/Govt.(P/G): ")
        if owner in ["P","G"]:
            break
        else:
            print("\nCan only enter P/G\n")
    with open("Hospital.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list1=list(csv_reader)
        while True:
            list2=[]
            codinp=input("Assign hospital code.3 characters only and no spaces: ")
            lis=codinp.split()
            code=lis[0]
            if len(code)==3:
                for i in list1[1:]:
                    list2.append(i[0])
                if code in list2:
                    print('\nCode already taken\n')  #hospital code is unique for each hospital
                else:
                    break
            else:
                ("Code should have 3 characters only")
    list2=[code,name,place,num_beds,owner]
    with open("Hospital.csv","a",newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerow(list2)
    print("\nHospital succesfully added\n")
    time.sleep(3)


def addpatient(date):   #To add patient to Patient.csv
    name=input("Enter patient name: ")
    days="18"           #Number of days left in quarantine
    place=input("Enter place of residence: ")
    phone_number=input("Enter phone number: ")
    phone_number2=input("Enter phone number of family member: ")
    with open("Patient.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list1=list(csv_reader)
    with open("Num.dat","rb") as f:  #Patient id is automatically assigned with a value in Num
        lst=pickle.load(f)
        id_number=lst[0]             #The value in Num.dat is increased by 1
    a=str(int(lst[0])+1)
    plist="0"*(10-len(a))+a         
    lst=[plist]
    with open("Num.dat","wb+") as f:
        pickle.dump(lst,f)
    with open("Hospital.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list1=list(csv_reader)   
        for i in list1[1:]:             
            if int(i[3])!=0:                 #The first hospital with a bed free is assigned the patient
                hospital_code=i[0]
                i[3]=str(int(i[3])-1)         #In-turn the number of beds in that hospital decreases by one
                break
    with open("Hospital.csv","w+",newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerows(list1)
    patientlist=[date,id_number,name,place,phone_number,phone_number2,hospital_code,days]
    with open("Patient.csv","a",newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerow(patientlist)
    url=pyqrcode.create(id_number)            #a qrcode is created with the patient id
    if not os.path.exists("QRCODE"):          #Code checks if a directory "QRCODE" is present
        os.mkdir("QRCODE")                  #if not it is created 
    a="QRCODE\\"+id_number+".png"           
    url.png(a,scale=6)                      #qrcode is saved in png format in QRCODE directory
    with open("Daily Numbers.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)         #Daily Numbers.csv is updated so infected increases by 1
        list1=list(csv_reader)
    for i in list1[1:]:
        if i[0]==date:
            i[2]=str(int(i[2])+1)
            break
    with open ("Daily Numbers.csv","w",newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerows(list1)
    print("\nPatient succesfully added to records\n") 
    time.sleep(3)

    
def adddaystopatient(pid):         #the number of days left for quarantine is updated
    with open ("Patient.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list1=list(csv_reader)
    for i in list1[1:]:
        if i[1]==pid:
            days=int(input("Enter number of days to be added: "))
            i[7]=str(int(i[7])+days)
            print("\nObservation days updated\n")
            time.sleep(3)
            with open ("Patient.csv","w",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)
                csv_writer.writerows(list1)
            break
    else:
        print("\nID not found\n")
        time.sleep(3)


def transferpatient(pid):          #Transfer patient to a new hospital
    with open ("Patient.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list1=list(csv_reader)
    with open ("Hospital.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list2=list(csv_reader)

    for i in list1[1:]:
        if i[1]==pid:
            a=i[6]
            for j in list2[1:]:
                if a==j[0]:
                    print("\nPatient's current hospital is:",j[0],":",j[1],"\n")
                    break
            else:
                print("\nPatient ID not found\n")
                time.sleep(3)
            ch=input("Do you want to transfer patient? Enter Y/N: ")
            availlist=[]
            if ch=="Y":
                print("\nThese are the available hospitals\n")
                for j in list2[1:]:             #All hospitals with beds available are taken into consideration
                    if int(j[3])>0:                             
                        print(j[1],(50-len(j[1]))*" ",":",j[0])
                        availlist.append(j)                     
                while True:
                    newhosp=input("Enter code of new hospital: ")
                    for j in availlist:
                        if newhosp==j[0]:
                            i[6]=newhosp
                            for k in list2[1:]:
                                if k[0]==a:
                                    k[3]=str(int(k[3])+1)       #Old hospital gets a freed up bed
                                if k[0]==newhosp:
                                    k[3]=str(int(k[3])-1)       #New hospital gets one bed less
                                    break
                            print("\nPatient has been transferred\n")
                            time.sleep(3)
                            break
                    else:
                        print("\nWrong hospital code\n")
                        time.sleep(3)
                        continue
                    break
    with open ("Patient.csv","w",newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerows(list1)
    with open ("Hospital.csv","w",newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerows(list2)


def patientdead(pid,date):              #If a patient dies
    with open ("Patient.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list1=list(csv_reader)
    with open ("Patient Critical Condition.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list2=list(csv_reader)
    with open ("Hospital.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list4=list(csv_reader)
    for i in list1[1:]:   #If patient records are in Patient.csv
        if i[1]==pid:
            for j in list4:
                if j[0]==i[6]:
                    j[3]=str(int(j[3])+1)       #The hospital gets a bed freed up
                    with open ("Hospital.csv","w+",newline='') as csv_file:
                        csv_writer=csv.writer(csv_file)
                        csv_writer.writerows(list4)
                    break
            list3=[date,i[1],i[2],i[3],i[5],i[6]]           
            list1.remove(i)
            with open ("Patient.csv","w+",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)
                csv_writer.writerows(list1)             #Patient records are removed from Patient.csv
            with open ("Dead.csv","a",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)
                csv_writer.writerow(list3)                      #Records are added to Dead.csv
            with open("Daily Numbers.csv","r") as csv_file:
                csv_reader=csv.reader(csv_file)
                list1=list(csv_reader)                          #Daily Numbers.csv gets updated with the death
            for i in list1[1:]:
                if i[0]==date:
                    i[3]=str(int(i[3])+1)
                    break
            with open ("Daily Numbers.csv","w",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)
                csv_writer.writerows(list1)
            print("\nDeath registered\n")
            time.sleep(3)
            break
    else:               #If patient records are in Patient Critical Condition.csv
        for i in list2[1:]:
            if i[1]==pid:
                for j in list4:
                    if j[0]==i[6]:
                        j[3]=str(int(j[3])+1)
                        with open ("Hospital.csv","w+",newline='') as csv_file:
                            csv_writer=csv.writer(csv_file)
                            csv_writer.writerows(list4)
                        break
                list3=[date,i[1],i[2],i[3],i[5],i[6]]
                list2.remove(i)
                with open("Daily Numbers.csv","r") as csv_file:
                    csv_reader=csv.reader(csv_file)
                    list1=list(csv_reader)
                for i in list1[1:]:
                    if i[0]==date:
                        i[3]=str(int(i[3])+1)
                        break
                with open ("Daily Numbers.csv","w",newline='') as csv_file:
                    csv_writer=csv.writer(csv_file)
                    csv_writer.writerows(list1)
                with open ("Patient Critical Condition.csv","w+",newline='') as csv_file:
                    csv_writer=csv.writer(csv_file)
                    csv_writer.writerows(list2)
                with open ("Dead.csv","a",newline='') as csv_file:
                    csv_writer=csv.writer(csv_file)
                    csv_writer.writerow(list3)
                print("\nDeath registered\n")
                time.sleep(3)
                break
        else:
            print("\nSuch a patient doesn't exist\n")   #If patient records are not found  in Patient.csv or Patient Critical Condition.csv
            time.sleep(3)


def patientrecovered(pid,date):   #If patient has recovered
    with open ("Patient.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list1=list(csv_reader)
    with open ("Patient Critical Condition.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list2=list(csv_reader)
    with open ("Hospital.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list4=list(csv_reader)
    for i in list1[1:]:    #If patient records are in Patient.csv
        if i[1]==pid:
            for j in list4:
                if j[0]==i[6]:
                    j[3]=str(int(j[3])+1)    #Hospital gets a bed freed up
                    with open ("Hospital.csv","w+",newline='') as csv_file:
                        csv_writer=csv.writer(csv_file)
                        csv_writer.writerows(list4)
                    break
                
            list3=[date,i[1],i[2],i[3],i[4],i[5],i[6]]
            list1.remove(i)
            with open ("Patient.csv","w+",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)     #Patient records are reoved from Patient.csv
                csv_writer.writerows(list1)
            with open ("Recovered.csv","a",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)     #Records are moved into Recovered.csv
                csv_writer.writerow(list3)
            with open("Daily Numbers.csv","r") as csv_file:
                csv_reader=csv.reader(csv_file)
                list1=list(csv_reader)
            for i in list1[1:]:
                if i[0]==date:
                    i[1]=str(int(i[1])+1)       #Daily Numbers are updated
                    break
            with open ("Daily Numbers.csv","w",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)
                csv_writer.writerows(list1)
            print("\nPatient Recovery status updated\n")
            time.sleep(3)
            break
    else:           #If patient records are in Patient Critical Condition.csv
        for i in list2[1:]:
            if i[1]==pid:
                for j in list4:
                    if j[0]==i[6]:
                        j[3]=str(int(j[3])+1)
                        break
                list3=[date,i[1],i[2],i[3],i[5],i[6]]
                list2.remove(i)
                with open ("Patient Critical Condition.csv","w+",newline='') as csv_file:
                    csv_writer=csv.writer(csv_file)
                    csv_writer.writerows(list2)
                with open ("Recovered.csv","a",newline='') as csv_file:
                    csv_writer=csv.writer(csv_file)
                    csv_writer.writerow(list3)
                with open("Daily Numbers.csv","r") as csv_file:
                    csv_reader=csv.reader(csv_file)
                    list1=list(csv_reader)
                for i in list1[1:]:
                    if i[0]==date:
                        i[1]=str(int(i[1])+1)
                        break
                with open ("Daily Numbers.csv","w",newline='') as csv_file:
                    csv_writer=csv.writer(csv_file)
                    csv_writer.writerows(list1)
                print("\nPatient Recovery status updated\n")
                time.sleep(3)
                break
        else:
            print("\nSuch a patient doesen't exist\n")      #If patient records are not in Patient Critical Condition.csv and Patient.csv
            time.sleep(3)


def patientcriticalcond(pid,date): #If patient is in critical condition
    with open ("Patient.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        list1=list(csv_reader)
    for i in list1[1:]:
        if i[1]==pid:
            list2=[date,pid,i[2],i[3],i[4],i[5],i[6]]
            list1.remove(i)
            with open ("Patient.csv","w+",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)
                csv_writer.writerows(list1)     #Records are removed from Patient.csv
            with open ("Patient Critical Condition.csv","a",newline='') as csv_file:
                csv_writer=csv.writer(csv_file)  
                csv_writer.writerow(list2)   #Records are added to Patient Critical Condition.csv
            print("\nPatient status updated\n")
            time.sleep(3)
            break
    else:
        print("\nSuch a patient doesnt exist\n")
        time.sleep(3)


def statistics():    #To show graph of Daily Numbers
    with open("Daily Numbers.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list1=list(csv_reader)
    x1=[]    #x and y axes of first plot
    y1=[]
    for i in list1[1:]:
        x1.append(i[0])
        y1.append(int(i[2]))
    with open("Daily Numbers.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list1=list(csv_reader)
    x2=[]       #x and y axes of second plot
    y2=[]
    for i in list1[1:]:
        x2.append(i[0])
        y2.append(int(i[1]))
    with open("Daily Numbers.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list1=list(csv_reader)
    x3=[]       #x and y axes of third plot
    y3=[]
    for i in list1[1:]:
        x3.append(i[0])
        y3.append(int(i[3]))
    plt.plot(x1,y1,label="Infected")
    plt.plot(x2,y2,label="Recovered")
    plt.plot(x3,y3,label="Dead")
    plt.xlabel('Dates')  #x axis label
    plt.xticks(rotation=90)
    plt.subplots_adjust(left=0.064, bottom=0.198, right=0.9, top=0.957, wspace=0.2, hspace=0.2)
    plt.ylabel=('Number')       #y axis label
    plt.title("Stats")      #Graph Heading
    plt.legend()    #Shows legend
    plt.show()


def passday():   #When the day is passed to the next
    with open (r"\Date.dat","rb") as f:
        list1=pickle.load(f)
        n=list1[0]
    date=convertor(n)  #Date is converted to following day
    with open('Date.dat',"wb+") as f:
        list1=[date]
        pickle.dump(list1,f)
    with open("Daily Numbers.csv","a",newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerow([date,0,0,0])  #Daily Numbers.csv gets an additional row with the date
    with open ('Patient.csv','r') as f:
        csv_reader=csv.reader(f)
        list1=list(csv_reader)
        for i in list1[1:]:
            i[7]=str(int(i[7])-1)     #The quarantine days are decreased by 1 for each patient
        with open ('Patient.csv','w',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerows(list1)
        for i in list1[1:]:
            if int(i[7])==0:    #Checks if any patient's quarantine period is over
                print("\nThe patient's observation period has ended\n")    #If over two options are given
                print("1. Release Patient")
                print("2. Add more time for observation")
                while True:
                    ch=int(input("Enter choice: "))
                    if ch==1:
                        patientrecovered(i[1],date)         #Patient is released
                        break
                    elif ch==2:
                        adddaystopatient(i[1])          #Quarantine is extended
                        break
                    else:
                        print('\nWrong input. Enter again\n')
                        
def search():       #Searches for a patient
    print("\n1.Search via ID")  
    print("2. Scan QRCODE")
    print("0.Exit")
    while True:
        ch=int(input("Enter choice: "))
        if ch==1:       #If the patient id is entered
            pid=input('Enter ID: ')
            break
        elif ch==2:
            cap=cv2.VideoCapture(0)  #The default webcam is set to capture
            qrpid=''   #Identifier stores the data from the qrcode
            while True:
                _, frame=cap.read()   #Captures every frame
                decoded=pyzbar.decode(frame)    #Iterates through the frame and qrcode data is stored in array
                for i in decoded:       #Iterates through the array 
                    i=i.data.decode("utf-8")    #IMPORTANT:Converts b' type into str type
                    qrpid+=i    #Decoded data is added to identifier
                    if len(qrpid)>0:    #If the identifier contains string the loop is broken
                        break
                cv2.imshow("Scanner",frame)    #The camera input is shown in a window
                key=cv2.waitKey(1)    #The window is kept open till destroyed
                if len(qrpid)>0:
                    cap.release()    #The camera is released
                    cv2.destroyWindow('Scanner')    #The window is destroyed 
                    break
            pid=qrpid
            break
        elif ch==3:
            break
    with open ("Patient.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list1=list(csv_reader)
    with open ("Patient Critical Condition.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list2=list(csv_reader)
    with open ("Dead.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list3=list(csv_reader)
    with open ("Recovered.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file)
        list4=list(csv_reader)
    with open ("Hospital.csv","r") as f:
        csv_reader=csv.reader(f)
        list5=list(csv_reader)
    for i in list1[1:]:
        if i[1]==pid:
            for j  in list5[1:]:
                if  i[6]==j[0]:
                    hospname=j[1]
            print('\nPatient Name: ',i[2])
            print("\nPatient is stable in ",hospname,"and was admitted on ",i[0],"and has",i[7],"days left under observation\n")
            break
    else:
        for i in list2[1:]:
            if i[1]==pid:
                for j  in list5[1:]:
                    if  i[6]==j[0]:
                        hospname=j[1]
                print('\nPatient Name: ',i[2])    
                print("\nPatient is in a critical condition in ",hospname,'. The ptients condition spiked on',i[0],"\n")
                break
        else:
            for i in list3[1:]:
                if i[1]==pid:
                    for j  in list5[1:]:
                        if  i[5]==j[0]:
                            hospname=j[1]
                    print('\nPatient Name: ',i[2])  
                    print("\nPatient died on ",i[0]," in  ",hospname,"\n")
                    break
            else:
                for i in list4[1:]:
                    if i[1]==pid:
                        for j  in list5[1:]:
                            if  i[6]==j[0]:
                                hospname=j[1]
                        print('\nPatient Name: ',i[2])  
                        print ("\nPatient recovered in ",hospname,"on",i[0],"\n")
                        break
                else:
                    print("\nPatient not recorded\n")
def patient_reports():
    print("\n1.All records")
    print("2.Dead patients")
    print("3.Recovered Patients")
    print("4.Stable patients")
    print("5.Serious Patients")
    print("6.All Entries by Date")
    print("7.All active patients in a hospital\n")
    ch=int(input("Enter choice: "))
    with open("Patient.csv",'r') as f:
        csv_reader=csv.reader(f,delimiter=',')
        list1=list(csv_reader)
    with open("Dead.csv",'r') as f:
        csv_reader=csv.reader(f,delimiter=',')
        list2=list(csv_reader)
    with open("Patient Critical Condition.csv",'r') as f:
        csv_reader=csv.reader(f,delimiter=',')
        list3=list(csv_reader)
    with open("Recovered.csv",'r') as f:
        csv_reader=csv.reader(f,delimiter=',')
        list4=list(csv_reader)
    with open("Daily Numbers.csv","r") as f:
        csv_reader=csv.reader(f,delimiter=',')
        list5=list(csv_reader)
    with open("Hospital.csv","r") as f:
        csv_reader=csv.reader(f,delimiter=',')
        list6=list(csv_reader)
    if ch==1:
        c=0
        print("\n"+"Stable Patients\n")
        print("+",152*"-","+")
        for i in list1[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        print("+",152*"-","+")
        for i in list1[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        if c==0:
            print("\n No Stable Patients \n")
        print("+",152*"-","+")
        print("\n"+"Dead"+"\n")
        c=0
        print("+",133*"-","+")
        for i in list2[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(35-len(i[4]))*' ',"|",i[5],(15-len(i[5]))*" ","|")
        print("+",133*"-","+")
        for i in list2[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(35-len(i[4]))*' ',"|",i[5],(15-len(i[5]))*" ","|")
        if c==0:
            print("\nNo Dead Patients\n")
        print("+",133*"-","+")
        print("\n"+"Critical Condition"+"\n")
        c=0
        print("+",152*"-","+")
        for i in list3[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        print("+",152*"-","+")
        for i in list3[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        if c==0:
            print("\nNo patients in critical condition\n")
        print("+",152*"-","+")
        print('\n'+"Recovered"+'\n')
        c=0
        print("+",152*"-","+")
        for i in list4[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        print("+",152*"-","+")
        for i in list4[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        if c==0:
            print("\nNo recovered patients\n")
        print("+",152*"-","+")
    if ch==2:
        c=0
        print("\n"+"Dead"+"\n")
        print("+",133*"-","+")
        for i in list2[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(35-len(i[4]))*' ',"|",i[5],(15-len(i[5]))*" ","|")
        print("+",133*"-","+")
        for i in list2[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(35-len(i[4]))*' ',"|",i[5],(15-len(i[5]))*" ","|")
        if c==0:
            print("\nNo dead patients\n")
        print("+",133*"-","+")
    if ch==3:
        c=0
        print('\n'+"Recovered"+'\n')
        print("+",152*"-","+")
        for i in list4[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        print("+",152*"-","+")
        for i in list4[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        if c==0:
            print("\nNo recovered patients\n")
        print("+",152*"-","+")
    if ch==4:
        c=0
        print("\n"+"Stable Patients")
        print("+",152*"-","+")
        for i in list1[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        print("+",152*"-","+")
        for i in list1[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        if c==0:
            print("\nNo stable patients\n")
        print("+",152*"-","+")
    if ch==5:
        c=0
        print("\n"+"Critical Condition"+"\n")
        print("+",152*"-","+")
        for i in list3[0:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        print("+",152*"-","+")
        for i in list3[1:]:
            c+=1
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(10-len(i[1]))*" ","|",i[2],(25-len(i[2]))*" ","|",i[3],(12-len(i[3]))*" ","|",i[4],(15-len(i[4]))*' ',"|",i[5],(35-len(i[5]))*' ',"|",i[6],(15-len(i[6]))*" ","|")
        if c==0:
            print("\nNo critical patients\n")
        print("+",152*"-","+")
    if ch==6:
        dat=input("Enter date to search in DD-MM-YYYY: ")
        for i in list5:
            if i[0]==dat:
                if int(i[1])>0:
                    print("\nRecovered"+"\n")
                    print("+",133*"-","+")
                    for j in list4[:1]:
                        print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(15-len(j[4]))*' ',"|",j[5],(35-len(j[5]))*' ',"|",j[6],(15-len(j[6]))*" ","|")
                    print("+",133*"-","+")
                    for j in list4[1:]:
                        if j[0]==dat:
                            print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(15-len(j[4]))*' ',"|",j[5],(35-len(j[5]))*' ',"|",j[6],(15-len(j[6]))*" ","|")
                    print("+",133*"-","+")
                else:
                    print("\nNo Recovered Patients\n")
                if int(i[2])>0:
                    print("\nInfected\n")
                    print("+",133*"-","+")
                    for j in list1[:1]:
                        print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(15-len(j[4]))*" ","|",j[5],(35-len(j[5]))*" ","|",j[6],(15-len(j[6]))*" ","|")
                    print("+",133*"-","+")
                    for j in list1[1:]:
                        if j[0]==dat:
                            print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(15-len(j[4]))*" ","|",j[5],(35-len(j[5]))*" ","|",j[6],(15-len(j[6]))*" ","|")
                    print("+",133*"-","+")              
                else:
                    print("\nNo Infected Patients\n")
                if int(i[3])>0:
                    print("\nDead\n")
                    print("+",114*"-","+")
                    for j in list2[:1]:
                        print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(35-len(j[4]))*' ',"|",j[5],(15-len(j[5]))*" ","|")
                    print("+",114*"-","+")
                    for j in list2[1:]:
                        if j[0]==dat:
                            print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(35-len(j[4]))*' ',"|",j[5],(15-len(j[5]))*" ","|")
                    print("+",114*"-","+")
                else:
                    print("\nNo Deaths\n")
                break
        else:
            print("\nThis date has not been recorded\n")
    if ch==7:
        c=0
        for i in list6:
            print(i[0],"\t",i[1])
        hosp=input("Enter hospital code: ")
        print("+",128*"-","+")
        for j in list1[:1]:
            print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(15-len(j[4]))*" ","|",j[5],(35-len(j[5]))*" ","|","Status",4*" ","|")
        print("+",128*"-","+")
        for j in list1[1:]:
            if j[6]==hosp:
                c+=1
                print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(15-len(j[4]))*" ","|",j[5],(35-len(j[5]))*" ","|","Stable",4*" ","|")
        if  c>0:
            print("+",128*"-","+")
        for j in list3[1:]:
            if j[6]==hosp:
                c+=1
                print("|",j[1],(10-len(j[1]))*" ","|",j[2],(25-len(j[2]))*" ","|",j[3],(12-len(j[3]))*" ","|",j[4],(15-len(j[4]))*" ","|",j[5],(35-len(j[5]))*" ","|","Serious",3*" ","|")
        if c==0:
            print("\nNo active cases in this hospital\n")
        print("+",128*"-","+")

        
def hospital_reports():
    print("\n1. All hospitals")
    print("2. All private hospitals")
    print("3. All Government hospitals")
    print("4. All full hospitals")
    print("5. Hospitals with beds available\n")
    ch=int(input('Enter choice: '))
    with open("Hospital.csv","r") as f:
        csv_reader=csv.reader(f,delimiter=',')
        list1=list(csv_reader)
    if ch==1:
        print("+",129*"-","+")
        for i in list1[:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[3],(17-len(i[3]))*" ","|",i[4],(20-len(i[4]))*" ","|")
        print("+",129*"-","+")
        for i in list1[1:]:
            if i[4]=="P":
                i[4]="Private"
            else:
                i[4]="Government"
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[3],(17-len(i[3]))*" ","|",i[4],(20-len(i[4]))*" ","|")
        if len(list1)==1:
            print("\nNo hospitals recorded\n")
        print("+",129*"-","+")
    if ch==2:
        c=0
        print("+",105*"-","+")
        for i in list1[:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[3],(17-len(i[3]))*" ","|")
        print("+",105*"-","+")
        for i in list1[1:]:
            if i[4]=="P":
                c+=1
                print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[3],(17-len(i[3]))*" ","|")
        if c==0:
            print("\nNo private hospitals\n")
        print("+",105*"-","+")
    if ch==3:
        c=0
        print("+",105*"-","+")
        for i in list1[:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[3],(17-len(i[3]))*" ","|")
        print("+",105*"-","+")
        for i in list1[1:]:
            if i[4]=="G":
                c+=1
                print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[3],(17-len(i[3]))*" ","|")
        if c==0:
            print("\nNo Government hospitals\n")
        print("+",105*"-","+")
    if ch==4:
        c=0
        print("+",108*"-","+")
        for i in list1[:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[4],(20-len(i[4]))*" ","|")
        print("+",108*"-","+")
        for i in list1[1:]:
            if i[4]=="P":
                i[4]="Private"
            else:
                i[4]="Government"
            if int(i[3])==0:
                c+=1
                print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[4],(20-len(i[4]))*" ","|")
        if c==0:
            print("\nNo full Hospitals\n")
        print("+",108*"-","+")
    if ch==5:
        c=0
        print("+",108*"-","+")
        for i in list1[:1]:
            print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[4],(20-len(i[4]))*" ","|")
        print("+",108*"-","+")
        for i in list1[1:]:
            if i[4]=="P":
                i[4]="Private"
            else:
                i[4]="Government"
            if int(i[3])>0:
                c+=1
                print("|",i[0],(15-len(i[0]))*" ","|",i[1],(50-len(i[1]))*" ","|",i[2],(10-len(i[2]))*" ","|",i[4],(20-len(i[4]))*" ","|")
        if c==0:
            print("\nNo empty Hospitals\n")
        print("+",108*"-","+")


def printdate(x=0):    #Date from Date.dat is inserted into an identifier
    with open ("Date.dat","rb") as f:
        list1=pickle.load(f)
        n=list1[0]
        if x==0:
            global date
            date=n
            return date
        elif x==1:
            print('\n',n,'\n')
