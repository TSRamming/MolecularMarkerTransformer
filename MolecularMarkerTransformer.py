import xml.etree.ElementTree as ET
import openpyxl


def build_string_from_treelist(treelist, result, indentation="", group=None):
    filtered_treelist = (value for value in treelist if value[2] == group)
    for treelist_item in filtered_treelist:
        result.append(indentation + treelist_item[0])
        build_string_from_treelist(treelist, result, "    " + indentation, treelist_item[1])


def generate_textfile_hierarchy(df):
    values = []
    for row in df.iter_rows(2, df.max_row):
        name = row[0].value
        symbol = row[1].value
        symbol_is_hgnc = row[2].value == 'ja'
        in_group = row[4].value

        text = name + (" [" + symbol + "]" if symbol_is_hgnc else "")
        values.append((text, name, in_group))
    values.sort(key=(lambda x: x[0].lower()))

    result = []
    build_string_from_treelist(values, result)

    with open('visualization.txt', 'w') as cFile:
        cFile.write("\n".join(result))


def generate_xml_studystar(df):
    # build import file for studystar
    # use an onkostar export xml as shell for entries
    with open('osexport.osc', 'r') as cFile:
        tree = ET.parse(cFile)

    root = tree.getroot()
    e = tree.findall('.//Versions/Version/Entries')
    for item in e:
        entries = item.findall('Entry')
        for entry in entries:
            item.remove(entry)

    for row in df.iter_rows(2, df.max_row):
        for entries in e:
            entry = ET.SubElement(entries, "Entry")
            ET.SubElement(entry, "Code").text = row[0].value
            ET.SubElement(entry, "ShortDescription").text = row[0].value
            ET.SubElement(entry, "Description").text = row[0].value
            ET.SubElement(entry, "Synonyms").text = row[3].value
            ET.SubElement(entry, "Note").text = row[7].value
            ET.SubElement(entry, "Position").text = ""
            ET.SubElement(entry, "ParentCode").text = row[4].value

    ET.indent(tree, space="   ", level=0)
    with open('import_file_molMarker_Studystar.osc', 'wb') as cFile:
        tree.write(cFile)


def generate_xlsx_gravity (df):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["eingang", "eingangDesc", "ausgang", "ausgangDesc", "bemerkung", "systeme", "markieren", "markierungshinweis"])
    for row in df.iter_rows(2, df.max_row):
        rowdata = [row[0].value, "", row[1].value, "", "", "", "0", ""]
        ws.append(rowdata);
    wb.save('gravity.xlsx')


def main():
    # get data from excel file
    workbook = openpyxl.load_workbook("MolMarker_Kategorisiert.xlsx")
    worksheet = workbook.active

    generate_textfile_hierarchy(worksheet)
    generate_xml_studystar(worksheet)
    generate_xlsx_gravity (worksheet)


if __name__ == "__main__":
    main()
