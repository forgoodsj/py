import csv

a = "places_country__row"
print(a[7:-5])

writer = csv.writer(open('countries2.csv','w'))
writer.writerow(a)
writer.writerow(a)
writer.writerow(a)