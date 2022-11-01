from pickle import NONE

import pythonbible as bible


def searchVerse(searchText,versionPass="nkj"): #if variable is defined then it is set to a default paramiter. 
    versionPass= versionPass.lower()
    #print(searchText)
    refText = bible.format_scripture_references(bible.get_references(searchText))
    #print ("refText",refText)
    #refsText = refText.split(";")    
    #verse_ids = []
    references = bible.get_references(refText)
    #print("references",references)
    verse_ids = bible.convert_references_to_verse_ids(references)
    #print ("verse_ids",verse_ids)
    verse_text=""
    version=bible.Version.KING_JAMES
    if "amp" in versionPass.lower():
        print ("AMPLIFIED Selected")
        #version=bible.Version.AMPLIFIED #error with this version for now
    elif "asv" in versionPass.lower():
        print ("American Standard Selected")
        version=bible.Version.AMERICAN_STANDARD
    for ID in verse_ids:
        verse_text = verse_text + bible.format_scripture_references(bible.convert_verse_ids_to_references([ID])) + "\n" + bible.get_verse_text(ID,version)+"\n"
        #print ("ID",bible.format_scripture_references(bible.convert_verse_ids_to_references([ID])))
    formatted_reference = bible.format_scripture_references(references)
    if verse_text =="":
        verse_text = "404"
    return verse_text
text = "My favorite verses are Philippians 4:8"#, Isaiah 55:13, and Philippians 4:4-7."
output=searchVerse(text,"asv")
print (output)
if output=="404":
    print ("404 true")
