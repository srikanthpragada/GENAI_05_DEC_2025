from huggingface_hub import snapshot_download
from transformers import pipeline

model = "facebook/bart-large-mnli"
# This will *actually* re-download files
snapshot_download(
    repo_id= model,
    revision="main",
    force_download=True,
    local_files_only=False,
)

# Then load the pipeline (it’ll reuse the freshly downloaded snapshot)
classifier = pipeline("zero-shot-classification",
                      model= model)


classifier = pipeline("zero-shot-classification", 
                      model="facebook/bart-large-mnli", 
                      revision="main", 
                      force_download=True)
output = classifier(
    "Apple Released a new iPhone - iPhone 17 Pro",
    candidate_labels = ["education", "politics", "business"],
)
print(output)