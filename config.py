import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("27862677"))
API_HASH = os.getenv("e343ce2c81b2b6c2c0d6bee58284e3bd")
BOT_TOKEN = os.getenv("6944835957:AAEFIiHb3cNOp0CI0BNTAT-AwK9vXf4lLFQ")
sudo_group = int(os.getenv("-4232283991"))
log_channel = int(os.getenv("5881684718"))




#import os

#API_ID = API_ID = 8130624

#API_HASH = os.environ.get("API_HASH", "67a71560b00a31ffa692c67428f06d38")

#BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

#PASS_DB = int(os.environ.get("PASS_DB", "721"))

#OWNER = int(os.environ.get("OWNER", 2026665680 ))

#LOG = -1001839916818

#SUDO_GROUP = -1001967980743

#try:
    #ADMINS=[]
   # for x in (os.environ.get("ADMINS","2018633153").split()):
    #    ADMINS.append(int(x))
#except ValueError:
    #    raise Exception("Your Admins list does not contain valid integers.")
#ADMINS.append(OWNER)
