# Thesis API

## Run The Application

- install requirements

  ```zsh
  pip install -r requirements.txt
  ```

- start API

  ```zsh
  flask run
  # or
  flask --debug run
  ```

## Deploy with docker compose

```
docker compose up -d
```

## Expected result

Listing containers must show one container running and the port mapping as below:

```
$ docker compose ps
NAME                COMMAND             SERVICE             STATUS              PORTS
flask-web-1         "python3 app.py"    web                 running             0.0.0.0:8000->8000/tcp
```

After the application starts, navigate to `http://localhost:8000` in your web browser or run:

```
$ curl localhost:8000
Hello World!
```

Stop and remove the containers

```
docker compose down
```

### Heroku

```zsh
heroku create
```
