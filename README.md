# SENTENCEPIECE 📝
It is a tokenizer model which can handle bilingual(Cantonese & English) tokenization.

### Get Started
- call /ping
- return "pong"

### Train API 🏃🏻‍♂️
- call /train
- request
```
{
    "json_link": "https://abc.s3.amazonaws.com/folder/file.json",
    "s3_link": "s3://bucket/folder/object"
}
```
- response
```
{
    "hash": "PFOIQH823P4OWIHFNP3QOFQ3OPIJFWE"
}
```

### CUT API ✂
- call /run
- request
```
{
    "model_file_name": "model_name",
    "model_file_hash": "hash",
    "s3_link": "https://bucket/model_folder/model_name",
    "array_text": [{"id":o, "message":"今天應該很高興"},...]
}
```
- return tokenized sentences
```
{
    "result": [{"id":o, "message":"今天 應該 很 高興"},...]
}
```

### start a docker host server
prerequisites:
- install docker desktop

start a docker host server
- in command line, type 
```
docker-compose up --build
```
- it needs time to start a docker server. Please wait patiently.

Testing api
- /ping (GET)
```
url: http://0.0.0.0:port/ping
```
- /pipe (POST)
```
url: http://0.0.0.0:port/run
body: 
{
    "result": [{"live_sid": 1, "message": "...", "pred": 1}, {"live_sid": 2, "message": "...", "pred": 0}, {"live_sid": 3, "message": "...", "pred": 1}] 
}
```

Stop a docker host server
- in command line, type
```
docker-compose down
```# sp_model
