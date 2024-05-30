FROM python:3.11-slim

WORKDIR /workspace

# 必要なビルドツール、git、OpenGLライブラリ、GLibライブラリをインストール
RUN apt-get update && \
    apt-get install -y gcc python3-dev git libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# FastSAM ディレクトリとします
ADD FastSAM /workspace/FastSAM

# main.py は個別に追加します
ADD main.py /workspace/

# requirements.txt をインストールします
RUN pip install -r /workspace/FastSAM/requirements.txt
RUN pip install gradio==3.39.0
RUN pip install google-generativeai

# OpenAIのCLIPをgitからインストールします
RUN pip install git+https://github.com/openai/CLIP.git

ENV GEMINI_API_KEY={YOUR_GEMINI_API_KEY}

CMD ["python", "main.py"]