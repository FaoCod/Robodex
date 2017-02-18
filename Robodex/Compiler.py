from openpyxl import load_workbook

class Compiler():
    def __init__(self):
        self.r = []
        self.Main()

    def Main(self):
        
        #Defined variables
        robots = []
        ro = []

        #Opens the excel sheet
        wb = load_workbook('Book1.xlsx')
        sheet = wb.get_sheet_by_name('Book1')

        #Appends each robot's team number to the list
        for item in sheet['B']:
            if item.value not in robots and item.value != 'Team Number' and item.value != None:
                robots.append(item.value)

        #Creates each team's dictionary
        for r in robots:
            file = {'Team':r, 'aG':[], 'gR':[], 'pR':[]}
            ro.append(file)
        #print(ro)
            

        #Fills each team's dictionary
        for rnd in sheet:
            for r in robots:
                if rnd[1].value == r:
                    ro[robots.index(r)]['aG'].append(rnd[3].value)
                    ro[robots.index(r)]['gR'].append(rnd[4].value)
                    ro[robots.index(r)]['pR'].append(rnd[6].value)
        #print(ro)

        for r in robots:
            file = {'Team':r,
                    'aG':self.aGHist(ro[robots.index(r)]['aG']),
                    'gR':self.gRHist(ro[robots.index(r)]['gR']),
                    'pR':self.pRHist(ro[robots.index(r)]['pR'])}
            self.r.append(file)
        

        '''#Prints each team's dictionary
        for robot in ro:
            print(robot)'''
        #(0,2,2,4,2,7)
    #Creates values for the Gear histogram
    def gRHist(self, scores):
        values = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for s in scores:
             values[s] += 1
        return(values)

    def aGHist(self, aGRound):
        values = [0,0]
        buckets = [0,1]
        for g in aGRound:
            values[g] += 1
        return(values, buckets)

    def pRHist(self, pRound):
        values = [0,0,0,0,0,0,0,0,0,0,0]
        buckets = ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40']
        for p in pRound:
            if p < 5:
                values[0] += 1
            elif p < 10:
                values[1] += 1
            elif p < 15:
                values[2] += 1
            elif p < 20:
                values[3] += 1
            elif p < 25:
                values[4] += 1
            elif p < 30:
                values[5] += 1
            elif p < 35:
                values[6] += 1
            elif p < 40:
                values[7] += 1
            else:
                values[8] += 1
        return values, buckets
            
                
        
        #Percent aG
        '''gSum = 0
        rDone = []
        gAvg = {}
        for r in ro:
            if r['Team'] not in rDone:
                for aG in r['aG']:
                    gSum += int(aG)
                    rDone.append(r['Team'])
                    print(rDone)
                    print(gSum)
                self.r[ro.index(r)]['aG'] = gSum'''
        #print(self.r)


comp = Compiler()
print(comp.r)
