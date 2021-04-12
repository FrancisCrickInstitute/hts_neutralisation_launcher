well_dict = {
    "A01": ["A01", "A02", "B01", "B02"],
    "A02": ["A03", "A04", "B03", "B04"],
    "A03": ["A05", "A06", "B05", "B06"],
    "A04": ["A07", "A08", "B07", "B08"],
    "A05": ["A09", "A10", "B09", "B10"],
    "A06": ["A11", "A12", "B11", "B12"],
    "A07": ["A13", "A14", "B13", "B14"],
    "A08": ["A15", "A16", "B15", "B16"],
    "A09": ["A17", "A18", "B17", "B18"],
    "A10": ["A19", "A20", "B19", "B20"],
    "A11": ["A21", "A22", "B21", "B22"],
    "A12": ["A23", "A24", "B23", "B24"],
    "B01": ["C01", "C02", "D01", "D02"],
    "B02": ["C03", "C04", "D03", "D04"],
    "B03": ["C05", "C06", "D05", "D06"],
    "B04": ["C07", "C08", "D07", "D08"],
    "B05": ["C09", "C10", "D09", "D10"],
    "B06": ["C11", "C12", "D11", "D12"],
    "B07": ["C13", "C14", "D13", "D14"],
    "B08": ["C15", "C16", "D15", "D16"],
    "B09": ["C17", "C18", "D17", "D18"],
    "B10": ["C19", "C20", "D19", "D20"],
    "B11": ["C21", "C22", "D21", "D22"],
    "B12": ["C23", "C24", "D23", "D24"],
    "C01": ["E01", "E02", "F01", "F02"],
    "C02": ["E03", "E04", "F03", "F04"],
    "C03": ["E05", "E06", "F05", "F06"],
    "C04": ["E07", "E08", "F07", "F08"],
    "C05": ["E09", "E10", "F09", "F10"],
    "C06": ["E11", "E12", "F11", "F12"],
    "C07": ["E13", "E14", "F13", "F14"],
    "C08": ["E15", "E16", "F15", "F16"],
    "C09": ["E17", "E18", "F17", "F18"],
    "C10": ["E19", "E20", "F19", "F20"],
    "C11": ["E21", "E22", "F21", "F22"],
    "C12": ["E23", "E24", "F23", "F24"],
    "D01": ["G01", "G02", "H01", "H02"],
    "D02": ["G03", "G04", "H03", "H04"],
    "D03": ["G05", "G06", "H05", "H06"],
    "D04": ["G07", "G08", "H07", "H08"],
    "D05": ["G09", "G10", "H09", "H10"],
    "D06": ["G11", "G12", "H11", "H12"],
    "D07": ["G13", "G14", "H13", "H14"],
    "D08": ["G15", "G16", "H15", "H16"],
    "D09": ["G17", "G18", "H17", "H18"],
    "D10": ["G19", "G20", "H19", "H20"],
    "D11": ["G21", "G22", "H21", "H22"],
    "D12": ["G23", "G24", "H23", "H24"],
    "E01": ["I01", "I02", "J01", "J02"],
    "E02": ["I03", "I04", "J03", "J04"],
    "E03": ["I05", "I06", "J05", "J06"],
    "E04": ["I07", "I08", "J07", "J08"],
    "E05": ["I09", "I10", "J09", "J10"],
    "E06": ["I11", "I12", "J11", "J12"],
    "E07": ["I13", "I14", "J13", "J14"],
    "E08": ["I15", "I16", "J15", "J16"],
    "E09": ["I17", "I18", "J17", "J18"],
    "E10": ["I19", "I20", "J19", "J20"],
    "E11": ["I21", "I22", "J21", "J22"],
    "E12": ["I23", "I24", "J23", "J24"],
    "F01": ["K01", "K02", "L01", "L02"],
    "F02": ["K03", "K04", "L03", "L04"],
    "F03": ["K05", "K06", "L05", "L06"],
    "F04": ["K07", "K08", "L07", "L08"],
    "F05": ["K09", "K10", "L09", "L10"],
    "F06": ["K11", "K12", "L11", "L12"],
    "F07": ["K13", "K14", "L13", "L14"],
    "F08": ["K15", "K16", "L15", "L16"],
    "F09": ["K17", "K18", "L17", "L18"],
    "F10": ["K19", "K20", "L19", "L20"],
    "F11": ["K21", "K22", "L21", "L22"],
    "F12": ["K23", "K24", "L23", "L24"],
    "G01": ["M01", "M02", "N01", "N02"],
    "G02": ["M03", "M04", "N03", "N04"],
    "G03": ["M05", "M06", "N05", "N06"],
    "G04": ["M07", "M08", "N07", "N08"],
    "G05": ["M09", "M10", "N09", "N10"],
    "G06": ["M11", "M12", "N11", "N12"],
    "G07": ["M13", "M14", "N13", "N14"],
    "G08": ["M15", "M16", "N15", "N16"],
    "G09": ["M17", "M18", "N17", "N18"],
    "G10": ["M19", "M20", "N19", "N20"],
    "G11": ["M21", "M22", "N21", "N22"],
    "G12": ["M23", "M24", "N23", "N24"],
    "H01": ["O01", "O02", "P01", "P02"],
    "H02": ["O03", "O04", "P03", "P04"],
    "H03": ["O05", "O06", "P05", "P06"],
    "H04": ["O07", "O08", "P07", "P08"],
    "H05": ["O09", "O10", "P09", "P10"],
    "H06": ["O11", "O12", "P11", "P12"],
    "H07": ["O13", "O14", "P13", "P14"],
    "H08": ["O15", "O16", "P15", "P16"],
    "H09": ["O17", "O18", "P17", "P18"],
    "H10": ["O19", "O20", "P19", "P20"],
    "H11": ["O21", "O22", "P21", "P22"],
    "H12": ["O23", "O24", "P23", "P24"]
}