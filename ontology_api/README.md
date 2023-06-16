# Ontology API

## Descriptions of functionality

The functionality of this API you can find [here](https://ontology-stage.affectivese.org/docs#/).

## Instalation

You should prepare virtual environment for Python. You can do it by:

```bash
python -m venv venv
```

Then you should enter there:

For Windows:

```bat
venv\Scripts\activate
```

For Linux
```bash
source venv/bin/activate
```

and then install requirements

```bash
pip install -r requirements.txt
```

## How to start tests?

For run tests you can use PyCharm. Then:

Working directory: ontology_api

Script path: ontology_api\manage.py

Parameters: tests

## How to run on docker?

You need to install docker. Then if you don't want to start every possible server, you can remove the rest from docker-compose.yaml.
If you need to return to previous state, you can use

```bash
git stash
```

to move changes to stack, you can use

```bash
git stash pop
```

to get change from stack.

To run docker use:

```bash
docker-compose up --build
```

To clean up everything:

```bash
docker rm $(docker ps -a -f status=exited -q)
docker rmi $(docker images -a -q)
```
Ontology API: http://localhost:18082/docs

Grisera Ontology API: http://localhost:18083/docs
