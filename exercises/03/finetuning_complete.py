from transformers import AutoModelForMaskedLM
import torch
from transformers import AutoTokenizer
from datasets import load_dataset
from transformers import DataCollatorForLanguageModeling
from transformers import TrainingArguments
from transformers import Trainer
import math



def test_model(model, tokenizer):
    text = "This is a great [MASK]."
    #text = "This is a great sdkfjsdhfjfj [MASK]."

    inputs = tokenizer(text, return_tensors="pt") # we want a pytorch tensor
    token_logits = model(**inputs).logits # what are logits? raw output, before applying softmax
    # predict an output for each input. If not masked -> input = output.
    print(inputs["input_ids"]) # insert special charaters for start and end. Replace the
    print(token_logits.shape)
    # exit()

    # Find the location of [MASK] and extract its logits
    mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]
    mask_token_logits = token_logits[0, mask_token_index, :]
    print(mask_token_index)
    print(mask_token_logits.shape)
    #exit()

    # Pick the [MASK] candidates with the highest logits
    top_5_tokens = torch.topk(mask_token_logits, 5, dim=1).indices[0].tolist()
    print(top_5_tokens) # highest values in the logit represent the likliest predictions
    for token in top_5_tokens:
        print(f"'>>> {text.replace(tokenizer.mask_token, tokenizer.decode([token]))}'") # token+1
    print()
    #exit()


def group_texts(examples):
    # Concatenate all texts
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    # Compute length of concatenated texts
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the last chunk if it's smaller than chunk_size
    total_length = (total_length // chunk_size) * chunk_size
    # Split by chunks of max_len
    result = {
        k: [t[i : i + chunk_size] for i in range(0, total_length, chunk_size)]
        for k, t in concatenated_examples.items()
    }
    # Create a new labels column
    result["labels"] = result["input_ids"].copy()
    return result



###########################
# Init Pre-trained model
###########################

model_checkpoint = "distilbert-base-uncased"
model = AutoModelForMaskedLM.from_pretrained(model_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint) # can someone tell me what a tokenizer is?

distilbert_num_parameters = model.num_parameters() / 1_000_000
print()
print(f"'>>> DistilBERT number of parameters: {round(distilbert_num_parameters)}M'")
print(f"'>>> BERT number of parameters: 110M'")
print()

test_model(model, tokenizer)
#exit()


###########################
# Init Dataset for Finetuning
###########################

imdb_dataset = load_dataset("imdb")

print(">>> IMDB Dataset structure:\n", imdb_dataset, "\n")
sample = imdb_dataset["train"].shuffle(seed=42).select(range(1))
for row in sample:
    print(f"\n'>>> Review: {row['text']}'")
    print(f"'>>> Label: {row['label']}'")
print()
#exit()



###########################
# Preparing the data for masked language modeling
###########################

def tokenize_function(examples):
    result = tokenizer(examples["text"])
    if tokenizer.is_fast:
        result["word_ids"] = [result.word_ids(i) for i in range(len(result["input_ids"]))]
    return result

tokenized_datasets = imdb_dataset.map(tokenize_function, batched=True, remove_columns=["text", "label"]) # tokenize the dataset (25_000 reviews)

chunk_size = 128
lm_datasets = tokenized_datasets.map(group_texts, batched=True)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15) # randomly replace tokens with [MASK]

print(lm_datasets) # 61_000 chunks, each containing 128 tokens
print("Masked corpus:")
sample = lm_datasets["train"][0] # sample = first chunk (128 tokens) in "input_ids"
sample.pop("word_ids")
chunk = torch.tensor(sample["input_ids"])
chunk_masked = data_collator([sample])["input_ids"][0]
print(chunk)
print(chunk.shape)
print(chunk_masked)
print(chunk_masked.shape)
print(f"\n'>>> {tokenizer.decode(chunk)}'") # what is a chunk? tensor, containing 128 integers. Decode it using the tokenizer
print(f"\n'>>> {tokenizer.decode(chunk_masked)}'")
print()
exit()


###########################
# Fine-tune the model
###########################

train_size = 10_000
test_size = int(0.1 * train_size)

downsampled_dataset = lm_datasets["train"].train_test_split(
    train_size=train_size, test_size=test_size, seed=42
)

batch_size = 64
logging_steps = len(downsampled_dataset["train"]) // batch_size
model_name = model_checkpoint.split("/")[-1]

training_args = TrainingArguments(
    output_dir=f"{model_name}-finetuned-imdb",
    overwrite_output_dir=True,
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    push_to_hub=False,
    fp16=False,
    logging_steps=logging_steps,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=downsampled_dataset["train"],
    eval_dataset=downsampled_dataset["test"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)

eval_results = trainer.evaluate()
print(f">>> Perplexity: {math.exp(eval_results['eval_loss']):.2f}")

for epoch in range(1):
    trainer.train()
    eval_results = trainer.evaluate()
    print(f">>> Perplexity: {math.exp(eval_results['eval_loss']):.2f}")

model.to("cpu")

test_model(model, tokenizer)
