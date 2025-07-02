class Column:
    def __init__(self, row):
        self.succeeded = False

        if len(row) == 7 and row[5] != "pp":
            self.index = int(row[0])
            self.quote_id = row[1].split("/")[-1]
            self.date = row[2]
            self.acc = float(row[3][:-1])
            self.wpm = float(row[4].split(" ")[0])
            try:
                self.pp_weighted = int(row[5].split("p")[0])
                self.pp = int(row[6].split("p")[0])
            except Exception:
                self.succeeded = False

                return
            self.succeeded = True

