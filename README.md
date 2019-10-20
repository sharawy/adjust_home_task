
## Generic Performance metric api

  - GET: api/v1/metrics/ 
# Response example:
```json
{
    "count": 1096,
    "next": "http://127.0.0.1:8000/api/v1/metrics/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "date": "2017-05-17",
            "channel": "adcolony",
            "country": "us",
            "os": "android",
            "impressions": 19887,
            "clicks": 494,
            "installs": 76,
            "spend": "148.20",
            "revenue": "149.04",
            "cpi": "1.95"
        },
        ...
```
# Query parameters:
all parameters are optional
* fields: comma separated list of fields name that return in response 
* grouping_by: comma separated list of fields that will be used in grouping the result
* ordering: comma separated list used for sorting the result
    - example:
        - Sort descending ordering=-id 
        - Sort ascending ordering=id 
* country: string
* date_to: string format YYYY-MM-DD
* date_from: string format YYYY-MM-DD
* channel: string 
* os: string

### Prerequisite
- Python version 3.6 

### How to setup and run
- run ```pip install -r requirements.txt```
- run ``` python manage.py migrate ```
- to load data run ```python manage.py csv_to_model performance_metrics.metric dataset.csv```
- run ```python manage.py runserver```

### Use cases

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
    - /api/v1/metrics/?fields=channel,country,impressions,clicks&grouping_by=channel,country&ordering=-clicks&date_to=2017-06-01


2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
 
    - /api/v1/metrics/?fields=installs,date&os=ios&grouping_by=date&ordering=date&date_from=2017-05-01&date_to=2017-05-31

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
    - /api/v1/metrics/?fields=revenue,os&grouping_by=os&ordering=-revenue&date=2017-06-01

4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.

    - /api/v1/metrics/?fields=channel,spend,installs,cpi&country=ca&grouping_by=channel&ordering=-cpi