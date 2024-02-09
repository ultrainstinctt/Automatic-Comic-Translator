from transformers import MarianTokenizer, MarianMTModel

src = "fr"  # source language
trg = "en"  # target language

model_name = f"Helsinki-NLP/opus-mt-{src}-{trg}"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

sample_text = "qui es-tu pour me dire ça, est-ce que tu me connais même ?"
batch = tokenizer([sample_text], return_tensors="pt")

generated_ids = model.generate(**batch)
jk=tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(jk)