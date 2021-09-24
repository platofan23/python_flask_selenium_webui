#Imports
from flask import Flask,render_template,request,jsonify
from flask_fontawesome import FontAwesome
from pathlib import Path
import csv,os,math,datetime,re

#Appname
app = Flask(__name__)
#Fontawesome for Icons
fa = FontAwesome(app)

#Global Variables
FILE_DATA = Path(r'/data/T_Data.csv')
FILE_STATE = Path(r'/data/T_state.csv')
DIRBASE = r'/data/'

#Default route
@app.route('/')
def show_Index():  
   '''
   This is the default route of the flask-server 
   
         Parameters:
                  
         Returns:
                  data (json): Data of the tests
   ''' 
   list_state_New = list()
   list_temp = list()
   list_all = get_all_data()
   #Getting the newest state
   for l_test in get_all_data()[3]: 
      #Splitting the List of status log
      list_temp=str(l_test).split('/')
      list_state_New.append(list_temp[len(list_temp)-1])
   #Returning the HTML-Document 
   return render_template('T_Index.html',len=len(list_all[0]),list_Number=get_all_data()[0],list_Name=list_all[1],list_Description=list_all[2],list_state=list_state_New)

#Log-List
@app.route('/T_List', methods = ['POST'])
def show_List():  
   '''This route gives back the list of all tests
         Parameters:
                  
         Returns:
                  data (json): List of the test status
   '''    
   #Parameters via post method
   if request.method == 'POST':
      num = int(request.form['number'])  
   #Parameters via get method
   else:
      num = int(request.args.get('number'))
   #Test the Number   
   if(test_Number(num) != 'okay'):
         #Return the state
         data = {'state': test_Number(num)}
         return jsonify(data)
   else:
      list_log_state = list()
      list_temp = list()
      #Getting the log-List for the certain row 
      for l_test in get_all_data()[3]: 
         list_temp=str(l_test).split('/')
         list_log_state.append(list_temp)
      #Reversing the List
      list_log_state[num-1].reverse()
      data = {'len': len(list_log_state[num-1]),'list_log':list_log_state[num-1]}
      #Returning the Data via JSON
      return jsonify(data)
   
