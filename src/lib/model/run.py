import logging
import regex as re
from os import getcwd, makedirs
from os.path import join, exists
import sentencepiece as spm
from multiprocessing import cpu_count, Pool
from functools import partial
from lib import ZipHandler
from lib.utils import get_digest
from lib import zip_type, aws_handler


# function for cleansing
def sp_cut(sent, sp, sepa):

    """Input: sentence string, sp model, separator
       Output: cleansed sentence string with space
       Process: sp tokenization, remove stopword"""

    if sent != None:
        seg_list_1 = sp.EncodeAsPieces(sent)
        seg_list_1 = [word.strip() for word in seg_list_1 if word.strip() != '']
        sent = sepa.join(seg_list_1)
        sent = re.sub("▁","",sent)
    else:
        sent = ''
    return sent

def process(obj, sp):
    return {"id":obj['id'], "text":sp_cut(obj['post_message'], sp, " ")}


# pipeline
def predict(model_file_name, model_file_hash, s3_link, array_text):

    """# download a model files
       # check hash
       # run the sentencepiece model and to tokenization
       # return an array of tokenized text"""

    try:

        logging.info("get variables")

        hashword = None
        model_folder, s3_path = s3_link.split("/")[-2], s3_link.split("/", 3)[-1]
        model_dir = join(getcwd(), model_folder)
        mdir = join(model_dir, model_file_name) #CWD + model_file_name
        local_path = mdir + zip_type

        # check if files exist
        if not exists(mdir) or not exists(local_path):
            makedirs(mdir)
            logging.info("download s3 path")
            aws_handler.download_fromS3(s3_path, local_path)
        else:
            # check hash
            hashword = get_digest(local_path)
            logging.info("hashword is {}".format(hashword))
            if hashword != model_file_hash:
                logging.info("sp model hash not match")
                aws_handler.download_fromS3(s3_path, local_path)

        # decompress
        logging.info("zip_helper decompressor")
        zip_helper = ZipHandler(model_file_name, zip_type, "")
        zip_helper.decompressor(model_dir, model_dir)

        # load sp model
        logging.info("load sp model")
        sp_path = "".join([mdir, "/" , model_file_name, ".model"])
        if sp_path != None:
            sp = spm.SentencePieceProcessor()
            sp.Load(sp_path)
        else:
            logging.error("There is no models {}".format(sp_path))
            sp = None

        # multiprocessing text cleansing
        logging.info("text cleansing in multiprocessing")
        cpu = cpu_count() - 1
        p = Pool(cpu)

        part_func = partial(process, sp=sp)
        l_tokenized = p.map(part_func, array_text)

        p.close()
        p.join()

        return {"array_text": l_tokenized}

    except Exception as e:
        logging.error("Error message is {}. ".format(e))
        return {"error": str(e)}
