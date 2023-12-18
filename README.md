# Foundry AI 

![Logo](foundry-image-widescreen.png)

## What is Foundry AI ?
It is your personal assitant for interacting with the foundry book for smart contract development. It requires gpt 3.5 and it answers with up-to-date information. This is possible because of retrieval augmented generation technique which sends over the relavant documentation files based on the question asked.

*It isn't really in a useable condition yet. We still need to figure out the best prompt, the best embedding, etc. But you certainly can run the program and play around with it!*

## How to use it ?

#### Create a locally running vector store
```
docker pull qdrant/qdrant
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

#### Clone this repository and inference

```
cd resolver
```

Now, install the dependencies from pyproject.toml 

Load the data into the vector store - 
```
python resolver/load_foundry_book.py # index the latest foundry book
```


Put your *OPENAI_API_KEY* in `.env` as shown in `.env.sample`

Now, let's go inference !!

```bash
python resolver/search_foundry.py
```

Enjoy :) 

-----------

### Feedbacks
Any and all feedbacks are welcome ! Positive or negative doesn't matter. (just don't insult people)



