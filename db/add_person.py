import pymongo
import sys
import gridfs
import os
#example: python add_person.py erin cs student
def main():
    client = pymongo.MongoClient("mongodb+srv://erinruby:colorado18@yame-project-6ex3z.mongodb.net/test?retryWrites=true") #ERIN's LOGIN
    db = client.prototype #name of the db
    col = client.people #name of the collection

    name = sys.argv[1]
    degree = sys.argv[2]
    occupation = sys.argv[3]
    photo = sys.argv[4]

    fs=gridfs.GridFS(db)
    # print (fs.list())
    im = fs.put(open('/Users/erinruby/Documents/Summer_2018/YAME/db/{0}'.format(photo), 'rb'), filename='{0}'.format(photo)) #ERINS COMP
    # im = fs.put(open('/Users/CourtSolano/YAME/form_ui/uploads/{0}'.format(photo), 'rb'), filename='{0}'.format(photo)) #COURTNEYS COMP


    person = {"name": name,
            "degree": degree,
            "occupation": occupation,
            "photo": im}
            # "photo": os.system("mongofiles --uri 'mongodb+srv://erinruby:colorado18@yame-project-6ex3z.mongodb.net/test' put 'download.jpg'")}

    if (db.people.insert_one(person).inserted_id != 0):
        print (name, "successfully added!")

    pup = db.fs.files.find({'_id':im})
    for att in pup:
        p = att['filename']
        # for i in att:
        #     print (i)
        #     if (i == "filename"):
        #         photo = i.value()
        #         print(photo)
    # print (pup)
    os.system("open /Users/CourtSolano/YAME/form_ui/uploads/{0}".format(photo))

if __name__ == '__main__':
    main()
