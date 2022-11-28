import xml.etree.ElementTree as ET
from xml.dom import minidom

daten = [
    ["BCL (B-cell lymphoma)", "", "", "Gruppe", ""],
    ["bcr-abl", "", "", "Translokation, Philadelphia Chromosom, t(9;22)", ""],
    ["BRAF V600", "", "BRAF", "definierte Mutation", "BRAF-Mutation an Position V600"],
    ["BRAF V600E", "", "BRAF", "definierte Mutation", "BRAF-Mutation an Position V600 kodierend zu Glutamat"],
    ["BRCA (BReast CAncer)", "", "", "Gruppe", ""],
    ["CD3", "", "", "Rezeptor", "mehrere Gene"],
    ["CDK (Cyclin-Dependent Kinase)", "", "", "Gruppe", ""],
    ["CELMoD (Cereblon E3 ubiquitin ligase Modulating Drug)", "", "", "Medikamente", ""],
    ["del (17p)", "", "", "Deletion", ""],
    ["del (Deletions)", "", "", "Deletion", "zu unspezifisch?"],
    ["EGFR T790M", "", "EGFR", "definierte Mutation", ""],
    ["ER-", "", "ER (Östrogenrezeptor)", "Rezeptor-Status", ""],
    ["ER (Östrogenrezeptor)", "", "", "Rezeptor", ""],
    ["ER+", "", "ER (Östrogenrezeptor)", "Rezeptor-Status", ""],
    ["FGFR (Fibroblast growth factor receptor)", "", "", "Gruppe", ""],
    ["FLT3 D835", "", "FLT3", "definierte Mutation", ""],
    ["GPRC5D x CD3", "", "", "bispezifischer Antikörper", ""],
    ["HPV16", "", "", "Virusinfektion", ""],
    ["IDH (Isocitrat-Dehydrogenase)", "", "", "Gruppe", "https://www.genenames.org/data/genegroup/#!/group/1926"],
    ["JAK (Januskinase)", "", "", "Gruppe", "https://www.genenames.org/data/genegroup/#!/group/1459"],
    ["MEK (MEK-Inhibitoren)", "", "", "Medikament", "Medikament hemmt MAP2K1/MAP2K2"],
    ["MSI (Mikrosatelliteninstabilität)", "", "", "MSI", ""],
    ["MSI-H", "", "MSI (Mikrosatelliteninstabilität)", "MSI", ""],
    ["PgR-", "", "PgR (Progesteronrezeptor)", "Rezeptor-Status", ""],
    ["PgR (Progesteronrezeptor)", "", "", "Rezeptor", ""],
    ["PgR+", "", "PgR (Progesteronrezeptor)", "Rezeptor-Status", ""],
    ["PSMA (Prostataspezifisches Membranantigen)", "", "", "Antigen", ""],
    ["SSTR (Somatostatin-Rezeptor)", "", "", "Rezeptor", ""],
    ["SSTR+ (Somatostatin-Rezeptor positiv)", "", "SSTR (Somatostatin-Rezeptor)", "Rezeptor-Status", ""],
    ["t(11;14)", "", "", "Translokation", ""],
    ["t(15;17)", "", "", "Translokation", ""],
    ["TCER (Bispecific T cell engaging receptors)", "", "", "Medikamente", ""],
    ["ALK", "ALK", "", "", ""],
    ["BCL-2", "BCL2", "BCL (B-cell lymphoma)", "", ""],
    ["BCL-6", "BCL6", "BCL (B-cell lymphoma)", "", ""],
    ["BRAF", "BRAF", "", "", ""],
    ["BRCA1", "BRCA1", "BRCA (BReast CAncer)", "", ""],
    ["BRCA2", "BRCA2", "BRCA (BReast CAncer)", "", ""],
    ["CD19", "CD19", "", "", ""],
    ["PD-L1", "CD274", "", "", ""],
    ["CD33", "CD33", "", "", ""],
    ["CD38", "CD38", "", "", ""],
    ["CD80", "CD80", "", "", ""],
    ["CDK4", "CDK4", "CDK (Cyclin-Dependent Kinase)", "", ""],
    ["CDK6", "CDK6", "CDK (Cyclin-Dependent Kinase)", "", ""],
    ["Cereblon (E3 Ubiquitin Ligase)", "CRBN", "", "", ""],
    ["CTLA-4 (cytotoxic T-lymphocyte-associated Protein 4)", "CTLA4", "", "", ""],
    ["DLL3 (Delta-like 3)", "DLL3", "", "", ""],
    ["EGFR", "EGFR", "", "", ""],
    ["HER2/neu", "ERBB2", "", "", ""],
    ["ESR1 (Estrogen Receptor 1 Gen)", "ESR1", "", "", ""],
    ["FGFR1", "FGFR1", "FGFR (Fibroblast growth factor receptor)", "", ""],
    ["FGFR2", "FGFR2", "FGFR (Fibroblast growth factor receptor)", "", ""],
    ["FGFR3", "FGFR3", "FGFR (Fibroblast growth factor receptor)", "", ""],
    ["FGFR4", "FGFR4", "FGFR (Fibroblast growth factor receptor)", "", ""],
    ["FLT3 (FMS-related tyrosine kinase 3)", "FLT3", "", "", ""],
    ["GDF15 (Growth/differentiation factor 15)", "GDF15", "", "", ""],
    ["HRAS", "HRAS", "", "", ""],
    ["IDH1", "IDH1", "IDH (Isocitrat-Dehydrogenase)", "", ""],
    ["IDH2", "IDH2", "IDH (Isocitrat-Dehydrogenase)", "", ""],
    ["IL-2", "IL2", "", "", ""],
    ["CD122", "IL2RB", "", "", ""],
    ["CD123 ", "IL3RA", "", "", ""],
    ["JAK1", "JAK1", "JAK (Januskinase)", "", ""],
    ["JAK2", "JAK2", "JAK (Januskinase)", "", ""],
    ["NKG2A (Natural Killer Cell Receptor NKG2A)", "KLRC1", "", "", ""],
    ["KRAS", "KRAS", "", "", ""],
    ["LAG-3", "LAG3", "", "", ""],
    ["MEK1", "MAP2K1", "", "", ""],
    ["MEK2", "MAP2K2", "", "", ""],
    ["c-Met", "MET", "", "", "!ist das korrekt?!"],
    ["MET", "MET", "", "", ""],
    ["CD20", "MS4A1", "", "", ""],
    ["mTOR (Mechanistic Target of Rapamycin)", "MTOR", "", "", ""],
    ["MYC (c-MYC)", "MYC", "", "", ""],
    ["NPM1 (Nukleophosmin-Gen1)", "NPM1", "", "", ""],
    ["NRAS", "NRAS", "", "", ""],
    ["PD-1 (Programmed cell death protein 1)", "PDCD1", "", "", ""],
    ["PI3K (Phosphoinosit-3-Kinase)", "PIK3CA", "", "", ""],
    ["PRAME (Nuclear Receptor Transcriptional Regulator)", "PRAME", "", "", ""],
    ["PSCA (Prostate stem cell antigen)", "PSCA", "", "", ""],
    ["PTEN (Phosphatase and Tensin homolog)", "PTEN", "", "", ""],
    ["RET (Rezeptor-Tyrosinkinase)", "RET", "", "", ""],
    ["ROS-1 (c-ros oncogene 1, receptor tyrosine kinase)", "ROS1", "", "", ""],
    ["SLAMF7", "SLAMF7", "", "", ""],
    ["TLR9 (Toll-Like Rezeptor 9)", "TLR9", "", "", ""],
    ["BCMA (B-Cell Maturation Antigen, TNFRSF17)", "TNFRSF17", "", "", ""],
    ["TP53", "TP53", "", "", ""],
    ["VEGF", "VEGFA", "", "", ""]
]

with open('osexport.osc', 'r') as cFile:
    tree = ET.parse(cFile)
    root = tree.getroot()

    e = tree.findall('.//Versions/Version/Entries')
    for item in e:
        entries = item.findall('Entry')
        for entry in entries:
            item.remove(entry)
    for data in daten:
        for entries in e:
            entry = ET.SubElement(entries, "Entry");
            item = ET.SubElement(entry, "Code"); item.text = data[0]
            item = ET.SubElement(entry, "ShortDescription"); item.text = data[0]
            item = ET.SubElement(entry, "Description"); item.text = data[0]
            item = ET.SubElement(entry, "Synonyms"); item.text = data[1]
            item = ET.SubElement(entry, "Note"); item.text = data[4]
            item = ET.SubElement(entry, "Position"); item.text = ""
            item = ET.SubElement(entry, "ParentCode"); item.text = data[2]
    tree.write('osexport2.osc')
