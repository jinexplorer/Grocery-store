import wx


class TextFrame (wx.Frame):
    def __init__(self):
        # 设置基本属性外观框
        wx.Frame.__init__ (self, None, -1, 'DES加密和解密', size=(655, 220))
        panel = wx.Panel (self, -1, )

        # 设置输入框
        self.plainLable = wx.StaticText (panel, -1, "明文:")
        self.plainText = wx.TextCtrl (panel, -1, "", size=(600, -1))
        self.plainText.SetToolTip (wx.ToolTip ("请输入64位明文"))
        self.plainText.SetInsertionPoint (0)
        self.keyLable = wx.StaticText (panel, -1, "密钥:")
        self.keyText = wx.TextCtrl (panel, -1, "", size=(600, -1))
        self.keyText.SetToolTip (wx.ToolTip ("请输入64位密钥"))
        self.cipherLabel = wx.StaticText (panel, -1, "密文:")
        self.cipherText = wx.TextCtrl (panel, -1, "", size=(600, -1))
        self.cipherText.SetToolTip (wx.ToolTip ("请输入64位密文"))
        sizer = wx.FlexGridSizer (cols=2, hgap=6, vgap=6)
        sizer.AddMany (
            [ self.plainLable, self.plainText, self.keyLable, self.keyText, self.cipherLabel, self.cipherText ])
        panel.SetSizer (sizer)

        # 设置按钮
        self.button = wx.Button (panel, -1, "加密", size=(300, 50), pos=(30, 100))
        self.button.SetToolTip (wx.ToolTip ("开始加密"))
        self.Bind (wx.EVT_BUTTON, self.OnClick, self.button)
        self.button2 = wx.Button (panel, -1, "解密", size=(300, 50), pos=(334, 100))
        self.button2.SetToolTip (wx.ToolTip ("开始解密"))
        self.Bind (wx.EVT_BUTTON, self.OnClick2, self.button2)
        self.warningLable = wx.StaticText (panel, -1, "tips:都要输入64位二进制哦",pos=(30,160),)
        self.warningLable.SetForegroundColour("#ff0000")

    # 加密按钮被点击时
    def OnClick(self, event):
        plainText = ''.join (self.plainText.GetValue ().split ())
        key = ''.join (self.keyText.GetValue ().split ())
        if len(plainText)!=64 or len(key)!=64:
            self.warningLable.SetLabel("warnning:请将明文/密钥输入为64位二进制")
        else:
            if self.isbinary(plainText) and self.isbinary(key):
                self.warningLable.SetLabel ("")
                des = Des (plainText, key, "")
                des.encrypt()
                self.cipherText.SetValue (des.cipherText)
            else:
                self.warningLable.SetLabel ("warnning:请将明文/密钥输入为64位二进制")

    # 解密按钮被点击时
    def OnClick2(self, event):
        cipherText = ''.join (self.cipherText.GetValue ().split ())
        key = ''.join (self.keyText.GetValue ().split ())
        if len(cipherText)!=64 or len(key)!=64:
            self.warningLable.SetLabel ("warnning:请将密文/密钥输入为64位二进制")
        else:
            if self.isbinary (cipherText) and self.isbinary (key):
                self.warningLable.SetLabel ("")
                des = Des ("", key, cipherText)
                des.decrypt()
                self.plainText.SetValue (des.plainText)
            else:
                self.warningLable.SetLabel ("warnning:请将明文/密钥输入为64位二进制")

    def isbinary(self,a):
        ret=True
        for i in a:
            if i=='0' or i =='1':
                pass
            else:
                ret=False
        return ret


