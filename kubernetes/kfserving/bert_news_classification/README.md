# News classification using HuggingFace Bert Model

This example performs news classification using Hugging Face bert model and requires `transformers` package to train and predict.
`trasnformers` package is added as a requirement in `requirements.txt` and stored along with the model using requirement argument.

Run the following command to train the model

Command: 
```
python news_classifier.py \
    --max_epochs 5 \
    --num_samples 50000
```

At the end of the training process, the trained model is exported as `bert.pt`

## Generating mar file

create model_store directory if not present

`mkdir model_store`

Run the following command to generate mar file into model_store

```
torch-model-archiver --model-name bert --serialized-file bert.pt --handler news_classifier_handler.py --export-path model_store/ -r requirements.txt --extra-files "class_mapping.json,bert_base_uncased_vocab.txt" -v 1.0 --model-file news_classifier.py
```

## Deploying the model

Ensure to set `model_snapshot` and `service_envelope` in config.properties file before starting torchserve

For example:

```
service_envelope=kfserving
model_snapshot={"name":"startup.cfg","modelCount":1,"models":{"bert":{"1.0":{"defaultVersion":true,"marName":"bert.mar","minWorkers":1,"maxWorkers":2,"batchSize":2,"maxBatchDelay":200,"responseTimeout":60}}}}
```

start the torchserve and wait for the worker to be loaded

```
torchserve --start --ts-config config.properties
```


## Performing predictions

Sample news text is placed in `kubernetes/kfserving/kf_request_json/bert.json`

Run the following command from root folder to perform prediction using KFServing api

```
curl -H "Content-Type: application/json" --data @kubernetes/kfserving/kf_request_json/bert.json http://127.0.0.1:8080/v1/models/bert:predict
```

Prediction result will appear in the console



