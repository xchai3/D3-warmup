import http.client
import json
import time
import timeit
import sys
import collections
import urllib.request

from pygexf import gexf
from pygexf.gexf import *


#
# implement your data retrieval code here
conn=http.client.HTTPConnection('www.rebrickable.com')
instr=sys.argv[1]
#conn.request('GET','https://rebrickable.com/api/v3/lego/colors/?key=29f5544763bccf831fdac67923a9d440')
# response=conn.getresponse()
# print(response.status, response.reason) # check the status
# data1=response.read() # read the entire content
# print(data1)
print('\n')
url='https://rebrickable.com/api/v3/lego/sets/'
key = '?key='+instr
order='&page_size=300&ordering=-num_parts%2Cid&min_parts=1150'   # sorting with sets number decreasing order?
URL=url+key+order
# print(URL)
conn.request('GET',URL)
r2=conn.getresponse();
d2=r2.read()
t=d2.decode()
map=json.loads(t)

#print(d2)
def min_parts():
    """
    Returns an integer value
    """
    # you must replace this with your own value

    return 1150
#print(map)
def lego_sets():
    """
    return a list of
    this may be a list of any type of values
    but each value should represent one set

    e.g.,
    biggest_lego_sets = lego_sets()
    print(len(biggest_lego_sets))
    > 280
    e.g., len(my_sets)
    """
    # you must replace this line and return your own list
    #return []
    list=[]
    for i in range(map['count']):
        list1=[]
        list1.append(map['results'][i]['set_num'])
        list1.append(map['results'][i]['name'])
        list.append(list1)
    return(list) ## output the "num_parts" for every set
#print(lego_sets())
set_num_name=lego_sets()

#1.1 B
sets_number=map['count']  # the number of total sets
Total_inve=[]      # a list use to store inventory for top 20 sets
number_parts_set=[]
for i in range(sets_number):  # the total number of sets  (sets_number, change later)
    set_num = map['results'][i]['set_num']   # get set_num
    # the set number
    print(set_num)
    url = 'https://rebrickable.com/api/v3/lego/sets/' + set_num + '/parts/'
    order='&page_size=1000'
    URL2 = url + key+order
    #print(URL2)
    conn.request('GET', URL2)
    r3 = conn.getresponse()
    print(r3.status, r3.reason)
    d3 = r3.read()
    t2 = d3.decode()
    sets = json.loads(t2)
    # all the information for a inventory of a set
    
    Total_num=sets['count']     # get the total number of inventory of this sets
    #print(Total_num)
    # Total_num=1
    result=sets['results']    # all the information about a part
    inven_onesets=[]
# find Top 20 most frequently used parts in every sets
    if(Total_num>1000):
        Total_num=1000
#re-order the parts
    for i in range(Total_num):
        for j in range(i + 1, Total_num):
            quantity1 = int(result[i]['quantity'])
            quantity2 = int(result[j]['quantity'])
            if (quantity1 < quantity2):
                result[i], result[j] = result[j], result[i]



    if(Total_num>20):
        Total_num=20
    number_parts_set.append(Total_num)
    for i in range(Total_num):   #758
        print("list add:",i)
        #one of the sets
       # print("start store")
        part_color=result[i]['color']
        part_quantity= result[i]['quantity']
        part_name=result[i]['part']['name']
        part_number=result[i]['part'] ['part_num']
        ID=part_number+'_'+part_color['rgb']
        # print(part_color)
        # print(part_quantity)
        # print(part_name)
        # print(part_number)
        # print(ID)
        inven_onepart=[]
        inven_onepart.append(ID)
        inven_onepart.append(part_color)
        inven_onepart.append(part_quantity)
        inven_onepart.append(part_name)
        inven_onepart.append(part_number)
        inven_onesets.append(inven_onepart)
        #print(inven_onesets)
        # print(inven_onesets)
      #  print(inven_onepart)
    Total_inve.append(inven_onesets)
print(Total_inve)

def gexf_graph():
    """
    return the completed Gexf graph object
    """
    # you must replace these lines and supply your own graph
    gexf = Gexf("Xipeng Chai", "Assign1")
    graph = gexf.addGraph("directed", "static", "Assign 1")
    attr=graph.addNodeAttribute('Type',type='string')

# loop to get set_number and set_name to generate set lop:
    EdgeID=0
    Edge_ID=str(EdgeID)
    for i in range(sets_number):
        # num is ID, name is
        set_node_num=set_num_name[i][0]
        set_node_name=set_num_name[i][1]
        set_node=graph.addNode(set_node_num,set_node_name,r="0", g="0", b="0")
        set_node.addAttribute(attr,"set")
#loop to get
        for j in range(number_parts_set[i]):
            part_node_ID=Total_inve[i][j][0] # ID
            part_qual = Total_inve[i][j][2]
            part_node_name=Total_inve[i][j][3] # label
            tem_color=Total_inve[0][0][1]['rgb']
            r1=str(int(tem_color[0:2],16))
            g1=str(int(tem_color[2:4]))
            b1=str(int(tem_color[4:6],16))
            part_node=graph.addNode(part_node_ID,part_node_name,r=r1, g=g1, b=b1)
            part_node.addAttribute(attr,"part")
            graph.addEdge(Edge_ID,set_node_num,part_node_ID,weight=part_qual)
            EdgeID+=1
            Edge_ID=str(EdgeID)
    # graph.
    # graph.addNode("0", "hello")
    # graph.addNode("1", "World")
    # graph.addEdge("0", "0", "1")
    output_file = open("ricks_graph.gexf", "wb")
    gexf.write(output_file)
    #return gexf.graphs[0]
gexf_graph()
def avg_node_degree():
    """
        hardcode and return the average node degree
        (run the function called “Average Degree”) within Gephi
        """
    # you must replace this value with the avg node degree
    return 2.694


def graph_diameter():
    """
        hardcode and return the diameter of the graph
        (run the function called “Network Diameter”) within Gephi
        """
    # you must replace this value with the graph diameter
    return 8


def avg_path_length():
    """
        hardcode and return the average path length
        (run the function called “Avg. Path Length”) within Gephi
        :return:
        """
    # you must replace this value with the avg path length
    return 4.432