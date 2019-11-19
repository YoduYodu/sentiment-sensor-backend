## Log
### CLI
```shell script
python3 manage.py runserver
```

#### OCT 6
* Initialize project

#### OCT 14, 15
* Grabs all the text file.
* Split the source dataset into train and test, 10% for validation
* Initialize the model, get the learning rate plot.
* Train the model, fine tune it, and save the fine-tuned encoder.
* Train another model classifier using the saved encoder and train the model 4 times.
* Save the model(model.pth) for future use.

#### OCT 27
* Implemented a predict API and its endpoint.

#### NOV 2
##### /predictions
* POST /predictions 
 
Request:

```json
{
  "user_id": "foo",
  "text": "foo"
}
```

Response:
```json
{
    "prediction_id": "foo",
    "user_id": "foo",
    "text": "foo",
    "is_positive": true,
    "time_date": "23:32:34PM",
    "object": "prediction"
}
```

##### /accuracies
* POST /accuracies  

Request:

```json
{
  "prediction_id": "foo",
  "is_accurate": "YES/NO"
}
```

Response:

```json
{
  "prediction_id": "foo",
  "is_accurate": "YES/NO",
  "object": "accuracy"
}
```

#### Nov 16
* Modify Prediction model
* Add Accuracy model

#### Nov 18
* Finish predictions api
* Connect to MongoDb

#### Next:
* Implement models using MongoDB engine.
* Change fastai models path