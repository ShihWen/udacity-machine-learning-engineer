from __future__ import print_function

import argparse
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# sklearn.externals.joblib is deprecated in 0.21 and will be removed in 0.23. 
#from sklearn.externals import joblib
# Import joblib package directly
import joblib

## TODO: Import any additional libraries you need to define a model
from sklearn.svm import SVR
#from sklearn import linear_model

# Provided model load function
def model_fn(model_dir):
    """Load model from the model_dir. This is the same model that is saved
    in the main if statement.
    """
    print("Loading model.")
    
    # load using joblib
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    print("Done loading model.")
    
    return model


## TODO: Complete the main code
if __name__ == '__main__':
    
    # All of the model parameters and training parameters are sent as arguments
    # when this script is executed, during a training job
    
    # Here we set up an argument parser to easily access the parameters
    parser = argparse.ArgumentParser()

    # SageMaker parameters, like the directories for training data and saving models; set automatically
    # Do not need to change
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    
    ## TODO: Add any additional arguments that you will need to pass into your model
    
    # args holds all passed-in arguments
    args = parser.parse_args()

    # Read in csv training file
    training_dir = args.data_dir
    train_data = pd.read_csv(os.path.join(training_dir, "train_tms.csv"), skiprows=1, header=None, names=None)

    # Labels are in the first column
    train_y = train_data.iloc[:,-1]
    train_x = train_data.iloc[:,:-1]
    
    # Normalize and split data
    scaler = MinMaxScaler()

    # store them in this dataframe
    train_x=pd.DataFrame(scaler.fit_transform(train_x.astype(float)))
    

    
    
    
    ## --- Your code here --- ##
    

    ## TODO: Define a model 
    #model = None
    #model = linear_model.LogisticRegression()
    model = SVR(kernel='rbf',
                C=100,
                gamma=0.1,
                epsilon=0.1)
    
    ## TODO: Train the model
    model.fit(train_x, train_y)
    
    
    
    ## --- End of your code  --- ##
    

    # Save the trained model
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