#Create a new test
@app.route('/T_New', methods = ['POST'])
def new_Test():  
   '''This route is for creating a new test
         Parameters:
                  
         Returns:
                  state (json): State of creating a new Test
   '''    
   #Parameters via post method
   if request.method == 'POST':
      name = str(request.form['name'])
      description = str(request.form['description'])      
      code = str(request.form['code'])      
   #Parameters via get method
   else:
      name = str(request.args.get['name'])
      description = str(request.args.get['description'])
      code = str(request.args.get['code']) 
   #Newest Date 
   date_time = datetime.datetime.now()
   list_all = get_all_data()
   #Validate Name
   if(test_String(name) != 'okay'):
      data = {'state': test_String(name)}
   else:
      #Validate Description
      if(test_String(description) != 'okay'):
         #Return the state
         data = {'state': test_String(description)}
      else:
         if(re.search('([A-Z]|[a-z]|[0-9])*.py',name) == 'null' or name.endswith('.py') == False):
            data = {'state': 'Name not matching with a Python-File-Name!'}
         else:   
            #Look if name already is used
            if (name in list_all[1]):
               data = {'state': 'Data already exists!'}
            else:
               try:
                  #Check Files
                  check_Files()                      
                  #Write data of the new test into the CSV file      
                  with open(FILE_DATA, mode='a') as t_file:
                     test_writer = csv.writer(t_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                     test_writer.writerow([name,description])                      
                  t_file.close()
                  #Write state of the new test into the CSV file  
                  with open(FILE_STATE, mode='a') as t_file:
                     test_writer = csv.writer(t_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                     test_writer.writerow([name,date_time.strftime('%c')+ ': Created'])                             
                  t_file.close()
                  #Creating the Python-Test-File
                  f = open(DIRBASE+ name, 'w')
                  f.write(code)
                  f.close()    
                  #Return the state
                  data = {'state': 'okay'}
               except:
                  data = {'state': 'File-Error!'}
   #Returning the state of the creation via JSON            
   return jsonify(data)

#Change the Details of a test
@app.route('/T_ChangeName', methods = ['POST'])
def change_Name():  
   '''This route is for changing a test name
         Parameters:
                  
         Returns:
                  data (json): Status of changing a test name
   '''     
   #Parameters via post method
   if request.method == 'POST':
      name = str(request.form['name'])
      num = int(request.form['number'])      
   #Parameters via get method
   else:
      name = str(str(request.args.get['name']))
      num = int(int(request.args.get['number']))  
   #Validate name
   if(test_String(name) != 'okay'):
      #Return the state
      data = {'state': test_String(name)}
   else:
      #Validate number
      if(test_Number(num) != 'okay'):
         #Return the state
         data = {'state': test_String(name)}
      else:
         if(re.search('([A-Z]|[a-z]|[0-9])*.py',name) == 'null' or name.endswith('.py') == False):
            data = {'state': 'Name not matching with a Python-File-Name!'}
         else: 
            #See if name is already used
            if (name in get_all_data()[1]):
               #Return the state
               data = {'state': 'Name already used!'}
            else:                    
               #Reading the Data of the CSV-File into a List   
               list_all = get_all_data()
               try:
                  #Check Files
                  check_Files()  
                  #Renaming the python-file     
                  if os.path.exists(DIRBASE+ list_all[1][int(num)-1]):
                     os.rename(DIRBASE+ list_all[1][int(num)-1],DIRBASE+ name)             
                  #Change the Element-Details in the list
                  list_all[1][int(num)-1]= name  
                  #Removing and recreating the files 
                  if os.path.exists(FILE_DATA):         
                     os.remove(FILE_DATA)
                  if os.path.exists(FILE_STATE):   
                     os.remove(FILE_STATE)
                  #Check Files
                  check_Files() 
                  for x in range(0, len(list_all[0])):     
                     #Write the test-data back into a csv-file                
                     with open(FILE_DATA, mode='a') as t_file:
                        test_writer = csv.writer(t_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        test_writer.writerow([list_all[1][x],list_all[2][x]])                         
                     t_file.close()
                     #Write the status-data back into a csv-file  
                     with open(FILE_STATE, mode='a') as t_file:
                        test_writer = csv.writer(t_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        test_writer.writerow([list_all[1][x],list_all[3][x]])                           
                     t_file.close()
                     #Return the state    
                     data = {'state': 'okay'}
               except:
                  data = {'state': 'File-Error!'}
   #Returning the state of the change via JSON  
   return jsonify(data)

#Change the Description of a test
@app.route('/T_ChangeDes', methods = ['POST'])
def change_Des():  
   '''This route is for changing a test description
         Parameters:
                  
         Returns:
                  data (json): State of changing a test description
   ''' 
   #Parameters via post method
   if request.method == 'POST':
      des = str(request.form['description'])
      num = int(request.form['number'])      
   #Parameters via get method
   else:
      num = int(request.args.get['number'])
      des = str(request.args.get['description'])    
   #Validate description
   if(test_String(des) != 'okay'):
      #Return the state
      data = {'state': test_String(des)}
   else:
      #Validate number
      if(test_Number(num) != 'okay'):
         #Return the state
         data = {'state': test_String(des)}
      else:               
         #Reading the Data of the CSV-File into a List   
         list_all = get_all_data()
         try:  
            #Check Files
            check_Files()  
            #Change the Element-Details in the list
            list_all[2][int(num)-1] = des  
            #Removing and recreating the file   
            if os.path.exists(FILE_DATA):         
               os.remove(FILE_DATA)
            #Check Files
            check_Files()        
            #Write data without the deleted one in a new csv-file        
            for x in range(len(list_all[2])):       
               with open(FILE_DATA, mode='a') as t_file:
                  test_writer = csv.writer(t_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                  test_writer.writerow([list_all[1][x],list_all[2][x]])                        
               t_file.close()     
            data = {'state': 'okay'}
         except:
            data = {'state': 'File-Error!'}
   #Returning the state of the change via JSON  
   return jsonify(data)

#Change the Details of a test
@app.route('/T_ChangeCode', methods = ['POST'])
def change_Code():  
   '''This route is for changing the code of a test name
         Parameters:
                  
         Returns:
                  data (json): State of changing the code of a test
   ''' 
   #Parameters via post method
   if request.method == 'POST':
      name = str(request.form['name'])
      code = str(request.form['code'])    
   #Parameters via get method
   else:
      name = str(request.args.get['name'])   
      code = str(request.args.get['code'])      
   #Validate name
   if(test_String(name) != 'okay'):
      #Return the state
      data = {'state': test_String(name)}
   else: 
      #Validate the code
      if(test_String(code) != 'okay'):   
         data = {'state': test_String(code)}
      else:  
         try:               
            #Removing the python-file     
            if os.path.exists(DIRBASE+ name):
               os.remove(DIRBASE+ name)
            #Creating the Python-Test-File
            f = open(DIRBASE+ name, 'w')
            f.write(code)
            f.close()    
            #Return the state      
            data = {'state': 'okay'}
         except:
               data = {'state': 'File-Error!'}
   #Returning the state of the change via JSON  
   return jsonify(data)

#Check if a Programm-Name exists
@app.route('/T_Del', methods = ['POST'])
def delete_Test():  
   '''This route is for deleting a test
         Parameters:
                  
         Returns:
                  state (json): State of deleting a test
   ''' 
   #Parameters via post method
   if request.method == 'POST':
      name = str(request.form['name'])
      num = int(request.form['number'])
   #Parameters via get method
   else:
      name  = str(request.args.get['name'])  
      num = int(request.form['number'])
   #Test number   
   if(test_Number(num) != 'okay'):  
      data = {'state': test_String(name)}
   else:
      #Test name
      if(test_String(name) != 'okay'):
         data = {'state': test_String(name)}
      else:
         try:
            list_all = get_all_data()
            #Check Files
            check_Files()  
            #Removing and recreating the files
            if os.path.exists(FILE_DATA):
               os.remove(FILE_DATA)
            if os.path.exists(FILE_STATE):
               os.remove(FILE_STATE)   
            #Check Files
            check_Files() 
            #Remove the Data out of the list        
            list_all[0].pop(int(num-1))
            list_all[1].pop(int(num-1))
            list_all[2].pop(int(num-1))
            list_all[3].pop(int(num-1))
            #Write data into the CSV file 
            for x in range(0, len(list_all[0])):     
               #Write the test-data back into a csv-file                
               with open(FILE_DATA, mode='a') as t_file:
                  test_writer = csv.writer(t_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                  test_writer.writerow([list_all[1][x],list_all[2][x]])                   
               t_file.close()
               #Write the status-data back into a csv-file  
               with open(FILE_STATE, mode='a') as t_file:
                  test_writer = csv.writer(t_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                  test_writer.writerow([list_all[1][x],list_all[3][x]])                 
               t_file.close()
            #Removing the python-file     
            if os.path.exists(DIRBASE+ name):   
               os.remove(DIRBASE + name)   
            data = {'state': 'okay'}
         except:
            data = {'state': 'File-Error!'} 
   #Returning the state of deleting via JSON           
   return jsonify(data)

#Check if a Programm-Name exists
@app.route('/T_Run', methods = ['POST'])
def run_Test(): 
   '''This route is for running a test name
         Parameters:
                  
         Returns:
                  data (json): State of running a test
   ''' 
   #Parameters via post method
   if request.method == 'POST':
      name = str(request.form['name'])
      num = int(request.form['number'])
   #Parameters via get method
   else:
      name  = str(request.args.get['name'])  
      num = int(request.form['number'])
   #Test number   
   if(test_Number(num) != 'okay'):  
      data = {'state': test_String(name)}
   else:
      #Test name
      if(test_String(name) != 'okay'):
         data = {'state': test_String(name)}
      else:
         #Starting the python file
         if os.path.exists(DIRBASE+ name):   
            os.system('python ' + DIRBASE + name) 
            data = {'state': 'okay'}
   #Returning the state of running via JSON
   return jsonify(data)

#Check if a Programm-Name exists
@app.route('/T_Name', methods = ['POST'])
def name_Exist():  
   '''This route is for seeing if a test name exists
         Parameters:
                  
         Returns:
                  data (json): Check of a name exists
   ''' 
   #Parameters via post method
   if request.method == 'POST':
      name = str(request.form['name'])
   #Parameters via get method
   else:
      name = str(request.args.get['name'])       
   #Reading the Data of the CSV-File into a List   
   list_all = get_all_data()  
   #If the name exists send response okay         
   if (name in list_all[1]):
      data = {'state': 'okay'}
   #If the name not exists send response nope
   else: 
      data = {'state': 'nope'}
   #Returning the result via JSON
   return jsonify(data)
   
#Check if a Programm-Number exists
@app.route('/T_Num', methods = ['POST'])
def num_Exist():  
   '''This route is for seeing if a test number exists
         Parameters:
                  
         Returns:
                  data (json): Check if a number exists
   ''' 
   #Parameters via post method
   if request.method == 'POST':
      num = int(request.form['number'])
   #Parameters via get method
   else:
      num = int(request.args.get['number'])    
   #Get The NameList 
   list_all = get_all_data()
   #If the number exists send response okay                     
   if (int(num) > 0  and int(num) <= len(list_all[0])):
      data = {'state': 'okay'}
   else: 
      #If the number not exists send response nope
      data = {'state': 'nope'}
   #Returning the result via JSON
   return jsonify(data)

#Return the code
@app.route('/T_Code', methods = ['POST'])
def code_Get():  
   '''This route is for returning the code of a test
         Parameters:
                  
         Returns:
                  data (json): The code of a test
   ''' 
   #Parameters via post method
   if request.method == 'POST':
      name = str(request.form['name'])
   #Parameters via get method
   else:
      name = str(request.args.get['name'])        
   #Reading the Data of the CSV-File into a List   
   list_all = get_all_data()
   code = ''
   #If the name exists send response okay         
   if (name in list_all[1]):
      #Getting the Code of the python-file
      with open(DIRBASE + name, mode='r') as test_file:
         for row in test_file:
            if len(row) == 0:
               continue  
            else:
               code = code + row  
      test_file.close()            
      data = {'state': 'okay','code': code}
   #If the name not exists send response nope
   else: 
      data = {'state': 'nope'}
   #Returning the result via JSON
   return jsonify(data)
   
#Method get_all_data
def get_all_data():
   '''This methode returns all the data
         Parameters:
                  
         Returns:
                  liste_All (list): List with all the information
   ''' 
   try:  
      #Check Files
      check_Files()    
      #Reading the Data of the CSV-File into a List  
      list_count = 0 
      list_Details = list()
      list_state_Name = list()
      list_Number = list()
      list_Name = list()
      list_Description = list()
      list_state = list()
      liste_All = list()
      #Reading the test data
      with open(FILE_DATA, mode='r') as data_file:
         test_reader = csv.reader(data_file)
         for row in test_reader:
               if len(row) == 0:
                  continue  
               else:
                  list_Details.append(row)
                  list_count = list_count + 1
                  list_Number.append(list_count)   
      data_file.close()
      #Reading the test states               
      with open(FILE_STATE, mode='r') as data_file:
         test_reader = csv.reader(data_file)
         for row in test_reader:
               if len(row) == 0:
                  continue  
               else:
                  list_state_Name.append(row)  
      data_file.close()
      #Split the original list into several lists  
      for name_des in list_Details: 
         #Removing unnecessary Symboles ('[']')
         splitter = str(name_des).split(",",2)
         list_Name.append(remove_Symbols(splitter[0]))
         list_Description.append(remove_Symbols(splitter[1]))  
      #Split the original list into several lists  
      for stat_name in list_state_Name: 
         splitter = str(stat_name).split(",",1)
         list_state.append(remove_Symbols(splitter[1])) 
      #Append all Lists to one list   
      liste_All.append(list_Number)
      liste_All.append(list_Name)
      liste_All.append(list_Description)
      liste_All.append(list_state)
      return liste_All
   except:
      liste_All = list()
      return liste_All

#Method remove symbols   
def remove_Symbols(word):
   '''This method removes symbols
         Parameters:
                  word(String): the word where the symbols gonna be removed
                  
         Returns:
                  word (String): the word with the symbols removed
   ''' 
   #Removing unnecessary Symboles ("[']")
   characters = "[']"
   for x in range(len(characters)):
      word = word.replace(characters[x],"")
   return word

#Method check Files
def check_Files():
   '''This method checks files
         Parameters:
                  
         Returns:
                  
   ''' 
   #If the file does not exist create
   if(os.path.exists(FILE_DATA) == False):
      f = open(FILE_DATA, 'x')
      f.close() 
   #If the file does not exist create   
   if(os.path.exists(FILE_STATE) == False):
      f = open(FILE_STATE, 'x')
      f.close() 

#Methode test a number
def test_Number(num):
   '''This method test numbers
         Parameters:
                  num(int): The number to be tested
                  
         Returns:
                  back(String): State of the test
   ''' 
   num = int(num)
   #Check undefined
   if(num == 'undefined' or num is None):
      return 'Number is undefined!'       
   else:
      #Check Nan
      if(math.isnan(num) or num != num):
         return 'Number is NaN!'
      else:
         #Check number finite
         if(math.isfinite(num) == False):
            return 'Number is not finite!'
         else:
            #Check whole number
            if(isinstance(num, int) == False or type(num) != int):
               return 'Number is not an Integer!'
            else:
               #Check in area
               if (num < 0 or num == math.inf or num == -math.inf):
                  return 'Number out of the area!'
               else:
                  return 'okay'
   
#Method test a string               
def test_String(str):
   '''This method tests strings
         Parameters: str(String): The string to be tested
                  
         Returns:
                  back(String): State of the test
   ''' 
   #Check undefined
   if (str == 'undefined' or str is None): 
      return 'String is undefined!'
   else:
      #Check string empty
      if (len(str) == 0 or str == '' or str == ' '):
         return 'String is empty!'
      else:
         return 'okay'
   
#Launch the app
if __name__ == '__main__':
   app.run(debug = True)