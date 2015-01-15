def get_sheets():
    return databaker.load('resource/table-a02.xls', table_name='seasonally adjusted')

def per_sheet(sheet):
    sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number).is_obs()

    gender = sheet.col('A').one_of(['Male', 'Female', 'All Persons'])
    gender.is_header('gender', UP)

    sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d").is_header('times', LEFT, strict=True)

    sheet.regex("All aged .*").is_header('ages', UP)

    indicator = sheet.filter("Total economically active").fill(LEFT).fill(RIGHT)
    indicator.is_header('indicator', UP, strict=True)

    "uk".is_header('geography')

