import pandas as pd


my_dict = {}
my_rank_dict ={}
my_rank_list = []


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
    val_node_source['sum'] += row[2]
  else:
    my_dict[row[0]] = {'out': [(row[1], row[2])], 'in': [],'sum': row[2]}

  #take care of in edges
  if val_node_target != None:
    val_node_target['in'].append((row[0], row[2]))
  else:
    my_dict[row[1]] = {'out': [], 'in': [(row[0], row[2])], 'sum': 0}





#function that load the graph
def load_graph(path):
  """

  loads the data to the data structure
  :param path: path of the data as csv file
  :return nothing
  """
  df = pd.read_csv(path)
  num_of_rows = df.shape[0]
  for i in range(num_of_rows):
    row = df.iloc[i]
    update_dict(row)

  return

def calculate_page_rank(b=0.85, d=0.001, max_iter=20):

  rank0 = 1/len(my_dict.keys())
  iters = 0
  # init the ranking dictionary to 1/n for each node
  delta = 2^30
  for key in my_dict.keys():
    #(x,y)->(former iteration,curr iteration)
    my_rank_dict[key] = [rank0]

  # as long as we have a big delta between erorrs and we hav iterations to run
  while (iters < max_iter and delta > d ):

    new_sum_err = 0
    sum_rank = 0
    for key in my_dict.keys():

      new_rank = 0
      if len(my_dict[key]["in"]) != 0:
        for income_edge in my_dict[key]["in"]:
          rank_mone = (b * income_edge[1] * my_rank_dict[income_edge[0]][0])
          rank_mehane = my_dict[income_edge[0]].get("sum")
          new_rank += rank_mone/rank_mehane
      my_rank_dict[key].append(new_rank)
      sum_rank+=new_rank
      len1= len(my_rank_dict[key])
      #make sure we always have list of 2
      my_rank_dict[key] = my_rank_dict[key][len1-2:len1]
      #new_sum_err += abs(my_rank_dict[key][1] - my_rank_dict[key][0])

    #fix of the lake
    fix_to_append = (1-sum_rank)/len(my_dict.keys())
    for key in my_rank_dict.keys():
      my_rank_dict[key][1]+=fix_to_append
      new_sum_err += abs(my_rank_dict[key][1] - my_rank_dict[key][0])
    delta = new_sum_err
    iters +=1


  for node in my_rank_dict.keys():
    my_rank_list.append((node, my_rank_dict[node][1]))

  my_rank_list.sort(key= lambda x: x[1],reverse= True)

def get_PageRank(node_name):
  if node_name in my_rank_dict.keys():
    return my_rank_dict[node_name][1]
  else:
    return -1

def get_top_PageRank(n):
  if len(my_dict.keys()) > 0:
    return my_rank_list[:n]

  else:
    return []

def get_all_PageRank():
  if len(my_dict.keys()) > 0:

    return my_rank_list
  else:
    return []


# ====  TESTS ======

load_graph('soc-sign-bitcoinotc.csv')
calculate_page_rank()
#print(type(my_rank_dict[5724][1]))
top_ten = get_top_PageRank(10)
index=1
for rank in top_ten:
  print(str(index)+". "+str(rank))
  index+=1
# print("===========")
#print(get_all_PageRank())
# print("===========")
# print(get_PageRank(5724))


