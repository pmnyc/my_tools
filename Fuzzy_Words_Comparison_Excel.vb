''''''''''''''''''''''''''''''''''''
''' @author pm
''' Column A is Wrong Name, Column B is Suggest Name, Column C is Reference Name
''' Cell I1 shows the similarity threshold for determining whether to show suggested name or not
''' WgtOfLen is the variable for adjusting the weight of difference between two name lengths
''''''''''''''''''''''''''''''''''''
''' Create a function to calculate similarity
''''''''''''''''''''''''''''''''''''
Dim NumOfMatches   As Integer
Dim CharIndex As Integer
Dim N As Long
Dim K As Long
Dim NewString As String
Dim NewMyString As String
Dim MyFixString As String
Dim MyTestString As String
Dim WgtOfLen As Double

Public Function FUZCOMPARE(MyString1 As String, MyString2 As String) As Single  'MyString1 is assumed to be the correct word

''''''''''''''''''''''''''''''''''''''''''''
WgtOfLen = 0.1
''''''''' This 0.1 is set to be the weight (though used as the power) of the difference of two string lengths for calculating similarity
''''''''''''''''''''''''''''''''''''''''''''''

Dim TempCount As Integer
TempCount = 0
''' Split into three pieces
For K = 1 To WorksheetFunction.Min(10, WorksheetFunction.RoundUp(WorksheetFunction.Max(1, Len(MyString2)) / 4, 0))
NumOfMatches = 0
MyFixString = Mid(UCase(Trim(MyString1)), 4 * K - 5 + 2 * (0 ^ (K - 1)), 8 - 2 * (0 ^ (K - 1)))
MyTestString = Mid(UCase(Trim(MyString2)), 4 * K - 3, 4)

   For N = 1 To 2 ^ Len(MyTestString)
   NewString = ""
     For CharIndex = 1 To Len(MyTestString)
       If (2 ^ CharIndex) And (2 * N) Then NewString = NewString & Mid(MyTestString, CharIndex, 1)
     Next CharIndex
  
   If NumOfMatches >= Len(NewString) Then
   NumOfMatches = NumOfMatches
   Else
      For J = 1 To Len(NewString)
        If J = 1 Then
        NewMyString = "*" & Mid(NewString, J, 1) & "*"
        Else
        NewMyString = NewMyString & Mid(NewString, J, 1) & "*"
        End If
      Next J

      If MyFixString Like NewMyString Then NumOfMatches = WorksheetFunction.Max(NumOfMatches, Len(Trim(NewString)))
    End If
    Next N

TempCount = NumOfMatches + TempCount
Next K

NumOfMatches = TempCount

MyFixString = UCase(Trim(MyString1))
MyTestString = UCase(Trim(MyString2))

FUZCOMPARE = ((Len(MyFixString) - Abs(Len(MyFixString) - Len(MyTestString))) / Len(MyFixString)) * WgtOfLen + (1 - WgtOfLen) * (NumOfMatches / WorksheetFunction.Max(2,WorksheetFunction.Min(Len(MyTestString), Len(MyFixString))))
''This fuzcompare only compares first 40 characters.

End Function

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Sub MatchNames()

NumOfTestNames = Range(Range("A2"), Range("A2").End(xlDown)).Rows.Count
NumOfRefNames = Range(Range("C2"), Range("C2").End(xlDown)).Rows.Count

For J = 1 To NumOfRefNames
TempRange = "E" & J + 1
Range(TempRange).FormulaR1C1 = "=RC[-2]"
Next J

For I = 1 To NumOfTestNames
For J = 1 To NumOfRefNames
TempRange = "D" & J + 1

 ''' If the lengths of two words compared are differ by over 3, then not run comparison
 '''' If Two cells don't have the same number of Blanks, then don't do the comparison
If Abs(Len(Range(("C" & (J + 1)))) - Len(Range(("A" & (I + 1))))) <= 3 And _
(Len(Range(("C" & (J + 1)))) - Len(WorksheetFunction.Substitute(Range(("C" & (J + 1))), " ", ""))) = (Len(Range(("A" & (I + 1)))) - Len(WorksheetFunction.Substitute(Range(("A" & (I + 1))), " ", ""))) _
Then

Range(TempRange).FormulaR1C1 = "=If(mid(RC[-1],1,1) <> mid(R" & I + 1 & "C[-3],1,1),0,IF(ISERROR(FUZCOMPARE(RC[-1],R" & I + 1 & "C[-3])" & "),0,FUZCOMPARE(RC[-1],R" & I + 1 & "C[-3])))"

Else
Range(TempRange).FormulaR1C1 = 0
End If

Next J
TempRange = "F" & I + 1

Range(TempRange).FormulaR1C1 = "=IF(MAX(R2C[-2]:R" & NumOfRefNames + 1 & "C[-2]) < " & Range("I1") & ",""" & """,VLOOKUP(MAX(R2C[-2]:R" & NumOfRefNames + 1 & "C[-2]),R2C[-2]:R" & NumOfRefNames + 1 & "C[-1],2,0))"
    'If the similarity is less than 70%, then do not suggest a name

Range(TempRange).Select
Selection.Copy
TempRange = "B" & I + 1
Range(TempRange).Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False

Range(("F" & I + 1)).FormulaR1C1 = ""
Next I

Columns("D:E").Select
Selection.ClearContents
Range("A1").Select
End Sub