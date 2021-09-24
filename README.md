<h1>python_flask_selenium_webui</h1>
<h2>Description of the project</h2>
The project is a web interface for: <br>
- Creating a python-selenium test <br>
- Deleting a python-selenium test <br>
- Running a a python-selenium test <br>
- Seeing the log of a python-selenium test <br>
- Changing the code of a python-selenium test <br>
- Changing the name of a python-selenium test <br>
- Changing the description of a python-selenium test of python-Selenium Test-Case. <br>
The project is written in python with the flask-framework (flask and flask-fontawesome), HTML, CSS (Bootstrap) and JavaScript (JQuery, Ajax). <br>
The whole page is a single page application. Everything work asynchron via Ajax-Calls <br>

![Unbenannt](https://user-images.githubusercontent.com/58483712/134743838-0f515895-5171-4a25-b013-bbfe9c59e428.png)

<h2>Project status</h2>
The project itself is complete and ready for use. However, it can be improved. For example, the use of CSV files can be replaced by a use of a database.

<h2>Requirements</h2>
Requirements for running the webui are:
- python (3.x.x) <br>
- pip (v3) or any other packetmanager <br>
- Selenium and the gecko-driver <br>
- flask <br>
- flask-fontawesome <br>
- Browser with JavaScript activated (Firefox or Chrome)

<h2>Installation</h2>
1. Download and Install Python. <br>
For windows go to (https://www.python.org/downloads/) <br>
For linux use <code>sudo apt-get install python3.x</code> <br>
2. Download and install pip-packetmanager <br>
3. Install flask <br>
For Windows <code> py -3 -m pip install flask </code> <br>
For Linux <code> pip3 install flask </code> <br>
4. Install flask-fontawesome <br>
For Windows <code> py -3 -m pip install flask-fontawesome </code> <br>
For Linux <code> pip3 install flask-fontawesome </code> <br>
5. Install python-selenium <br>
For Windows <code> py -3 -m pip install selenium </code> <br>
For Linux <code> pip3 install selenium </code> <br>
6. Download Geckodriver ((https://github.com/mozilla/geckodriver/releases) and move in the path <br>
For Windows put the path of the driver into the PATH Variable of windows (https://www.toolsqa.com/selenium-webdriver/selenium-geckodriver/) <br>
For Linux move into /usr/local/bin/ via <code> xxx mv /usr/local/bin/ </code> <br>
7. Now run the Pages.py - File
For Windows <code> py -3 Pages.py </code> <br>
For Linux <code> python3 Pages.py </code> <br>

<h2>Instruction manual</h2>
- <bold> Adding a new Test </bold>: Press the add(+)-Icon and enter a name (needs to end with .py), a descritpion and the selenium code (needs the code snippet to save the result) <br>
- <bold> Deleting a Test </bold>: Go to the desired test and press the remove button
- <bold> Running a test </bold>: Go to the desired test and press the run button
- <bold> Seeing the log of a test </bold>: Go to the disered Test and press on the status. A modal window will open. <br>
- <bold> Changing the code of a test </bold>: Go to the disered Test and press on the code-symbol. A modol window with the code will open. Modidy the code and press the save button <br>
- <bold> Changing the name of a test </bold>: Go to the disered Test and change the name in the name field. Than press the save-symbol to save the name <br>
- <bold> Changing the description of a test </bold>: Go to the disered Test and change the description in the description field. Than press the save-symbol to save the description <br>
- <bold> Closing a modal window </bold>: In the modal window press the x button in the top left corner <br>

<h2>Additional information</h2>
- The the table refreshes every 30 seconds and the page reloads every 60 seconds <br>
- Error are shown via JS-Alert <br>
- Inputs are getting validated (numer, string, pattern-matching, element exists or not) <br>
- JavaScript needs to be activated in the browser! <br>
- The needes html, css and js files are included in the reposetory <br>

<h2> Running the programm in a Docker-Container </h2>
- First Option is pulling the container from Docker-Hub (docker pull platofan23/flask_selenium_ui) <br>
- Second Option is to build the container via the existing dockerfile <br>
- In both options the container is ready to be run. <br>
- Parameters are the port (5000), Hostpath (your path where the data should be saved) and the Contaienr path (enter /data) <br>

