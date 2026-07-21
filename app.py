# Write your code here
# Write your code here
from langchain_docling.loader import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

loader = TextLoader("tool_calling.py")
documents = loader.load()

# Split the Python file into code chunks
text_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

# Print the total number of chunks
print("Total number of chunks:", len(chunks))

# Print the content of the first chunk
print("\nFirst Chunk:\n")
print(chunks[0].page_content)

# Print the content of the second chunk
print("\nSecond Chunk:\n")
print(chunks[1].page_content)