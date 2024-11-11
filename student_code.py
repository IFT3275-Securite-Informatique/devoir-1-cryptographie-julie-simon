# Simon Voglimacci Stéphanopoli - 20002825
# Julie Yang - 20239909
# Date: 2024-11-10

# IFT 3275 Devoir 2 - Question 2


import requests
from collections import Counter
import random as rnd

URLS = ["https://www.gutenberg.org/ebooks/13846.txt.utf-8", "https://www.gutenberg.org/ebooks/4650.txt.utf-8" ]

SYMBOLS = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

def load_text_from_web(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"An error occurred while loading the text: {e}")
    return None

def cut_string_into_pairs(text):
  pairs = []
  for i in range(0, len(text) - 1, 2):
    pairs.append(text[i:i + 2])
  if len(text) % 2 != 0:
    pairs.append(text[-1] + '_')  # Add a placeholder if the string has an odd number of characters
  return pairs

def M_vers_symboles(M, K, custom_dict):
    encoded_text = []
    i = 0

    while i < len(M):
        # Vérifie les paires de caractères
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in custom_dict:
                encoded_text.append(pair)
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifie le caractère seul
        if M[i] in K:
            encoded_text.append(M[i])
        else:
            # Conserve le caractère tel quel si non trouvé
            encoded_text.append(M[i])
        i += 1

    return encoded_text


def split_string(text, n):
    return [text[i:i+n] for i in range(0, len(text), n)]


def get_frequencies(string):
    result = Counter(string)

    # sort in descending order of frequency
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))



def gen_decryption_key(corpus_symbols, cipher_symbols):
   key = {}

   for (corpus_symbol), (cipher_symbol) in zip(corpus_symbols, cipher_symbols):
       key[corpus_symbol] = cipher_symbol

   return key


def decode(C, K):
    string = []
    for c in C:
       char = next((key for key, value in K.items() if value == c), "#")

       string.append(char)

    return string

def chiffrer(M,K, custom_dict):
  l = M_vers_symboles(M, K, custom_dict)
  l = [K[x] for x in l]
  return ''.join(l)

def gen_key(symboles):

  l=len(symboles)
  if l > 256:
    return False

  rnd.seed(1337)
  int_keys = rnd.sample(list(range(l)),l)
  dictionary = dict({})
  for s,k in zip(symboles,int_keys):
    dictionary[s]="{:08b}".format(k )
  return dictionary

def decrypt(C):

   # Create the corpus used for frequency analysis
  corpus = ""
  for url in URLS:
      corpus += load_text_from_web(url)

  dictionnaire = gen_key(SYMBOLS)
  K = gen_key(SYMBOLS)
  encrypted_corpus = chiffrer(corpus, K, dictionnaire)

  # Get the frequencies of the symbols in the corpus
  corpus_frequencies = get_frequencies(M_vers_symboles(corpus, SYMBOLS, SYMBOLS))

  # Split the Cipher text into blocks of 8 characters
  encrypted_corpus = split_string(encrypted_corpus, 8)

  # Get the frequencies of the symbols in the encrypted corpus
  cipher_frequencies = get_frequencies(encrypted_corpus)

  # Generate a key by matching the most frequent symbols in the cipher text with the most frequent symbols in the corpus
  key = gen_decryption_key(corpus_frequencies, cipher_frequencies)

  cipher = split_string(C, 8)

  # Decrypt the cipher text using the statistically generated key
  message = ''.join(decode(cipher, key))


  return message


