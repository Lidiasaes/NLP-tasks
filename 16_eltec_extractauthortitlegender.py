# -*- coding: utf-8 -*-
"""ELTeC_ExtractAuthorTitleGender.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/baltuna/LT4DH/blob/main/ELTeC_ExtractAuthorTitleGender.ipynb

# Extracting author, title and gender and more from ELTeC corpus

Adaptation of a great Colab by Borja Navarro for the LT4DH course in the University of the Basque Country.

This version (to be cleaned) uses English resources in contrast to the Spanish one used by Borja Navarro.

Original reference here:

Borja Navarro Colorado | University of Alicante

This notebook contains basic Python code to extract information from the ELTeC corpus (https://github.com/COST-ELTeC)

## Loading ELTeC corpus in Colab

Only ELTeC-ENG will be loaded.

Corpus URL is https://github.com/COST-ELTeC/ELTeC-eng > "code" > copy "Download ZIP"

To load other collection (other languages): https://github.com/COST-ELTeC
"""

import zipfile

!wget "https://github.com/COST-ELTeC/ELTeC-eng/archive/refs/heads/master.zip" # paste here corpus url

zip_ref = zipfile.ZipFile('master.zip', 'r') #Opens the zip file in read mode
zip_ref.extractall() #Extracts files here (/content/)
zip_ref.close() 
!rm master.zip #Removes ZIP to save space

"""Now, the novels with the XML-TEI annotation are in this directory:

/content/ELTeC-eng-master/level1/

It is the level 1 that contains novels annotated with XML-TEI tags: header, structure and other textual data. See encoding guidelines:

https://distantreading.github.io/Training/Budapest/encodingGuide-1.html

https://distantreading.github.io/Training/Budapest/encodingGuide-2.html#(1)

Level 0 will contain novels in plain texts (currently is empty)

Leve 2 will contain novels annotated with Part of Speech and lemmas (soon).

## List the files

To see the files of each novel, we can iterate over the directory "level1":
"""

import os

dir_in = "/content/ELTeC-eng-master/level1/"

for base, directorios, ficheros in os.walk(dir_in): #Go through directory and open file one by one
  for fichero in ficheros: #the iteration begins
    if fichero[0:3] == "ENG": #to avoid open README file
      print(fichero) # to see the name of each file

"""## Open each file and extract informatio about author and title

To parse XML tags, we will use BeautifulSoup 4:

https://beautiful-soup-4.readthedocs.io/en/latest/#quick-start

This script is similar to the previous one, but it includes how to open each file and extract information.
"""

from bs4 import BeautifulSoup

dir_in = "/content/ELTeC-eng-master/level1/"

metadata = []

for base, directorios, ficheros in os.walk(dir_in):
  for fichero in ficheros:
    ficheroEntrada = base + fichero
    directorio = base.split('/')[-1]
    if fichero[0:3] == "ENG": # Language ID. Change if you are processing text from ther collection.
      with open(ficheroEntrada, 'r') as tei: #Opens the file
        soup = BeautifulSoup(tei, 'xml') #Parse the XML
        print("Processing", ficheroEntrada) #Only to see the process. Comment if it's not important.
        title = soup.title.text #extracts the title
        author = soup.author.text #extracts author name
        gender = soup.authorGender['key']
        size = soup.size['key']
        reprints = soup.reprintCount['key']
        timeslot = soup.timeSlot['key']
        metadata.append((author, title, size, reprints, timeslot, gender)) #and stores the information in "metadata" variable.
        #metadata.append((author, title)) #and stores the information in "metadata" variable.

for item in metadata:
  print(item[0], item[1], item[2], item[3], item[4], item[5]) #Only to show the results.

"""To save results in a file (CSV) and download:"""

from google.colab import files

metadata_out = ''
for item in metadata:
  author = item[0]
  title = item[1]
  gender = item[5]
  size = item[2]
  reprints = item[3]
  timeslot = item[4]
  metadata_out+=author+'\t'+title+'\t'+gender+'\t'+size+'\t'+reprints+'\t'+timeslot+'\n'

out = open('metadata.csv', 'w') #Opens a file in write mode ("w").
out.write(metadata_out) # "Writes" the content of metadata_out in the file
out.close() #Closes the file

files.download('metadata.csv') #To download the file. Now you can open it with a spreadsheet application.

"""# Open each file and extract information about author and gender

Now let's see female and male authors. 
"""

dir_in = "/content/ELTeC-eng-master/level1/"

females = []
males = []

for base, directorios, ficheros in os.walk(dir_in): #Go through directory and open file one by one
  for fichero in ficheros:
    ficheroEntrada = base + fichero
    if fichero[0:3] == "ENG": # Language ID. Change if you are processing text from ther collection.
      with open(ficheroEntrada, 'r') as tei:
        soup = BeautifulSoup(tei, 'xml')
        print("Processing", ficheroEntrada)
        author = soup.author.text # Extract author
        gender = soup.authorGender["key"] # Extract gender
        if gender == 'F':
          if author not in females: 
            females.append(author) #stores the information
          
        elif gender == 'M':
          if author not in males:
            males.append(author)  #stores the information

