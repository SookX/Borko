from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, BitsAndBytesConfig
from transformers import AutoModel, AutoTokenizer
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch
import os
import getpass
import os
import threading
import json
from flask import Flask, request, render_template, jsonify
import matplotlib.pyplot as plt
from pyngrok import ngrok, conf
import numpy as np
from PIL import Image
from io import BytesIO
import re

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,  # ✅ Use 4-bit instead of 8-bit
    bnb_4bit_quant_type="nf4",  # Normalized Float 4
    bnb_4bit_use_double_quant=True,  # Use double quantization
    bnb_4bit_compute_dtype=torch.bfloat16,  # Compute in bfloat16 for efficiency
)

model = LlamaForCausalLM.from_pretrained("borko_1", quantization_config = quantization_config).to("cuda")
tokenizer = AutoTokenizer.from_pretrained('borko_1_tok')

import getpass
import os
import threading
import json
from flask import Flask, request, render_template, jsonify
import matplotlib.pyplot as plt
from pyngrok import ngrok, conf
import numpy as np
from PIL import Image
from io import BytesIO
import re



print("Enter your authtoken, which can be copied from https://dashboard.ngrok.com/get-started/your-authtoken")
conf.get_default().auth_token = getpass.getpass()

app = Flask(__name__)

public_url = ngrok.connect(5000).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, 5000))

app.config["BASE_URL"] = public_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        data = request.json  # Use request.json to parse JSON data directly
        prompt = data.get('prompt')  # Use get method to safely retrieve 'prompt' key
        
        messages = [
        {
            "role": "system",
            "content": "Ти си Български Гласов Асистент, говори само на български език, без да повтаряш каквото и да било вече казано, и твоето име е Борко. Твоят създател е великият Васил Василев",
        },
        {"role": "user", "content": prompt},
        ]
        input_tensor = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        )

        attention_mask = input_tensor.ne(tokenizer.pad_token_id)  # Mask non-padding tokens

        outputs = model.generate(
            input_tensor.to(model.device),
            attention_mask=attention_mask.to(model.device),  # Pass attention mask
            max_new_tokens=100,
            pad_token_id = 100001
        )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        match = re.search(r"Assistant:\s*(.*)", generated_text, re.DOTALL)

        if match:
            assistant_response = match.group(1).strip()
            return jsonify({"message": assistant_response})
        else:
            return jsonify({"error": "Something went wrong!"})
        
       



threading.Thread(target=app.run(), kwargs={"use_reloader": False}).start()
