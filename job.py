import csv

class Job:
    def __init__(self,job,salary,date,jid):
        self.job = job
        self.salary = salary
        self.date = date
        self.jid = jid
        self.next = None
        self.pre = None

size = 0




class Portal:
    def __init__(self):
        self.head = None
        self.tail = None

    def tail(self):
        global size
        if size > 1:
            current = self.head
            while current:
                if current.next is None:
                    self.tail = current
                current = current.next
        return self.tail

    def travers(self):
        current = self.head
        print(100*"=")
        while current:
            print(f"Job : {current.job}    salary : {current.salary}    date : {current.date}   id : {current.jid}")
            current = current.next
        print(100*"=")

    def add_job(self):
        global size

        new_job = input("enter job: ")
        new_salat = float(input("enter salary: "))
        new_date = input("enter date when the job was posted (year/month/day): ")
        new_jid = input("enter job ID: ")
        new_job = Job(new_job,new_salat,new_date,new_jid)

        if self.head is None:
            self.head = new_job
            print("job added successfully")
            size += 1
            print(100 * "=")
            return

        current = self.head
        new_job.next = current
        current.pre = new_job
        self.head = new_job

        print("job added successfully")
        size += 1
        print(100*"=")

    def remove(self):
        global size

        jid = input("enter the job id to be removed")
        current = self.head
        while current:
            if current.jid == jid:
                after = current.next.next
                current.next = after
                after.pre = current
                print("job removes successfully")
                size -= 1
                return
            current = current.next
        print("could not find the job id in the database")



    def filter_display(self):
        att = input("chose the attribute (job, salary, date ,jid): ")
        value = input("the value of the attribute to be filtered: ")

        arr = []
        if att == "job":
            current = self.head
            while current:
                if current.job == value:
                    arr.append(current)
                current = current.next
        elif att == "salary":
            value = float(value)
            current = self.head
            while current:
                if current.salary == value:
                    arr.append(current)
                current = current.next
        elif att == "date":
            current = self.head
            while current:
                if current.date == value:
                    arr.append(current)
                current = current.next
        else:
            print("wrong input")
        # current = self.head
        # while current:
        #     if getattr(current, att, None) == value:
        #         arr.append(current)
        #     current = current.next

        print(100*"=")
        for i in arr:
            print(f"Job : {i.job}    salary : {i.salary}    date : {i.date}")
        print(100*"=")

    def sort_display(self):
        att = input("enter the attribute to be sorted by (salary/date): ")
        order = input("ascending or descending order (A/D): ")
        hold = []
        current = self.head
        while current:
            hold.append(current)
            current = current.next


        if att == "salary":
            if order == "A" or order == "a":
                for i in range(len(hold)):
                    for j in range(i+1,len(hold)):
                        if hold[i].salary > hold[j].salary:
                            hold[i],hold[j] = hold[j],hold[i]


            elif order == "D" or order == 'd':
                for i in range(len(hold)):
                    for j in range(i+1,len(hold)):
                        if hold[i].salary < hold[j].salary:
                            hold[i],hold[j] = hold[j],hold[i]


            else:
                print("wrong input please try again")
                self.sort_display()

        elif att == "date":
            if order == "A" or order == "a":

                for i in range(len(hold)):
                    for j in range(i+1,len(hold)):
                        if hold[i].date > hold[j].date:
                            hold[i], hold[j] = hold[j], hold[i]



            elif order == "D" or order == 'd':
                for i in range(len(hold)):
                    for j in range(i+1,len(hold)):
                        if hold[i].date < hold[j].date:
                            hold[i], hold[j] = hold[j], hold[i]


            else:
                print("wrong input please try again")
                self.sort_display()
        else:
            print("wrong input please try again")

            self.sort_display()

        print(100*"=")
        for i in hold:
            print(f"Job : {i.job}    salary : {i.salary}    date : {i.date}")

    def save_to_file(self, filename="jobs.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Job", "Salary", "Date", "Job ID"])
            current = self.head
            while current:
                writer.writerow([current.job, current.salary, current.date, current.jid])
                current = current.next
        print(f"Data saved to {filename}")

    def load_from_file(self, filename="jobs.csv"):
        global size
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                self.head = None
                self.tail = None
                size = 0
                for row in reader:
                    if len(row) < 4:
                        continue
                    job_name, salary, date, jid = row[0], float(row[1]), row[2], row[3]
                    new_job = Job(job_name, salary, date, jid)

                    if self.head is None:
                        self.head = new_job
                        self.tail = new_job
                    else:
                        self.tail.next = new_job
                        new_job.pre = self.tail
                        self.tail = new_job
                    size += 1
            print(f"Data loaded successfully from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty list.")




work = Portal()
work.load_from_file()





def employ():
    while True:
        print(100*"=")
        print("1, display jobs")
        print("2, filter jobs")
        print("3, sort jobs")
        print("0, return to previous page")
        print("#, exit system")
        ch = input("            :")
        if ch == "1":
            work.travers()
        elif ch == "2":
            work.filter_display()
        elif ch == "3":
            work.sort_display()
        elif ch == "0":
            menu()
        elif ch == "#":

            break
        else:
            print("wrong input please try again")
            employ()


def employer():
    while True:
        print(100*"=")
        print("1, add job")
        print("2, remove job")
        print("3, display job")
        print("0, to return to previous page")
        print("#, exit system")
        ch = input("              :")
        if ch == "1":
            work.add_job()
        elif ch == "2":
            work.remove()
        elif ch == "3":
            work.travers()
        elif ch == "0":
            menu()
        elif ch == "#":
            work.save_to_file()
            break
        else:
            print("wrong input please try again")
            employer()
        work.save_to_file()





def menu():
    while True:
        print("1, Employer")
        print("2, Employ")
        print("#, exit system")
        print(100*"=")
        ch = input("             :")

        if ch == "1":
            employer()
        elif ch == "2":
            employ()
        elif ch == "#":
            work.save_to_file()
            break
        else:
            print("wrong input pleas try again")
            menu()

menu()