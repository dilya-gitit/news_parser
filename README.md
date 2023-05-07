# Finnhub Stock Market News Parser

Test assignment for [zimran.io](https://zimran.io/)

Consists of two parts:
1.  Microservice to parse and store Stock market news every hour through the API in [Finnhub.io](https://finnhub.io/)
2.  Endpoint to retrieve saved news from DB via the REST API on the microservice itself with the logic of filtering by dates

#### Built with
- Python
- Django Rest Framework
- Postgresql
- APScheduler


## Prerequisites

The following are needed to run this web application:

- [Docker](https://docs.docker.com/install/) (version 20.10)
- [Docker compose](https://docs.docker.com/compose/install/) (version 1.29)


## Install

Once the prerequisites are installed, execute the following commands from the project's root:
```bash
docker-compose up
```
This command will create containers for the Django server app and Postgres database.


## Usage

You can access the API endpoints by pasting the following URL in your browser or in Postman: 
```bash
http://localhost:8000/news/stock/TSLA/
```
This will return the list of all news with 'TSLA' ticker. Instead of 'TSLA' you can also try 'META', 'AMZN', 'TWTR', 'NFLX'.


You can also filter news by dates:
```bash
http://localhost:8000/news/stock/TSLA/?date_from=2023-05-04&date_to=2023-05-05
```
This will return the list of all news with 'TSLA' ticker dated form 2023-05-04 to 2023-05-05.


### Try running requests in Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/26583558-ed41a17a-3dae-4e51-b8f4-bcc959d726de?action=collection%2Ffork&collection-url=entityId%3D26583558-ed41a17a-3dae-4e51-b8f4-bcc959d726de%26entityType%3Dcollection%26workspaceId%3D14c6c675-d72c-4fc3-a26e-371fa7171831)


## Note

As the database is initially empty and news is populated only once in an hour for a single day, the database will be empty during the first hour.
To address this, you can modify the scheduler settings in `market_news/jobs/scheduler.py` by changing the value of `seconds` in the following line of code:

```bash
scheduler.add_job(NewsViewSet.fetch_data, "interval", seconds=3600)
```

You can also change how many days of news you want to see in your database. Go to `market_news/views.py` and change the value of `days` in the following line of code:
```bash
yesterday = timezone.now() - timezone.timedelta(days=1)
```
By updating these parameters, you can customize the behavior of the microservice according to your needs.

When you've made any changes in the source code, to see their effect, you have to re-build the image and compose the Docker container again. Run:
```bash
docker build --tag=app . && docker-compose up
```


