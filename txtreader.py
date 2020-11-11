import numpy as np

def filereader(filename):
    count = 0
    CL = 0
    ylst = []
    chord = []
    Ai = []
    Cl = []
    ICd = []
    Cm = []

    f = open(filename, 'r')
    for lines in f.readlines():
        count+=1
        words = lines.split(" ")
        for i in range(len(words)):
           if '' in words:
               words.remove('')
        if words[0] == 'CL':
           
            word = words[2].replace("\n","")
            
            CL = float(word)

        elif count>59:
            break
        elif count <22:
            pass
        elif float(words[0])>0:
            ylst.append(float(words[0]))
            chord.append(float(words[1]))
            Ai.append(float(words[2]))
            Cl.append(float(words[3]))
            ICd.append(float(words[5]))
            Cm.append(float(words[7]))
    y_array = np.array(ylst)
    chord_array = np.array(chord)
    Ai_array = np.array(Ai)
    Cl_array = np.array(Cl)
    ICd_array = np.array(ICd)
    Cm_array = np.array(Cm)
    f.close()
    return(y_array,chord_array,Ai_array,Cl_array,ICd_array,Cm_array,CL)


