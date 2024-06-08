Адрес репозитория:

https://github.com/MultikPatin/ugc_sprint_2

# Сервис UGC Movies
Проектная работа 9 спринта

### Run
```shell
docker compose up -d --build
```

#### OpenApi docs
http://127.0.0.1:5000/api/openapi

#### UI Kafka
http://127.0.0.1:8080/


### Run local
```shell
flask --app main run --port=5001
```


### UML

#### UGC component
![UGC Components](../docs/ugc/UGC_service.png)

#### Event UGC sequence
![Events UGC Sequence](../docs/ugc/Event_UGC_Sequence_v2.png)

#### Favorite UGC sequence
![Favorites UGC Sequence](../docs/ugc/Favorites_UGC_Sequence_v2.png)

#### Grades UGC sequence
![Grades UGC Sequence](../docs/ugc/Grades_UGC_Sequence_v2.png)

#### Reviews UGC sequence
![Reviews UGC Sequence](../docs/ugc/Reviews_UGC_Sequence_v2.png)