class Des ():

    def __init__(self, plainText, key, cipherText):
        self.plainText = plainText
        self.key = key
        self.cipherText = cipherText
        self.sonkey = [ ]
        self.substitution1 = [
            [ 57, 49, 41, 33, 25, 17, 9,
              1, 58, 50, 42, 34, 26, 18,
              10, 2, 59, 51, 43, 35, 27,
              19, 11, 3, 60, 52, 44, 36 ],
            [ 63, 55, 47, 39, 31, 23, 15,
              7, 62, 54, 46, 38, 30, 22,
              14, 6, 61, 53, 45, 37, 29,
              21, 13, 5, 28, 20, 12, 4 ] ]
        self.substitution2 = [
            14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32
        ]
        self.substitutionIP = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]
        self.substitutionIP_1 = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
        ]
        self.substitutionP = [
            16, 7, 20, 21,
            29, 12, 28, 17,
            1, 15, 23, 26,
            5, 18, 31, 10,
            2, 8, 24, 14,
            32, 27, 3, 9,
            19, 13, 30, 6,
            22, 11, 4, 25
        ]
        self.S = [
            [
                [ 14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7 ],
                [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8 ],
                [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0 ],
                [ 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ] ],
            [
                [ 15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10 ],
                [ 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5 ],
                [ 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15 ],
                [ 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ] ],

            [
                [ 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8 ],
                [ 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1 ],
                [ 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7 ],
                [ 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ] ],
            [
                [ 7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15 ],
                [ 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9 ],
                [ 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4 ],
                [ 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 ] ],
            [
                [ 2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9 ],
                [ 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6 ],
                [ 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14 ],
                [ 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ] ],
            [
                [ 12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11 ],
                [ 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8 ],
                [ 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6 ],
                [ 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 ] ],

            [
                [ 4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1 ],
                [ 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6 ],
                [ 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2 ],
                [ 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 ] ],
            [
                [ 13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7 ],
                [ 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2 ],
                [ 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8 ],
                [ 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11 ] ]
        ]

        self.circularLeftShift = [ 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1 ]
        self.selectE = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        ]
        self.getSonKey ()

    def xor(self,a, b):
        ret = ""
        for i in range (len (a)):
            ret += str ((int (a[ i ]) + int (b[ i ])) % 2)
        return ret

    def substitutionSelect1(self, key):
        a = ""
        b = ""
        for i in self.substitution1[ 0 ]:
            a += key[ i - 1 ]
        for i in self.substitution1[ 1 ]:
            b += key[ i - 1 ]
        return a, b

    def substitutionSelect2(self, key):
        a = ""
        for i in self.substitution2:
            a += key[ i - 1 ]
        return a

    def getSonKey(self):
        C, D = self.substitutionSelect1 (self.key)
        for i in range (0, 16):
            C = C[ self.circularLeftShift[ i ]: ] + C[ :self.circularLeftShift[ i ] ]
            D = D[ self.circularLeftShift[ i ]: ] + D[ :self.circularLeftShift[ i ] ]
            K = self.substitutionSelect2 (C + D)
            self.sonkey.append (K)

    def initialSubstitutionIP(self, key):
        a = ""
        for i in self.substitutionIP:
            a += key[ i - 1 ]
        return a[ :32 ], a[ 32: ]

    def initialSubstitutionIP_1(self, key):
        a = ""
        for i in self.substitutionIP_1:
            a += key[ i-1]
        return a

    def selectCompute(self, key):
        a = ""
        for i in range (48):
            a += key[ self.selectE[i]-1 ]
        return a

    def sx(self, i, key):
        row = int (key[ 0 ] + key[ -1 ], 2)
        col = int(key[ 1:5 ],2)
        ret = self.S[ i ][ row ][ col ]
        return bin (ret)[ 2: ].zfill (4)

    def substitutionComputeP(self, key):
        a = ""
        for i in self.substitutionP:
            a += key[ i - 1 ]
        return a

    def F(self, key, A):
        A = self.selectCompute (A)
        B = self.xor (A, key)
        C = ""
        for i in range (8):
            C += self.sx (i, B[ 6 * i:6 * i + 6 ])
        return self.substitutionComputeP (C)

    def encrypt(self):
        L, R = self.initialSubstitutionIP (self.plainText)
        for i in range (16):
            L,R = R, self.xor (self.F (self.sonkey[ i ], R), L)
        self.cipherText = self.initialSubstitutionIP_1 (R + L)
    def decrypt(self):
        L, R = self.initialSubstitutionIP (self.cipherText)
        for i in range (16):
            L,R = R, self.xor (self.F (self.sonkey[ 15-i ], R), L)
        self.plainText = self.initialSubstitutionIP_1 (R + L)


if __name__ == '__main__':
    app = wx.App ()
    frame = TextFrame ()
    frame.Show ()
    app.MainLoop ()
