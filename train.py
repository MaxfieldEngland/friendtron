# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:15:49 2021

"""

import gpt_2_simple as gpt2
from datetime import datetime
import os
import requests
import tensorflow as tf

#355M is a larger model. 124M is less sophisticated, but is about a third of the filesize and takes much less time and effort to use.
model_name = "124M"
#model_name = "355M"
#Downloads the model if it's not already present. 
if not os.path.isdir(os.path.join("models", model_name)):
 	print(f"Downloading {model_name} model...")
 	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

#Enter your file name here.
#file_name = "MY_TRAINING_CORPUS_FILE_NAME" 
tf.reset_default_graph()
sess = gpt2.start_tf_sess()
 gpt2.generate(sess)
 gpt2.finetune(
             sess,
             dataset=file_name,
             model_name='124M', # Model you have already downloaded
             steps=-1, # -1 will do unlimited. Enter number of iterations otherwise
             restore_from='fresh', # 'fresh' or 'latest' : fresh will restart training from scratch, while latest will use the highest available iteration
             run_name='friendtron', # The name to pull or create a checkpoint under; you will use this in the future!
             print_every=50, # Print iterations every X numebr
             sample_every=150, # Generate a text sample ever X number of iter.
             save_every=500, # Save a snapshot every X number of iter.
             learning_rate=0.0001, # Lower to 0.00001 if you are not getting massive changes in results
             batch_size=1 # Keep at 1 or 2, will use up more memory if you raise this
)