# JustWatch API

A basic [JustWatch](https://www.justwatch.com/) API.

Since standard free JustWatch API was removed this one uses [Selenium](https://www.selenium.dev/) to gather responses from JustWatch website directly.
It's slower than regular API would be, as Selenium has an execution time overhead.



* [Requirements](#requirements)
* [Configuration](#configuration)
* [Running the API](#running-the-api)
  * [Docker](#docker)
  * [Manually](#manually)
* [Endpoints](#endpoints)
* [Limitations and performance](#limitations-and-performance)



## Requirements

This API is built using [`FastAPI`](https://fastapi.tiangolo.com/), [`Selenium`](https://www.selenium.dev/) and `Python 3.11`.
Full list of Python requirements is in `requirements.txt` file.



## Configuration

Configuration is done through `.env` file. You can use provided `.env.example` as reference.

You can configure country used for JustWatch via `COUNTRY` environment variable:
```dotenv
COUNTRY=US
```
Values are matching JustWatch URLs. By default `US` is used.

You must configure paths for both Firefox and Firefox driver (geckodriver).
Normally you could use Selenium Manager to figure out paths, unfortunately it doesn't support ARM64 (e.g. Raspberry PI).
Specifying paths to both is a workaround disabling Manager:
```dotenv
FIREFOX_BIN=/path/to/firefox/binary
FIREFOX_DRIVER=/path/to/geckodriver
```
You can find geckodriver on its [GitHub](https://github.com/mozilla/geckodriver/releases).



## Running the API

### Docker

**Docker (and Docker Compose) assumes that geckodriver is present in project root directory to copy it into images.**

You can run the API through Docker Compose, only requirement is geckodriver present in project root:
```shell
docker compose up -d --build
```
Dockerfile will handle installing and setting up Firefox path and geckodriver path.

By default, Compose will forward local port 5031 to container port 8000, where the API is listening.
You can change both ports in `docker-compose.yml`, just make sure, that environment variable `UVICORN_PORT` matches new forwarded port on container side.


### Manually

1. Download geckodriver and make sure that Firefox is installed
2. Optionally configure search country
3. Set paths to geckodriver and Firefox in `.env` file
4. Install all Python packages from `requirements.txt`
5. Start the api via `uvicorn` setting up `PYTHONPATH` to project root

```shell
echo "FIREFOX_BIN=/path/to/firefox" >> .env
echo "FIREFOX_DRIVER=/path/to/geckodriver" >> .env
pip install -r requirements.txt
PYTHONPATH=$PWD uvicorn src.main.py
```

Uvicorn will by default start the API on address `127.0.0.1:8000`, you can change it via `--host <new host>` and `--port <new port>` parameters.
More details are in [Uvicorn documentation](https://www.uvicorn.org/settings/).



## Endpoints

You can access docs (automatically generated) by `/` or `/redoc/`.

Besides docs there's only one endpoint:
```shell
/search/{item_name}
```
Where `item_name` is your search query.

API responds with a JSON with first 5 found entries, e.g.:
```json
[
    [
        "The Matrix",
        "1999",
        {
            "Stream": [
                [
                    "Max Amazon Channel",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "Subs HD"
                ],
                [
                    "Max",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "Subs 4K"
                ]
            ],
            "Rent": [
                [
                    "Apple TV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$3.99 4K"
                ],
                [
                    "Amazon Video",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$3.99 4K"
                ]
            ],
            "Buy": [
                [
                    "Apple TV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$14.99 4K"
                ],
                [
                    "Amazon Video",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$14.99 HD"
                ]
            ]
        }
    ],
    [
        "The Matrix Resurrections",
        "2021",
        {
          "Rent": [
                [
                    "Amazon Video",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$3.79 4K"
                ],
                [
                    "Apple TV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$3.99 4K"
                ]
            ],
            "Buy": [
                [
                    "Apple TV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$14.99 4K"
                ],
                [
                    "Amazon Video",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$14.99 4K"
                ]
            ]
        }
    ],
    [
        "The Matrix Reloaded",
        "2003",
        {
            "Stream": [
                [
                    "Max Amazon Channel",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "Subs HD"
                ],
                [
                    "Max",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "Subs 4K"
                ]
            ]
            "Buy": [
                [
                    "AMC on Demand",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$4.99 HD"
                ],
                [
                    "DIRECTV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$11.99 4K"
                ]
            ]
        }
    ],
    [
        "The Matrix Revolutions",
        "2003",
        {
            "Stream": [
                [
                    "Max Amazon Channel",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "Subs HD"
                ],
                [
                    "Max",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "Subs 4K"
                ]
            ],
            "Rent": [
                [
                    "Apple TV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$3.99 4K"
                ],
                [
                    "Amazon Video",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$3.99 4K"
                ]
            ]
        }
    ],
    [
        "The Matrix Revisited",
        "2001",
        {
            "Rent": [
                [
                    "Apple TV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$2.99"
                ],
                [
                    "Amazon Video",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$2.99"
                ]
            ],
            "Buy": [
                [
                    "Apple TV",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$9.99"
                ],
                [
                    "Amazon Video",
                    "https://click.justwatch.com/super-long-just-watch-url-to-external-service",
                    "$9.99"
                ]
            ]
        }
    ]
]
```
(actual response has more options for services where you can access movies, I've trimmed it down for this example)

API will always respond with 5 best matching values, as JustWatch will match any string to something.



## Limitations and performance

API doesn't return any additional details other than title, year and where to watch things.
It looks only at search result site, it doesn't access individual movies/shows.

It responds always with 5 best matching entries as by default JustWatch loads only 5, and it will always load up something, regardless of whether input made any sense.

API is also quite slow, especially when running on less powerful machine, like Raspberry PI.
That's the reason for limited details in responses.
