Information retrieval development for a potential application, hereby named _MobilAll_, using data from universities, cost of living and mobility flows provided by _UNESCO_.

---

# MobilAll

**Mobility** -> Mobil + ity  
_tripartite motto_ (ity) : Quality, Flexibility, Utility

**Quality**: assuring the authority of data provided  
**Flexibility**: easily accommodate the user choices and preferences  
**Utility**: the application do not only inform the user but also tries to help the user/student making a decision  

Italy -> **It** + al + **y**  
Bologna, a Italian city but also a process that actually helped boosting European Mobility exchange flows

Portugal -> Portug + **al**  
Lisbon, capital of Portugal where Bologna process created the European Higher Education Area under the Lisbon Recognition Convention

Let's take all into consideration, or do we mean _al_, maybe it’s all, because the application is universal, targets all students that want to have an amazing **l**ife experience.

**MobilAll** -> Mobilty for All


---

# Instructions

### Pre-requirements:
* Python (recommended Version 3.6.3)
* ElasticSearch Version 6.0.0 or newer
* Logstash Version 6.0.0 or newer

### Recommended:
* Windows 10 -> if using other operating system other than Windows, it may be necessary to modify some paths from '\\' to '/'
* Python package manager pip -> other managers like Anaconda can be used
* Kibana Version 6.0.0

### Install dependencies:
* ElasticSearch python library -> 'pip install elasticsearch'
* Scrapy -> 'pip install Scrapy', on windows it may be needed to run 'pip install pypiwin32'
* Requests -> 'pip install requests'
* Flask -> 'pip install Flask'

In _\<src\>/lifeQuality/config.txt_, change _LOGSTASH_ and _KIBANA_ to the correct paths

**Run server**:

`<src>/start.bat [<args>]` or `python <src>/lifeQuality/init.py [<args>]`

_\<args\>_ can be _-kibana_, _-index_, _-lifeQuality_.
* no arguments, just run the server
* _-kibana_, opens a new process with Kibana
* _-index_, index information (it will open processes to run Scrapy and Logstash)
* _-lifeQuality_, index only lifeQuality (prices, indices and climate), before running the server

### Next steps:
**See information (after opening the server)**:
* Open the browser in _localhost:5000_ (default Flask port)
* Click on a query to see it working and change params to evaluate results

### Extras:
**Other way to run server alone**:
* set _FLASK_APP_ environment variable to _mobilAll.py_ inside _lifeQuality_ folder
* run the following command: `flask run`

**Index students flows alone**:
* set environment variable _MOBIL_ALL_ to _\<src\>_, on Windows type in cmd `SET MOBIL_ALL=<src>`
* run the following command: `<Logstash install path>/bin/logstash.bat -f <src/mobilityFlows>/flows.conf`

**Index universities alone:**
* go to _\<src\>/universities_
* run the following command: `scrapy crawl univSpider`
