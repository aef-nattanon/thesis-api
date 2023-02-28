from re import sub
import multiprocessing
import shutil


def snake_case(s):
  s = str(s)
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()
############################################################

# model type
# not to bitwise_not
# 1 light numbers (white) on a dark (black, red) background
MODEL_1_CLASS = 1
MODEL_1_NAME = "model 1"
# to bitwise_not
# 2 dark numbers (black, red) on a light (white) background.
MODEL_2_CLASS = 2
MODEL_2_NAME = "model 2"
############################################################


def remove_file(ts):
  print(f"Removing {ts}", './run_meter/'+ts)
  shutil.rmtree(f"./run_meter/{ts}")
  shutil.rmtree(f"./run_number/{ts}")