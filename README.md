# 環境構築

- Dockerfile の GEMINI_API_KEY を設定する部分で自分の GEMINI_API_KEY を設定する
```python
ENV GEMINI_API_KEY={YOUR_GEMINI_API_KEY}
```

- docker イメージ作成
```
$ make docker-build
```

- 作成したイメージでコンテナ起動
```
$ make docker-run
```


# テスト方法
http://localhost:7860/ にアクセスして確認

# FastSAM の変更点
- FastSAM/fastsam/prompt.py の fast_show_mask, fast_show_mask_gpu, plot_to_result 関数に対して、BGR 情報が入った color_dict を受け取って処理する変更を行いました。