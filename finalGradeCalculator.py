def calcGrade():
  sg=float(input("Semester Grade: "))
  tg=float(input("Desired True Grade: "))
  fg=(10*(float(tg)-(0.9*float(sg))))
  print("Required Final Grade: " + str(fg))
  if input("Press 'Enter' to exit, or press any other key to try another score.\n") == "":
      pass
  else:
    print("")
    calcGrade()
calcGrade()
