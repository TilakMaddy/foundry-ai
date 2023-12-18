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


print(len(url2fs))


from qdrant_client import QdrantClient
import json
from tqdm import tqdm


qdrant_client = QdrantClient("http://localhost:6333")
qdrant_client.set_model("sentence-transformers/all-MiniLM-L6-v2")

qdrant_client.recreate_collection(
    collection_name="foundry-book",
    vectors_config=qdrant_client.get_fastembed_vector_params(),
)

metadata = []
documents = []

for (live_url, local_path) in url2fs.items():
    
    with open(local_path) as f:
        document = f.read()

    _metadata = {
        "url": live_url
    }

    documents.append(document)
    metadata.append(_metadata)


qdrant_client.add(
    collection_name="foundry-book",
    documents=documents,
    metadata=metadata,
    ids=tqdm(range(len(documents))),
)
