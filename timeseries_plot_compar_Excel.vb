Sub Plot_Volume()
' Macro for automating plots by pm

    Sheets("SourceData").Select

    Dim LastDataRow As Long
    Dim StartRow As Long
    Dim pointer As Long
    Dim FirstRow As Long
    Dim LastRow As Long
    Dim TotalRows As Long
    Dim TotalIter As Long

    Dim i As Long

    TotalRows = Range(Range("A2"), Range("A2").End(xlDown)).Rows.Count
    TotalIter = Cells(TotalRows + 1, 12).Value
    LastRow = 1 'set initial last row to be first row

    For i = 1 To TotalIter
        Sheets("SourceData").Select
        FirstRow = LastRow + 1
            For j = FirstRow To TotalRows
                If Range("L" & j).Value = i Then
                  LastRow = j
                Else
                  Exit For
                End If
                Next j
        Range("C1:G1,C" & FirstRow & ":G" & LastRow).Select
        Charts.Add
        ActiveChart.ChartType = xlLineMarkers
        ActiveChart.SetSourceData
Source:=Sheets("SourceData").Range("C1:G1,C" & FirstRow & ":G" &
LastRow), PlotBy:=xlColumns
        ActiveChart.Location Where:=xlLocationAsObject, Name:="SourceData"
        ActiveChart.Location Where:=xlLocationAsNewSheet
        ActiveChart.Move After:=Sheets(Sheets.Count)
        ActiveChart.SeriesCollection(2).Select
        ActiveChart.PlotArea.Select
        ActiveChart.SeriesCollection(1).Delete
        ActiveChart.SeriesCollection(1).Delete
        ActiveChart.Legend.Select
        Selection.Position = xlBottom
        ActiveChart.Axes(xlCategory).Select
        With ActiveChart.Axes(xlCategory)
            .CrossesAt = 1
            .TickLabelSpacing = 6
            .TickMarkSpacing = 1
            .AxisBetweenCategories = True
            .ReversePlotOrder = False
        End With
        With Selection.TickLabels
            .Alignment = xlCenter
            .Offset = 100
            .ReadingOrder = xlContext
            .Orientation = xlUpward
        End With

            ActiveChart.SeriesCollection(1).Select
    With Selection.Border
        .ColorIndex = 5
        .Weight = xlThin
        .LineStyle = xlContinuous
    End With
    With Selection
        .MarkerBackgroundColorIndex = 5
        .MarkerForegroundColorIndex = 5
        .MarkerStyle = xlDiamond
        .Smooth = False
        .MarkerSize = 5
        .Shadow = False
    End With
    ActiveChart.SeriesCollection(2).Select
    With Selection.Border
        .ColorIndex = 7
        .Weight = xlThin
        .LineStyle = xlContinuous
    End With
    With Selection
        .MarkerBackgroundColorIndex = 7
        .MarkerForegroundColorIndex = 7
        .MarkerStyle = xlDiamond
        .Smooth = False
        .MarkerSize = 5
        .Shadow = False
    End With

    ActiveChart.ChartArea.Select
    ActiveChart.PlotArea.Select
    With Selection.Interior
        .ColorIndex = 15
        .PatternColorIndex = 1
        .Pattern = xlSolid
    End With
    With Selection.Border
        .ColorIndex = 57
        .Weight = xlThin
        .LineStyle = xlContinuous
    End With
    Selection.Interior.ColorIndex = xlNone

        ActiveSheet.Name = Left(Replace(Sheets("SourceData").Range("A"
& FirstRow).Value & "_" & Sheets("SourceData").Range("B" &
FirstRow).Value, "/", "_"), 30)
    Next i

    Sheets("SourceData").Select
End Sub