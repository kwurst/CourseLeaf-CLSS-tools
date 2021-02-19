import csv
import textwrap

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

def formatComments(wantComments, wrapper, printed, internal):
    if wantComments:
        comments = ''
        if printed != None and printed != '':
            comments = comments + wrapper.fill('WebAdvisor Comments: ' + printed) + '\n'
        if internal != None and internal != '':
            comments = comments + wrapper.fill('Comments to Registrar: ' + internal.replace('\n', ' ')) + '\n'
        return comments
    else:
        return ''
    
def getLinkedSections(csvfile):
    csvfile.seek(0)
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    next(readCSV)
    dictCSV = csv.DictReader(csvfile)

    linkedDict = {}
    for row in dictCSV:
        if row[''] == '' and 'See' in row['Cross-listings']:
            linkedDict[row['Course'] + "-" + row['Section #']] = row['Section Cap Enrollment']

    return linkedDict

def main():
    with open('export.csv') as csvfile:
        comments = True
        wrapper = textwrap.TextWrapper(width = 70, initial_indent = '      ', subsequent_indent = '        ')
        linkedDict = getLinkedSections(csvfile)

        csvfile.seek(0)

        readCSV = csv.reader(csvfile, delimiter=',')
        semester = next(readCSV)[0]
        generated = next(readCSV)[0]

        dictCSV = csv.DictReader(csvfile)

        with open("output.txt", "w") as f:

            print(semester, file=f)
            print(generated, file=f)
            if comments:
                print("With Internal Comments and Printed Comments", file=f)
            print('', file=f)

            courseListing = ''
            notCancelled = False
            for row in dictCSV:
                if row[''] != '':
                    if notCancelled:
                        print(courseListing, file=f)
                        courseListing = ''
                        notCancelled = False
                    courseListing = row[''] + '\n'
                else:
                    if 'Cancelled' not in row['Status']:
                        notCancelled = True
                        if 'See' not in row['Cross-listings']:
                            courseListing = courseListing + '    {}  {}  {}  {}  {}\n'.format(formatSection(row['Section #']), formatInstructor(row['Instructor']), formatCap(row['Section Cap Enrollment']), formatMeetings(row['Meetings'].split('; ')[0]), formatRoom(row['Room'].split(';')[0]))
                            if '; ' in row['Meetings']:
                                if ';' not in row['Room']:
                                    room = row['Room'].split('; ')[0]
                                else:
                                    room = row['Room'].split('; ')[1]
                                courseListing = courseListing + '                                        {}   {}\n'.format(formatMeetings(row['Meetings'].split(';')[1]), formatRoom(room))
                            courseListing = courseListing + formatComments(comments, wrapper, row['Printed Comments#1'], row['Internal Comments'])
                        if 'Also' in row['Cross-listings']:
                            crossListing = row['Cross-listings'].split('-')
                            sectionNo = crossListing[-1]
                            courseListing = courseListing + '    {}                             {}\n'.format(formatSection(sectionNo), formatCap(linkedDict[row['Cross-listings'][5:]]))
                            courseListing = courseListing + formatComments(comments, wrapper, row['Printed Comments#1'], row['Internal Comments'])
            if notCancelled:
                print(courseListing, file=f)

if __name__== "__main__":
  main()