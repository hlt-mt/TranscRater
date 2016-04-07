'''
Created on Sep 17, 2013

@author: desouza
'''
import argparse
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


desc = """
Performs randomized parameter estimation on training data using k-fold
cross-validation (shuffled). Outputs the best SVR RBF kernel parameters.
"""


def buildDir(dir):
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)


def run(args):
    X_train = np.nan_to_num(
        np.genfromtxt(args.training_data, delimiter=args.delimiter))
    y_train = np.clip(np.genfromtxt(args.training_labels), 0, 1)

    X_trains = X_train
    if args.scale:
        print "Scaling features (mean removal divided by std)..."
        scaler = StandardScaler().fit(X_train)
        X_trains = scaler.transform(X_train)

    # create output folders
    outF = args.output_folder + "/" + os.path.basename(
        args.training_data) + "--FS_" + str(
        args.select_features) + "--i_" + str(args.iterations)
    buildDir(outF)
    maskF = outF + "/masks/"
    buildDir(maskF)
    #evaluation  features  first_experiments  labels  logs  masks  parameters
    #  predictions  src  suca
    paramF = outF + "/parameters/"
    buildDir(paramF)
    #featF = outF+"/features/"
    #buildDir(featF)    

    #evalF = buildDir(outF+"/evaluation")



    #os.path.basename(
    #        args.training_data)]) + featsel_str + "--" + os.path.basename(
    # test_label



    # initializes numpy random seed
    np.random.seed(args.seed)

    # performs feature selection
    featsel_str = ".all-feats"
    if args.select_features:
        print "Performing feature selection ..."
        # initializes selection estimator
        sel_est = RandomizedLasso(alpha="bic", verbose=True, max_iter=1000,
                                  n_jobs=8, random_state=args.seed,
                                  n_resampling=1000)

        sel_est.fit(X_trains, y_train)
        X_trains = sel_est.transform(X_trains)

        selected_mask = sel_est.get_support()
        selected_features = sel_est.get_support(indices=True)

        sel_feats_path = os.sep.join(
            #    [".", "masks", os.path.basename(args.training_data)])
            [maskF, os.path.basename(args.training_data)])

        # saves indices
        np.savetxt(sel_feats_path + ".idx", selected_features, fmt="%d")
        # saves mask
        np.save(sel_feats_path + ".mask", selected_mask)
        featsel_str = ".randcv"

    estimator = ExtraTreesRegressor(random_state=args.seed, n_jobs=1)

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
                                n_iter=args.iterations,
                                scoring=mae_scorer, n_jobs=8, refit=True,
                                cv=KFold(X_train.shape[0], args.folds, shuffle=True,
                                         random_state=args.seed), verbose=1,
                                random_state=args.seed)

    # fits model using best parameters found
    search.fit(X_trains, y_train)

    # ................SHAHAB ........................ 
    
    models_dir = sorted(glob.glob(args.models_dir + os.sep + "*"))
    
    estimator2 = ExtraTreesRegressor(bootstrap=search.best_params_["bootstrap"], 
                                     max_depth=search.best_params_["max_depth"], 
                                     max_features=search.best_params_["max_features"],
                                     min_samples_leaf=search.best_params_["min_samples_leaf"], 
                                     min_samples_split=search.best_params_["min_samples_split"], 
                                     n_estimators=search.best_params_["n_estimators"], 
                                     verbose=1, 
                                     random_state=42, 
                                     n_jobs=8)
   
    estimator2.fit(X_trains,y_train)
    from sklearn.externals import joblib
    print "koooonnn %s" % args.models_dir
    joblib.dump(estimator2, args.models_dir+"/XRT.pkl")
    joblib.dump(scaler, args.models_dir+"/scaler.pkl")
    joblib.dump(sel_est, args.models_dir+"/sel_est.pkl")
    
