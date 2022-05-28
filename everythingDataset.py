import torch
import pandas as pd
from transformers import AutoTokenizer


class EverythingDataset(torch.utils.data.Dataset):
    def __init__(self, df, tokenizer):
        self.size = len(df)
        self.features = tokenizer((df['prompt'] + ' [SEP] ' + df['utterance_data'] + '[SEP]' + df['speaker_utterance']).values.tolist(), truncation=True, padding=True)
        self.labels = df['emotion'].values.tolist() if ('emotion' in df.columns) else None

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.features.items()}
        if self.labels:
          item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return self.size