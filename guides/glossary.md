# Glossary

**Token:** A unit of text consumed by the model, often part of a word.

**Context length:** The number of tokens a model processes in one sequence.

**Parameters:** Learned numbers that determine model behavior.

**LoRA:** A method that trains small adapter matrices while freezing base weights.

**QLoRA:** LoRA training using a quantized base to reduce memory.

**Adapter:** The extra weights learned during parameter-efficient training. It needs the matching base.

**Merge:** Combine an adapter with base weights into one model.

**Quantization:** Represent weights with fewer bits to reduce storage and memory.

**GGUF:** A file format used by llama.cpp and compatible local runtimes.

**MLX:** Apple’s array framework for machine learning on Apple Silicon.

**Epoch:** One pass through the training dataset.

**Learning rate:** The scale of each optimizer update.

**Chat template:** The exact formatting and special tokens used for conversation roles.

**SFT:** Supervised fine-tuning on examples of desired responses.

**Validation set:** Data used while choosing training settings.

**Held-out evaluation:** Examples kept outside model fitting and tuning, used for the final comparison.

Next: [Start here](00-start-here.md).
