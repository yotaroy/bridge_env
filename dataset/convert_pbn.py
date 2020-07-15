import json
from tqdm import tqdm

dataset_path = 'eval/deal_5000k.json'
pbn_file_path = 'eval/deal_5000k.pbn'


with open(dataset_path, 'r') as fr:
    for line in tqdm(fr):
        game = json.loads(line)

        dealer = game['dealer']
        vulnerable = game['vul']
        deal = game['pbn_hands']
        seed = game['seed']
        dds = json.dumps(game['dds_results'])

        with open(pbn_file_path, 'a') as fw:
            fw.write('[Dealer "{}"]\n'.format(dealer))
            fw.write('[Vulnerable "{}"]\n'.format(vulnerable))
            fw.write('[Deal "{}"]\n'.format(deal))
            fw.write('[Seed "{}"]\n'.format(seed))
            fw.write('[DDS "{}"]\n'.format(dds))
            fw.write('\n\n')







