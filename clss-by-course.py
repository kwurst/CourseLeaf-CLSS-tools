import csv

def formatSection(section):
    return section.ljust(4)

def formatMeetings(meetings):
    return meetings.ljust(20)

def formatInstructor(instructor):
    return instructor[:instructor.find(' (')].ljust(25)

def formatRoom(room):
    if '-' in room:
        return room[:room.find(' -')].replace('*', ' ').ljust(30)
    else:
        return room.ljust(30)

def formatCap(cap):
    return cap.rjust(2)

def formatCrossList(crossList):
    return crossList.ljust(20)

def getLinkedSections(csvfile):
    csvfile.seek(0)
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    next(readCSV)
    dictCSV = csv.DictReader(csvfile)

    linkedDict = {}
    for row in dictCSV:
        if row[''] is '' and 'See' in row['Cross-listings']:
            linkedDict[row['Course'] + "-" + row['Section #']] = row['Section Cap Enrollment']

    return linkedDict

def main():
    with open('export.csv') as csvfile:

        linkedDict = getLinkedSections(csvfile)

        csvfile.seek(0)

        readCSV = csv.reader(csvfile, delimiter=',')
        semester = next(readCSV)[0]
        generated = next(readCSV)[0]

        dictCSV = csv.DictReader(csvfile)

        with open("output.txt", "w") as f:

            print(semester, file=f)
            print(generated, file=f)

            for row in dictCSV:
                if row[''] != '':
                    print('',file=f)
                    print(row[''], file=f)
                else:
                    if 'Cancelled' not in row['Status']:
                        if 'See' not in row['Cross-listings']:
                            print('    %s  %s  %s  %s  %s' % (formatSection(row['Section #']), formatInstructor(row['Instructor']), formatCap(row['Section Cap Enrollment']), formatMeetings(row['Meetings'].split('; ')[0]), formatRoom(row['Room'].split(';')[0])), file=f )
                            if '; ' in row['Meetings']:
                                if ';' not in row['Room']:
                                    room = row['Room'].split('; ')[0]
                                else:
                                    room = row['Room'].split('; ')[1]
                                print('                                        %s   %s' % (formatMeetings(row['Meetings'].split(';')[1]), formatRoom(room)), file=f)
                        if 'Also' in row['Cross-listings']:
                            crossListing = row['Cross-listings'].split('-')
                            sectionNo = crossListing[-1]
                            print('    %s                             %s' % (formatSection(sectionNo), formatCap(linkedDict[row['Cross-listings'][5:]])), file=f)

if __name__== "__main__":
  main()