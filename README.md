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

```zsh
docker compose up -d
```

## Expected result

Listing containers must show one container running and the port mapping as below:

```zsh
$ docker compose ps
NAME                COMMAND             SERVICE             STATUS              PORTS
flask-web-1         "python3 app.py"    web                 running             0.0.0.0:8000->8000/tcp
```

After the application starts, navigate to `http://localhost:8000` in your web browser or run:

```zsh
$ curl localhost:8000
Hello World!
```

Stop and remove the containers

```zsh
docker compose down
```

### Heroku

```zsh
heroku create
```

--------

## API Routes

### GET

```zsh
  http://127.0.0.1:5000/detection?url=https://aef-nattanon.github.io/demo1.jpg
  # or
  http://127.0.0.1:5000/detection?url=https://aef-nattanon.github.io/demo2.jpg
  # or
  http://127.0.0.1:5000/detection?url=https://aef-nattanon.github.io/demo3.jpg
```

**result**

```json
{
  "number": [
    "0",
    "3",
    "9",
    "6"
  ],
  "result_image": {
    "meter": "http://127.0.0.1:5000//view/meter/1670170018.270384",
    "number": "http://127.0.0.1:5000//view/number/1670170018.270384"
  },
  "results": [
    {
      "class": 0,
      "confidence": 0.9053506851,
      "name": "0",
      "xmax": 149.8361053467,
      "xmin": 68.9033966064,
      "ymax": 219.2411804199,
      "ymin": 45.1701431274
    },
    {
      "class": 3,
      "confidence": 0.8478618264,
      "name": "3",
      "xmax": 262.9045410156,
      "xmin": 167.8337402344,
      "ymax": 220.8316955566,
      "ymin": 45.3346633911
    },
    {
      "class": 9,
      "confidence": 0.9266092181,
      "name": "9",
      "xmax": 355.5003051758,
      "xmin": 269.3481140137,
      "ymax": 217.0911712646,
      "ymin": 43.5526580811
    },
    {
      "class": 6,
      "confidence": 0.9363228083,
      "name": "6",
      "xmax": 467.5668029785,
      "xmin": 363.3840332031,
      "ymax": 258.7028503418,
      "ymin": 46.1848907471
    }
  ]
}
```
