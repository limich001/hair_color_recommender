import gradio as gr
from PIL import Image
import os
import json

from FastSAM.fastsam import FastSAM, FastSAMPrompt
import google.generativeai as genai

import matplotlib

# Use TkAgg if tk is available, otherwise fallback to Agg
matplotlib.use('TkAgg' if 'DISPLAY' in os.environ else 'Agg')

def hair_color_recommender(user_input) -> str:
  # Google Generative AI（Gemini API）のAPIキー設定
  genai.configure(api_key=os.environ['GEMINI_API_KEY'])

  # Geminiモデルの設定
  model = genai.GenerativeModel(
    model_name='gemini-1.5-pro-latest',
    system_instruction=[
      "あなたはヘアスタイリストです。",
      "これからユーザがおすすめの色を提案してくるので、それに基づいた回答をRGBの値で、次のJSON形式でお願いします。",
      "{\"color\": [\"RED\", \"GREEN\", \"BLUE\"]}"
    ]
  )

  # Gemini APIを使って応答を生成
  response = model.generate_content(user_input)

  # 応答をテキストとして取得
  assistant_response = response.text
  print(assistant_response)

  return json.loads(assistant_response)

def uploaded_image(image, state):
    new_state = {
        "user_input_text": state["user_input_text"],
        "user_input_image": image,
    }

    if state["user_input_image"] != None and state["user_input_text"] != "":
        return new_state
    else:
        return new_state

def input_text(text, state):
    new_state = {
        "user_input_text": text,
        "user_input_image": state["user_input_image"]
    }

    if state["user_input_image"] != None and state["user_input_text"] != "":
        return new_state
    else:
        return new_state

def userImge_to_haircolorImage(input_image, recommend_color_json):
  model = FastSAM('FastSAM-x.pt')
  DEVICE = "cpu"

  everything_results = model(input_image, device=DEVICE, retina_masks=True, imgsz=1024, conf=0.4, iou=0.9,)
  prompt_process = FastSAMPrompt(input_image, everything_results, device=DEVICE)

  ann = prompt_process.text_prompt(text='hair')
  output_image = prompt_process.plot_to_result(annotations=ann, withContours=False, mask_random_color=False, color_dict=recommend_color_json)

  return Image.fromarray(output_image, 'RGB')

def recommend_hair_color_image(state):
    recommend_color_json = hair_color_recommender(state["user_input_text"])
    output_image = userImge_to_haircolorImage(state["user_input_image"], recommend_color_json)

    return output_image # レコメンド後の画像を出力

with gr.Blocks() as demo:
    initial_state = {
        "user_input_text": "",
        "user_input_image":  None
    }
    state = gr.State(initial_state)

    user_input_image = gr.Image(type="pil", label="あなたの顔画像をアップロードしてください")
    user_input_text = gr.Textbox()
    hair_color_image_output_button = gr.Button(value="あなたのおすすめの髪色を表示", visible=True)
    hair_color_image_output = gr.Image(type="pil", label="あなたにおすすめの髪色です")

    user_input_image.upload(fn=uploaded_image, inputs=[user_input_image, state], outputs=[state])
    user_input_text.change(fn=input_text, inputs=[user_input_text, state], outputs=[state])
    hair_color_image_output_button.click(fn=recommend_hair_color_image, inputs=[state], outputs=[hair_color_image_output])

demo.launch(debug=True, server_name="0.0.0.0")
