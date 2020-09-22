import pandas as pd
from German_spelling_and_stopwords import non_european_countries

# header = ['id','date','surname', 'firstname', 'publishing location', 'text class']
df = pd.read_csv('C:/Users/jackewiebohne/Documents/python tests/DTA/DTA outputs/GP_csv.txt', sep=';', encoding='utf8', error_bad_lines=False)
df.pop('id')

def varcharRemover(path_to_files, df_geodata_column, sep=';', sep_count=4): #sep_count is the number of separators until we get to the geodata column
    with open(path_to_files, 'r', encoding='utf8') as f:
        lines = []
        for line in f:
            counter = 0
            string = ''
            for i in range(len(line)):
                if counter == sep_count:
                    if line[i] != '[' and line[i] != ']' and line[i] != '\'' and line[i:i+1] != '\\n' and line[i] != ',':
                        string += line[i]
                if line[i] == sep:
                    counter += 1
            lines.append(string)

    ###removing line breaks###
    lines2 = []
    for line in lines:
        restring = ''
        for i,c in enumerate(line):
            if line[i:i+2] != '\n':
                restring += line[i]
        lines2.append(restring)
    df['geodata'] = lines2[1:]
    return lines2


def DataSplitter(df_geodata_column, df):
    rows = [list(str(element).split()) for element in df_geodata_column]
    exclude = ['GERMAN_CITY:', 'REGION_IN_GERMANY:', 'SWISS_CITY:', 'POLISH_CITY:', 'COUNTRY:', 'SPANISH_CITY:',
               'AUSTRIAN_CITY:', 'FRENCH_CITY:', 'ITALIAN_CITY:', 'UK_CITY:']

    size_rows = []
    italian_rows = []
    french_rows = []
    german_rows = []
    austrian_rows = []
    swiss_rows = []
    polish_rows = []
    spanish_rows = []
    uk_rows = []
    non_european_rows = []
###for total count of references###
    for row in rows:
        counter = 0
        for i in range(len(row)):
            # print(row[i])
            if row[i] not in exclude:
                try:
                    counter += int(row[i])
                    counter -= 1
                except:
                    if row[i] != '': #to prevent empty georeferences being recorded as 1
                        counter += 1
        size_rows.append(counter)

        italian_counter = 0
        french_counter = 0
        german_counter = 0
        austrian_counter = 0
        swiss_counter = 0
        polish_counter = 0
        spanish_counter = 0
        uk_counter = 0
        non_european_counter = 0

        for i in range(len(row)):
        ###italian georeferences###
            if row[i] == 'ITALIAN_CITY:':
                try:
                    italian_counter += int(row[i+2])
                except:
                    italian_counter += 1
            if row[i] == 'Italien':
                try:
                    italian_counter += int(row[i+1])
                except:
                    italian_counter += 1

        ###german georeferences###
            if row[i] == 'GERMAN_CITY:' or row[i] == 'REGION_IN_GERMANY:':
                try:
                    german_counter += int(row[i+2])
                except:
                    german_counter += 1
            if row[i] == 'Deutschland':
                try:
                    german_counter += int(row[i+1])
                except:
                    german_counter += 1

        ###french georeferences###
            if row[i] == 'FRENCH_CITY:':
                try:
                    french_counter += int(row[i+2])
                except:
                    french_counter += 1
            if row[i] == 'Frankreich' or row[i] == 'Franckreich':
                try:
                    french_counter += int(row[i+1])
                except:
                    french_counter += 1

        ###uk georeferences###
            if row[i] == 'UK_CITY:':
                try:
                    uk_counter += int(row[i+2])
                except:
                    uk_counter += 1
            if row[i] == 'Großbritannien' or row[i] == 'England' or row[i] == 'Schottland' or row[i] == 'Wales':
                try:
                    uk_counter += int(row[i+1])
                except:
                    uk_counter += 1

        ###polish georeferences###
            if row[i] == 'POLISH_CITY:':
                try:
                    polish_counter += int(row[i+2])
                except:
                    polish_counter += 1
            if row[i] == 'Polen':
                try:
                    polish_counter += int(row[i+1])
                except:
                    polish_counter += 1

        ###spanish###
            if row[i] == 'SPANISH_CITY:':
                try:
                    spanish_counter += int(row[i+2])
                except:
                    spanish_counter += 1
            if row[i] == 'Spanien' or row[i] == 'Katalonien' or row[i] == 'Kastilien':
                try:
                    spanish_counter += int(row[i+1])
                except:
                    spanish_counter += 1

        ###swiss###
            if row[i] == 'SWISS_CITY:':
                try:
                    swiss_counter += int(row[i+2])
                except:
                    swiss_counter += 1
            if row[i] == 'Schweiz':
                try:
                    swiss_counter += int(row[i+1])
                except:
                    swiss_counter += 1

        ###austrian###
            if row[i] == 'AUSTRIAN_CITY:':
                try:
                    austrian_counter += int(row[i+2])
                except:
                    austrian_counter += 1
            if row[i] == 'Österreich':
                try:
                    austrian_counter += int(row[i+1])
                except:
                    austrian_counter += 1

        ###non_european_country###
            if row[i] in non_european_countries:
                try:
                    non_european_counter += int(row[i + 1])
                except:
                    non_european_counter += 1

        italian_rows.append(italian_counter)
        german_rows.append(german_counter)
        french_rows.append(french_counter)
        uk_rows.append(uk_counter)
        polish_rows.append(polish_counter)
        spanish_rows.append(spanish_counter)
        swiss_rows.append(swiss_counter)
        austrian_rows.append(austrian_counter)
        non_european_rows.append(non_european_counter)

    #adding the data to new rows in the dataframe
    df['no of georeferences'] = size_rows
    df['italian georeferences'] = italian_rows
    df['spanish georeferences'] = spanish_rows
    df['french georeferences'] = french_rows
    df['swiss georeferences'] = swiss_rows
    df['austrian georeferences'] = austrian_rows
    df['uk georeferences'] = uk_rows
    df['polish georeferences'] = polish_rows
    df['german georeferences'] = german_rows
    df['non-european georeferences'] = non_european_rows

    return size_rows, italian_rows, spanish_rows, french_rows, swiss_rows, austrian_rows, uk_rows, polish_rows, german_rows, non_european_rows


