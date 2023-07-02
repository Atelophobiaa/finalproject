from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

class dna(APIView):
    def post(self, request, *args, **kwargs):
        martyr = request.data.get('martyr')
        mother_father = request.data.get('mother_father') 
        print (martyr)
        print (mother_father)
        m = len(martyr)
        n = len(mother_father)
        L = [[0 for i in range(n+1)] for j in range(m+1)]

        for i in range(m+1):
            for j in range(n+1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif martyr[i-1] == mother_father[j-1]:
                    L[i][j] = L[i-1][j-1] + 1
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])

        lcs = ""
        i = m
        j = n
        while i > 0 and j > 0:
            if martyr[i-1] == mother_father[j-1]:
                lcs += martyr[i-1]
                i -= 1
                j -= 1
            elif L[i-1][j] > L[i][j-1]:
                i -= 1
            else:
                j -= 1
            lcs = lcs[::-1]
        result = "LCS of " + martyr + " and " + mother_father + " is " + lcs

        res = {
            'data' : result
        }
        return Response(res, status=status.HTTP_200_OK)
    
class msg(APIView):
    def post(self, request, *args, **kwargs):
        the_data = request.data.get('data')
        class Nodes:  
            def __init__(self, probability, symbol, left = None, right = None):  
                # probability of the symbol  
                self.probability = probability  
        
                # the symbol  
                self.symbol = symbol  
        
                # the left node  
                self.left = left  
        
                # the right node  
                self.right = right  
        
                # the tree direction (0 or 1)  
                self.code = ''  
        
        def CalculateProbability(the_data):  
            the_symbols = dict()  
            for item in the_data:  
                if the_symbols.get(item) == None:  
                    the_symbols[item] = 1  
                else:   
                    the_symbols[item] += 1       
            return the_symbols  
        
        the_codes = dict()  
        
        def CalculateCodes(node, value = ''):  
            # a huffman code for current node  
            newValue = value + str(node.code)  
        
            if(node.left):  
                CalculateCodes(node.left, newValue)  
            if(node.right):  
                CalculateCodes(node.right, newValue)  
        
            if(not node.left and not node.right):  
                the_codes[node.symbol] = newValue  
                
            return the_codes  
        
        def OutputEncoded(the_data, coding):  
            encodingOutput = []  
            for element in the_data:  
                # print(coding[element], end = '')  
                encodingOutput.append(coding[element])  
                
            the_string = ''.join([str(item) for item in encodingOutput])      
            return the_string  
                
        def TotalGain(the_data, coding):  
            # total bit space to store the data before compression  
            beforeCompression = len(the_data) * 8  
            afterCompression = 0  
            the_symbols = coding.keys()  
            for symbol in the_symbols:  
                the_count = the_data.count(symbol)  
                # calculating how many bit is required for that symbol in total  
                afterCompression += the_count * len(coding[symbol])  
        
        def HuffmanEncoding(the_data):  
            symbolWithProbs = CalculateProbability(the_data)  
            the_symbols = symbolWithProbs.keys()  
            the_probabilities = symbolWithProbs.values()  
            
            the_nodes = []  
            
            # converting symbols and probabilities into huffman tree nodes  
            for symbol in the_symbols:  
                the_nodes.append(Nodes(symbolWithProbs.get(symbol), symbol))  
            
            while len(the_nodes) > 1:  
                # sorting all the nodes in ascending order based on their probability  
                the_nodes = sorted(the_nodes, key = lambda x: x.probability)  
                # for node in nodes:    
                #      print(node.symbol, node.prob)  
            
                # picking two smallest nodes  
                right = the_nodes[0]  
                left = the_nodes[1]  
            
                left.code = 0  
                right.code = 1  
            
                # combining the 2 smallest nodes to create new node  
                newNode = Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)  
            
                the_nodes.remove(left)  
                the_nodes.remove(right)  
                the_nodes.append(newNode)  
                    
            huffmanEncoding = CalculateCodes(the_nodes[0])   
            TotalGain(the_data, huffmanEncoding)  
            encodedOutput = OutputEncoded(the_data,huffmanEncoding)  
            return encodedOutput, the_nodes[0]  
        
        def HuffmanDecoding(encodedData, huffmanTree):  
            treeHead = huffmanTree  
            decodedOutput = []  
            for x in encodedData:  
                if x == '1':  
                    huffmanTree = huffmanTree.right     
                elif x == '0':  
                    huffmanTree = huffmanTree.left  
                try:  
                    if huffmanTree.left.symbol == None and huffmanTree.right.symbol == None:  
                        pass  
                except AttributeError:  
                    decodedOutput.append(huffmanTree.symbol)  
                    huffmanTree = treeHead  
                
            string = ''.join([str(item) for item in decodedOutput])  
            return string  
        
        encoding, the_tree = HuffmanEncoding(the_data)  
        data = {
            "real_data" : the_data,
            "Encode" : encoding,
            "Decode" : HuffmanDecoding(encoding, the_tree)
        }    
        return Response(data, status=status.HTTP_200_OK)