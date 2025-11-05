# Python Open-Source Code
# CustomSourcetextParser module — custom_sourcetext_parser.py
# Author: @Citizen0India
# Release Date: 2025.11.05
# Github Link: @Citizen0India

import os #file i/o
import re #regular expressions
import time 

        
class CustomSourcetextParser:
         
        text_chapverse_dict = {}
        text_chapverse_count = {}
        text_wordpairs_dict = {}
        text_wordpairs_count = {}
        
        # This parser function populates the data dictionaries from the custom source text and prints them into local directory files per custom alphabetical & unicode index order. Parser assumes all non-ascii letters in text are language-specific unicode.
        #The souce text formatting is expected as follows: Chapter-[Number] \n TEXT/TEXTS [Verse-Number or Verse-Number-Range] \n [Transliteration—Translation Word Pair;] [...] \n
                       

        def parse_source_text(self, sourcetext_filename, /): 
       
            source_text = open(sourcetext_filename,'rt', encoding = 'utf-8').read()

            total_word_count = 0
            total_verse_count = 0
            total_chap_count = 0
            chap_num = 1
            verse_num = 1
            chap_num_str = '1'
            verse_num_str = '1'
            text_unparsed = source_text
            ascii_letters = 'abcdefghijklmnopqrstuvwxyz'
            unicode_letters = ''
            while(text_unparsed != ''):
                    chap_loc = text_unparsed.rfind('Chapter-')
                    if (chap_loc != -1):
                        total_chap_count += 1
                        chap_num = (ord(text_unparsed[chap_loc+8]) - 48) # ascii to decimal
                        if (text_unparsed[chap_loc+9].isdigit()):
                            chap_num = chap_num*10 + (ord(text_unparsed[chap_loc+9]) - 48) # ascii to decimal
                        chap_num_str = '%d'%chap_num
                    else:
                        break #no more chapters in text
                            
                    chap_header = 'Chapter-%d' % chap_num                     
                    (text_unparsed, chap_separator, chap_text) = text_unparsed.rpartition(chap_header)
                    
                    while (chap_text != ''):
                         verse_loc = chap_text.rfind('TEXT') #verse header
                         
                         if (verse_loc != -1): # and verse_loc1 > verse_loc2):
                              if(chap_text[verse_loc+4] == 'S'): #'TEXTS 1-9' or 'TEXTS 1-10' or 'TEXTS 10-11'
                             
                          
                                  verse_num = (ord(chap_text[verse_loc+6]) - 48)
                                  
                                 # also check for '-' and successive verse numbers
                                  if (chap_text[verse_loc+7] == '-'):
                                      verse_num_to  = (ord(chap_text[verse_loc+8]) - 48)
                                      if (chap_text[verse_loc+9].isdigit()):
                                          verse_num_to = verse_num_to*10 + (ord(chap_text[verse_loc+9]) - 48)
                                  elif (chap_text[verse_loc+8] == '-'):
                                          verse_num = verse_num*10 + (ord(chap_text[verse_loc+7]) - 48)#ascii to decimal
                                          verse_num_to  = (ord(chap_text[verse_loc+9]) - 48)
                                          if (chap_text[verse_loc+10].isdigit()):
                                              verse_num_to = verse_num_to*10 + (ord(chap_text[verse_loc+10]) - 48)
                                  verse_header = 'TEXTS %d-%d' % (verse_num, verse_num_to)
                                  verse_num_str = '%d-%d' % (verse_num, verse_num_to)
                                  total_verse_count += verse_num_to - verse_num + 1                         
                              else:  #'TEXT''          
                                  verse_num = (ord(chap_text[verse_loc+5]) - 48) # ascii to decimal
                                  
                                  if (chap_text[verse_loc+6].isdigit()):
                                      verse_num = verse_num*10 + (ord(chap_text[verse_loc+6]) - 48) # ascii to decimal
                                  
                                  verse_header = 'TEXT %d' % verse_num
                                  verse_num_str = '%d' % verse_num
                                  total_verse_count += 1    
                                                                                           
                         (chap_text, verse_separator, verse_text) = chap_text.rpartition(verse_header)
                         
                      
                         while (verse_text != ''):
                                wordpair_separator = ';'
                                (wordpairs, wordpair_footer, verse_text) = verse_text.partition('.')
                                wordpairs += ';'
                                
                                word_num = 1
                                while (wordpairs != '' and wordpair_separator == ';'):
                                     (cur_wordpair, wordpair_separator, wordpairs) = wordpairs.partition(';')
                                     (transliteration, dash_separator, translation) = cur_wordpair.partition('—')
                                     if (dash_separator == '—'):
                                        transliteration = transliteration.lstrip().rstrip()
                                        translation = translation.lstrip().rstrip()

                                        for letters_ii in transliteration:
                                              if (letters_ii.isascii() == False):
                                                  if (letters_ii not in unicode_letters):
                                                      unicode_letters += letters_ii
                         
 
                                        index_key = transliteration + '♥' + translation
                                        index_ref = chap_num_str + '.' + verse_num_str
                                        chapverse_key = 'TEXT—' + index_ref
                                        if (self.text_wordpairs_dict.get(index_key) != None):
                                            if (index_ref not in self.text_wordpairs_dict[index_key]):
                                                self.text_wordpairs_dict[index_key] += ',' + index_ref
                                                self.text_wordpairs_count[index_key] += 1
                                        else:
                                            self.text_wordpairs_dict[index_key] = chapverse_key
                                            self.text_wordpairs_count[index_key] = 1
                                                                                       
                                        if (self.text_chapverse_dict.get(chapverse_key) != None):
                                                if (index_key not in self.text_chapverse_dict[chapverse_key]):
                                                    self.text_chapverse_dict[chapverse_key] += '♪' + index_key
                                                    self.text_chapverse_count[chapverse_key] += 1
                                        else:
                                            self.text_chapverse_dict[chapverse_key] = index_key
                                            self.text_chapverse_count[chapverse_key] = 1
                   
                                        word_num += 1    
                                        total_word_count += 1
  
         
                                                                                                                      
            # alphabetical dictionary index
            alphabetlist = ascii_letters + unicode_letters
           
            file_path = sourcetext_filename.rpartition('.')
            file_name = sourcetext_filename.rpartition('/')
            today = time.localtime()
            dir_name = file_path[0] + '-%d'%today.tm_year + '%d'%today.tm_mon + '%d'%today.tm_mday
            os.makedirs(dir_name, 511, True)
   
            alphabet_file_open = False
            dictionary_file = {}
            alphabet_count = {}
            for ii in alphabetlist:
                                                      dictionary_filename = dir_name + '/page-' + ii + '-' + file_name[2]
                                                      dictionary_file[dictionary_filename] = open(dictionary_filename,'w', encoding = 'utf-8')
                                                      dictionary_header = '\n%s\n [%s] Indexed Transliteration-Translation Chapter-Verse Page [%s]\n\n[chapter.verse] (number of repetitions)    transliteration    —    translation\n\n' % (file_name[2], alphabetlist, ii)
                                                      dictionary_file[dictionary_filename].write(dictionary_header)
                                                      alphabet_count[ii] = 0

            wordlist  = [(' ',' ',' ', 0)]
            for text_word in self.text_wordpairs_dict.keys():
                                             (transliteration, translation) = text_word.split('♥')
                                             wordlist.insert(len(wordlist), (transliteration, translation, self.text_wordpairs_dict[text_word], self.text_wordpairs_count[text_word]))
           
                                                   
            wordlist.sort()                        
            for word in wordlist:
                                              dictionary_entry = '[' + word[2] + ']' + '(*%d'% word[3] + ')          ' + word[0] + '    —    ' + word[1]+ '\n'
                                              alphabet_found = False
                                              for ii in alphabetlist:
                                                      if (word[0][0].startswith(ii) == True):
                                                           alphabet_found = True
                                                           dictionary_filename = dir_name + '/page-' + ii + '-' + file_name[2]
                                                           dictionary_file[dictionary_filename].write(dictionary_entry)
                                                           
                                                           alphabet_count[ii] += 1 
                                                      if (alphabet_found == True):
                                                          break
                                                          
                
            for ii in alphabetlist:
                                                                                                            dictionary_filename = dir_name + '/page-' + ii + '-' + file_name[2]
                                                                                                            dictionary_footer = '\n%s\n Number of unique transliterated-translated words beginning with [%s]:%d\n' % (file_name[2], ii,alphabet_count[ii])
                                                                                                            dictionary_file[dictionary_filename].write(dictionary_footer)
                                                                                                            dictionary_file[dictionary_filename].close()
                                                             
              
            print('STATUS: Done parsing source text: %s — \n Total chapters found: %d \n Total verses found: %d \n Total transliteration-translation wordpairs found: %d \n Total unique transliteration-translation wordpairs:%d \n Alphabetical Index [%s, %s] parsed in Python code by @Citizen0India \n' % (sourcetext_filename, total_chap_count,  total_verse_count, total_word_count, len(wordlist), ascii_letters,unicode_letters))

                                               
                                                
            
#def __main()__:

sourcetext = input ('Enter Source Text Name with Full File Path: \n')                        
st = CustomSourcetextParser()
st.parse_source_text(sourcetext)
#example: '/storage/emulated/0/Document/coding/Sanskrit-Project/bhagavadgitaasitis-wordlist.txt'