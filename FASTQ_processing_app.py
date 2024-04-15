import os 
import re 
from Bio import SeqIO
import pandas as pd 
import PySimpleGUI as sg
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

import copy
import os
import shutil
import os.path
import glob

# reference folder global
Out_folder="Fastas"
parent_path=os.getcwd()
Out_folder=os.path.join(parent_path,Out_folder)
if not os.path.exists(Out_folder):
        os.makedirs(Out_folder)
else:
        ref_folder=Out_folder
def store_fastas (file):
   
    global Out_folder

    
    

   
    shutil.move(file,Out_folder)
    return(Out_folder)

def process_FQS(dict_path,forward_primer,reverse_primer):
    files=os.listdir(dict_path)





    R1=list(filter(lambda k: 'R1' in k, files))


    R2=list(filter(lambda k: 'R2' in k, files))


    R1_seqs=list()
    for i in R1:
        for seqrecord in SeqIO.parse(dict_path+"/" +i, "fastq"):
            R1_seqs.append(seqrecord.seq)
        
    R2_seqs=list()
    for i in R2:
        for seqrecord in SeqIO.parse(dict_path+"/" +i, "fastq"):
            R2_seqs.append(seqrecord.seq)


    trimmed_R1_seqs=list()  
    for i in R1_seqs:
        trimmed_R1_seq=i.replace(forward_primer,"") 
        trimmed_R1_seqs.append(trimmed_R1_seq)     
        trimmed_R1_seqs_strings=list()
        for i in trimmed_R1_seqs:
         string=str(i)
         trimmed_R1_seqs_strings.append(string)
  
    trimmed_R2_seqs=list()  
    for i in R2_seqs:
      trimmed_R2_seq=i.replace(reverse_primer,"") 
      trimmed_R2_seqs.append(trimmed_R2_seq)

      trimmed_R2_seqs_strings=list()
    for i in trimmed_R2_seqs:
      string=str(i)
      trimmed_R2_seqs_strings.append(string)
    
    joined=list()
    for i in range(len(trimmed_R1_seqs_strings)):
     
         joined_seq =trimmed_R2_seqs_strings[i]+trimmed_R1_seqs_strings[i]
         joined.append(joined_seq)
    seq_ids=list()
    for i in range(len(joined)):
        seq_id="seq"+ str(i) +".fasta"
        seq_ids.append(seq_id)
    indentifier_lines=list()
    for i in range(len(seq_ids)):
        indentifier_line= ">"+seq_ids[i]+"\n"
        indentifier_lines.append(indentifier_line)      
    sequence_lines=list()
    for i in joined:
        sequence_line=i + "\n" 
        sequence_lines.append(sequence_line)
    
    output_paths=list()
    fasta_files=list()
    for i in range(len(joined)):
               parent_path=os.getcwd()
               output_path=os.path.join(parent_path,seq_ids[i])
               
               output_file = open(output_path,'w')
               output_file.write(indentifier_lines[i])
               output_file.write(sequence_lines[i])
               output_file.close()
               fasta_files.append(output_file)
               output_paths.append(output_path)
    
    

              
              
            
    
    for i in output_paths :
        store_fastas(i)
              
    return(Out_folder)          
        




sg.theme('Reddit')
layout =  [ [sg.Text( " Process demultiplexed FASTQ files "), sg.Input(),sg.FolderBrowse(key="-IN-")],[sg.Submit()],[sg.Cancel()],[sg.Text('forward primer', size =(15, 1)), sg.InputText(key="_forward_")],
[sg.Text('Reverse Primer ', size =(15, 1)), sg.InputText(key="_reverse_")]]


        
newlayout = copy.deepcopy(layout)
window = sg.Window('Submit a folder with demultiplexed FASTQ files  and  the reverse and forward primers', newlayout, size=(270*4,4*100))
event, values = window.read()

while True:
    event, values = window.read()
    print(event, values)
    
    if event == 'Cancel':
        break
    elif event == 'Submit':
        
       
         dict_path= values["-IN-"]
         forward_primer= values["_forward_"]
         reverse_primer= values["_reverse_"]
         if dict_path:
    
            output =   process_FQS(dict_path,forward_primer,reverse_primer)
         
            break
window.close()

if output:
        my_w = tk.Tk()
        my_w.geometry("400x300")  # Size of the window 
        my_w.title('Save fastas in folder')
        my_font1=('times', 18, 'bold')
        l2 = tk.Label(my_w,text='Save Folder',width=30,font=my_font1)
        l2.grid(row=3,column=1)
        def save_folder():
            print("Save folder pressed: ", Out_folder)
            destFolder = filedialog.askdirectory()
            print("Destination folder: ", destFolder)
            if (os.path.exists(Out_folder) and os.path.exists(destFolder)):
                shutil.copytree(Out_folder, destFolder, dirs_exist_ok=True)
        b2 = tk.Button(my_w, text='Save', 
        width=20,command = lambda:save_folder())
        b2.grid(row=4,column=1)    
        
        b3=tk.Button(my_w, text="Quit", command=my_w.destroy)
        b3.grid(row = 6, column=1)    
        my_w.mainloop()  # Keep the window open   
