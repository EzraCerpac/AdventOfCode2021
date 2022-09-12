from octopus import Field, Octopus

field = Field('input.txt')
field.progress(400)
print(field.flash_count)
# field.print_map()