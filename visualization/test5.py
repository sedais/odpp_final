from nltk.tokenize import word_tokenize, sent_tokenize
from keybert import KeyBERT
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from pymongo import MongoClient
import pandas as pd
client = MongoClient(
    "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

print(client.list_database_names())
db = client.youtube_db
collection = db.transcripts
data = pd.DataFrame(collection.find())

list1 = ["apple", "orange", "tomato"]
text = "I would love an apple. It is a nice day. How are you? Tasty orange..."
sentences_with_word = []
for sen in sent_tokenize(text):
    l = word_tokenize(sen)
    if len(set(l).intersection(list1))>0:
        sentences_with_word.append(sen)

print(sentences_with_word)

list = ['repair', 'healthy', 'battery', 'change', 'remove', 'removal', 'easy', 'hard', 'repair', 'repairability']



doc = "on the outside the iPhone 14 looks just. like the iPhone 13 but internally. something major has happened. " \
         "last week I took apart the iPhone 14 pro. and found it's been programmed to reject. third-party repair this " \
         "week let's tear. down and assess the standard iPhone 14.. what they've done inside is something. none of us " \
         "saw coming. there's also been a rumor that Apple has. software paired the back glass to each. device but " \
         "that's just a speculation for. now we won't know until we've opened. them up and start swapping Parts " \
         "between. the phones. as there aren't any replacement parts to. test this I'll be using the other phone. as " \
         "a donor this time around I've. purchased a purple and red unit. just like the 12 and 13 series there's. no " \
         "included charger or headphones but. with these being International models. they still have a SIM reader " \
         "something. the US model doesn't. once both are out of the box I'll get. them set up and ensure they're " \
         "working. both phones are iPhone 14 A2 882 models. running iOS 16.0. how will its repairability stack up. " \
         "against the iPhone 14 pro. there's only one way to find out. I'll begin opening one of the phones by. first " \
         "placing it on a heat plate for. five minutes after I remove the. pentalobe security screws I Can Begin. " \
         "prying off the display. a suction cup can be used to lift up the. screen creating a gap just wide enough. " \
         "to get my pick in place working the pick. around the perimeter I can slice through. the adhesive. the " \
         "stronger adhesive Apple has been. using since the iPhone 12 has made this. step more difficult but if you " \
         "preheat. the display correctly it comes up fairly. easily. getting our first look inside the iPhone. 14 " \
         "you'll notice we can't see any. internals just a large section of. aluminum and two connections for the. " \
         "display. but don't fear there is a way inside. before we do that I'll continue. detaching the display there " \
         "are only two. screws and two brackets to remove an. improvement over previous models. with the display off " \
         "it's back to the. hay plate this time for the rear glass. another five minutes of heating and it. can be " \
         "pried off just like the display. unlike the 14 pro and previous. glass-backed iPhone models no longer do. " \
         "you need lasers to remove the glass the. back has now been made to be removable. it's held in with adhesive " \
         "and metal. Clips just like the display. opening this side up shows us a more. familiar layout the most " \
         "notable thing. is that now that we're looking at the. phone from the other side the rear. camera is facing " \
         "us the only iPhones to. open this way have been the first. generation iPhone 4 and 4S. before we get too " \
         "far I need to get the. other device open. it's great to see the back go from. almost impossible to remove " \
         "to quite. easy to replace but just because it's. now modular doesn't mean the iOS. software will allow you " \
         "to replace it in. my iPhone 14 pro video I demonstrated. how the phone prevented third-party. repair by " \
         "braking functionality when. certain parts are replaced rumor has it. that replacing the back causes " \
         "software. issues with the phone. I'll detach the back by removing two. brackets and unplugging the battery. " \
         "before the one cable running to the rear. panel. from here I'll begin disassembling the. necessary pieces " \
         "to gain access to the. phone's logic board or brain this will. be the part I swap between the phones. " \
         "simulating the replacement of every part. to see if this phone's design change has. led to any new " \
         "anti-third party repair. tactics. while the back is easier to remove when. compared to the 14 pro the logic " \
         "board. removal is harder there is one screw. hidden beneath the earpiece meaning I. have to take out some " \
         "more components to. be able to access that one screw even so. from a modularity standpoint this phone. is " \
         "still holding out quite well. the camera cable is held down with some. adhesive but once the two cameras " \
         "are. removed we can get a closer look at them. these are not as large as the 14 pro but. are still quite " \
         "substantial. with the final screws for the earpiece. out I can finally free the logic board. the iPhone 14 " \
         "features the a15 processor. from the previous year's iPhone making. it almost the same phone as last year " \
         "in. performance and exterior looks. internally as we can see things have. changed significantly the logic " \
         "board. now has connections on the back to allow. the display to be disconnected without. opening the other " \
         "side of the phone. to perform my part swab I'll also need. to remove the board from the other phone. now " \
         "it's time for our Switcheroo every. part inside each phone is genuine Apple. but just from the other phone " \
         "the red. bones logic board will go into the. purple phone and vice versa. before attaching the battery " \
         "I'll. install the display while I assume it's. safe to install the screen with the. battery connected based " \
         "on the new. internal design of the phone however I. don't want to risk it before conducting. my tests. " \
         "another interesting design Choice with. the 14 is having the bottom screws. fastening to both the rear and " \
         "front. display. I'll reassemble the other phone with its. foreign logic board so we can compare. results " \
         "which will allow me to double. check any issues that arise. upon boot we see the same error messages. that " \
         "arised on the 14 pro letting a user. know their parts may not be genuine it's. not a bad thing but Apple " \
         "has used this. to take away functionality making it. appear as though the repair was done. poorly like the " \
         "14 pro I tested last. week true tone is vanished auto. brightness no longer works. battery health is " \
         "disabled and face ID. no longer functions. as for the rumor about the rear glass. being software linked to " \
         "each specific. phone I cannot find that to be the case. wireless charging and the Flash work. fine and no " \
         "anti-third party messages. have appeared that's not to say they. couldn't be added in an update but. " \
         "there's nothing as of yet. the front cameras also display the same. issues as I was facing with the 14 pro. " \
         "however there's a fix to the issue. while attempting to update to iOS 16.0.2. using iTunes I accidentally " \
         "flashed the. wrong file and reinstalled iOS 16.0 what. I discovered from this is the front. cameras began " \
         "working again meaning if. you replace the front camera on the 14. and 14 pro you must restore update the. " \
         "phone to return functionality. however it should be noted that portrait. and cinematic mode don't function " \
         "with a. replacement camera. even after updating the phone to iOS. 16.0.2 it still didn't restore face ID. " \
         "or any other missing functionality. I understand preventing the replacement. of face ID on a passcode " \
         "locked phone. but if the phone is unlocked or reset. why can I not be allowed to enable it. again remember " \
         "this is supposed to be my. phone. of course if you pay Apple to repair the. phone or purchase parts from " \
         "their. self-repair program this won't be an. issue this is because Apple runs system. configuration which " \
         "pairs the parts and. removes the anti-third party repair. mechanisms this means to have a fully. functional " \
         "device you must use apple. this also means they can control the. pricing and possibly entice you into. " \
         "buying a new phone instead. considering this if you had to rate the. phone from 1 to 10 in terms of. " \
         "repairability what would you rate it at. iFixit gave it a 7 out of 10 saying it. was the most repairable " \
         "iPhone in years. and I couldn't disagree more. it's the most modular phone they've made. but modularity " \
         "doesn't mean. repairability especially if the software. prevents you from retaining full. functionality " \
         "after the replacement of. parts. I feel as though the 7 out of 10. repairability score is totally. " \
         "misleading. in contrast iFixit rates most Samsung. phones at a three or four penalizing. them for glued in " \
         "batteries and rear. glass entry. if you've watched any of my Samsung tear. down videos you'll know just how " \
         "easy. they are to work on all screws are. Phillips and most of the same size it. has a similar amount of " \
         "modularity as an. iPhone and when I perform the same. motherboard swap between the two phones. the Samsung " \
         "continued working as if. nothing had happened I could even unlock. the bootloader and Flash alternative. " \
         "software if I like. iFixit has been a channel sponsor since. 2019 I reached out to them because I was. so " \
         "impressed with their toolkits and I. still am I stand behind the products I. promote and I fix it is no " \
         "different but. when it comes to their repair scores I. just have to disagree with them. but with no new " \
         "software locks to report. it's time we continue taking apart the. phone down at the lower section you'll. " \
         "find the Sim reader and vibration motor. which Apple calls the taptic engine. next to come out is the " \
         "battery a. consumable item that will eventually. need replacement no matter how you treat. your phone Apple " \
         "has included two. stretch release tabs but they are. cramped between the battery and a metal. wall. given " \
         "the lack of space I'll wrap the. adhesive around my tweezers and pull it. out from beneath the battery " \
         "it's. important that you don't catch the. adjacent cable and tear it while doing. this. foreign. well it " \
         "looked like I got both tabs out. it appears they snapped at the bottom. which usually happens so it's time " \
         "for. some alcohol to break down the remaining. adhesive. once it's done its job I can pry out the. battery. " \
         "this. 3279 milliamp hour battery is ever so. slightly larger than the 3200 milliamp. hour battery found in " \
         "the iPhone 14 pro. with the battery out we're left with a. mid frame consisting of just a charging. port " \
         "speaker and some buttons. with that we've taken apart the iPhone. 14. it's proven vastly different to the. " \
         "insides of the iPhone 14 pro and even. the iPhone 13 it replaced apple is still. using four different types " \
         "of screws and. continues locking down third-party. repair but the ability to replace the. back glass is " \
         "still an improvement. now it's come time to reassemble both. phones. I often see comments about how " \
         "someone. doesn't want third-party repair or. wouldn't take their device anywhere else. but the manufacturer " \
         "and that's their. choice choice is what right to repair. fights for it's not about forcing people. into " \
         "fixing their own device or. preventing you from taking it to the. manufacturer to have it fixed it's about. " \
         "taking back control of something you. purchased I understand not all third. party repair is done correctly " \
         "but if. you want to take the risk or save money. that should be your choice. the repair history Apple is " \
         "implemented. in settings is actually useful to. second-hand buyers but it shouldn't. disable functionality " \
         "and make it look. as though the replacement part is faulty. that's the big issue I'm trying to. highlight. " \
         "for reinstalling the battery I've. modified an iPhone 6s adhesive to fit. there's currently not any " \
         "replacement. adhesive available so I've had to make. do with what I have. once installed I can attach the " \
         "front. cameras before plugging in the front. display. each bracket latches in place on one. side and is " \
         "secured with a screw on the. opposite end. I'll wipe down the inside to remove any. fingerprints or dust " \
         "before closing up. the display I haven't applied any new. adhesive as just like the battery it's. not yet " \
         "available. I'll connect the rear panel and fasten. its bracket into place after. reconnecting the battery " \
         "there's one. more bracket and two screws before I can. clean off the insides and seal down the. rear cover. " \
         "I'll reinstall the SIM card tray and the. two pentalobe screws on the bottom. and we're almost done there's " \
         "still one. more phone left to reassemble thankfully. I've kept track of all the screws and. correct parts " \
         "for each phone meaning we. shouldn't have any issues after both. phones are back together. after closing up " \
         "the rear panel and. installing the two pentalobe screws into. the bottom of the iPhone. we're done. so this " \
         "is it the iPhone 14. despite its. more modular design it still houses the. same anti-third party repair " \
         "mechanisms. as the iPhone 14 pro after reassembly. auto brightness true tone and battery. health have " \
         "returned but I'm still. getting a face ID error like I mentioned. before I'll need to reset the phone with. " \
         "iTunes to fix that issue it should be. noted that face ID will only return if. the module is the original " \
         "one. breaking down all the anti-third party. repair locks replacing your display will. remove true tone and " \
         "Brake auto. brightness a new battery will disable. battery health a new front camera will. break face ID " \
         "portrait mode and. cinematic mode a rear camera will only. give you a warning message and lastly. replacing " \
         "the logic board will trigger. all of the previous penalties. and on that note this has been a Hugh. " \
         "Jeffries video if you like what you saw. consider subscribing and check out the. tear down and repair " \
         "assessment playlist. for more videos just like this one and. if you're looking for any used devices. be " \
         "sure to check out my online store. link for which is down in the. description that's all for this video. " \
         "and I'll catch you guys next time. "

doc_fairphone = data.loc[240,'transcript_list']
id = data.loc[240,'video_id']
print(id)
#doc_fairphone = ' '.join(doc_fairphone).replace(".", " ")

# sentences_with_word = []
# for sen in sent_tokenize(doc_fairphone):
#     l = word_tokenize(sen)
#     if len(set(l).intersection(list))>0:
#         sentences_with_word.append(sen)
# print(sentences_with_word)

# kw_model = KeyBERT()
# keywords = kw_model.extract_keywords(sentences_with_word)
# words = kw_model.extract_keywords(sentences_with_word, keyphrase_ngram_range=(1, 1), stop_words='english')
# print(words)


task = 'sentiment'


# MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
# tokenizer = AutoTokenizer.from_pretrained(MODEL)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL)
# encoded_text = tokenizer(sentences_with_word, return_tensors='pt')
# output = model(**encoded_text)
# scores = output[0][0].detach().numpy()
# scores = softmax(scores)
#
# scores_dict ={
#     'roberta_neg': scores[0],
#     'roberta_neu': scores[1],
#     'roberta_pos': scores[2],
# }
#
# print(scores_dict)

doc_fairphone = ' '.join(doc_fairphone).replace(".", " ")
print(doc_fairphone)


# Split the text into words
words = doc_fairphone.split()

# Create a list of punctuated sentences
punctuated_sentences = []

# Iterate over the words and add punctuation marks between them
for i, word in enumerate(words):
    if i == 0:
        punctuated_sentences.append(word.capitalize())
    elif i == len(words) - 1:
        punctuated_sentences.append(word + '.')
    else:
        punctuated_sentences.append(word)


print(punctuated_sentences)

import spacy
nlp = spacy.load('en_core_web_sm')

# Tokenize the text
doc = nlp(doc_fairphone)

# Apply part-of-speech tagging
pos_tags = [(token.text, token.pos_) for token in doc]


# Create a list of punctuated sentences
punctuated_sentences = []

import nltk

# Text to be split into sentences
text = "I am a sentence. I am another sentence. I am a third sentence."

# Split the text into sentences
sentences = nltk.sent_tokenize(doc_fairphone)

# Print the sentences
print(sentences)

# import deepcorrect
#
# corrector = deepcorrect.DeepCorrect('models/english', 'cpu')
#
# text = 'hello how are you doing today'
#
# corrected_text = corrector.correct(text)
# print(corrected_text)

from deepcorrect import DeepCorrect
corrector = DeepCorrect('params_path', 'checkpoint_path')
corrector.correct('hey')
# 'Hey!'


