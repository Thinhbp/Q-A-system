from transformers import BertTokenizer
from transformers import BertForQuestionAnswering
import torch





def load_model():
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    return tokenizer,model

def processing(question,paragraph):

    tokenizer, model=load_model()
    input_ids = tokenizer.encode(question, paragraph)
    sep_index = input_ids.index(tokenizer.sep_token_id)
    num_seg_a = sep_index + 1
    num_seg_b = len(input_ids) - num_seg_a
    segment_ids = [0] * num_seg_a + [1] * num_seg_b
    assert len(segment_ids) == len(input_ids)
    start_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]))[0]
    end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]))[1]
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer = tokens[answer_start]

    for i in range(answer_start + 1, answer_end + 1):
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        else:
            answer += ' ' + tokens[i]

    result =  answer

    return result
