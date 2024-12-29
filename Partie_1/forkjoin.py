from arbresEntrant import ArbreEntrant

class Node:
    def __init__(self,weight,label):
        self.weight = weight
        self.parent = {"node" : None,"cost" : 0}
        self.label = label
        self.linkCost = None
        self.enfant = []

class terminaisonNode:
     def __init__(self,weight,label):
          self.enfant = []
          self.parent = []
          self.weight = weight
          self.label = label

class forkJoin:
    def __init__(self,weightStart,weightEnd):
       self.start = terminaisonNode(weightStart,"s")
       self.end = terminaisonNode(weightEnd,"t")
       self.chain = []
    def start_chain(self,node,linkCostTo,linkCostFrom):
         self.start.enfant.append(node)
         minNode = None
         minValue = None
         if(linkCostTo < linkCostFrom):
              minNode = self.start
              minValue = linkCostTo
         else:
              minNode = node
         self.chain.append({"node":node,"linkCost":linkCostTo,"linkCostMin":{"node":minNode,"value":min(linkCostTo,linkCostFrom)}})
         node.parent["node"] = self.start
         node.parent["linkCost"] = linkCostTo
         node.enfant.append(self.end)
         node.linkCost = linkCostFrom
         self.end.parent.append({"node" : node,"cost" : linkCostFrom})
    def add_node(self,chainIndex,node,linkCostFrom):
       
            current = self.chain[chainIndex]["node"]
            while current.enfant[0] != self.end:
                    current = current.enfant[0]
            current.enfant.remove(self.end)
            self.end.parent.remove({"node" : current,"cost" : current.linkCost})
            current.enfant.append(node)
            self.end.parent.append({"node" : node,"cost" : linkCostFrom})
            node.parent["node"] = current
            node.parent["linkCost"] = current.linkCost
            node.enfant.append(self.end)
            node.linkCost = linkCostFrom
            if linkCostFrom < self.chain[chainIndex]["linkCostMin"]:
                 self.chain[chainIndex]["linkCostMin"] = {"node":node,"value":linkCostFrom}
            
    def nbChain(self):
        return len(self.chain)
    def minChain(self):
        minLink = []
        for chain in self.chain:
             minLink.append(chain["linkCostMin"])
        return minLink
    def print_chain(self,chainIndex):
         nodeLabel = []
         nodeLabel.append({"label":"s","linkCost":self.chain[chainIndex]["linkCost"]})
         current = self.chain[chainIndex]["node"]
         while current.enfant != []:
            nodeLabel.append({"label":current.label,"linkCost":current.linkCost})
            current = current.enfant[0]
         nodeLabel.append({"label":current.label,"linkCost":0})
         return nodeLabel
    def ordonnancementForkJoin(self):
         for i in range(len(self.start.enfant)):
              cut = False
              current = self.start
              if self.chain[i]["linkCostMin"]["node"]==current:
                   cut = True
              else:
                self.chain[i]["linkcost"]-=self.chain[i]["linkCostMin"]["minValue"]
                self.chain[i]["node"].parent["linkcost"]-=self.chain[i]["linkCostMin"]["minValue"]
              current = self.chain[i]["node"]
              last = None
              while current.enfant != []:
                   last = current
                   current.weight+= self.chain[i]["linkCostMin"]["minValue"]
                   if cut:
                            current.linkCost-=self.chain[i]["linkCostMin"]["minValue"]
                            current.enfant[0].parent["linkcost"]-=self.chain[i]["linkCostMin"]["minValue"]
                            tmp = current.enfant.pop()
                            tpm.parent.push(current)
                            current = tpm
                   else:
                        if current == self.chain[i]["linkCostMin"]["node"]:
                             cut = True
                        else:
                          current.linkCost-=self.chain[i]["linkCostMin"]["minValue"]
                          current.enfant[0].parent["linkcost"]-=self.chain[i]["linkCostMin"]["minValue"]  
                          current = current.enfant[0] 

fk = forkJoin(20,12)
a = Node(10,"a")
c = Node(0,"c")
b = Node(20,"b")
fk.start_chain(a,5,10)
fk.add_node(0,c,1)
print(fk.nbChain())
fk.start_chain(b,20,10)
print(fk.nbChain())
print(fk.minChain())
print(fk.print_chain(0))