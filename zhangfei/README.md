# Zhangfei

1.[Introduce](#introduce)

2.[Installation Document](#Run)

3.[Api Document](#Api)

<p id='introduce'></p>

## Introduce
### Zhangfei

Provides scanning analysis software, PR license and copyright functions in a service-oriented manner, and supports Gitee, Github, Gitlab, http, and purl link input.

For rules documentation, see [License baselines and Best practices](doc/scanner/zhangfei.md)

### Directory Structure
```
|-Zhanfei
|  |-doc #Design rules document
|  |-src
|     |-reposca
|     |   |-config
|     |        |-License.yaml #License access list
|     |   |-analyzeSca.py #Analyze scan results
|     |   |-commSca.py #Command line scan logic
|     |   |-itemLicSca #Project level scanning logic
|     |    |-licenseCheck.py #Determine license compliance logic
|     |   |-prSca.py #PR level scanning logic
|     |   |-queryBoard #Query board data 
|     |   |-queryMeasure #Query metric data
|     |   |-repoCrawl.py #Crawl software logic
|     |   |-repoDb.py #SQL query
|     |   |-scheduleSca.py #Timed task
|     |   |-sourceAnalyze.py #Analyze the command line scan result
|     |-util
|     |   |-authApi.py #Use the Gitee open api
|     |   |-catchUtil.py #Catch exception
|     |   |-downUtil.py #File download logic
|     |   |-extractUtil.py #Unzip file logic
|     |   |-formateUtil.py #Formatted path
|     |   |-popUtil.py #Control command line closure
|     |   |-postOrdered.py #The License description is converted to postOrdered
|     |   |-scheduleUtil.py #Timing task controller
|     |   |-stack.py  #Stack out controller
|     |command.py #Command line running entry
|     |config.py #Service port configuration file
|     |main.py #Service start entry
|   |LICENSE #License information
|   |requirements.txt #Dependency component list
|   |setup.py #Installation program
```

--- 
<p id='Run'></p>

## Run
* Pull dependency
    ```
    pip install -r zhangfei/requirements.txt
    ```
* Set up system environment
    ```
    env:
        - name: MYSQL_HOST
          value: your_db_host
        - name: MYSQL_USER
          value: your_db_name
        - name: MYSQL_PASSWORD
          valueFrom:your_db_password
        - name: MYSQL_DB_NAME
          value: your_db_name
        - name: MYSQL_PORT
          value: your_db_port
        - name: GITE_REDIRECT_URI
          value: your_gitee_api_token_redirect_uri
        - name: GITEE_CLIENT_ID
          value: your_gitee_api_token_client_id
        - name: GITEE_CLIENT_SECRET
          value: your_gitee_api_token_client_secret
        - name: GITEE_USER
          value: your_gitee_user
        - name: GITEE_PASS
          value: your_gitee_password
    ```
* Run
    
    as a service
    ```
    python zhangfei/src/main.py
    ```
    as a command
    ```
    python zhangfei/src/command.py -m pr/repo/local input --token
    ```
  
---

<p id='Api'></p>

### API doc

1. [PR compliance scan](doc/api/pr.md)
2. [Software compliance scan](doc/api/repo.md)
3. [Software compliance information query](doc/api/repoQuery.md)