import pandas as pd
import os

ed_label_dict = {'sad': 0, 'trusting': 1, 'terrified': 2, 'caring': 3, 'disappointed': 4,
         'faithful': 5, 'joyful': 6, 'jealous': 7, 'disgusted': 8, 'surprised': 9,
         'ashamed': 10, 'afraid': 11, 'impressed': 12, 'sentimental': 13, 
         'devastated': 14, 'excited': 15, 'anticipating': 16, 'annoyed': 17, 'anxious': 18,
         'furious': 19, 'content': 20, 'lonely': 21, 'angry': 22, 'confident': 23,
         'apprehensive': 24, 'guilty': 25, 'embarrassed': 26, 'grateful': 27,
         'hopeful': 28, 'proud': 29, 'prepared': 30, 'nostalgic': 31}

ed_emo_dict =  {v: k for k, v in ed_label_dict.items()}


def get_speaker_info(speaker_id):
    if int(speaker_id) % 2 == 0:
        speaker = 1 # listener utterance
    else:
        speaker = 0  # speaker utterance
    return speaker

def data_reader(data_folder, datatype,save=True):

    '''
    Reads the raw data from EmpatheticDialogues dataset, preprocess the data and save it in a pickle file

    '''
    print("Datatype:",datatype)

    ongoing_utterance_list = []
    ids = []
    speaker_info = []

    # data = {'utterance_data':[],'emotion_label':[],'emotion':[],'prompt':[], 'utterance_data_combined':[],'utterance_id':[],"speaker_info":[],"speaker_utterance":[]}
    data = {'utterance_data':[],'emotion_label':[],'emotion':[],'prompt':[], 'utterance_data_combined':[],'utterance_id':[],"speaker_info":[],"speaker_utterance":[], "listener_utterance":[], "conv_id":[]}
    df = open(os.path.join(data_folder, f"fixed_{datatype}.csv")).readlines()

    for i in range(2,len(df)): # starts with 2 becauase df[0] is the coloumn headers, so i-1 i.e. 2-1=1 will start from the actual data

        prev_utterance_parts = df[i-1].strip().split(",")
        current_utterance_parts = df[i].strip().split(",")
        # print(current_utterance_parts)

        if prev_utterance_parts[0] == current_utterance_parts[0]: #to detect if its the ongoing conversation or the next conversation
            # print(prev_utterance_parts[3])
            prev_utterance_str = prev_utterance_parts[3].replace("_comma_", ",") #replace _comma_ for utterance
            ongoing_utterance_list.append(prev_utterance_str)
            ids.append((prev_utterance_parts[0],prev_utterance_parts[1]))
            speaker_info.append(get_speaker_info(prev_utterance_parts[1]))


            if i == len(df)-1 : # reaches the end of the dataset and this adds the last utterance to the ongoing utterance list


                current_utterance_str = current_utterance_parts[3].replace("_comma_", ",") #replace _comma_ for utterance
                prompt_str = current_utterance_parts[2].replace("_comma_", ",")
                if (datatype != 'test'):
                    emotion_label_int = int(current_utterance_parts[4])
                    emotion_label_str = ed_emo_dict[emotion_label_int]
                conv_id = current_utterance_parts[0]

                ongoing_utterance_list.append(current_utterance_str)
                ids.append((current_utterance_parts[0],current_utterance_parts[1]))
                speaker_info.append(get_speaker_info(current_utterance_parts[1]))

                data["utterance_data"].append(ongoing_utterance_list)
                if (datatype != 'test'):
                    data["emotion_label"].append(emotion_label_str)
                    data["emotion"].append(emotion_label_int)
                data["utterance_id"].append(ids)
                data["prompt"].append(prompt_str)
                data["speaker_info"].append(speaker_info)
                data["utterance_data_combined"].append("".join(ongoing_utterance_list))
                data["speaker_utterance"].append("".join(ongoing_utterance_list[0::2]))
                data["listener_utterance"].append("".join(ongoing_utterance_list[1::2]))
                data["conv_id"].append(conv_id)


        else:  # condition where it reaches the end of a conversation, so the prev_utterance was part of the previous conversation which is added to the ongoing utterance list

            prev_utterance_str = prev_utterance_parts[3].replace("_comma_", ",") #replace _comma_ for utterance
            prompt_str = prev_utterance_parts[2].replace("_comma_", ",")
            if (datatype != 'test'):
                emotion_label_int = int(prev_utterance_parts[4])
                emotion_label_str = ed_emo_dict[emotion_label_int]
            conv_id = prev_utterance_parts[0]

            ongoing_utterance_list.append(prev_utterance_str)
            ids.append((prev_utterance_parts[0],prev_utterance_parts[1]))
            speaker_info.append(get_speaker_info(prev_utterance_parts[1]))

            data["utterance_data"].append(ongoing_utterance_list)
            if (datatype != 'test'):
                data["emotion_label"].append(emotion_label_str)
                data["emotion"].append(emotion_label_int)
            data["utterance_id"].append(ids)
            data["prompt"].append(prompt_str)
            data["speaker_info"].append(speaker_info)
            data["utterance_data_combined"].append("".join(ongoing_utterance_list))
            data["speaker_utterance"].append("".join(ongoing_utterance_list[0::2]))
            data["listener_utterance"].append("".join(ongoing_utterance_list[1::2]))
            data["conv_id"].append(conv_id)

            ongoing_utterance_list = []
            ids = []
            speaker_info = []

    if (datatype != 'test'):
        assert len(data["prompt"]) == len(data["emotion"]) == len(data["utterance_data"]) == len(data["utterance_id"]) == len(data["speaker_info"])
        save_data = {"prompt":data["prompt"],"utterance_data":data["utterance_data_combined"],"speaker_utterance":data["speaker_utterance"],"listener_utterance":data["listener_utterance"], "emotion":data["emotion"],"emotion_label":data["emotion_label"], "speaker_info":data["speaker_info"]}
    elif (datatype == 'test'):
        assert len(data["prompt"]) == len(data["utterance_data"]) == len(data["utterance_id"]) == len(data["speaker_info"]) == len(data["conv_id"])
        save_data = {"conv_id":data["conv_id"], "prompt":data["prompt"],"utterance_data":data["utterance_data_combined"],"speaker_utterance":data["speaker_utterance"],"listener_utterance":data["listener_utterance"], "speaker_info":data["speaker_info"]}
    df = pd.DataFrame(save_data)
    df.to_csv("data/empathetic_dialogues/"+datatype+".csv",index=False)

if __name__ == '__main__':
    
    if not os.path.isdir('data/empathetic_dialogues/'):
        os.mkdir('data/empathetic_dialogues/')

    for i in ['train','valid', 'test']:
        data_reader("data/",i)