def uniqueGeodata(df_geodata_column, df):
    exclude = ['UK_CITY:', 'ITALIAN_CITY:', 'FRENCH_CITY:', 'GERMAN_CITY:', 'REGION_IN_GERMANY:', 'COUNTRY:',
               'SPANISH_CITY:', 'POLISH_CITY:', 'AUSTRIAN_CITY:', 'SWISS_CITY:']
    filtered = [j for i, j in df_geodata_column.iteritems()]
    further_filter = []
    for element in filtered:
        filtered2 = []
        try:
            for geovalue in element.split():
                try:
                    int(geovalue)
                except:
                    if geovalue not in exclude:
                        filtered2.append(geovalue)
            further_filter.append(filtered2)
        except:
            further_filter.append([])

    unique_geodata = []
    count_unique_geodata = []
    for lst in further_filter:
        counter = 0
        if lst:
            menge = set(lst)
            for element in menge:
                counter += 1
            count_unique_geodata.append(counter)
            unique_geodata.append(list(menge))
        else:
            count_unique_geodata.append(counter)
            unique_geodata.append([])

    #adding data to new rows in the dataframe
    df['unique georeferences'] = unique_geodata
    df['no of unique georeferences'] = count_unique_geodata
    return


def relativeGeodata(df, df_word_count_column):
    # df2 = pd.read_csv('C:/Users/jackewiebohne/Documents/python tests/DTA/DTA outputs/dta_word_count.txt', sep=';',
    #                   encoding='utf8')

    #adding new rows based on old rows to dataframe
    # df['word count'] = df['word count of text']
    df['rel. no of georeferences'] = (df['no of georeferences'] / df_word_count_column) * 1000
    df['rel. italian georeferences'] = (df['italian georeferences'] / df_word_count_column) * 1000
    df['rel. spanish georeferences'] = (df['spanish georeferences'] / df_word_count_column) * 1000
    df['rel. french georeferences'] = (df['french georeferences'] / df_word_count_column) * 1000
    df['rel. swiss georeferences'] = (df['swiss georeferences'] / df_word_count_column) * 1000
    df['rel. austrian georeferences'] = (df['austrian georeferences'] / df_word_count_column) * 1000
    df['rel. uk georeferences'] = (df['uk georeferences'] / df_word_count_column) * 1000
    df['rel. polish georeferences'] = (df['polish georeferences'] / df_word_count_column) * 1000
    df['rel. german georeferences'] = (df['german georeferences'] / df_word_count_column) * 1000
    df['rel. no of non-European georeferences'] = (df['non-european georeferences'] / df_word_count_column) * 1000
    df['rel. no of unique georeferences'] = (df['no of unique georeferences'] / df_word_count_column) * 1000
    return

###setting up function parameters###
path_to_files = 'C:/Users/jackewiebohne/Documents/python tests/DTA/DTA outputs/GP_csv.txt'
dataframe_column = df['geodata']

###calling the functions###
x = varcharRemover(path_to_files, df_geodata_column=dataframe_column)
y = DataSplitter(df_geodata_column=dataframe_column, df=df)
z = uniqueGeodata(df_geodata_column=dataframe_column, df=df)
w = relativeGeodata(df=df, df_word_count_column=df['word count of text'])

# print(df.describe())

df.to_csv(r'C:/Users/jackewiebohne/Documents/python tests/DTA/DTA outputs/GP_filed_geodata.csv', index=False, sep=';', encoding='utf-8-sig')