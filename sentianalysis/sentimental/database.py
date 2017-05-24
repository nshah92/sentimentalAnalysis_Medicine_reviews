from models import Employee, brandnameReviews, genericnameReviews
from dateutil.parser import parse

import csv
import re

def CSVtoMongoDB():

    print "copying data to database....."
    f = open('/Users/Nil/Desktop/Project/Others/Scrapper/ReviewBuilder/finalDrugReview_with_dates.csv', 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            dt = parse(str(row[3]))
            data = brandnameReviews(name=row[0].lower(), genericname=row[1].lower(), review=' '.join(row[2].split()), date=dt.strftime('%d-%b-%Y'), condition="High Blood Pressure")
            data.save()
    finally:
        f.close()

    f1 = open('/Users/Nil/Desktop/Project/Others/Scrapper/ReviewBuilder/finalDrugReview_with_dates1.csv', 'rt')
    try:
        reader = csv.reader(f1)
        for row in reader:
            dt = parse(str(row[3]))
            dt = parse(str(row[3]))
            data1 = genericnameReviews(name=row[0].lower(), brandname=row[1].lower(), review=' '.join(row[2].split()), date=dt.strftime('%d-%b-%Y'), condition="High Blood Pressure")
            data1.save()
    finally:
        f.close()
    print "Database is Ready to use.."