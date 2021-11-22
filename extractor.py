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

# manually code dictionary of o-conjugations
o_conj = {'お出かけください': '出かけてください',
          'お楽しみください': '楽しんでください',
          'お電話をください': '電話をかけてください',
          'お電話ください': '電話をかけてください',
          'お聞かせください': '聞かせてください',
          'おたずねください': '来てください',
          'お尋ねください': '来てください',
          'お越しください': '来てください',
          'お選びください': '選んでください',
          'お待ちください': '待ってください',
          'おまちください': 'まってください',
          'お確かめください': '確かめてください',
          'お入りください': '入ってください',
          'お過ごしください': '過ごしてください',
          'お考えください': '考えてください',
          'お座りください': '座ってください',
          'お声掛けください': '声をかけてください',
          'お任せください': '任せてください',
          'お答えください': '答えてください',
          'お申しつけください': '申しつけてください'}

conj_type = []
common_sent = []
business_sent = []
# add conjugations and converted sentence to dataset
for sent in data_sent:
    for key in conjugations.keys():
        if key in sent:
            conj_type.append(conjugations[key][0])
            common_sent.append(sent.replace(key, conjugations[key][1]))
            business_sent.append(sent.replace(key, f"「{key}」"))

    # the two common conjugations, お/ご...ください → ...してください
    # note: there are more conjugations involved with the root than originally thought
    research = re.search(r"[おご].{2,4}ください", sent) # [おご].{2,4}ください
    if research is not None and research.group() not in conjugations.keys():
        # ご... only requires a simple replace
        if research.group()[0] == 'ご':
            # unfortunate inclusion (過)ごしてきてください
            if research.group() == 'ごしてきてください':
                continue
            common_term = f'「{research.group()[1:-4]}してください」'
        # お... requires more conjugation
        # unfortunate inclusion of verb that isn't a business conjugation
        elif research.group() == 'おいてください':
            continue
        elif research.group() in o_conj.keys():
            common_term = f'「{o_conj[research.group()]}」'
        else:
            common_term = research.group()
        conj_type.append('てください')
        common_sent.append(sent.replace(research.group(), common_term))
        business_sent.append(sent.replace(research.group(), f"「{research.group()}」"))

# export to csv
dataset = pd.DataFrame({'conjugation_type': conj_type,
                        'business_sentence': business_sent,
                        'common_sentence': common_sent})
dataset.to_csv('corpus.csv')