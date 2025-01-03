from arbresEntrant import ArbreEntrant,ordonnancementArbre

class Node:
     def __init__(self, weight, label):
          self.weight = weight
          self.parent = {"node" : None, "cost" : 0}
          self.label = label
          self.linkCost = None
          self.enfant = []

     def getType(self):
          return "Node"

class terminaisonNode:
     def __init__(self, weight, label):
          self.enfant = []
          self.parent = []
          self.weight = weight
          self.label = label

     def getType(self):
          return "terminaisonNode"

class forkJoin:
     def __init__(self, weightStart, weightEnd):
          self.start = terminaisonNode(weightStart,"s")
          self.end = terminaisonNode(weightEnd,"t")
          self.chain = []

     def start_chain(self, node, linkCostTo, linkCostFrom):    
          self.start.enfant.append(node)
          minNode = None
          minValue = None

          if (linkCostTo < linkCostFrom):
               minNode = self.start
               minValue = linkCostTo
          else:
               minNode = node

          self.chain.append({"node":node,"linkCost":linkCostTo,"linkCostMin":{"node":minNode,"value":min(linkCostTo,linkCostFrom)}})

          node.parent["node"] = self.start
          node.parent["linkCost"] = linkCostTo
          node.enfant.append(self.end)
          node.linkCost = linkCostFrom

          self.end.parent.append({"node" : node, "cost" : linkCostFrom})

     def add_node(self, chainIndex, node, linkCostFrom):
          current = self.chain[chainIndex]["node"]

          while current.enfant and current.enfant[0] != self.end:
               current = current.enfant[0]
          
          current.enfant.remove(self.end)

          self.end.parent.remove({"node" : current,"cost" : current.linkCost})
          current.enfant.append(node)

          self.end.parent.append({"node" : node,"cost" : linkCostFrom})
          node.parent["node"] = current
          node.parent["linkCost"] = current.linkCost
          node.enfant.append(self.end)
          node.linkCost = linkCostFrom

          if linkCostFrom < self.chain[chainIndex]["linkCostMin"]["value"]:
               self.chain[chainIndex]["linkCostMin"] = {"node":node, "value":linkCostFrom}
            
     def nbChain(self):
          return len(self.chain)

     def minChain(self):
          minLink = []

          for chain in self.chain:
               minLink.append(chain["linkCostMin"])
          return minLink

     def print_chain(self,chainIndex):
          nodeLabel = []
          nodeLabel.append({"label" : "s", "linkCost" : self.chain[chainIndex]["linkCost"]})
          current = self.chain[chainIndex]["node"]

          while current.enfant != []:
               nodeLabel.append({"label":current.label,"linkCost":current.linkCost})
               current = current.enfant[0]

          nodeLabel.append({"label":current.label,"linkCost":0})
 
          return nodeLabel
     
     def print_forkJoin(self):
          output = "Affiche le forkJoin : \n"

          for enfant in self.start.enfant:
               current = enfant

               while current != self.end:
                    output += current.label + "(" + str(current.weight) + ")" + "-{" + str(current.linkCost) + "}->"
                    current = current.enfant[0]

               output += "\n"
               
          print(output)
     
     '''
          Ajoute une chaîne complète au forkJoin.
     '''
     def add_chain(self, chain, linkCostTo, linkCostFrom):
          chainIndex = self.nbChain()

          # On crée la nouvelle chaîne
          self.start_chain(chain[0], linkCostTo, linkCostFrom)

          # On itère chaque maillon et on les ajoute à la nouvelle chaîne
          for i in range(1, len(chain)):
               linkCost = chain[i].linkCost
               self.add_node(chainIndex, chain[i], linkCost)

     def ordonnancementForkJoin(self):
          # Itère sur chaque chaîne de l'arbre
          for i in range(len(self.start.enfant)):
               cut = False
               current = self.start

               if self.chain[i]["linkCostMin"]["node"] == current:
                    cut = True
               else:
                    self.chain[i]["linkCost"] -= self.chain[i]["linkCostMin"]["value"]
                    self.chain[i]["node"].parent["cost"] = self.chain[i]["linkCost"]
                    
               current = self.chain[i]["node"]
               last = None

               # Parcours des nodes de la chaîne i
               while current != self.end:
                    last = {"node" : current,"cost" : current.linkCost}
                    current.weight += self.chain[i]["linkCostMin"]["value"]

                    if cut:
                         current.linkCost -= self.chain[i]["linkCostMin"]["value"]
                         tmp = current.enfant.pop(0)
                         
                         if tmp != self.end :
                              tmp.parent["cost"]-= self.chain[i]["linkCostMin"]["value"]
                              tmp.linkcost = tmp.parent["linkCost"]

                         current.parent = ({"node" : tmp, "cost" : current.linkCost})

                         tmp.enfant.append(current)
                         current = tmp
                    else:
                         if current == self.chain[i]["linkCostMin"]["node"]:
                              cut = True
                         else:
                              current.linkCost -= self.chain[i]["linkCostMin"]["value"]
                              current.enfant[0].parent["cost"] = current.linkCost

                         current = current.enfant[0] 
               
               self.end.parent.remove(last)
               self.chain[i]["linkCostMin"]["node"].enfant.pop()

          arbreStart = ArbreEntrant(self.start)
          arbreEnd = ArbreEntrant(self.end)
          ordonnancementStart = ordonnancementArbre(arbreStart)
          ordonnancementStart.reverse()
          ordonnancementEnd = ordonnancementArbre(arbreEnd)
          ordonnancementStart.extend(ordonnancementEnd)

          return ordonnancementStart 
