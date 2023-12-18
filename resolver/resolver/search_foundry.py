import os
from urllib.parse import urljoin

docs_path = os.path.join("foundry-book", "src")

BASE_URL = "https://book.getfoundry.sh/"

url2fs = {} # url -> file system (*.md) mapping

for root, dirnames, filenames in os.walk(docs_path):
    for filename in filenames:
        if not filename.endswith(".md"):
            continue
        if "README" in filename or "SUMMARY" in filename:
            continue
        rel_path = root.removeprefix("foundry-book/src")
        u = urljoin(BASE_URL, rel_path + "/" + filename[:-3])
            
        live_url = u # where you can go to find docs
        path_to_rst = os.path.join(root, filename)
        url2fs[live_url] = path_to_rst



from qdrant_client import QdrantClient
import ask_chatgpt
import os

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # initialize Qdrant client
        self.qdrant_client = QdrantClient("http://localhost:6333")
        self.qdrant_client.set_model("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, text: str):
        search_result = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=None,  # If you don't want any filters for now
            limit=3  # 3 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        metadata = [hit.metadata for hit in search_result]
        return metadata


docs_searcher = NeuralSearcher(collection_name='foundry-book')

while True:

    print("Foundry Interactive Docs ~ \n")
    print()

    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    search_term = "".join(contents)

    relavent_docs = docs_searcher.search(search_term)
    urls = [x["url"] for x in relavent_docs]
    print()
    print("Relavnt foundry book links: ")
    print(urls)
    print()

    conf = input("Ask chatgpt for help too? (y/n) ")
    if conf.lower() == "n":
        continue

    print("Frame your question: ")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    question = "".join(contents)

    relavent_docs = docs_searcher.search(search_term + " " + question)
    urls = [x["url"] for x in relavent_docs]
    print("Relavnt foundry book links: ")
    print(urls)

    context = ""

    for u in urls:
        with open(url2fs[u]) as f:
            content = f.read()
            if len(context) + len(content) < 900:
                context += f"""
                Document
                --------
                {content}


                """
    
    prompt = f"""
    Here is the data from the official documents that you should refer to. At the end,
    you will find the question to answer. Make sure you answer correctly.

    {context}

    Question 
    --------
    {search_term}
    {question}

    Please answer the question

    """

    print("asking chatgpt ... ")
    chat_gpt_ans = ask_chatgpt.ask_chatgpt(prompt)
    relavent_docs = docs_searcher.search(chat_gpt_ans)
    urls = [x["url"] for x in relavent_docs]
    print("Relavnt solidity docs links:")
    print(urls)
    print()
    print("Chat gpt answer:")
    print(chat_gpt_ans)
    print()



    print()
    print()



