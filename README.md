# Using AWS IoT button for group chat

## Getting setup

create a virtualenv updog_env

```
$ virtualenv updog_env
$ source updog_env/bin/activate
(updog_env)$ pip install -r requirements.txt
```

Then run it

```
(updog_env)$ cd src
(updog_env)$ python updog.py
```

## Running things

Important creds and settings are not in git (coz public)
So they must be in your env variables when you run things

In your terminal window do this:

```
export BOT_USER=<username>
export BOT_PASS=<password>
export GROUP_ID=<group_id>
```

### Updog

```
(updog_env)$ cd src
(updog_env)$ python updog.py
```

### Greetings

```
(updog_env)$ cd src/greetings
(updog_env)$ python greetings.py
```

## Deploying

1. Create a dist folder
2. Add the relevant code to the dist folder
3. From the virtualenv add the contents of env/lib/site-packages/
4. Replace lxml from `lambda-lxml-base` into dist
5. Replace PIL and Pillow from `lambda-pil-lib` into dist
6. Select the files in dist and compress those files
7. Upload the Archive.zip to S3
8. Copy the link and apply to the lambda method
9. Save and Test
