from models import Employee, brandnameReviews, genericnameReviews
from dateutil.parser import parse

import csv

def CSVtoMongoDB():
    f = open('/Users/Nil/Desktop/Project/Others/Scrapper/ReviewBuilder/finalDrugReview_with_dates.csv', 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            dt = parse(str(row[3]))
            data = brandnameReviews(name=row[0], genericname=row[1], review=row[2], date=dt.strftime('%d-%b-%Y'))
            data.save()
    finally:
        f.close()

    f1 = open('/Users/Nil/Desktop/Project/Others/Scrapper/ReviewBuilder/finalDrugReview_with_dates1.csv', 'rt')
    try:
        reader = csv.reader(f1)
        for row in reader:
            dt = parse(str(row[3]))
            dt = parse(str(row[3]))
            data1 = genericnameReviews(name=row[0], brandname=row[1], review=row[2], date=dt.strftime('%d-%b-%Y'))
            data1.save()
    finally:
        f.close()