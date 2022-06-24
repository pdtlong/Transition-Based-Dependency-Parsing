'''
Hướng dẫn compile code:
python main.py --corpus=wsj-clean.txt --pos=piper.txt

'''
import argparse

parser = argparse.ArgumentParser(description='Transition-Based Dependency Parsing')

parser.add_argument('--corpus',type=str,help='input corpus')
parser.add_argument('--pos', type=str,
                   help='input POS file')
                   
args = parser.parse_args()

corpus_file = args.corpus
test_file = args.pos

test = open(test_file)
tsdata = test.read()
test.close()

trdata = open(corpus_file)
lines_data = trdata.readlines()
trdata.close()

stack_test =[]
buffer_test = []

def read_train(tr_file):
    corpus = open(tr_file,'r')
    corpus_data = corpus.read()
    corpus_data = corpus_data.split("\n\n")
    return corpus_data

def tokens_corpus(tr_file):
    token = []
    tagger = []
    left_arc = 0
    right_arc = 0
    with open(tr_file) as f:
        for line in f:
            if line == '\n':
                continue
            else:
                tk = line[:-1].split(' ')
                token.append(tk[1])
                tagger.append(tk[2])
                if int(tk[0]) < int(tk[3]):
                    left_arc = left_arc +1
                else:
                    right_arc = right_arc + 1
             
    return token,tagger,left_arc,right_arc
    
def sentences_corpus(lines_data):
    
    lines_data.append('\n')
    sentences = []
    words_tags_indices = []
    i = 0
    while True:
        if not i < len(lines_data):
            break
        line = lines_data[i]
        if line != '\n':
            words_tags_indices.append(line[:-1].split(' '))
        else:
            sentences.append(words_tags_indices)
            words_tags_indices = []
        i+=1 
    return sentences

def tags_relations(sentences):
    
    relations = []
    
    for _ , sentence in enumerate(sentences):       
        tags_dict = {}    
        for _ , words in enumerate(sentence):        
            if words[2] in tags_dict:               
                tags_dict[words[2]].extend([int(words[3]),int(words[0])])      
            else:               
                tags_dict[words[2]] = [int(words[3]),int(words[0])]              
        relations.append(tags_dict)     
    return relations

def common_arcs(relations,unique_tags,lr_list):
    arc_dict = {}
    arc = {}
    for tag in unique_tags:
        tag_left_right = []   
        for _, tags_relation in enumerate(relations):   
            if tag in tags_relation:
                tag_left_right.append(list(tags_relation[tag][1::2]))      
            else:
                tag_left_right.append(['none']) 
        arc_dict[tag] = tag_left_right
    
    for tag in unique_tags:
        count = 0
        temp_dict = {}
        for sentence in lr_list:
            if tag in sentence:
                relation = sentence[tag]
                for tags in arc_dict:
                    head = arc_dict[tags]
                    value = head[count]
                    for rel in range(len(relation)):
                        if relation[rel] in value or relation[rel] == value:
                            if tags in temp_dict:
                                temp_dict[tags] = temp_dict[tags] + 1
                            else:
                                temp_dict[tags] = 1
            count += 1
        arc[tag] = temp_dict  
    return arc
    

def calculate_left_arc(relations,unique_tags):
    left_list = []
    for indx, tags_relation in enumerate(relations):      
        dict_left_temp = dict()   
        for tag in tags_relation:        
            head = tags_relation[tag][::2]
            index = tags_relation[tag][1::2]       
            for l in range(len(head)):
                if head[l] > index[l]:
                    dict_left_temp.setdefault(tag, []).append(head[l])       
        left_list.append((dict_left_temp))           
    left_arc = common_arcs(relations,unique_tags,left_list)
    return left_arc        

def calculate_right_arc(relations,unique_tags):
    right_list = []
    for indx, tags_relation in enumerate(relations):       
        dict_right_temp = dict() 
        for tag in tags_relation: 
            head = tags_relation[tag][::2]
            index = tags_relation[tag][1::2]
            for l in range(0,len(head)):
                if head[l] < index[l] and head[l]!=0:
                    dict_right_temp.setdefault(tag, []).append(head[l])
        
        right_list.append((dict_right_temp))
    right_arc = common_arcs(relations,unique_tags,right_list)
    return right_arc
	
