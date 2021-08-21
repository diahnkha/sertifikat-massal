$documents_path = '.'

$word_app = New-Object -ComObject Word.Application

# This filter will find .doc as well as .docx documents
Get-ChildItem -Path $documents_path -Filter *.doc? | ForEach-Object {

    $document = $word_app.Documents.Open($_.FullName, $false, $true)

    $pdf_filename = "$($_.DirectoryName)\$($_.BaseName).pdf"

    $document.SaveAs([ref] $pdf_filename, [ref] 17)

    $document.Close($false)
}

#Close Word
[gc]::Collect()
[gc]::WaitForPendingFinalizers()
$word_app.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word_app)

#Cleanup
Remove-Variable word_app

Get-ChildItem *.docx | foreach { Remove-Item -Path $_.FullName }