#    print "Kioonnn number of feat:\n", n_feature
    # ................SHAHAB ........................

    print "Best parameters: ", search.best_params_

    # saves parameters on yaml file
    #param_path = os.sep.join([".", "parameters", os.path.basename(
    param_path = os.sep.join([paramF, os.path.basename(
        args.training_data)]) + featsel_str + ".params.yaml"
    param_file = codecs.open(param_path, "w", "utf-8")
    yaml.dump(search.best_params_, stream=param_file)
    testF = os.sep.join([outF, "/test/"])
    buildDir(testF)

    m = y_train.mean()

    # evaluates model on the different test sets
    test_features = sorted(glob.glob(args.test_data + os.sep + "*"))
    test_labels = sorted(glob.glob(args.test_labels + os.sep + "*"))
    for test_feature, test_label in zip(test_features, test_labels):
        print "Evaluating on %s" % test_label
    	X_test = np.nan_to_num(
        	np.genfromtxt(test_feature, delimiter=args.delimiter))
    	y_test = np.clip(np.genfromtxt(test_label), 0, 1)

    	X_tests = X_test
    	if args.scale:
        	X_tests = scaler.transform(X_test)

    	if args.select_features:
        	X_tests = sel_est.transform(X_tests)

    	# gets predictions on test set
    	#y_pred = search.predict(X_tests)
    	y_pred = np.clip(search.predict(X_tests), 0, 1)

    	# evaluates on test set
    	mae = mean_absolute_error(y_test, y_pred)
    	rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    	print "Test MAE = %2.8f" % mae
    	print "Test RMSE = %2.8f" % rmse
    	print "Prediction range: [%2.4f, %2.4f]" % (y_pred.min(), y_pred.max())
    	# saves evaluation
    	testFX = testF + "/" + os.path.basename(test_label)
    	buildDir(testFX)
    	buildDir(testFX + "/evaluation/")

    	eval_path = os.sep.join([testFX, "evaluation", os.path.basename(
        	args.training_data)]) + featsel_str + "--" + os.path.basename(
        	test_label)
    	mae_eval = codecs.open(eval_path + ".mae", 'w', "utf-8")
    	mae_eval.write(str(mae) + "\n")
    	rmse_eval = codecs.open(eval_path + ".rmse", 'w', "utf-8")
    	rmse_eval.write(str(rmse) + "\n")

    	mu = m * np.ones(y_test.shape[0])  # baseline on test set
    	maeB = mean_absolute_error(y_test, mu)
    	rmseB = np.sqrt(mean_squared_error(y_test, mu))
    	print "Test MAE Baseline= %2.8f" % maeB
    	print "Test RMSE Baseline= %2.8f" % rmseB
    	mae_eval = codecs.open(eval_path + ".mae.Base", 'w', "utf-8")
    	mae_eval.write(str(maeB) + "\n")
    	rmse_eval = codecs.open(eval_path + ".rmse.Base", 'w', "utf-8")
    	rmse_eval.write(str(rmseB) + "\n")



	# saves predictions
	buildDir(testFX + "/predictions/")
	preds_path = os.sep.join([testFX, "predictions", os.path.basename(
        	args.training_data)]) + featsel_str + "--" + os.path.basename(
        	test_label) + ".preds"
	np.savetxt(preds_path, y_pred, fmt="%2.15f")


def main():
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("training_data", help="path to the training data file.")
    parser.add_argument("training_labels",
                        help="path to the training labels file.")
    parser.add_argument("models_dir", default="./models",
                        help="models dir where RR models will be saved " )

    parser.add_argument("test_data", help="path to the test data directory.")
    parser.add_argument("test_labels",
                        help="path to the test labels directory.")

    parser.add_argument("--select_features", action="store_true", default=False,
                        help="performs feature selection. Currently only "
                             "Randomized Lasso.")

    parser.add_argument("--scale", action="store_true", default=True,
                        help="scales the data (centers to the mean of each "
                             "feature and divides by the standard deviation).")
    parser.add_argument("-d", "--delimiter", default="\t",
                        help="default character to separate values in the "
                             "data.")
    parser.add_argument("-i", "--iterations", type=int, default=100,
                        help="number of iterations to perform when using the "
                             "randomized parameter estimation.")
    parser.add_argument("--seed", type=int, default=42,
                        help="sets the seed for the random number generator.")
    parser.add_argument("--folds", type=int, default=10,
                        help="sets k for k-fold cross-validation.")                        
    parser.add_argument("--output_folder", default="./",
                        help="Output folder where all the results will be "
                             "saved.")
    args = parser.parse_args()

    run(args)


if __name__ == '__main__':
    main()
