import collections
import random

def create_ngram_models(textPath):
  # Read text from file
  with open(textPath, 'r', encoding='utf-8') as f:
    text = f.read()

  # Preprocess text (remove punctuation)
  for punct in "!,.?':;":
    text = text.replace(punct, "")
    
  # Split text into words, ensuring no empty words
  words = [word for word in text.split() if word]

  # Create empty dictionaries for ngrams and vocabulary
  vocab = set()
  unigrams = collections.Counter()
  bigrams = collections.Counter()
  trigrams = collections.Counter()

  # Build vocabulary and count unigrams simultaneously
  for word in words:
    vocab.add(word)
    unigrams[word] += 1

  # Count bigrams and trigrams, handling vocabulary limitations
  for i in range(len(words) - 1):
    prev_word, word = words[i], words[i + 1]
    bigrams[(prev_word, word)] += 1

    if i < len(words) - 2:
      next_word = words[i + 2]
      trigram = (prev_word, word, next_word)

      # Check if all words in the trigram are in the vocabulary
      if all(word in vocab for word in trigram):
        trigrams[trigram] += 1

  return vocab, unigrams, bigrams, trigrams
    
def generate_sentences(initial_words, unigrams, bigrams, trigrams, max_length=10):
  sentences = []

   # Generate sentence using unigrams
  sentence = initial_words.copy()
  while len(sentence) < max_length:
    next_word = random.choices(list(unigrams.keys()), weights=list(unigrams.values()))[0]
    sentence.append(next_word)
  sentences.append(" ".join(sentence).capitalize())

  # Generate sentence using bigrams with fallback to unigrams
  sentence = initial_words.copy()
  while len(sentence) < max_length:
    prev_word, curr_word = sentence[-2:]
    next_word_candidates = [w for w, count in bigrams.items() if w[0] == curr_word]
    if next_word_candidates:
      next_word = random.choices(next_word_candidates, weights=[count for _, count in bigrams.items() if _[0] == curr_word])[0][1]
    else:
      # Fallback to unigrams if no valid bigram found
      next_word = random.choices(list(unigrams.keys()), weights=list(unigrams.values()))[0]
    sentence.append(next_word)
  sentences.append(" ".join(sentence).capitalize())

  # Generate sentence using trigrams with fallback to bigrams/unigrams
  sentence = initial_words.copy()
  while len(sentence) < max_length:
    prev_word1, prev_word2, curr_word = sentence[-3:]
    next_word_candidates = [w for w in trigrams.keys() if w[0] == prev_word2 and w[1] == curr_word]
    if next_word_candidates:
      next_word = random.choices(next_word_candidates, weights=[count for _, count in trigrams.items() if _[0] == prev_word2 and _[1] == curr_word])[0][2]
    else:
      # Fallback to bigrams if no valid trigram found
      prev_word, curr_word = sentence[-2:]
      next_word_candidates = [w for w, count in bigrams.items() if w[0] == curr_word]
      if next_word_candidates:
        next_word = random.choices(next_word_candidates, weights=[count for _, count in bigrams.items() if _[0] == curr_word])[0][1]
      else:
        # Final fallback to unigrams if no valid bigram either (or end of sentence)
        next_word = random.choices(list(unigrams.keys()), weights=list(unigrams.values()))[0]
    sentence.append(next_word)
  sentences.append(" ".join(sentence).capitalize())

  return sentences

# Example
# Book path file
textPath = 'English-Language-Model-using-N-gram-probabilistic-model\Text.rtf'

vocab, unigrams, bigrams, trigrams = create_ngram_models(textPath)

#print(f"Vocabulary: {vocab}")
#print(f"Unigrams: {unigrams}")
#print(f"Bigrams: {bigrams}")
#print(f"Trigrams: {trigrams}")

# Initial words to start the generated sentences
initial_words = ["my", "name", "is"]

# Generate three sentences (one for each n-gram model)
sentences = generate_sentences(initial_words, unigrams, bigrams, trigrams)

# Print the generated sentences
print("Generated Sentences:")
for sentence in sentences:
  print(sentence)