
seq_start = 1
amino_acid_count = (0+seq_start)-1


with open('seq.txt') as sequence_file:

    sequence_list = [ sequence.strip().upper() 
                     for sequence in sequence_file.readlines())]
    
    ##you got the amino acid list like ["MSYQVLARKW", "MSYQVLAR", "RHHMSYQVLARKW"] 
    # My guess is that you require how many letters are here
    ##>>> Counter("".join(["mingle", "jingle", "twinkle"]))
    ##   Output:  Counter({'i': 3, 'n': 3, 'l': 3, 'e': 3, 'g': 2, 'm': 1, 'j': 1, 't': 1, 'w': 1, 'k': 1})
    
    from collections import Counter
    c = Counter("".join(sequence_list))     
        
        for word in stripped_amino_acid:
            amino_acid_count += 1
            sequence_list.append(str(amino_acid_count)+word)
y = 0


sparta_file_list1 = []
sparta_file_list2 = []
proline_counter = 0
with open('sparta_pred.tab') as sparta_predictions:
    for line in sparta_predictions:
        modifier = line.strip().upper()
        if re.findall('^\d+', modifier):
            A = modifier.split()
            del A[5:8]
            del A[3]
            A[0:3] = ["".join(A[0:3])]
            joined = " ".join(A)
            proline_searcher = re.search('\BP', joined)
            if proline_searcher != None:
                proline_counter += 1
                if proline_counter < 2:
                    proline_count = re.search('^\d+', joined)
                    sparta_file_list1.append(
                        f'{proline_count.group(0)}PN'+' 1000'+' 1000')
            sparta_file_list1.append(joined)
            if proline_searcher != None:
                y += 1
                if y == 4:
                    proline_count = re.search('^\d+', joined)
                    sparta_file_list1.append(
                        f'{proline_count.group(0)}PHN'+' 1000'+' 1000')
                    y = 0
                    proline_counter = 0
mutation_list1 = ['133R']
mutation_list2 = ['133A']
if mutation_list1 == () or mutation_list2 == ():
    for amino_acids in sparta_file_list1:
        sparta_file_list2.append(amino_acids)
else:
    for mutations, mutations2 in zip(mutation_list1, mutation_list2):
        for amino_acids in sparta_file_list1:
            if re.findall(mutations, amino_acids):
                splitting = amino_acids.split()
                mutation = re.sub(mutations, mutations2, splitting[0])
                mutation_value = re.sub('\d+.\d+', ' 1000', splitting[1])
                mutation_value2 = re.sub('\d+.\d+', ' 1000', splitting[2])
                mutation_replacement = mutation+mutation_value+mutation_value2
                sparta_file_list2.append(mutation_replacement)
            else:
                sparta_file_list2.append(amino_acids)
sparta_file_list3 = []
for aa in sparta_file_list2:
    modifiers = aa.strip()
    splitter = modifiers.split()
    searcher = re.search('^\d+[A-Z]', splitter[0])
    compiler = re.compile(searcher.group(0))
    sparta_sequence_comparison = list(filter(compiler.match, sequence_list))
    if sparta_sequence_comparison != []:
        sparta_file_list3.append(aa)

temp_list = []
temp_counter = 0
for checker in sparta_file_list3:
    temp_modifier = checker.strip()
    temp_split = temp_modifier.split()
    temp_finder = re.search('^\d+', temp_split[0])
    temp_list.append(temp_finder.group(0))
    temp_counter += 1
    if temp_counter == 5:
        if int(temp_finder.group(0)) == int(temp_list[0]):
            break
        else:
            del sparta_file_list3[0:4]
            break

if len(sparta_file_list3) % 6 != 0:
    del sparta_file_list3[-5:-1]
