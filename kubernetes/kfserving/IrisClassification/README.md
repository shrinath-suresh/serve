# Iris Classification

This example performs classification of flower as one among these three types - `SETOSA` , `VERSICOLOR`, `VIRGINICA`

Run the following command to train the model

Command: 
```
python iris_classification.py

```

At the end of the training process, the trained model is exported as `iris.pt`

## Generating mar file

create model_store directory if not present

`mkdir model_store`

Run the following command to generate mar file into model_store

```
torch-model-archiver --model-file iris_classification.py --handler iris_handler.py --version 1.0 --export-path model_store --serialized-file iris.pt --model-name iris --extra-files index_to_name.json
```

## Deploying the model

Ensure to set `model_snapshot` and `service_envelope` in config.properties file before starting torchserve

For example:

```
service_envelope=kfserving
model_snapshot={"name":"startup.cfg","modelCount":1,"models":{"iris":{"1.0":{"defaultVersion":true,"marName":"iris.mar","minWorkers":1,"maxWorkers":2,"batchSize":2,"maxBatchDelay":200,"responseTimeout":60}}}}
```

start the torchserve and wait for the worker to be loaded

```
torchserve --start --ts-config config.properties
```


## Performing predictions

Sample input is placed in `kubernetes/kfserving/kf_request_json/iris.json`

Run the following command from root folder to perform prediction using KFServing api

```
curl -H "Content-Type: application/json" --data @kubernetes/kfserving/kf_request_json/iris.json http://127.0.0.1:8080/v1/models/iris:predict
```

Prediction result will appear in the console



