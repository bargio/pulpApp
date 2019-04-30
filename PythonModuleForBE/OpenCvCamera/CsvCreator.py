import csv
class CsvCreator:
    fieldnames = ['image_byte']
    def __init__(self,csv,path):
        self.csv = csv
        self.path = path


    def createFile(self):
        with open(self.path+self.csv, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()


    # def addStringToCsv(self,name,lenght,image_byte):
    #     with open(self.path+self.csv, mode='a') as csv_file:
    #         writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
    #         writer.writerow({'name': name, 'lenght': lenght, 'image_byte': image_byte})

    def addStringToCsv(self,image_byte):
        with open(self.path+self.csv, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writerow({'image_byte': image_byte})

