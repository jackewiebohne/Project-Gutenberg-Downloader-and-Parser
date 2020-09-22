import pathlib
import time, os



def PunctuationRemover(wordsstring, normalise_spelling=False, return_list=True):
    a = wordsstring
    if normalise_spelling == True:
        a = wordsstring.replace('oͤ', 'ö').replace('Oͤ', 'Ö').replace('aͤ', 'ä').replace('Aͤ', 'Ä').replace('uͤ', 'ü').replace('Uͤ', 'Ü')\
            .replace('ſ', 's').replace('æ', 'ae').replace('ï', 'i').replace('ꝛc', 'etc').replace('Ï', 'I').replace('Æ', 'Ae').replace('/', ' ')\
            .replace('-', '').replace('̃n', 'n').replace('̃N', 'N')
    translator = str.maketrans('', '', string.punctuation) # This uses the 3-argument version of str.maketrans with arguments (x, y, z) where 'x' and 'y' must be equal-length strings and characters in 'x'  are replaced by characters in 'y'. 'z'  is a string (string.punctuation here) where each character in the string is mapped to None     f.translate(str.maketrans("",""), string.punctuation) #then the translator is passed on to the translate function in string
    g = a.translate(translator)
    h = re.sub('(«|»)', '', g)
    if return_list == True:
        h = h.split()
    return h

  
 def GermanCityDeLatiniser(wordstring):
    string = ''
    for word in wordstring.split():
        if word in gss.Latin_to_German_cities:
            string += gss.Latin_to_German_cities.get(word) + ' '
        else:
            string += word + ' '
    return string

  
 def WordLabeler(wordlist): #make sure punctuation is removed in the wordlist, otherwise it won't return, say, a city if is followed by punctuation
    h = [] #ultimately for this to work, the wordlist has to go through the suffixremover first## should the suffixremover be built in?
    # lang = [x for x in gss.languages[0]] #list comprehension is needed because str(gss.languages) would match any string-part of the languages in the language list with the word (e.g. 'ich' in 'Österreich'). The [0] is needed because the countries are read as a list from the file via list comprehension which creates a list of lists. Thus e.g. countries[0] is the first list (of the countries list) which is the list containing all countries.
    coun = [x for x in gss.countries.split()]
    ita = [x for x in gss.Italian_cities.split()]
    fre = [x for x in gss.French_cities.split()]
    ger = [x for x in gss.German_cities.split()]
    aus = [x for x in gss.Austrian_cities.split()]
    reg = [x for x in gss.German_regions.split()]
    tc = gss.territorial_classifiers#[x for x in gss.territorial_classifiers]
    # dia = [x for x in gss.German_dialects.split()]
    uk = [x for x in gss.UK_cities.split()]
    pol = [x for x in gss.Polish_cities.split()]
    swiss = [x for x in gss.Swiss_cities.split()]
    span = [x for x in gss.Spanish_cities.split()]
    spec = [x for x in gss.special_cases.split()]

    for index, word in enumerate((wordlist)): #should this be build in as a second-order conditional?: 'or wordlist[index - 1] not in gss.loc_prepositions and wordlist[index - 1] not in gss.loc_prepositions_caps'
        # if word in lang:
        #     h.extend(('LANGUAGE:', word))
        if word in spec:
            if wordlist[index - 8: index + 8] in tc or wordlist[index - 1] in gss.loc_prepositions \
                    or wordlist[index - 1] in gss.loc_prepositions_caps:
                h.extend(('GERMAN_CITY:', word))
        if word[:-1] in spec:
            if wordlist[index - 8: index + 8] in tc or wordlist[index - 1] in gss.loc_prepositions \
                    or wordlist[index - 1] in gss.loc_prepositions_caps:
                h.extend(('GERMAN_CITY:', word[:-1]))
        if wordlist[index - 1] not in gss.determiners and wordlist[index - 1] not in tc \
                or wordlist[index-5: index+5] in tc: #to check whether the preceding word is a determiner, which would likely indicate that it is not a city (e.g. 'Essen' == Stadt, 'das Essen'== food) or a territorial classifiers are used in the surroundings of the word
            if word in ger:
                h.extend(('GERMAN_CITY:', word))
            if word in reg:
                h.extend(('REGION_IN_GERMANY:', word))
            if word in swiss:
                h.extend(('SWISS_CITY:', word))
            if word in pol:
                h.extend(('POLISH_CITY:', word))
            if word[-1:] == 's': #word[:-1] removes the last letter of word to check whether the word is used in genitive case with added 's'
                if word[:-1] in ger:
                    h.extend(('GERMAN_CITY:', word[:-1]))
                if word[:-1] in reg:
                    h.extend(('REGION_IN_GERMANY:', word[:-1]))
                if word[:-1] in coun:
                    h.extend(('COUNTRY:', word[:-1]))
                if word[:-1] in span:
                    h.extend(('SPANISH_CITY:', word[:-1]))
                if word[:-1] in aus:
                    h.extend(('AUSTRIAN_CITY:', word[:-1]))
                if word[:-1] in fre:
                    h.extend(('FRENCH_CITY:', word[:-1]))
                if word[:-1] in ita:
                    h.extend(('ITALIAN_CITY:', word[:-1]))
                if word[:-1] in uk:
                    h.extend(('UK_CITY:', word[:-1]))
                if word[:-1] in swiss:
                    h.extend(('SWISS_CITY:', word[:-1]))
                if word[:-1] in pol:
                    h.extend(('POLISH_CITY:', word[:-1]))
            if word in span:
                h.extend(('SPANISH_CITY:', word))
            if word in aus:
                h.extend(('AUSTRIAN_CITY:', word))
            if word in fre:
                h.extend(('FRENCH_CITY:', word))
            if word in ita:
                h.extend(('ITALIAN_CITY:', word))
            if word in uk:
                h.extend(('UK_CITY:', word))
            if word in coun:
                h.extend(('COUNTRY:', word))
        # if word in dia:
        #     h.extend(('GERMAN_DIALECT:', word))
        # if word in tc:
        #     h.extend(('TERRITORIAL CLASSIFICATION:', word))
        # elif word not in h: #comment these two lines for just the list, otherwise gives complete list, not just langs, countries etc.
        #     h.append(word) #comment these two lines for just the list, otherwise gives complete list, not just langs, countries etc.
    # return h
    ##uncomment all of below, if above lines are commented and vice versa
    l = []
    counter = 1
    for i in range(1, len(h), 2):
        if h[i] == '/':
            continue
        unique = True
        l.append(h[0 + i - 1])  # appends the classifier
        l.append(h[i])  # append the element in above-specified range (2n+1)
        counter = 1
        for j in range(i + 2, len(h), 2):  # then iterate over all the remaining (2n+1)+2 elements
            if h[i] == h[j]:
                h[j] = '/'
                unique = False
                counter += 1
        if unique == False:  # this operation cannot be integrated into the 2nd loop (e.g. by l[i] = '/'), because then it would not go through the entire list with j to find all the matches with i. so in the following list [0, 'a', 2, 'b', 4, 'b', 6, 'c', 8, 'c', 10, 'a', 12, 'a'] the 'a' at index 11 would be matched in the j loop by the 'a' in index 2, but the 'a' in index 13 would not be ranged over anymore if after the match between index 2 and 11 l[i] would already be appended and replaced
            h[i] = '/'
            l.append(counter)  # to count how many times l[i] and l[j] were matched
    return l 
  

