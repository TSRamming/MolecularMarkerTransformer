import xml.etree.ElementTree as ET
import openpyxl
import json


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
        values.append((text, symbol, in_group))
    values.sort(key=(lambda x: x[0].lower()))

    result = []
    build_string_from_treelist(values, result)

    with open('visualization.txt', 'w') as cFile:
        cFile.write("\n".join(result))


def generate_xml_studystar(df, genelist):
    # build import file for studystar
    # use an onkostar export xml as shell for entries
    with open('osexport.osc', 'r') as cFile:
        tree = ET.parse(cFile)

    e = tree.findall('.//Versions/Version/Entries')
    for item in e:
        entries = item.findall('Entry')
        for entry in entries:
            item.remove(entry)

    for row in df.iter_rows(2, df.max_row):
        description = row[0].value
        code = row[1].value
        code_is_hgnc = row[2].value == 'ja'
        custom_synonyms = row[3].value
        parent_group = row[4].value
        comment = row[7].value

        for entries in e:
            # find synonyms in hgnc-code and hgnc aliases
            synonyms_list = []
            if row[3].value is not None:
                synonyms_list = custom_synonyms.split(",")
            if code_is_hgnc:
                synonyms_list.append(code)
                hgnc_synonyms = (list(value.get("alias_symbol", []) for value in genelist if value["symbol"] == code))
                if len(hgnc_synonyms) > 0:
                    synonyms_list.extend(hgnc_synonyms[0])
            synonyms = ""
            if len(synonyms_list) > 0:
                # convert to set to remove duplicates
                synonyms = ",".join(sorted(set(synonyms_list), key=lambda x: x.lower()))
            # add new node
            entry = ET.SubElement(entries, "Entry")
            ET.SubElement(entry, "Code").text = code
            ET.SubElement(entry, "ShortDescription").text = description
            ET.SubElement(entry, "Description").text = description
            ET.SubElement(entry, "Synonyms").text = synonyms
            ET.SubElement(entry, "Note").text = comment
            ET.SubElement(entry, "Position").text = ""
            ET.SubElement(entry, "ParentCode").text = parent_group

    ET.indent(tree, space="   ", level=0)
    with open('import_file_molMarker_Studystar.osc', 'wb') as cFile:
        tree.write(cFile)


def generate_xlsx_gravity(df):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(
        ["eingang", "eingangDesc", "ausgang", "ausgangDesc", "bemerkung", "systeme", "markieren", "markierungshinweis"]
    )
    for row in df.iter_rows(2, df.max_row):
        name = row[0].value
        code = row[1].value
        rowdata = [name, "", code, "", "", "", "0", ""]
        ws.append(rowdata)
    wb.save('gravity.xlsx')


def main():
    # get data from Excel file
    workbook = openpyxl.load_workbook("MolMarker_Kategorisiert.xlsx")
    worksheet = workbook.active

    # get data from hgnc json
    with open('hgnc_complete_set.json', 'r', encoding="UTF8") as file:
        hgnc = json.load(file)
    genelist = hgnc["response"]["docs"]

    generate_textfile_hierarchy(worksheet)
    generate_xml_studystar(worksheet, genelist)
    generate_xlsx_gravity(worksheet)


if __name__ == "__main__":
    main()
