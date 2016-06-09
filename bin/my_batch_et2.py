'''
Created on Sep 17, 2013

@author: desouza

this code train the Extremely Randomized Tree regression models 
on the training set and saves the models.


'''
import argparse
import sys
import os
import codecs
import glob
import math

from sklearn.ensemble import ExtraTreesRegressor
from scipy.stats import randint as sp_randint
from sklearn.grid_search import RandomizedSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import KFold
from sklearn.linear_model import RandomizedLasso
import yaml
import numpy as np


def main(train_label, train_feat, modelsdir, selfeat, iterations, folds):

  X_train = np.nan_to_num(np.genfromtxt(train_feat, delimiter=' '))
  y_train = np.nan_to_num(np.genfromtxt(train_label, delimiter=' '))

  X_trains = X_train
  scaler = StandardScaler().fit(X_train)
  X_trains = scaler.transform(X_train)


    # performs feature selection
  featsel_str = ".all-feats"
  if int(selfeat):
    print "Performing feature selection ..."
    # initializes selection estimator
    sel_est = RandomizedLasso(alpha="bic", verbose=True, max_iter=1000,
                              n_jobs=8, random_state=42,
                              n_resampling=1000)
  
    sel_est.fit(X_trains, y_train)
    X_trains = sel_est.transform(X_trains)
  
    selected_mask = sel_est.get_support()
    selected_features = sel_est.get_support(indices=True)
  
    sel_feats_path = os.sep.join([modelsdir, os.path.basename(train_feat)])
  
    # saves indices
    np.savetxt(sel_feats_path + ".idx", selected_features, fmt="%d")
    # saves mask
    np.save(sel_feats_path + ".mask", selected_mask)
    featsel_str = ".randcv"


  estimator = ExtraTreesRegressor(random_state=42, n_jobs=1)

  mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)
  #rmse_scorer = make_scorer(mean_absolute_error, greater_is_better=False)

  # performs parameter optimization using random search
  print "Performing parameter optimization ... "


  param_distributions = \
    {"n_estimators": [5, 10, 50, 100, 200, 500],
     "max_depth": [3, 2, 1, None],
     "max_features": ["auto", "sqrt", "log2", int(X_trains.shape[1]/2.0)],
     "min_samples_split": sp_randint(1, 11),
     "min_samples_leaf": sp_randint(1, 11),
     "bootstrap": [True, False]}
   # "criterion": ["gini", "entropy"]}

  search = RandomizedSearchCV(estimator, param_distributions,
            n_iter=int(iterations),
            scoring=mae_scorer, n_jobs=8, refit=True,
            cv=KFold(X_train.shape[0], int(folds), shuffle=True, random_state=42),
            verbose=1, random_state=42)
  
  # fits model using best parameters found
  search.fit(X_trains, y_train)

  # ................SHAHAB ........................ 
  
  models_dir = sorted(glob.glob(modelsdir + os.sep + "*"))
  
  estimator2 = ExtraTreesRegressor(bootstrap=search.best_params_["bootstrap"], 
       max_depth=search.best_params_["max_depth"], 
       max_features=search.best_params_["max_features"],
       min_samples_leaf=search.best_params_["min_samples_leaf"], 
       min_samples_split=search.best_params_["min_samples_split"], 
       n_estimators=search.best_params_["n_estimators"], 
       verbose=1, 
       random_state=42, 
       n_jobs=8)

  print "Train the model with the best parameters ..."
  estimator2.fit(X_trains,y_train)

  from sklearn.externals import joblib
  joblib.dump(estimator2, modelsdir+"/XRT.pkl")
  joblib.dump(scaler, modelsdir+"/scaler.pkl")
  joblib.dump(sel_est, modelsdir+"/sel_est.pkl")
  
  #  print "Kioonnn number of feat:\n", n_feature
  # ................SHAHAB ........................


if __name__=='__main__':
  sys.exit(main(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]))
  
  
  
  
