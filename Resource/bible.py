import pythonbible as bible

def searchVerse(searchText):
    #print(searchText)
    refText = bible.format_scripture_references(bible.get_references(searchText))
    #print ("refText",refText)
    refsText = refText.split(";")    
    #verse_ids = []
    references = bible.get_references(refText)
    #print("references",references)
    verse_ids = bible.convert_references_to_verse_ids(references)
    #print ("verse_ids",verse_ids)
    verse_text=""
    for ID in verse_ids:
        verse_text = verse_text + bible.format_scripture_references(bible.convert_verse_ids_to_references([ID])) + "\n" + bible.get_verse_text(ID, version=bible.Version.KING_JAMES)+"\n"
        #print ("ID",bible.format_scripture_references(bible.convert_verse_ids_to_references([ID])))
    formatted_reference = bible.format_scripture_references(references)
    return verse_text
text = "My favorite verses are Philippians 4:8, Isaiah 55:13, and Philippians 4:4-7."
print (searchVerse(text))