import sys
import ROOT as rt
import fnmatch
rt.gROOT.SetBatch(True)    
import array

class inputFile():

    def __init__(self, fileName,transpose = False):
        self.transpose = transpose
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

    def transposeGraph(self,graph):
        outputGraph = graph.Clone()
        outputSize = graph.GetN()
        outputX,outputY = array.array('d',[0.]*outputSize),array.array('d',[0.]*outputSize)
        tempX,tempY = rt.Double(0.),rt.Double(0.)
        for i in range(outputSize):
            graph.GetPoint(i,tempX,tempY)
            outputX[i],outputY[i] = tempX,tempX-tempY
        outputGraph = rt.TGraph(outputSize,outputX,outputY)
        outputGraph.SetName(graph.GetName())
        return outputGraph
    #
    # def transposeHist(self,inHist):
    #     outName = inHist.GetName()
    #     binWidthX = 2*(inHist.GetXaxis().GetBinCenter(1)-inHist.GetXaxis().GetBinLowEdge(1))
    #     binWidthY = 2*(inHist.GetYaxis().GetBinCenter(1)-inHist.GetYaxis().GetBinLowEdge(1))
    #     xMass = [inHist.GetXaxis().GetBinCenter(x) for x in range(1,inHist.GetXaxis().GetNbins()+1)]
    #     yMass = [inHist.GetYaxis().GetBinCenter(y) for y in range(1,inHist.GetYaxis().GetNbins()+1)]
    #     yLow = [inHist.GetYaxis().GetBinLowEdge(y) for y in range(1,inHist.GetYaxis().GetNbins()+1)]
    #     xAxisTranspose = []
    #     for y in yMass:
    #         for x in xMass:
    #             if x-y >= binWidthY/2:
    #                 xAxisTranspose.append(x-y-binWidthY/2.) 
    #     minX = max(0,min(xAxisTranspose))
    #     maxX = max(xAxisTranspose)
    #     yAxis = array.array('d',yLow)
    #     xValue = minX
    #     xAxisTranspose = []
    #     while xValue <= maxX+binWidthX:
    #         xAxisTranspose.append(xValue)
    #         xValue += binWidthX
    #     xAxisTranspose = array.array('d',xAxisTranspose)
    #     outHist = rt.TH2D(outName+"temp","",len(xAxisTranspose)-1,xAxisTranspose,len(yAxis)-1,yAxis)
    #     outHist.SetDirectory(0)
    #     for x in range(1,outHist.GetXaxis().GetNbins()+1):
    #         for y in range(1,outHist.GetYaxis().GetNbins()+1):
    #             value = inHist.GetBinContent(x,y)
    #             xValue,yValue = self.getBinCenter2D(x,y,inHist)
    #             newMass = xValue - yValue
    #             outHist.Fill(xValue,newMass,value)
    #     outHist.SetName(outName)
    #     return outHist
    def transposeHist(self,inHist):
        outName = inHist.GetName()
        binWidthX = 2*(inHist.GetXaxis().GetBinCenter(1)-inHist.GetXaxis().GetBinLowEdge(1))
        binWidthY = 2*(inHist.GetYaxis().GetBinCenter(1)-inHist.GetYaxis().GetBinLowEdge(1))
        xMass = [inHist.GetXaxis().GetBinCenter(x) for x in range(1,inHist.GetXaxis().GetNbins()+1)]
        yMass = [inHist.GetYaxis().GetBinCenter(y) for y in range(1,inHist.GetYaxis().GetNbins()+1)]
        xLow = [inHist.GetXaxis().GetBinLowEdge(x) for x in range(1,inHist.GetXaxis().GetNbins()+1)]
        yAxisTranspose = []
        for x in xMass:
            for y in yMass:
                if x-y >= binWidthY/2:
                    yAxisTranspose.append(x-y-binWidthY/2.) 
        minY = max(0,min(yAxisTranspose))
        maxY = max(yAxisTranspose)
        xAxis = array.array('d',xLow)
        yValue = minY
        yAxisTranspose = []
        while yValue <= maxY+binWidthY:
            yAxisTranspose.append(yValue)
            yValue += binWidthY 
        yAxisTranspose = array.array('d',yAxisTranspose)
        outHist = rt.TH2D(outName+"temp","",len(xAxis)-1,xAxis,len(yAxisTranspose)-1,yAxisTranspose)
        outHist.SetDirectory(0)
        for x in range(1,outHist.GetXaxis().GetNbins()+1):
            for y in range(1,outHist.GetYaxis().GetNbins()+1):
                value = inHist.GetBinContent(x,y)
                xValue,yValue = self.getBinCenter2D(x,y,inHist)
                newMass = xValue - yValue
                outHist.Fill(xValue,newMass,value)
        outHist.SetName(outName)
        return outHist

    def getBinCenter2D(self,x,y,hist):
        xValue = hist.GetXaxis().GetBinCenter(x)
        yValue = hist.GetYaxis().GetBinCenter(y)
        return xValue,yValue

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "HISTOGRAM": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            x = rootFileIn.Get(tmpLINE[2])
            if self.transpose:
                x = self.transposeHist(x)
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
        maxDelta = -1
        index = -1
        for histogram in histograms:
            index += 1
            for i in range(histogram.GetN()):
                x,y = rt.Double(),rt.Double()
                histogram.GetPoint(i,x,y)
                if x-y < minDelta:
                    minDelta = x-y
                    minI = i
                    minIndexFinal = index
                if x-y > maxDelta:
                    maxDelta = x-y
                    maxHist = histogram
                    maxIndexFinal = index
        if "T5ttttDM175" in name:
            histograms[maxIndexFinal] = self.removePoints(histograms[maxIndexFinal]) 
        if minI > 0:
            histograms[minIndexFinal].SetPoint(histograms[minIndexFinal].GetN(),minDelta,0)
        else:
            index = histograms.index(histograms[minIndexFinal])
            histograms[minIndexFinal] = self.addPoint(histograms[minIndexFinal],minDelta,0)
            histograms[minIndexFinal].GetPoint(0,x,y)
            histograms[0] = histograms[minIndexFinal]
        if self.transpose:
            for i in range(len(histograms)):
                histograms[i] = self.transposeGraph(histograms[i])
        return histograms

    def removePoints(self,minHist):
        xs =[]# [0.]
        ys = []#[50.]
        appened=False
        for i in range(minHist.GetN()):
            x,y = rt.Double(),rt.Double()
            minHist.GetPoint(i,x,y)
            if y >= 50 :
                xs.append(x)
                ys.append(y)
            else:
                appended=True
        if xs[1] -ys[1] < 600: 
            xs.append(xs[-1])
            ys.append(50.)
            xs.append(0)
            ys.append(50.)
        else:
            xs.insert(0,0)
            ys.insert(0,50.)
            xs.insert(1,xs[1])
            ys.insert(1,50.)
        xs = array.array('d',xs)
        ys = array.array('d',ys)
        minHist = rt.TGraph(len(xs),xs,ys)
        return minHist

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

