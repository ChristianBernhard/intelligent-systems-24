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

    # TODO: tokenize the text
    # TODO: predict the logits for each input token

    # TODO: Find the location of [MASK] and extract its logits
    mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]

    # TODO: print the top 5 predicted tokens for the masked token

def group_texts(examples):
    # TODO: Concatenate all texts
    # TODO: Compute length of concatenated texts
    # TODO: Drop the last chunk if it's smaller than chunk_size
    # TODO: Split by chunks of max_len
    # TODO: Create a new labels column
    return result



###########################
# Init Pre-trained model
###########################

model_checkpoint = "distilbert-base-uncased"

# TODO: load the distilBERT model and its tokenizer

distilbert_num_parameters = model.num_parameters() / 1_000_000
print()
print(f"'>>> DistilBERT number of parameters: {round(distilbert_num_parameters)}M'")
print(f"'>>> BERT number of parameters: 110M'")
print()

test_model(model, tokenizer)



###########################
# Init Dataset for Finetuning
###########################

# TODO: load the IMDB film review dataset

print(">>> IMDB Dataset structure:\n", imdb_dataset, "\n")
sample = imdb_dataset["train"].shuffle(seed=42).select(range(1))
for row in sample:
    print(f"\n'>>> Review: {row['text']}'")
    print(f"'>>> Label: {row['label']}'")
print()



###########################
# Preparing the data for masked language modeling
###########################

def tokenize_function(examples):
    result = tokenizer(examples["text"])
    if tokenizer.is_fast:
        result["word_ids"] = [result.word_ids(i) for i in range(len(result["input_ids"]))]
    return result

# TODO: tokenize the dataset

chunk_size = 128
lm_datasets = tokenized_datasets.map(group_texts, batched=True)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

# TODO: print the first sample of the masked corpus



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

# TODO: fine-tune the model

# TODO: model is at cuda. Move it to cpu

test_model(model, tokenizer)
