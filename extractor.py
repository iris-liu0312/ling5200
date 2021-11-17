import pandas as pd
import re
from pandas._libs.missing import NA

# import data
with open('../BSD/train.json', encoding='utf8') as f:
    data = pd.read_json(f)

# extract conversations that were originally in japanese
og_jp = data[data['original_language'] == 'ja']['conversation']

# extract japanese sentences into a separate dataset
data_sent = []
for i in og_jp:
    for j in i:
        data_sent.append(j['ja_sentence'])

# create common conjugation dictionary
# format: 'business_conjugation': ('conjugation type', 'common_conjugation')
conjugations = {'と申します': ('と申します', '「です」'),
                'おります': ('います', '「います」'),
                'いらっしゃいます': ('います', '「います」'),
                'おっしゃる': ('言う', '「言う」'),
                'いかが': ('どう', '「どう」'),
                'いただき': ('もらう', '「もらい」'),
                'いただけます': ('もらう', '「もらえます」'),
                'いただいた': ('もらう', '「もらった」'),
                'お越しいただいて': ('もらう', '「来てもらって」'),
                'いたします': ('します', '「します」'),
                '致します': ('します', '「します」'),
                'ご覧ください': ('てください', '「見てください」'),
                'お目通しください': ('てください', '「見てください」')}

conj_type = []
common_sent = []
business_sent = []
ogo_conj = set()
# add conjugations and converted sentence to dataset
for sent in data_sent:
    for key in conjugations.keys():
        if key in sent:
            conj_type.append(conjugations[key][0])
            common_sent.append(sent.replace(key, conjugations[key][1]))
            business_sent.append(sent.replace(key, f"「{key}」"))

    # the two common conjugations, お/ご...ください → ...してください
    # problem: there are more conjugations involved with the root than originally thought
    # TODO: deal with the "exception" conjugations
    research = re.search(r"[おご].{2,4}ください", sent) # [おご].{2,4}ください
    if research is not None and research.group() not in conjugations.keys():
        ogo_conj.add(research.group())
        # ご... only requires a simple replace
        if research.group()[0] == 'ご':
            common_term = f'「{research.group()[1:-4]}してください」'
        # お... requires more conjugation
        elif research.group() == 'お待ちください':
            common_term = '「待ってください」'
        # unfortunate verb that isn't a conjugation but was captured anyway
        elif research.group() == 'おいてください':
            continue
        else:
            common_term = research.group()
        conj_type.append('てください')
        common_sent.append(sent.replace(research.group(), common_term))
        business_sent.append(sent.replace(research.group(), f"「{research.group()}」"))
# print(ogo_conj)

# export to csv
dataset = pd.DataFrame({'conjugation_type': conj_type,
                        'business_sentence': business_sent,
                        'common_sentence': common_sent})
dataset.to_csv('corpus.csv')