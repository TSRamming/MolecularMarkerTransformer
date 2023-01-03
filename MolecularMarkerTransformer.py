import xml.etree.ElementTree as ET
import openpyxl
import json


def build_string_from_treelist(treelist, result, indentation="", group=None):
    filtered_treelist = (value for value in treelist if value[2] == group)
    for treelist_item in filtered_treelist:
        result.append(indentation + treelist_item[0])
        build_string_from_treelist(treelist, result, "    " + indentation, treelist_item[1])


def generate_textfile_hierarchy(spec_entries, filename):
    values = []
    for spec_entry in spec_entries:
        synonyms = ", ".join(sorted(spec_entry["Synonyms"]))
        text = spec_entry["DisplayName"]
        additional_info = (spec_entry["Code"] if spec_entry["IsHGNC"] else "na") +\
            (" / " + synonyms if synonyms != "" else "")
        if additional_info != "na":
            text += " [" + additional_info + "]"
        values.append((text, spec_entry["Code"], spec_entry["InGroup"]))
    values.sort(key=(lambda x: x[0].lower()))

    result = []
    build_string_from_treelist(values, result)

    with open(filename, 'w', encoding="utf-8") as cFile:
        cFile.write("\n".join(result))


def generate_xml_studystar(spec_entries, filename):
    # build import file for studystar
    # use an onkostar export xml as shell for entries
    with open('osexport.osc', 'r') as cFile:
        tree = ET.parse(cFile)

    entries = tree.findall('.//Versions/Version/Entries')
    for entry in entries:
        items = entry.findall('Entry')
        for item in items:
            entry.remove(item)

    for spec_entry in spec_entries:
        for entry in entries:
            # add new node
            items = ET.SubElement(entry, "Entry")
            ET.SubElement(items, "Code").text = spec_entry["Code"]
            ET.SubElement(items, "ShortDescription").text = spec_entry["DisplayName"]
            ET.SubElement(items, "Description").text = spec_entry["DisplayName"]
            ET.SubElement(items, "Synonyms").text = ",".join(spec_entry["Synonyms"])
            ET.SubElement(items, "Note").text = spec_entry["Comment"]
            ET.SubElement(items, "Position").text = ""
            ET.SubElement(items, "ParentCode").text = spec_entry["InGroup"]
    ET.indent(tree, space="   ", level=0)
    with open(filename, 'wb') as cFile:
        tree.write(cFile)


def generate_xlsx_gravity(spec_entries, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(
        ["eingang", "eingangDesc", "ausgang", "ausgangDesc", "bemerkung", "systeme", "markieren", "markierungshinweis"]
    )
    for spec_entry in spec_entries:
        rowdata = [spec_entry["DisplayName"], "", spec_entry["Code"], "", "", "", "0", ""]
        ws.append(rowdata)
    wb.save(filename)


def get_spec_from_worksheet(worksheet):
    entries = []
    for row in worksheet.iter_rows(2, worksheet.max_row):
        synonyms = set()
        if row[3].value:
            synonyms.update({item.strip() for item in row[3].value.split(",")})
        entry = {
            "DisplayName": row[0].value,
            "Code": row[1].value,
            "IsHGNC": row[2].value == "ja",
            "Synonyms": synonyms,
            "InGroup": row[4].value,
            "Comment": row[7].value
        }
        entries.append(entry)
    return entries


def add_synonyms_from_hgnc(spec_entries, hgnc_filename):
    """
    adds synonyms from a hgnc json dataset to entries

    :param spec_entries: the list of entries the synonyms are added to
    :param hgnc_filename: filename of the json file
    """
    # get data from hgnc json
    with open(hgnc_filename, 'r', encoding="UTF8") as file:
        hgnc = json.load(file)
    gene_list = hgnc["response"]["docs"]

    for spec_entry in spec_entries:
        if spec_entry["IsHGNC"]:
            aliases = [value.get("alias_symbol", []) for value in gene_list if value["symbol"] == spec_entry["Code"]]
            for alias in aliases:
                spec_entry["Synonyms"].update(alias)


def main():
    # get data from Excel file
    workbook = openpyxl.load_workbook("MolMarker_Kategorisiert.xlsx")
    worksheet = workbook.active
    spec_entries = get_spec_from_worksheet(worksheet)
    add_synonyms_from_hgnc(spec_entries, "hgnc_complete_set.json")

    generate_textfile_hierarchy(spec_entries, 'visualization.txt')
    generate_xml_studystar(spec_entries, 'import_file_molMarker_Studystar.osc')
    generate_xlsx_gravity(spec_entries, 'gravity.xlsx')


if __name__ == "__main__":
    main()