results = [len(females), len(males)] # Counts the number of female and male authors.
print("Results:\n\tFemale: "+str(len(females))+"\n\tMale: "+str(len(males))) # shows results

females_out = '' # To store the names of females authors in string format
males_out = '' # Idem male authors

for item in females: #Extract each name and write it in "out" variable (as string).
  females_out+=item+'\n'
for item in males:
  males_out+=item+'\n'

outF = open('author_females.txt', 'w') #Opens a file in write mode ("w").
outM = open('author_males.txt', 'w') #Opens a file in write mode ("w").
outF.write(females_out) # "Writes" the content of "female_out" in the file
outF.close() #Closes the file
outM.write(males_out) # "Writes" the content of "male_out" in the file
outM.close() #Closes the file

files.download('author_females.txt')
files.download('author_males.txt')

"""### Plotting"""

import matplotlib.pyplot as plt

x = ['Female', 'Male'] 
y = results #data
plt.bar(x,y) #Creates the plot
plt.xlabel('Gender')
plt.title('Gender distribution in ELTeC-SPA')
plt.show()

#For test: calculate percentage
#total = results[0]+results[1]
#data = [(results[0]*100/total), (results[1]*100/total)]

"""# Open each file and extract information about gender and work length

See the lengths of the works written by men and women. 
"""

dir_in = "/content/ELTeC-eng-master/level1/"

females = []
males = []

longfem = []
mediumfem = []
shortfem = []

longmal = []
mediummal = []
shortmal = []

for base, directorios, ficheros in os.walk(dir_in): #Go through directory and open file one by one
  for fichero in ficheros:
    ficheroEntrada = base + fichero
    if fichero[0:3] == "ENG": # Language ID. Change if you are processing text from ther collection.
      with open(ficheroEntrada, 'r') as tei:
        soup = BeautifulSoup(tei, 'xml')
        print("Processing", ficheroEntrada)
        author = soup.author.text # Extract author
        gender = soup.authorGender["key"] # Extract gender
        size = soup.size['key']
        if gender == 'F' and size == 'long':
          if author not in longfem: 
            longfem.append(author) #stores the information
        elif gender == 'F' and size == 'medium':
          if author not in mediumfem: 
            mediumfem.append(author) #stores the information
        elif gender == 'F' and size == 'short':
          if author not in shortfem: 
            shortfem.append(author) #stores the information          
        elif gender == 'M' and size == 'long':
          if author not in longmal: 
            longmal.append(author) #stores the information
        elif gender == 'M' and size == 'medium':
          if author not in mediummal: 
            mediummal.append(author) #stores the information
        elif gender == 'M' and size == 'short':
          if author not in shortmal: 
            shortmal.append(author) #stores the information    


resultsfem = [len(longfem), len(mediumfem), len(shortfem)] # Counts the number of female and male authors.
resultsmal = [len(longmal), len(mediummal), len(shortmal)]
print("Results:\t Long \t Medium \t Short \nFemale \t"+str(len(longfem))+'\t'+str(len(mediumfem))+'\t'+str(len(shortfem))+"\nMale \t"+str(len(longmal))+'\t'+str(len(mediummal))+'\t'+str(len(shortmal))+'\n') # shows results

# females_out = '' # To store the names of females authors in string format
# males_out = '' # Idem male authors

# for item in females: #Extract each name and write it in "out" variable (as string).
#   females_out+=item+'\n'
# for item in males:
#   males_out+=item+'\n'

# outF = open('author_females.txt', 'w') #Opens a file in write mode ("w").
# outM = open('author_males.txt', 'w') #Opens a file in write mode ("w").
# outF.write(females_out) # "Writes" the content of "female_out" in the file
# outF.close() #Closes the file
# outM.write(males_out) # "Writes" the content of "male_out" in the file
# outM.close() #Closes the file

# files.download('author_females.txt')
# files.download('author_males.txt')

import matplotlib.pyplot as plt

x = ['Long', 'Medium', 'Short'] 
y = resultsfem #data
plt.bar(x,y) #Creates the plot
plt.xlabel('Female')
plt.title('Length of works written by women')
plt.show()

x = ['Long', 'Medium', 'Short'] 
y = resultsmal #data
plt.bar(x,y) #Creates the plot
plt.xlabel('Male')
plt.title('Length of works written by men')
plt.show()

#For test: calculate percentage
#total = resultsfem[0]+resultsfem[1]+resultsfem[2]
#data = [(results[0]*100/total), (results[1]*100/total), (results[2]*100/total)]

#print(total)
#print(data)