def calculate_confusion_arc_array(left_arc,right_arc):
    confusion_arc_dict = {}
    count = 0
    for tag in left_arc.keys():
        get_left_dict = left_arc[tag]
        get_right_dict = right_arc[tag]
        common_dict = {}
        for sub_tag in get_left_dict.keys():
            if sub_tag in get_right_dict:
                common_dict[sub_tag] = [get_left_dict[sub_tag],get_right_dict[sub_tag]]
        confusion_arc_dict[tag] = common_dict
    
    for tag in confusion_arc_dict.keys():
        count = count + len(confusion_arc_dict[tag].keys())
    
    return confusion_arc_dict,count
    
def print_arc(arc,unique_tags):   
    for tags in sorted(unique_tags):
        
        dict_relations_tags = arc[tags]
        print(tags + " : "),
        for tags in sorted(unique_tags):
            if tags in dict_relations_tags:
                count = dict_relations_tags[tags]
                print(""+"[  "+tags+","+"   "+str(count)+"]"),
        print("\n")
        
def print_conf_arc(arc,unique_tags):
    
    for tags in sorted(unique_tags):
        
        dict_relations_tags = arc[tags]
        print(tags + " : "),
        for tags in sorted(unique_tags):
            if tags in dict_relations_tags:
                count = dict_relations_tags[tags]
                print(""+"[  "+tags+","+"   "+str(count[0])+",  "+str(count[1])+"]"),
        print("\n")
       
def read_print_test(test_file):
    test_dict = {}
    with open(test_file,'r') as tr:
        for line in tr:
            if line == '\n':
                continue
            else:
                test_line = line[:-1].split("/")
                test_dict[test_line[0]] = test_line[1]
                print (line[:-1],)
    
    return test_dict


