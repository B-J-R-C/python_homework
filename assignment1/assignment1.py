#Q1
def hello():
 
 print("This is for debugging")
 return "Hello!"

#Q2
def greet(name: str) -> str:
 
  # f-string 
  return f"Hello, {name}!"

#Q3
def calc(value1, value2, operation: str = "multiply"):
  
  try:
    if operation == "add":
      result = value1 + value2
    elif operation == "subtract":
      result = value1 - value2
    elif operation == "multiply":
      result = value1 * value2
    elif operation == "divide":
      if value2 == 0:
        return "You can't divide by 0!"
      result = value1 / value2
    elif operation == "modulo":
      if value2 == 0:
        return "You can't divide by 0!"
      result = value1 % value2
    elif operation == "int_divide":
      if value2 == 0:
        return "You can't divide by 0!"
      result = value1 // value2
    elif operation == "power":
      result = value1 ** value2
    else:
     
#Q4 


def data_type_conversion(value, target_type_name: str):

  try:
    if target_type_name == "float":
      return float(value)
    elif target_type_name == "str":
      return str(value)
    elif target_type_name == "int":
      return int(value)
    else:
      return f"Unsupported target type: '{target_type_name}'. Choose from 'float', 'str', 'int'."
  except (ValueError, TypeError):
    return f"You can't convert {value!r} into a {target_type_name}."

  
  #q5
  def grade(*scores):
 
  if not scores:
    return "No scores provided"

  try:
    # Calculate the sum of all scores
    total_score = sum(scores)
    # Calculate the average
    average = total_score / len(scores)
  except TypeError:
    # This catches errors if any of the 'scores' are not numbers (e.g., strings)
    return "Invalid data was provided."

  # Determine the letter grade based on the average
  if average >= 90:
    return "A"
  elif 80 <= average < 90:
    return "B"
  elif 70 <= average < 80:
    return "C"
  elif 60 <= average < 70:
    return "D"
  else:
    return "F"
  
  #q6
  def repeat(s: str, count: int) -> str:
  
  repeated_string = ""
  for _ in range(count):
    repeated_string += s
  return repeated_string

#q7
def student_scores(analysis_type: str, **kwargs):

  scores = list(kwargs.values())
  student_names = list(kwargs.keys())

  if not scores:
    return "No student score"

  if analysis_type == "best":
    if not student_names:
        return "Cannot determine best student without student names."
    # Find maximum score
    best_score = -1
    best_student = ""
    for name, score in kwargs.items():
      if score > best_score:
        best_score = score
        best_student = name
    return best_student
  elif analysis_type == "mean":
    # average score
    total_score = sum(scores)
    average_score = total_score / len(scores)
    return average_score
  else:
    return "Invalid analysis type. Choose 'best' or 'mean'."

#Q8
def titleize(text: str) -> str:
  """
  Rules:
  1. The first word is always capitalized.
  2. The last word is always capitalized.
  3. All other words are capitalized, except "a", "on", "an", "the", "of", "and", "is", "in".

  """
  little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
  words = text.split()
  titleized_words = []

  if not words:
    return ""

  for i, word in enumerate(words):
    # Rule 1
    if i == 0:
      titleized_words.append(word.capitalize())
    # Rule 2
    elif i == len(words) - 1:
      titleized_words.append(word.capitalize())
    # Rule 3
    else:
      if word.lower() in little_words:
        titleized_words.append(word.lower())
      else:
        titleized_words.append(word.capitalize())

  return " ".join(titleized_words)

#Q9
def hangman(secret: str, guess: str) -> str:

  revealed_word_list = []
  for char in secret:
    if char in guess:
      revealed_word_list.append(char)
    else:
      revealed_word_list.append("_")
  return "".join(revealed_word_list)

#Q10
def pig_latin(text: str) -> str:
  """
  Rules:
  1. If a word starts with a vowel (a, e, i, o, u), add "ay" to end.
  2. If a word starts with consonant, move consonants
     to the end, and add "ay" 
  3. "qu" is special case: 'q' and 'u' are moved to the end together.

  """
  vowels = "aeiou"
  words = text.split()
  pig_latin_words = []

  for word in words:
    if not word:  # for empty string
      pig_latin_words.append("")
      continue

    # Rule 1
    if word[0] in vowels:
      pig_latin_words.append(word + "ay")
    else:
      # Rule 3
      if word.startswith("qu"):
        pig_latin_words.append(word[2:] + "quay")
      else:
        # Rule 2
        consonant_cluster = ""
        for i, char in enumerate(word):
          if char not in vowels:
            consonant_cluster += char
          else:
            break
        pig_latin_words.append(word[len(consonant_cluster):] + consonant_cluster + "ay")

  return " ".join(pig_latin_words)
