## Log
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

#### NOV 2:
* prediction_request:
```json
{
  "user_id": "user_id_foo",
  "text": "This is a great movie",
  "time_date": "23:32:21PM"
}
```

* prediction_response:
```json
{
  "prediction_id": "foo",
  "user_id": "foo",
  "text": "This is a great movie",
  "time_date": "23:32:34PM",
  "prediction": "positive"
}
```

* DB 
```json
{
  "predictions": {
    "prediction_1": {
      "user_id": "foo",
      "text": "THis is a bad movie",
      "prediction": "positive",
      "feedback": "true",
      "time_date": "23:32:34PM"
    },
    "prediction_2": {
      "user_id": "foo",
      "text": "This is a bad movie",
      "prediction": "positive",
      "feedback": "true",
      "time_date": "23:32:34PM"
    } 
  }
}
```

#### Next:
* Implement models using MongoDB engine.