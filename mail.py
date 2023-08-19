from pprint import pprint

db_location = "~/.thunderbird/13qld9w3.default-default/global-messages-db.sqlite"
address = "example@gmail.com"
get_mail_query = f"SELECT c0body from messagesText_content WHERE c3author LIKE '%{address}%' OR c4recipients LIKE '%{address}%'"

#update db
import os
#copy db_location to tmp
os.system("cp " + db_location + " /tmp/mail.sqlite")

# query db_location for mail from address
import sqlite3

conn = sqlite3.connect("/tmp/mail.sqlite")
c = conn.cursor()
c.execute(get_mail_query)
mail = c.fetchall()
conn.close()

#output mail
#print(corpus)

#from transformers import pipeline
corpus = ''.join([x[0] for x in mail])

chunk_n = len(corpus)//2000

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

chunks = [''.join(x) for x in list(split(corpus.splitlines(), chunk_n))]

from transformers import T5Tokenizer, T5ForConditionalGeneration

def generate(input_text):
  input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
  output = model.generate(input_ids, max_length=100)
  return tokenizer.decode(output[0], skip_special_tokens=True)

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl").to("cuda")

for chunk in chunks:
    input_text = "Summarize the following email conversation:\n{chunk}"
    print(generate(input_text))

#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


#print(summarizer(corpus, max_length=625, min_length=200, do_sample=False))