def GP_parser(path_to_files: str, csv_filename: str, file_path_text_cleaner_output, text_cleaner=True, csv_header=False, author=False, title=False,
                   geodata=False, word_count=False, skip_translations=True, flush_buffer_n_write_to_file=True):

###for text cleaning###
    most_common_engl_words_custom = 'the be any to of Gutenberg before downloading, copying, displaying, performing, distributing copying, distributing, performing, THE FULL PROJECT GUTENBERG LICENSE permission and without paying copyright royalties. Special rules, redistribution. displaying See paragraph electronic creating derivative particular state visit ways including http://www.gutenberg.net West, Salt Lake City, including checks License Dr. Gregory B. Newby Chief Executive and Director gbnewby@pglaf.org as specified Literary Archive Foundation For additional contact information page often in several formats including plain compressed others online payments please visit works and credit card donations To donate array of equipment including outdated equipment Many small donations Project provide by produce provided produced and a that have I it is was for not on with he as you do at this but his by from they we say her she or of if even an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us'
    set_most_common_engl_words_custom = set([x for x in most_common_engl_words_custom.split()])


    with open(csv_filename, "a", encoding='utf8', errors='ignore') as a:

        with open(csv_filename, "r", encoding='utf8', errors='ignore') as r:

###csv header###
            id = -1
            counter = -1 #for stop-n-go parsing: to continue from last parsing step
            lines = []
            for line in r:
                counter += 1
                print(counter)
                lines.append(line.split(';')) #the csv separator is an underscore instead of a comma to avoid possible conflicts with commas in the xml and the geodata lists, which contain commas
            if csv_header:
                try:
                    if lines[0][0] == 'id':
                        pass
                except:
                    csv_head = 'id'
                    if title:
                        csv_head += ';title'
                    if author:
                        csv_head += ';author name'
                    if not skip_translations:
                        csv_head += ';translator name'
                    if text_cleaner:
                        print(
                            'Note that the texts will be saved as numbered .txt files, followed by author name and title, from the csv in your CWD.')
                    if geodata:
                        csv_head += ';geodata'
                        print('Please make sure to first clean up the texts before extracting metadata and creating a csv. For parsing for metadata and create csv'
                              'run this parser again with the path_to_files directed ad the folder with the cleaned-up Gutenberg txts')
                    if word_count:
                        csv_head += ';word count of text'
                    csv_head += '\n'
                    a.write(csv_head)

    ###parser starts here###
            for txt in pathlib.Path(path_to_files).iterdir():
                if txt.is_file():
                    id += 1
                    athr = ''
                    gdata = ''
                    ttle = ''
                    string = ''
                    trnslator = ''
                    skipper = False
                    memoriser = True
                    memoriser2 = True
                    memoriser3 = True
                    if counter == -1 or counter == 0 or id >= counter:  # to pick up at the last point
                        if geodata:
                            print('Parsing document ' + str(id) + ' for geodata')
                            start1 = time.time()

                ###csv metadata###
                        if title or author or geodata or word_count:
                            with open(txt, 'r', encoding='utf8') as g:
                                if word_count:
                                    word_counter = 0
                                for line in g:
                                    string += line
                                    for i in range(len(line.split())):
                                        if skip_translations:
                                            if line.split()[i] == 'Translator:':
                                                skipper = True
                                                print('Skipping translation')
                                                break
                                        else:
                                            if line.split()[i] == 'Translator:':
                                                trnslator += ';(Translator:) '
                                                trnslator += ' '.join(line.split()[i + 1:])
                                                memoriser = False
                                        if word_count:
                                            word_counter += 1
                                        if author:
                                            if line.split()[i] == 'Author:':
                                                athr += ';'
                                                athr += ' '.join(line.split()[i + 1:])
                                                memoriser2 = False
                                        if title:
                                            if line.split()[i] == 'Title:':
                                                ttle += ';'
                                                temp_string4 = ' '.join(line.split()[i + 1:])
                                                temp_string4 = temp_string4.replace(';', '')
                                                ttle += temp_string4
                                                memoriser3 = False
                                if geodata and skipper == False:
                                    try:
                                        temp_string = PunctuationRemover(string, normalise_spelling=True, return_list=False)
                                        temp_string2 = GermanCityDeLatiniser(temp_string)
                                        temp_string3 = WordLabeler(temp_string2.split())
                                        gdata += ';' + str(temp_string3)
                                    except:
                                        gdata += ';'
                                        continue

                            ###write metadata to file###
                            if skipper == False:
                                a.write(str(id))
                                if title:
                                    if memoriser3:
                                        ttle += ';-99999'
                                    a.write(ttle)
                                if author:
                                    if memoriser2:
                                        athr += ';-99999'
                                    a.write(athr)
                                if not skip_translations:
                                    if memoriser:
                                        trnslator += ';-99999'
                                    a.write(trnslator)
                                if geodata:
                                    a.write(gdata)
                                    duration1 = time.time() - start1
                                    print('finished parsing text for geolocations. duration:', duration1)
                                if word_count:
                                    a.write(';' + str(word_counter))
                                a.write('\n')
                                if flush_buffer_n_write_to_file:
                                    a.flush()  # flushing internal buffers
                                    os.fsync(a.fileno())  # force-writing buffers to file

                ###text###
                    if text_cleaner:
                        try:
                            with open(txt, 'r', encoding='utf8') as f:
                                txts = ''
                                ttle = ''
                                athr = ''
                                for line in f:
                                    line_split = line.split()
                                    for i in range(len(line_split)):
                                        if line_split[i] == 'Title:':
                                            ttle += ' '.join(line_split[i + 1:])
                                            ttle = PunctuationRemover(ttle, normalise_spelling=True, return_list=False)
                                            ttle = ttle.replace('(', ' ')
                                            ttle = ttle.replace(')', ' ')
                                            ttle = ttle.replace('  ', ' ')
                                            ttle = ttle.replace(';', '.')
                                        if line_split[i] == 'Author:':
                                            athr += ', '
                                            athr += ' '.join(line_split[i + 1:])
                                            athr += ', '
                                    counter = 0
                                    for word in line.split():
                                        if word.lower() in set_most_common_engl_words_custom or word in set_most_common_engl_words_custom or word.upper() in set_most_common_engl_words_custom:
                                            counter += 1
                                    if counter >= 2:
                                        continue
                                    if counter < 2:
                                        txts += line
                            print('writing text ' + str(id) + ' to file')
                            try:
                                with open(file_path_text_cleaner_output + str(id) + str(athr) + str(ttle) + '.txt', 'w+', encoding='utf8', errors='ignore') as w:
                                    w.write(str(txts))
                            except:
                                try:
                                    with open(file_path_text_cleaner_output + str(id) + str(athr) + '.txt', 'w+', encoding='utf8', errors='ignore') as w:
                                        w.write(str(txts))
                                except:
                                    with open(file_path_text_cleaner_output + str(id) + '.txt', 'w+', encoding='utf8', errors='ignore') as w:
                                        w.write(str(txts))

                        #in case encoding of text is different
                        except:
                            with open(txt, 'r', encoding='ISO-8859-1') as f:
                                txts = ''
                                ttles = ''
                                athrs = ''
                                for line in f:
                                    line_split = line.split()
                                    for i in range(len(line_split)):
                                        if line_split[i] == 'Title:':
                                            ttle += ' '.join(line_split[i + 1:])
                                            ttle = PunctuationRemover(ttle, normalise_spelling=True, return_list=False)
                                            ttle = ttle.replace('(', ' ')
                                            ttle = ttle.replace(')', ' ')
                                            ttle = ttle.replace('  ', ' ')
                                            ttle = ttle.replace(';', '.')
                                        if line_split[i] == 'Author:':
                                            athr += ', '
                                            athr += ' '.join(line_split[i + 1:])
                                            athr += ', '
                                    counter = 0
                                    for word in line.split():
                                        if word.lower() in set_most_common_engl_words_custom or word in set_most_common_engl_words_custom or word.upper() in set_most_common_engl_words_custom:
                                            counter += 1
                                    if counter >= 2:
                                        continue
                                    if counter < 2:
                                        txts += line
                            print('writing text ' + str(id) + ' to file')
                            try:
                                with open(file_path_text_cleaner_output + str(id) + str(athr) + str(ttle) + '.txt', 'w+', encoding='utf8', errors='ignore') as w:
                                    w.write(str(txts))
                            except:
                                try:
                                    with open(file_path_text_cleaner_output + str(id) + str(athr) + '.txt', 'w+', encoding='utf8', errors='ignore') as w:
                                        w.write(str(txts))
                                except:
                                    with open(file_path_text_cleaner_output + str(id) + '.txt', 'w+', encoding='utf8', errors='ignore') as w:
                                        w.write(str(txts))



path = './Gutenberg cleaned files/'
# path2 = './Gutenberg ebooks/'
csv = './DTA outputs/GP_csv.txt'
text_clnr_output = './Gutenberg cleaned files/'
x = GP_parser(path_to_files=path, csv_filename=csv, file_path_text_cleaner_output=text_clnr_output, csv_header=True, text_cleaner=False, author=True, title=True, word_count=True, geodata=True, skip_translations=False)
