def get_sheets():
    sheet = xypath.Table.from_filename('resource/table-a02.xls', table_name='seasonally adjusted')
    return sheet

def per_sheet(sheet):
    genders = sheet.col('A').one_of(['Male', 'Female', 'All Persons'])
    times = sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d")
    ages = sheet.regex("All aged .*")
    indicators = sheet.filter("Total economically active").fill(LEFT).fill(RIGHT)

    obs = sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number)
    return obs

def per_cell(cell):
    out = {}
    out['ob'] = ob

    out['gender'] = ob.lookup(genders, UP)
    out['time'] = ob.lookup(times, LEFT, strict=True)
    out['age'] = ob.lookup(ages, UP)
    out['indicator'] = ob.lookup(indicators, UP, strict=True)

    return out


