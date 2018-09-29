## Project for Mapillary Automation Technical Challenge

### Requirements
1) Create a Python Rest API Service with 2 APIs  
     a) Create User (username, email, birthdate, address)  
     b) Get Users
    
2) Create a Web Application that displays the list of users created in a table and allow you to create new users
3) Test (1) and (2) in the smartest way possible


### IMPORTANT  

 A) The information should be persisted in a database of your choice (mongodb, psql, elasticsearch)  
 B) The output of the task should be a docker-compose environment where anyone can run the tests with just one command  
 C) We DO NOT care about the webapp, the uglier the better  
 D) We DO NOT care about the Api code, it just needs to work  
 E) We DO care about the tests
 
---
## Development environment
<table border=0>
<tr><td>

Tool/OS/Path | Details/Version
-------------| --------
|Operating System | Windows 8.1 SL |
|Python | 3.7.0 |
|pip | 18.0 |
|Elasticsearch | 6.4.1 |
|Java|1.8.0_60|
|Docker Toolbox | 18.03.0-ce |
|Docker-Compose | 1.20.1 |
|PyCharm IDE | 2018.2.4 CE |

</td><td>

Python libraries used | Version
-------------| --------
|Flask | 1.0.2 |
|Pytest | 3.8.1 |
|Elasticsearch | 6.3.1 |
|selenium | 3.13.0 |

</td></tr> </table>


## Approach followed

The Project is partitioned into API and UI, Test, Reports, Docker and a README.md (refer [Folder Structure])

The APIs are developed using python library: ```flask, elasticsearch``` and UI is basic html with ```jquery``` and templates

The Tests are developed using python libraries: ```pytest, elasticsearch, selenium```
Page Object pattern was used to segregate the locators from the test script itself.

The ```Dockerfile``` will contain the aspects for the container: It will install Python with all the library requirements, download code from GitHub, download elasticsearch and expose required ports for elasticsearch, flask API and webapp.  
The ```Docker-Compose``` will spawn the elasticsearch at port 9200, app.py at port 9100 and wait for stipulated time and trigger the automation in single command.  
The ```Docker-Compose``` can do all these in 1 command and this can be triggered via a Jenkins Job over Windows Server 2016 or CentOS VM.


Folder Structure | 
|-----------------
```commandline
C:\Users\SaiPrasad\PycharmProjects\mapillarytest>
Folder PATH listing for volume Windows8_OS
Volume serial number is A869-4B35
C:.
├───.idea
├───api
│   └───templates
│   │   └───index.html
│   └───app.py
│   └───dropindex.py
├───reports
│   └───assets
│   └───report.html
│   └───test_report.xml
├───test
│   ├───.pytest_cache ...
│   ├───pageobject
│   │   └───BasePage.py
│   ├───testobject
│   │   └───BaseTest.py
│   └───base_test.py
│   └───conftest.py
├───Dockerfile
├───README.md
├───requirements.txt
└───venv
    ├───Include
    ...
``` 



#### To spawn the API, UI (individually)
```commandline
python.exe api\app.py
```
This would launch the webapp URL and accessible at :  (http://localhost:9100)
and the REST API for User: (http://localhost:9100/user) ```[POST, GET, DELETE]```



#### To run the Tests (individually)
```commandline
python.exe -m pytest test\base_test.py --junitxml=.\reports\test_report.xml --html .\reports\report.html
```

The automated test execution report are placed under ```test\reports``` folder
```C:\Users\SaiPrasad\PycharmProjects\mapillarytest\reports\reports.html```

#### To run entirely using docker
Since the current setup is on Windows 8.1, and only supportes Docker Tookbox with VirtualBox, docker image and docker-compose were created with required targets.  
Execution was not possible, please refer [Where are we at?]


## Where are we at? What is pending/blocker
- [x] API and UI
    - [x] API hosted on 9100 for /user
    - [x] API for /user for GET and POST
- [x] Test Automation
    - [x] Page Objects
    - [x] Test covering API and UI tests with Page objects
    - [x] Run locally with Reports
    - [ ] Run via "Docker for Windows" (on Windows 10, Windows Server 2016)
- [ ] Docker
    - [x] Docker Toolbox installed
    - [x] Dockerfile created (not supported on current Windows 8.1)
    - [x] Docker-Compose created (not executed)
- [ ] Jenkins
    - [x] Basic Job which triggers Job and generates Test reports
    - [ ] Job with Docker-Compose integration to run the Tests

```Docker Toolbox``` used in this Project is supported on ```Windows8.1``` with certain limitations, however ```Docker for Windows``` is supported on Windows10 or Windows Server 2016  
*Later is preferred, could not explore it due to lack of Hardware, OS license and for want of extra time*  
Refer: https://stackoverflow.com/questions/42482154/can-i-run-windows-containers-using-docker-toolbox-on-windows-7

## Test Plan
Automation Testplan has been prepared to showcase few of the best practises like: *Fixture*, *Singleton Webdriver object*, *Page Object*, *Data Provider* and *Junit/HTML report* (Allure, ReportalReport can be supported)

Test Id | Test case | Test Details | Test Expectation | Test Observation | Data | Comments  
-------------| -------- | -------- | -------- | -------- | -------- | --------
|1 | Launch Mapillary test webapp and check heading             | Launch the dummy webapp url ```http://localhost:9100``` , page loads and it has a Heading the reads as  | {'Project' : 'Mapillary Automation test challenge'} | | | 
|2 | Validate about the User List header                        | Verify that the Header for User List is correct and displayed| Header is ```User List``` | | | | |
|3 | Validate about the User List table headers                 | Verify that the User List Table column headers are correct and displayed| Column headers are ```#, UserName, Email, Birthdate, Address```| | | | 
|4 | Seeding the UserList with seed data                        | Add few Users using the ```seeddata``` in the form| Each seed record is added without error, Empty records are not added| | ```seeddata = [("a", "a", "1900-01-01", "a street"),("b", "b", "1900-01-01", "b street"),("c", "c", "1900-01-01", "c street"),("d", "d", "1900-01-01", "d street"),("e", "e", "1900-01-01", "e street"),] ``` | |
|5 | Validate about the Search options, perform a search        | Perform tests with positive search and negative search criteria, Validate and assert the search results for successful search and unsuccessful search| Search and its corresponding result assertion will be done for each set in the datasource | | ```search = [("a", True),("test1", False),("e", True),("test4", False),] ``` | |
|6 | Validate about the User Form for form elements             | Verify that the User List Form input fields are correct and displayed | The form is listed and ```Username, Email, Birthdate, Address``` and ```Add``` are displayed and enabled| | | | 
|7 | Seeding the UserList with testdata                         | Add few Users using the ```testdata``` in the form | Each test user record is added without error, Empty records are not added| | ```testdata = [("test1", "test1@test1.com", "1900-01-01", "test1 street"),("test2", "test2@test2.com", "1900-02-02", "test2 street"),("test3", "test3@test2.com", "1900-03-03", "test3 street"),("test4", "test4@test2.com", "1900-04-04", "test4 street"),]``` | | 


