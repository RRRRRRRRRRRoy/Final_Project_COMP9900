This is the simplied version of setup instruction based on the Lubuntu Linux system. The detailed version is in the 9900-ALL-PASS team's report.pdf section 6

Version declare:
The version of each developing tool and language mentioned in this document is given as follow:
1. git  2.25.1
2. node.js  10.19.0
3. Vue Cli 4.5.15
4. Vue  3.x
5. anaconda3 64-Bit(x86)
6. Pycharm professional 2021.2.3(Linux) 
7. python3 3.6

If the code in .zip or .tgz file is used, please skip the Part 1 Code Clone. Starting at Part 2 System Implementation Guide.

Part 1 Code Clone:

1. Install the Git 
Step1:	When the Lubuntu system has been set up, open the Qterminal in the system tools tag to start the command-line tool. 
Step2:	Enter the following command to update the tool and install the git.
		sudo apt update 
		sudo apt install git 
Step3:	After installing the git, use the following command line to check the git version. If the git version is shown, the insallation is successed
		git ––version 

2. The Configuration of Git 
Step1:	Setting the global username and user email to continue. 
		git config ––global user.name "Your Name" 
		git config ––global user.email "YourEmail@yourDomain.com" 
Step2:	Generating the SSH Key to connect to GitHub by entering the following command. 
		ssh–keygen –t rsa –C "YourEmail@yourDomain.com" 
Step3:	Move to the 
		directory /home/lubuntu/.sshdirectory /home/lubuntu/.ssh
Using the cat command to open id_rsa.pub. Copy the content in the file and move to the GitHub website. 
		cd /home/lubuntu/.ssh 
		cat id_rsa.pub 
Step4:	Move to set, select the “SSH and GPG key”, paste the content in id_rsa.pub, to connect to the GitHub. 

3. Clone the source code from GitHub
Step1:	Go to the directory which you want to set up the project. 
Step2:	Copy the HTTPS link or SSH link, the location is the same as the following picture. 
Step3:	Enter the following command under the directory you want to set up the project. 
		git clone git@github.com:unsw–cse–comp3900–9900–21T3/capstone–project–9900–h18c–all–pass.git 
Step4:	Clone the source code from GitHub. 


Part 2 System Implementation Guide:

1. Install the dependencies for the front-end
Step1:	Install the node and npm for Lubuntu by entering the following command in Qterminal. 
		sudo apt install nodejs 
After finishing the installation, enter the following command.  
		node -V
If the node.js version is shown, the insallation is successed.

Step2:	Install the Vue-cli by entering the following command. 
		sudo npm install -g @vue/cli 
After finishing the installation, enter the following command.  
		Vue -V
If the Vue version is shown, the insallation is successed 
Step3:	Move to the directory of the project, currently, the test directory of the project is under the documents. Go to the folder “ris_gui” and install Vue-cli dependencies by using the following command. 
		cd <Your Own directory>/capstone-project-9900-h18c-all-pass/ris_gui  
		npm install 
When the dependencies have been installed, in the same ris_gui directory, run the following command to check whether the front-end can run normally. 
		npm run serve 
If the project local and Network running address is shown, the front-end has been set up successfully. 

2. Install the dependencies for the Back-End
Step1:	Install the Anaconda3. Download the shell file of Anaconda3 from the website. 
Step2:	Change the directory to the Downloads which is the default downloading directory of Lubuntu. Enter the following command to start the installation. 
		cd Downloads (The default downloaded directory) 
		sh Anaconda3-2021.05-Linux-x86_64.sh 
When the Anaconda3 has been installed, restart the QTerminal in Lubuntu.
Step3:	Create a python 3.6 environment for the project by entering the following command in QTerminal in Lubuntu. 
		conda create -n your_env_name python=3.6 
		conda activate your_env_name 
Step4:	Activate the current environment for the project and run the following command to install the requirements for the project. Notice: the requirements.txt file is under the project folder. 
		conda activate your_env_name 
		cd <Your Own directory>/cap*/proj* 
		pip install -r requirements.txt 

3. 	Downloading the PyCharm and setup the environment of anaconda. 
Step1:	Downloading the PyCharm of Linux from the website. 
Step2:	Extract the PyCharm.tar.gz under the Downloads directory 
Step3:	Open the QTerminal, move it to the folder bin under the PyCharm folder. Using the following command line to start up the PyCharm. 
		sh pycharm.sh 	
Step4:	Import the project folder, which is in capstone-project-9900-h18c-all-pass, as a python project into PyCharm. 
Step5:	Make the configuration whith python 3.6 environment created with anaconda. 
Step6:	Set both API_v1 and model folder as the “Sources Root” directory. 
Step7:	Run the back-end file app.py, if the "* Running on http://localhost:5000/ (Press CTRL+C to quit)" can be observed in PyCharm run, the Back-End code runing successfully. 

4.	Running system
Step1:	Running the app.py and Vue-cli as mentioned in the previous step. 
Step2:	Open the Firefox browser, enter the URL as localhost:8080 to enter in the rental inspection system. 


Part 3 Impletation tips:

1. This rental inspection system is based on Google Maps. Before using this system, please register a Google Map API key that contains the following functions.  
a. Directions API
b. Distance Matrix API
c. Geocoding API
d. Maps JavaScript API
e. Places API
And replace the API in the following places. 
Front-end: 
	/ris_gui/public/index.html 			around line 9
	/ris_gui/src/components/AddProperties.vue	around line 160 
	/ris_gui/src/components/propertyDetail.vue 	around line 263 
Back-end: 
	/project/API_v1/Route_Plan.py 			around line 43 
2. When the user is testing or using the current system, if the console shows error regarding No "Access-Control-Allow-Origin", please do the following changes to continue. 
For Windows 10: 
	Click the Chrome icon to open the setting. 
	Select the shortcut of chrome browser by pressing the tag on the banner. 
	Adding the following string behind the target.  
		--args --disable-web-security --user-data-dir="C:/ChromeDevSession" 
	Apply and restart the chrome browser shortcut. 
For macOS: 
	Open the terminal of MacOS 
	Run the following command and press enter to continue 
	open -n /Applications/Google\ Chrome.app/ --args --disable-web-security  --user-data-dir=/Users/Your_Macbook_name/MyChromeDevUserData/ 
