import sys
import ROOT as rt
import fnmatch
rt.gROOT.SetBatch(True)    
import array

class inputFile():

    def __init__(self, fileName):
        self.HISTOGRAM = self.findHISTOGRAM(fileName)
        self.EXPECTED = self.findEXPECTED(fileName)
        self.OBSERVED = self.findOBSERVED(fileName)
        self.LUMI = self.findATTRIBUTE(fileName, "LUMI")
        self.ENERGY = self.findATTRIBUTE(fileName, "ENERGY")
        self.PRELIMINARY = self.findATTRIBUTE(fileName, "PRELIMINARY")

    def findATTRIBUTE(self, fileName, attribute):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != attribute: continue
            fileIN.close()
            return tmpLINE[1]

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "HISTOGRAM": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            x = rootFileIn.Get(tmpLINE[2])
            x.SetDirectory(0)
            return {'histogram': x}
    def getall(self,d, basepath="/"):
        "Generator function to recurse into a ROOT file/dir and yield path"
        for key in d.GetListOfKeys():
            kname = key.GetName()
            if key.IsFolder():
                # TODO: -> "yield from" in Py3
                for i in self.getall(d.Get(kname), basepath+kname+"/"):
                    yield i
            else:
                yield basepath+kname

    def findHistograms(self,rootFile,name):
        if name[0] != "/":
            name = "/"+name
        histograms = []
        for path in self.getall(rootFile):
            if fnmatch.fnmatch(path,name):
                histograms.append(rootFile.Get(path))

        minDelta = 1E9
        for histogram in histograms:
            for i in range(histogram.GetN()):
                x,y = rt.Double(),rt.Double()
                histogram.GetPoint(i,x,y)
                if x-y < minDelta:
                    minHist = histogram
                    minDelta = x-y
                    minI = i
        if minI > 0:
            minHist.SetPoint(minHist.GetN(),minDelta,0)
        else:
            index = histograms.index(minHist)
            minHist = self.addPoint(minHist,minDelta,0)
            minHist.GetPoint(0,x,y)
            histograms[0] = minHist
        return histograms

    def addPoint(self,minHist,xstart,ystart):
        xs = [xstart]
        ys = [ystart]
        for i in range(minHist.GetN()):
            x,y = rt.Double(),rt.Double()
            minHist.GetPoint(i,x,y)
            xs.append(x)
            ys.append(y)
        xs = array.array('d',xs)
        ys = array.array('d',ys)
        minHist = rt.TGraph(minHist.GetN()+1,xs,ys)
        return minHist

            
    def findEXPECTED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            if len(tmpLINE) <= 7:
                return {'nominal': self.findHistograms(rootFileIn,tmpLINE[2]),
                        'plus': self.findHistograms(rootFileIn,tmpLINE[3]),
                        'plus2': [],
                        'minus': self.findHistograms(rootFileIn,tmpLINE[4]),
                        'minus2': [],
                        'colorLine': tmpLINE[5],
                        'colorArea': tmpLINE[6]}
            else:
                return {'nominal': self.findHistograms(rootFileIn,tmpLINE[2]),
                        'plus': self.findHistograms(rootFileIn,tmpLINE[3]),
                        'plus2': self.findHistograms(rootFileIn,tmpLINE[4]),
                        'minus': self.findHistograms(rootFileIn,tmpLINE[5]),
                        'minus2': self.findHistograms(rootFileIn,tmpLINE[6]),
                        'colorLine': tmpLINE[7],
                        'colorArea': tmpLINE[8]}

    def findOBSERVED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {'nominal': self.findHistograms(rootFileIn,tmpLINE[2]),
                    'plus': self.findHistograms(rootFileIn,tmpLINE[3]),
                    'minus': self.findHistograms(rootFileIn,tmpLINE[4]),
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

