import xlrd

def read_file(self,file,name):
        f1 = xlrd.open_workbook(file)
        st = f1.sheet_by_name(name)
        nr = st.nrows
        cn = st.row_values(0)

        list = []

        for i in range(1,nr):
            r = st.row_values(i)
            app = {}
            for i in range(0,len(cn)):
                app[cn[i]] = r[i]

            list.append(app)
        return list
        print (len(list[1]))