
import logging
import json
import wget
from os.path import basename, join, exists
from os import getcwd, makedirs, remove
import sentencepiece as spm
from lib import aws_handler, ZipHandler
from lib.utils import get_digest
from lib import vocab_size, zip_type, accessKey, secretKey, region, bucket

def sp_train(mdir, model_file_name, vocab_size=1000000):

    logging.info("create params")
    params = ('--input_sentence_size=1000000 '
            '--max_sentence_length=1000000 '
            '--split_by_unicode_script=true '
            '--input={0}/{1}.txt '
            '--model_prefix={0}/{1} '
            '--vocab_size={2} '
            '--character_coverage=0.9995 '
            '--hard_vocab_limit=false '
            '--model_type=unigram ').format(mdir, model_file_name, vocab_size)

    logging.info("start training sentencepiece")
    spm.SentencePieceTrainer.Train(params)

def train(json_link, s3_link):

    """It is a training pipeline to train a tokenization model"""

    try:

        logging.info("get variables")
        json_file_name = basename(json_link).split(".", 1)[0]
        model_file_name, model_folder = s3_link.split("/")[-1], s3_link.split("/")[-2]
        model_dir = join(getcwd(), model_folder)
        mdir = join(model_dir, model_file_name)

        # check if mdir exist
        if not exists(mdir):
            makedirs(mdir)
            logging.info("created mdir: %s" % mdir)

        # wget json file
        filename = wget.download(json_link, out=mdir)
        array_text = json.load(open(join(mdir, filename)))
        
        # create text.txt
        logging.info("create text.txt")
        text_gen = (i['post_message'] for i in array_text)
        txt_file = "".join([mdir, '/', model_file_name, '.txt'])
        json_file = "".join([mdir, '/', model_file_name, '.json'])
        with open(txt_file, 'w') as f:
            for sent in text_gen:
                f.write(next(sent))

        # train model
        train(mdir, model_file_name, vocab_size)

        # remove txt file
        remove(txt_file)
        remove(json_file)
        
        # zip model and vocan file
        logging.info("zip file")
        zip_helper = ZipHandler(model_file_name, zip_type, "")
        zip_helper.compressor(mdir, model_dir)

        # hash
        logging.info("hashing")
        hashword = get_digest(join(model_dir, model_file_name + zip_type))

        # upload to S3
        logging.info("upload to s3")
        local_path = join(model_dir, model_file_name + zip_type)
        s3_path = s3_link.split("/", 3)[-1]
        aws_handler.upload_2S3(s3_path, local_path)

        return {"hash": hashword}
    except Exception as e:
        logging.error("There might be something wrong with the params setting. Please check!!!!")
        logging.error("Error message is {}. ".format(e))
        return {"error": str(e)}