def oracle_parsing(tsdata,left_arc,right_arc,confusion_arc):
    print ("-----------Khởi tạo giá trị ban đầu-----------")
    print("\n")
    i=1;
    buffer_test = tsdata.split()
    print ("Bước",i," :Stack:",stack_test)    
    print ("----------Buffer:",buffer_test)
    print("Transition: SHIFT(",buffer_test[0],")")
    print("\n")
    stack_test.append(buffer_test.pop(0))

    stack_test.append(buffer_test.pop(0))
    print ("-----------Quá trình chính-----------")
    print("\n")
    while (len(stack_test) > 0):
        if len(stack_test) == 1 and len(buffer_test)!=0 :
            i+=1
            print ("Bước",i," :Stack:",stack_test)    
            print ("----------Buffer:",buffer_test)
            print("Transition: SHIFT(",buffer_test[0],")")
            print("\n")
            stack_test.append(buffer_test.pop(0))

            
        if (len(stack_test) == 1 and len(buffer_test) == 0):
            i+=1
            print ("Bước",i," :Stack:",stack_test)    
            print ("----------Buffer:",buffer_test)
            print( "ROOT -->", stack_test[0])
            print("\n")
            stack_test.pop(0)
            
        if len(stack_test) > 1:
            
            top_jth_tag = stack_test[-1].split("/")[1]
            second_ith_tag = stack_test[-2].split("/")[1]
        
            if second_ith_tag[0] == "V" and (top_jth_tag[0] == "." or top_jth_tag[0] == "R"):
                i+=1
                print ("Bước",i," :Stack:",stack_test)    
                print ("----------Buffer:",buffer_test)
                print ("Transition: Right Arc: ",stack_test[-2]," -->",stack_test[-1])
                print("\n")
                stack_test.pop(-1)
                
            elif second_ith_tag[0] ==  "I" and top_jth_tag[0] == ".":
                i+=1
                print ("Bước",i," :Stack:",stack_test)    
                print ("----------Buffer:",buffer_test)
                print ("Transition: SWAP")
                print("\n")
                buffer_test.append(stack_test.pop(-2))
                
            elif len(buffer_test) != 0 and (second_ith_tag[0] == "V" or second_ith_tag[0] == "I") and (top_jth_tag[0] == "D" or top_jth_tag[0] == "I" or top_jth_tag[0] == "J" or top_jth_tag[0] == "P" or top_jth_tag[0] == "R"):
                i+=1
                print ("Bước",i," :Stack:",stack_test)    
                print ("----------Buffer:",buffer_test)
                print("Transition: SHIFT(",buffer_test[0],")")
                print("\n")

                if len(buffer_test) > 0:
                   stack_test.append(buffer_test.pop(0))

            #confusion arc
            elif second_ith_tag in confusion_arc and top_jth_tag in confusion_arc[second_ith_tag]:
                
                if confusion_arc[second_ith_tag][top_jth_tag].index(max(confusion_arc[second_ith_tag][top_jth_tag])) == 1:
                    i+=1
                    print ("Bước",i," :Stack:",stack_test)    
                    print ("----------Buffer:",buffer_test)
                    print ("Transition: Right Arc: ",stack_test[-2]," -->",stack_test[-1])
                    print("\n")                 
                    stack_test.pop(-1) 

                elif confusion_arc[second_ith_tag][top_jth_tag].index(max(confusion_arc[second_ith_tag][top_jth_tag])) == 0:
                    i+=1
                    print ("Bước",i," :Stack:",stack_test)    
                    print ("----------Buffer:",buffer_test)
                    print ("Transition: Left Arc:",stack_test[-2]," <--",stack_test[-1])
                    print("\n")  
                    stack_test.pop(-2)

            #left arc
            elif second_ith_tag in left_arc and top_jth_tag in left_arc[second_ith_tag]:
                    i+=1
                    print ("Bước",i," :Stack:",stack_test)    
                    print ("----------Buffer:",buffer_test)   
                    print ("Buffer:",buffer_test)
                    print ("Transition: Left Arc:",stack_test[-2]," <--",stack_test[-1])
                    print("\n")  
                    stack_test.pop(-2)
            #right arc
            elif top_jth_tag in right_arc and second_ith_tag in right_arc[top_jth_tag]:
                    i+=1
                    print ("Bước",i," :Stack:",stack_test)    
                    print ("----------Buffer:",buffer_test)    
                    print ("Buffer:",buffer_test)
                    print ("Transition: Right Arc: ",stack_test[-2]," -->",stack_test[-1])
                    print("\n")                 
                    stack_test.pop(-1) 
                    
            else:
                i+=1
                print ("Bước",i," :Stack:",stack_test)    
                print ("----------Buffer:",buffer_test)    
                print ("Buffer:",buffer_test)
                print ("Transition: Right Arc: ",stack_test[-2]," -->",stack_test[-1])
                print("\n")
                stack_test.pop(-1)
                if len(buffer_test) > 0 :
                    stack_test.append(buffer_test.pop(-1))



corpus_data = read_train(corpus_file)

tokens,tags,left_arc,right_arc = tokens_corpus(corpus_file)

sentences = sentences_corpus(lines_data)

relations = tags_relations(sentences) 

left_arc_counts = calculate_left_arc(relations,list(set(tags)))

right_arc_counts = calculate_right_arc(relations,list(set(tags)))

confusion_arc,count = calculate_confusion_arc_array(left_arc_counts,right_arc_counts)

print ("Dependency Parser\n")

print ("\nCorpus Statistics:\n")
print( "\t# sentences  :", len(corpus_data))
print ("\t# tokens     :", len(tokens))
print ("\t# POS tags   :", len(list(set(tags))))
print ("\t# Left-Arcs  :", left_arc)
print ("\t# Right-Arcs :", right_arc - len(corpus_data))
print ("\t# Root-Arcs  :", len(corpus_data))

print ("\nLeft Arc Array Nonzero Counts:\n")
print_arc(left_arc_counts,list(set(tags)))

print ("\nRight Arc Array Nonzero Counts:\n")
print_arc(right_arc_counts,list(set(tags)))

print ("\nArc Confusion Array:\n")
print_conf_arc(confusion_arc,list(set(tags)))

print ("\n")
print (u"\tSố lượng confusing arcs = ",count)

print("\nInput Sentence:")
test_dict = read_print_test(test_file)

print("\n\n\nQuá trình thực hiện Các Transition-Based :\n\n")
oracle_parsing(tsdata,left_arc_counts,right_arc_counts,confusion_arc)
