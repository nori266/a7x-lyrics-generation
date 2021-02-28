import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config


tokenizer = GPT2Tokenizer.from_pretrained(
    'gpt2',
    bos_token='<|startoftext|>',
    eos_token='<|endoftext|>',
    pad_token='<|pad|>'
)

configuration = GPT2Config.from_pretrained('gpt2', output_hidden_states=False, vocab_size=50257)
model = GPT2LMHeadModel.from_pretrained("gpt2", config=configuration)
model.resize_token_embeddings(len(tokenizer))

m_state_dict = torch.load('model/pytorch_model.bin', map_location='cpu')
model.load_state_dict(m_state_dict)
model.eval()


def generate_by_prompt(prompt: str = None) -> str:
    tokens = prompt.split()
    if len(tokens) > 1:
        prompt = f"{prompt}\n"
    else:
        prompt = f"{prompt} "

    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    generated = generated.to('cpu')

    sample_output = model.generate(
        generated,
        do_sample=True,
        top_k=50,
        max_length=300,
        top_p=0.95,
        num_return_sequences=1
    )

    return tokenizer.decode(sample_output[0], skip_special_tokens=True)
