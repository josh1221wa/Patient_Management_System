# Patient_Management_System
During any pandemic the need arises for efficient and user-friendly documentation
programs to record all cases and deaths which can help us to predict the extent of said
pandemic.

Keeping the coronavirus in mind I designed this project which can keep records of patients,
available hospitals, and free beds and also count down the number of quarantine days for a
patient.

All major functions are stored in Funclib.py which is then called by Main.py.

Each patient is given a unique patient id which is automatically assigned to them. A
QRcode is also created which contains this patient id for easy and efficient identification.

The patient is assigned to a hospital with free beds and so the hospital loses a bed.

All these numbers are recorded into a csv file which is then used to make a line graph of
numbers vs dates to efficiently record the rise and fall of the pandemic

If any patient falls into a serious condition their data is entered into another csv file. This
feature enables doctors to have an understanding of high priority patients.

In the event of a death the data is sent into a different csv file, a bed is freed up in the
respective hospital and the numbers are updated for the statistical data chart.

This program also has a search feature which uses either the patient id input or an inbuilt
webcam QRcode scanner.

It also prints out records under various categories in a neat SQL table style format.
