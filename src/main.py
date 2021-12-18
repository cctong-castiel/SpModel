import logging
from os import getenv
from sanic import Sanic
from sanic.response import json as Json, text
from dotenv import load_dotenv
from lib.model.train import train
from lib.model.run import predict

app = Sanic(__name__)

# load env
load_dotenv()

# logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="./log/tokenizer.log", filemode="a", level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# route
@app.route("/ping", methods=["GET"])
async def home(request):
    return text("IMU pong")

@app.route("/train", methods=["POST"])
async def runTrain(request):

    data = request.json
    json_link, s3_link = data["json_link"], data["s3_link"]
    
    logging.info("run train")
    result = train(
        json_link, 
        s3_link
    )

    return Json(result)

@app.route("/run", methods=["POST"])
async def runPred(request):

    data = request.json
    model_file_name, model_file_hash = data["model_file_name"], data["model_file_hash"]
    s3_link, array_text = data["s3_link"], data["array_text"]

    logging.info("run predict")
    result = predict(
        model_file_name,
        model_file_hash,
        s3_link,
        array_text
    )

    return Json(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=getenv("POST"), debug=True)

