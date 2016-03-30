import sys
import ROOT as rt
import fnmatch
rt.gROOT.SetBatch(True)    

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
        return histograms

            
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

