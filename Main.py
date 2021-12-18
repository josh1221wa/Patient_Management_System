import FuncLib
import csv
import os
import time

print('\t\t\t',"Patient Management System",'\n')

mainmenu="1-Patient Menu\t\t\t\t\t\t0-Exit\n2-Hospital Menu\n3-Statistics\n4-Pass Day\n"
patientmenu="1-Add Patient\n2-Transfer Patient\n3-Update Patient Status\n4-Patient Reports\n5-Search Patient\n6-Add more observation time\n0-Back To Main Menu\n"
hospitalmenu="1-Add Hospital\n2-Hospital Reports\n0-Back to Main Menu\n"
updatepatientstat="1-Patient Recovered\t\t\t\t\t\t0-Exit\n2-Patient Critical\n3-Patient Dead"
menu="main"
close=0
date=""

while True:
    while menu=="main":
        FuncLib.printdate(1)
        print(mainmenu)
        ch=int(input("Enter Choice: "))
        if ch==0:
            close=1
            os.system('cls')
            break
            
        if ch==1:
            menu="patient"
            continue
        elif ch==2:
            menu="hospital"
            continue
        elif ch==3:
            FuncLib.statistics()
            continue
        elif ch==4:
            FuncLib.passday()
            continue
        print("Invalid Choice")

    while menu=="patient":
        FuncLib.printdate(1)
        print(patientmenu)
        ch=int(input("Enter Choice: "))
        if ch==0:
            menu="main"
            os.system('cls')   #Clears screen 
            continue
        if ch==1:
            date=FuncLib.printdate()
            with open("Hospital.csv","r") as csv_file:
                csv_reader=csv.reader(csv_file)
                list1=list(csv_reader)
            for i in list1[1:]:
                if int(i[3])!=0:
                    break
            else:
                print("No hospital available")
                time.sleep(3)
                continue
            FuncLib.addpatient(date)
            continue
        elif ch==2:
            pid=input("Enter Patient ID: ")
            FuncLib.transferpatient(pid)
            continue
        elif ch==4:
            FuncLib.patient_reports()
            continue
        elif ch==5:
            FuncLib.search()
            continue
        elif ch==6:
            pid=input("Enter patient ID: ")
            FuncLib.adddaystopatient(pid)
            continue
        while True:
            os.system('cls')
            FuncLib.printdate(1)
            print(updatepatientstat)
            ch=int(input("Enter Choice: "))                                                      
            if ch==0:
                break
            date=FuncLib.printdate()
            if ch==1:
                pid=input("Enter Patient ID: ")
                FuncLib.patientrecovered(pid,date)
                continue
            elif ch==2:
                pid=input("Enter Patient ID: ")
                FuncLib.patientcriticalcond(pid,date)
                continue
            elif ch==3:
                pid=input("Enter Patient ID: ")
                FuncLib.patientdead(pid,date)
                continue
            print("Inavlid Choice")

    while menu=="hospital":
        FuncLib.printdate(1)
        print(hospitalmenu)
        ch=int(input("Enter Choice: "))
        if ch==0:
            os.system('cls')
            menu="main"
            continue
        os.system('cls')
        if ch==1:
            FuncLib.addhospital()
            continue
        elif ch==2:
            FuncLib.hospital_reports()
            continue
        print("Invalid Choice")


    if close==1:
        break
print("\n\nThank You For Using Patient Management System")
time.sleep(3)
