def get_sheets():
    sheet = xypath.Table.from_filename('resource/table-a02.xls', table_name='seasonally adjusted')
    return sheet

def per_sheet(sheet):
    sheet.genders = sheet.col('A').one_of(['Male', 'Female', 'All Persons'])
    sheet.times = sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d")
    sheet.ages = sheet.regex("All aged .*")
    indicators = sheet.filter("Total economically active").fill(LEFT).fill(RIGHT)

    obs = sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number)
    return obs

def per_cell(sheet, cell):
    out = {}
    out['ob'] = ob

    out['gender'] = ob.lookup(sheet.genders, UP)
    out['time'] = ob.lookup(sheet.times, LEFT, strict=True)
    out['age'] = ob.lookup(sheet.ages, UP)
    out['indicator'] = ob.lookup(sheet.indicators, UP, strict=True)

    return out


