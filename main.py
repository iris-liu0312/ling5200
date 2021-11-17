import pandas as pd

dataset = pd.read_csv('corpus.csv', encoding='utf8')
# print(dataset[dataset['conjugation_type']=='どう'].shape)


def select_form():
    print("\n=== Settings ======================================================")
    sent_type = input("Do you want to practice converting business terms to informal terms?\n(Y/N) >")
    if input in ['Q', 'q', '']:
        return None
    sent_type = 'business_sentence' if sent_type in ['Y','y','Yes','yes'] else 'common_sentence'
    print(f"You will be given {sent_type.replace('_', ' ')}s to convert.\n")
    return sent_type

def select_conj(dataset):
    conj_type = {}
    unq_id = 0
    for i in set(dataset['conjugation_type']):
        conj_type[unq_id] = i
        unq_id += 1

    print("Which conjugation do you want to practice? Enter the number of the corresponding conjugation.")
    for i in conj_type.keys():
        print(f"{i}: {conj_type[i]}")
    practice_conj = input(">")
    if practice_conj in ['Q', 'q', '']:
        return None
    while(int(practice_conj) not in conj_type.keys()):
        if practice_conj in ['Q', 'q', '']:
            return None
        print("Invalid input.")
        for i in conj_type.keys():
            print(f"{i}: {conj_type[i]}")
        practice_conj = input(">")
    return conj_type[int(practice_conj)]

def practice(dataset, conj, sent_type):
    print(f"\n=== {conj} ======================================================")
    conversion = 'informal form' if sent_type == 'business_sentence' else 'business form'
    print(f"Convert the term in the brackets 「...」to {conversion}.")
    print("Press enter to show the correct answer.")
    conversion = 'common_sentence' if sent_type == 'business_sentence' else 'business_sentence'
    for _, row in dataset.iterrows():
        q = input(row[sent_type])
        if q in ['Q', 'q']:
            return None
        print(row[conversion])
        q = input("Enter for the next sentence. >")
    return 'f'

def main():
    print("====================================================================")
    print("Welcome to the mini Japanese Business-Informal conjugation program.")
    print("This program will give you sentences with the conjugation you want\nto practice.")
    print("Press Ctrl+C or type 'q' at any time if you want to quit.")
    
    dataset = pd.read_csv('corpus.csv', encoding='utf8')
    cont = True

    while cont:
        sent_type = select_form()
        if sent_type is None:
            return
        conj = select_conj(dataset)
        if conj is None:
            return

        finish = practice(dataset[dataset['conjugation_type']==conj], conj, sent_type)
        if finish is None:
            return

        cont_q = input("You've finished practicing this set. Do you want to continue?\n(Y/N) >")
        if input in ['Q', 'q', '']:
            return 
        cont = True if cont_q in ['Y','y','Yes','yes'] else False

main()