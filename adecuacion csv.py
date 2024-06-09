import csv


def cambio(input_csv, output_csv):
    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]

    for row in data:
        for i in range(len(row)):
            if row[i] == '2':
                row[i] = '0'

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


# Reemplaza 'input.csv' y 'output.csv' con los nombres de tus archivos
cambio('map.csv', 'map.csv')
