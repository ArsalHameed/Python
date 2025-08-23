import pprint
people={}
people['Ford']={'Name':'Ford Perfect',
                'Gender':'male',
                'Occupation':'Researcher',
                'Home planet':'Betelgeuse Seven'}
people['Arthur']={'Name':'Arthur Dent',
                'Gender':'male',
                'Occupation':'Sandwitch-Maker',
                'Home planet':'Earth'}
people['Trilian']={'Name':'Trillian McMillan',
                'Gender':'female',
                'Occupation':'Mathematician',
                'Home planet':'Earth'}
people['Robot']={'Name':'Marvin',
                'Gender':'unknown',
                'Occupation':'Paranoid Android',
                'Home planet':'unknown'}
pprint.pprint(people)
for person in people:
    print(person)
print("Occupation of Arthur: ",people['Arthur']['Occupation'])
