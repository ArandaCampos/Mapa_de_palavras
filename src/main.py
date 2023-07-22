from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import pandas as pd
import sys

# Variáveis
start =  end = file = word = None
text = ''

# Argvs
for i, arg in enumerate(sys.argv):
    if '--start' == arg or '-s' == arg:
        start = int(sys.argv[i + 1])
    elif '--end' == arg or '-e' == arg:
        end = int(sys.argv[i + 1])
    elif '--file' == arg or '-f' == arg:
        file = sys.argv[i + 1]
    elif '--word' == arg or '-w' == arg:
        word = sys.argv[i + 1]

# Leitura
try:
    reader = PdfReader(file)
except:
    print('Erro!')
    raise SystemExit

if not start:
    start = 0
if not end:
    end = int(len(reader.pages))

ignored_words = [
    # Artigos
    'a', 'o', 'as', 'os', 'aos', 'ao', 'à', 'às', 'um', 'uma', 'uns', 'umas',
    # Preposições
    'ante', 'perante', 'após', 'até', 'com', 'contra', 'de', 'desde', 'em', 'entre',
    'para', 'por', 'sem', 'sob', 'sobre', 'trás', 'atrás', 'dentro', 'para', 'cada',
    'no', 'na', 'nas', 'nos', 'da', 'do', 'das', 'dos', 'pelo', 'pela', 'que', 'somente'
    # Conjunções
    'mas', 'porém', 'contudo', 'todavia', 'e', 'também', 'mas', 'além',
    'como', 'apenas', 'tão', 'enquanto', 'isso', 'ademais', 'consequentemente',
    # Advérbios
    'não', 'sim', 'muito', 'mais', 'pouco', 'ou', 'bastante',
    # Verbos
    'é', 'são', 'era', 'eram', 'foi',
    # Pronomes
    'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
    'meu', 'meus', 'minhas', 'teu', 'teus', 'tua', 'tuas', 'seu', 'seus', 'sua', 'suas', 'vosso', 'nosso',
    'me', 'se', 'ti',
    'todo', 'toda', 'todos', 'todas', 'aquele', 'aqueles', 'aquela', 'aquelas', 'este', 'esta', 'estes', 'estas','esse', 'esses',
    'aquilo', 'isso',
    # Caracteres especiais
    '-', '_', '*',
]
punctuation = [
    '.', ',', ' -', '- ' , '!', '?', '(', ')', '"', "'"
]

for n in range(start, end):
    page = reader.pages[n]
    text += str(page.extract_text()).lower()
    print("Progresso: {:.1f}%".format((n - start)/ (end - start) * 100), end="\r")

for x in punctuation:
    text = text.replace(x, "")

words = text.split()
words = pd.Series(words, dtype="string")
words = words[~words.isin(ignored_words)]

count = words.value_counts()
analyzer = count.sort_values(ascending=False)

if word:
    print(count[word])

print(analyzer)

plt.suptitle('Análise do livro {}'.format(file))
plt.xlabel('Menções')
plt.ylabel('Palavras')
plt.barh(list(reversed(analyzer.iloc[0:20].index.values)), list(reversed(analyzer.iloc[0:20].values)))# , width=0.75)
plt.show()
