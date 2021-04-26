import joblib

class ChairmanStatementClassifier(object):
    """
    This is the Chairman Statement Classifier

    ...

    Attributes
    ----------
    model : sklearn.pipeline.Pipeline
        the pipeline that contains the model on which this classifier is based (default is a random forest model)

    Methods
    -------
    classify(text)
        Classifies the input data set into new dialog or dialog continuation
    classification_score(text)
        Presents the probability of being a new dialog or a dialog continuation
    
    """
    def __init__(self, model_name='ChairmanStatementsClassifier_randomforest.pkl'):
      """
        Parameters
        ----------
        model_name : str
            The model chosen by the user that is present on the directory 
            (default is 'classifier1_randomforest.pkl')
      """
      #Loads the default model or the one chosen by the user
      self.model = joblib.load(model_name)

    def classify(self,text):
      """Classifies the input data set into two classes: new dialog (True) or dialog continuation (False)

      Parameters
      ----------
      text : Union[str, list, numpy.ndarray]
          The data to be classified

      Returns
      -------
      Union[bool, numpy.ndarray]
          a bool (if the data is a str) or a numpy array (if data is a list or 
          array) with the predicted results
      """
      predicted = self.model.predict(text)
      if len(predicted) == 1:
        return int(predicted) == 1
      else:
        return predicted

    def classification_score(self,text):
      """Presents the probability of being a new dialog or a dialog continuation based on the model

      Parameters
      ----------
      text : Union[str, list, numpy.ndarray]
          The data to be classified

      Returns
      -------
      numpy.ndarray
          a numpy array with the scores for each text given
      """
      return self.predict_proba(text)

    def __call__(self, _input):
      """
      Parameters
      ----------
      text : Union[str, list, numpy.ndarray]
          The data to be classified

      Returns
      -------
      Union[bool, numpy.ndarray]
          a bool (if the data is a str) or a numpy array (if data is a list or 
          array) with the predicted results
      """
      return self.classify(_input)