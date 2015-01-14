import xypath

sheet = xypath.Table.from_filename('resource/table-a02.xls', table_name='seasonally adjusted')
showtime("file imported")

obs = sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number)

genders = sheet.col('A').one_of(['Male', 'Female', 'All Persons'])
times = sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d")
ages = sheet.regex("All aged .*")
indicators = sheet.filter("Total economically active").fill(LEFT).fill(RIGHT)

for i, ob in enumerate(obs.unordered_cells):
    out = {}
    out['ob'] = ob

    out['gender'] = ob.lookup(genders, UP)
    out['time'] = ob.lookup(times, LEFT, strict=True)
    out['age'] = ob.lookup(ages, UP)
    out['indicator'] = ob.lookup(indicators, UP, strict=True)

    mystical_output_function(out)


