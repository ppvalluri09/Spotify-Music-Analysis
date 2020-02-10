import pickle
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import pickle

brc = pickle.load(open('models/model.sav', 'rb'))

# Need to extract data for prediction
