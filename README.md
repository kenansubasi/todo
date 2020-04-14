# Todo App


## Installation

We use docker to run the project.

[Download Docker](https://www.docker.com/community-edition)

Docker can't help for some devices. If the project does not work with Docker, Docker Toolbox will help you.

[Download Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/#step-2-install-docker-toolbox)


## How to Run?

To build the project:
```
docker-compose -p todo -f docker/docker-compose.yml -f docker/docker-compose.dev.yml build
```

To run the project:
```
docker-compose -p todo -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d
```

To restart the project:
```
docker-compose -p todo -f docker/docker-compose.yml -f docker/docker-compose.dev.yml restart
```

To stop the project:
```
docker-compose -p todo -f docker/docker-compose.yml -f docker/docker-compose.dev.yml stop
```

To see logs:
```
docker-compose -p todo -f docker/docker-compose.yml -f docker/docker-compose.dev.yml logs -f --tail 50
```

To status docker containers:
```
docker-compose -p todo -f docker/docker-compose.yml -f docker/docker-compose.dev.yml ps
```


## Technologies

This is a list of mostly used awesome technologies and libraries that are used in Todo Project:

- [Python](https://www.python.org/): Python is an interpreted high-level programming language for general-purpose programming.

- [Django](https://www.djangoproject.com/): Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

- [PostgreSQL](https://www.postgresql.org/): PostgreSQL is a powerful, open source object-relational database system that has strong reputation for reliability, feature robustness, and performance.

- [Celery](http://www.celeryproject.org/): Celery is an asynchronous task queue/job queue based on distributed message passing.

- [Redis](https://redis.io/): Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker.


## Maintainers

* **Kenan Subaşı**  - *kenansubasiceng@gmail.com*

