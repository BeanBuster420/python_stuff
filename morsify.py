morse_code = {
"A" : ".-", 
"B" : "-...", 
"C" : "-.-.", 
"D" : "-..", 
"E" : ".", 
"F" : "..-.", 
"G" : "--.", 
"H" : "....", 
"I" : "..", 
"J" : ".---", 
"K" : "-.-", 
"L" : ".-..", 
"M" : "--", 
"N" : "-.", 
"O" : "---", 
"P" : ".--.", 
"Q" : "--.-", 
"R" : ".-.", 
"S" : "...", 
"T" : "-", 
"U" : "..-", 
"V" : "...-", 
"W" : ".--", 
"X" : "-..-", 
"Y" : "-.--", 
"Z" : "--..", 
"0" : "-----", 
"1" : ".----", 
"2" : "..---", 
"3" : "...--", 
"4" : "....-", 
"5" : ".....", 
"6" : "-....", 
"7" : "--...", 
"8" : "---..", 
"9" : "----.", 
"." : ".-.-.-", 
"," : "--..--",
" " : ""        
}

def morsify(string):
  string = string.upper()
  morse_string = ""
  for x in string:
    morse_string = morse_string + str(morse_code[x]) + " "
  return morse_string
  
print morsify(input("morsify: "))
