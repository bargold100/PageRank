import pandas as pd


my_dict = {}

def update_dict(row):
  """
  update the data structure of the graph
  :param row: the row of the dataframe
  :return: null
  """
  val_node_source = my_dict.get(row[0])
  val_node_target = my_dict.get(row[1])
  #take care of out edges
  if val_node_source != None:
    val_node_source['out'].append((row[1], row[2]))
  else:
    my_dict[row[0]] = {'out': [(row[1], row[2])], 'in': []}

  #take care of in edges
  if val_node_target != None:
    val_node_target['in'].append((row[0], row[2]))
  else:
    my_dict[row[1]] = {'out': [], 'in': [(row[0], row[2])]}


#function that load the graph
def load_graph(path):
  df = pd.read_csv(path)
  num_of_rows = df.shape[0]
  for i in range(num_of_rows):
    row = df.iloc[i]
    update_dict(row)
  return df


df = load_graph('soc-sign-bitcoinotc.csv')
print(df.iloc[0][1])
print(df.shape)