from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import main

Window.size = (450, 800)
VarAmount = 0
EqAmount = 0
TIs = []
EqAmountTI = TextInput(size_hint=(0.5, 1))
VarAmountTI = TextInput(size_hint=(0.5, 1))
LB = Label(size_hint=(None, None), height=1200, valign='top', width=400, markup=True)


class MyLayout(BoxLayout):
    def __init__(self):
        super(MyLayout, self).__init__()

        VarAmountBL = BoxLayout(size_hint= (None, None), height=30, width=300)
        VarAmountBL.add_widget(Label(text="Количество переменных:", width=200, valign='middle', halign='left'))
        VarAmountBL.add_widget(VarAmountTI)
        self.add_widget(VarAmountBL)

        EqAmountBL = BoxLayout(size_hint= (None, None), height=30, width=300)
        EqAmountBL.add_widget(Label(text="Количество уравнений:", valign='middle', halign='left'))
        EqAmountBL.add_widget(EqAmountTI)
        self.add_widget(EqAmountBL)

        self.submit = Button(text="Ввод коэффициентов", size_hint=(None, None), width=170, height=30)
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)
        SW = ScrollView(effect_cls = 'ScrollEffect')
        SW.add_widget(LB)
        self.add_widget(SW)

    def press(self, instance):
        main.EqAmount = int(EqAmountTI.text)
        main.VarAmount = int(VarAmountTI.text)
        for i in range (EqAmount+1):
            self.bo = BoxLayout(size_hint=(None, None), height=30, width=350)
            self.add_widget(self.bo, i+1)
            for j in range (VarAmount+1):
                TI = TextInput(size_hint=(None, None), height=30, width=40)
                main.TIs.append(TI)
                self.bo.add_widget(TI)
        self.add_widget(Button(text='Вычислить', on_press = Calculating, size_hint=(None, None), width=170, height=30), 1)


def Calculating(a):

    # Определение размеров
    m = VarAmount
    n = EqAmount

    # Создание списка nxm
    A = [0] * (n + 1)
    for i in range(n + 1):
        A[i] = [0] * (m + 1)

    # Ввод переменных

    for i in range(n+1):
        for j in range(m+1):
            A[i][j] = float(TIs[i*(m+1)+j].text)
    A.reverse()

    BasisVars = []
    for i in range(m-n+1, m+1):
        BasisVars.append(i)

    itnum = 0
    isOptimal = False
    while isOptimal != True:
        LB.text+= "Итерация №{}\n".format(itnum)

        BiIsPos = True
        for i in range(n):
            if A[i][m] < 0:
                BiIsPos = False

        CjIsPos = True
        for j in range(m+1):
            if A[n][j] < 0:
                CjIsPos = False

        rCol = 0
        rRow = 0
        rEl = 0
        if BiIsPos == True and CjIsPos == False: # ОСНОВНОЙ СИМПЛЕКС-МЕТОД
            maxEl = 0
            for j in range(m):
                if A[n][j] < 0 and abs(A[n][j]) > maxEl:
                    maxEl = abs(A[n][j])
                    rCol = j

            minEl = 1000
            for i in range(n):
                if A[i][rCol] > 0 and (A[i][m] / A[i][rCol]) < minEl:
                    minEl = A[i][m] / A[i][rCol]
                    rRow = i

            rEl = A[rRow][rCol]


        elif CjIsPos == True and BiIsPos == False: # ДВОЙСТВЕННЫЙ СИМПЛЕКС-МЕТОД
            maxEl = 0
            for i in range(n):
                if A[i][m] < 0 and abs(A[i][m]) > maxEl:
                    maxEl = abs(A[i][m])
                    rRow = i

            minEl = 1000
            for j in range(m):
                if A[rRow][j] < 0 and abs(A[n][j] / A[rRow][j]) < minEl:
                    minEl = abs(A[n][j] / A[rRow][j])
                    rCol = j

            rEl = A[rRow][rCol]

        elif CjIsPos == False and BiIsPos == False: # СМЕШАННЫЙ СИМПЛЕКС-МЕТОД
            maxEl = 0
            for j in range(m):
                if A[n][j] < 0 and abs(A[n][j]) > maxEl:
                    maxEl = abs(A[n][j])
                    rCol = j

            minEl = 1000
            for i in range(n):
                if A[i][rCol] > 0 and A[i][m] >= 0 and (A[i][m] / A[i][rCol]) < minEl:
                    minEl = A[i][m] / A[i][rCol]
                    rRow = i

            rEl = A[rRow][rCol]

        else:
            return

        BasisVars[rRow] = rCol+1
        for i in range(n + 1):
            for j in range(m + 1):
                if i == rRow and j == rCol:
                    LB.text += ("[color=#ff0000]{0:<7.2f}[/color]".format(A[i][j]))
                else:
                    LB.text += ("{0:<7.2f}".format(A[i][j]))
            LB.text += "\n"
        LB.text += "\n\n"

        NewA = [None] * (n + 1)
        for i in range(n + 1):
            NewA[i] = [None] * (m + 1)

        for i in range(n + 1):
            if i != rRow:
                NewA[i][rCol] = 0

        for j in range(m + 1):
            NewA[rRow][j] = A[rRow][j] / rEl

        for i in range(n + 1):
            if A[i][rCol] == 0:
                for j in range(m + 1):
                    NewA[i][j] = A[i][j]


        for i in range(n + 1):
            for j in range(m + 1):
                if NewA[i][j] == None:
                    if i == (n) and j == (m):
                        NewA[i][j] = A[i][j] + A[i][rCol] * NewA[rRow][j]
                    else:
                        NewA[i][j] = A[i][j] - A[i][rCol] * NewA[rRow][j]

        isOptimal = True
        for i in range(n):
            if NewA[i][m] < 0:
                isOptimal = False
        for j in range(m):
            if NewA[n][j] < 0:
                isOptimal = False

        for i in range(n + 1):
            for j in range(m + 1):
                A[i][j] = NewA[i][j]
        LB.text +="\n"
        itnum+=1

    LB.text += "Итерация №{}\n".format(itnum)
    for i in range(n + 1):
        for j in range(m + 1):
            LB.text += ("{0:<7.2f} ".format(NewA[i][j]))
        LB.text += "\n"
    LB.text +="\n"
    for i in range(n):
        LB.text += ("X{}={:.2f}\n".format(BasisVars[i], NewA[i][m]))
    LB.text += "F={}\n".format(NewA[n][m])




class SimplexApp(App):

    def build(self):
        return MyLayout() #Builder.load_file('SimplexApp.kv')

    def texting(self):
        main.VarAmount = int(self.root.ids.VarAmount.text)
        print(main.VarAmount)
        main.EqAmount = int(self.root.ids.EqAmount.text)
        print(main.EqAmount)

    def Calc(self):
        Calculating()

SimplexApp().run()

