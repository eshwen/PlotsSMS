import sys
from inputFile import *
from smsPlotXSEC import *
from smsPlotCONT import *
from smsPlotBrazil import *
class ContPlotCollection():
    def __init__(self,modelNames,modelType):
        self.modelNames = modelNames
        modelTypeDict = {"gluino":"pp #rightarrow #tilde{g} #tilde{g}",\
                "squark":"pp #rightarrow #tilde{q} #tilde{q}",\
                "stop":"pp #rightarrow #tilde{t} #tilde{t}"}
        if modelType not in modelTypeDict:
            raise AttributeError, "Unsupported model type: "+modelType
        self.modelType = modelType
        self.label = modelTypeDict[modelType]

        self.contPlotDict = {}
    def setContPlots(self,filenameTemplate):
        self.models = []
        for modelname in self.modelNames:
            makeHisto = True
            if modelname != self.modelNames[0]:
                makeHisto = False
            # read the config file
            fileIN = inputFile(filenameTemplate.format(modelname.replace("T2qqDegen","T2qq")))
            contPlot = smsPlotCONT(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, 
                    fileIN.PRELIMINARY, "CONT",makeHisto)
            self.contPlotDict[modelname] = contPlot
            self.models.append(contPlot.model)
        self.getRanges()
        self.setStandard()
    def setStandard(self): 
        self.preliminary = self.contPlotDict[self.modelNames[0]].preliminary
        self.lumi = self.contPlotDict[self.modelNames[0]].lumi
        self.energy = self.contPlotDict[self.modelNames[0]].energy
        self.c = self.contPlotDict[self.modelNames[0]].c
        self.histo = self.contPlotDict[self.modelNames[0]].histo
        self.contPlotDict[self.modelNames[0]].emptyHistogramFromModel((self.Xmin,self.Xmax,self.Ymin,self.Ymax))
    def getRanges(self):
        Xmin,Ymin,Xmax,Ymax = 1E7,1E7,-1,-1
        for contPlot in self.contPlotDict.itervalues():
            Xmin = min(contPlot.model.Xmin,Xmin)
            Ymin = min(contPlot.model.Ymin,Ymin)
            Xmax = max(contPlot.model.Xmax,Xmax)
            Ymax = max(contPlot.model.Ymax,Ymax)
        self.Xmin = Xmin
        self.Ymin = Ymin
        self.Xmax = Xmax
        self.Ymax = Ymax

    def DrawLegend(self):
        LObsList = []
        LExpList = []
        textObsList = []
        xRange = self.Xmax-self.Xmin
        yRange = self.Ymax-self.Ymin

        for iM,model in enumerate(self.models):
            offset = -(yRange/18.)*iM
            
            LObs = rt.TGraph(2)
            LObs.SetName("LObs")
            LObs.SetTitle("LObs")
            LObs.SetLineColor(model.color)
            LObs.SetLineStyle(1)
            LObs.SetLineWidth(4)
            LObs.SetMarkerStyle(20)
            LObs.SetPoint(0,self.Xmin+3*xRange/100, self.Ymax-1.35*yRange/10+offset)
            LObs.SetPoint(1,self.Xmin+10*xRange/100, self.Ymax-1.35*yRange/10+offset)

            textObs = rt.TLatex(self.Xmin+11*xRange/100, self.Ymax-1.50*yRange/10+offset, model.label+" "+model.label2)
            textObs.SetTextFont(42)
            textObs.SetTextSize(0.030)
            textObs.Draw()
            textObsList.append(textObs)

            LExp = rt.TGraph(2)
            LExp.SetName("LObsP")
            LExp.SetTitle("LObsP")
            LExp.SetLineColor(model.color)
            LExp.SetLineStyle(7)
            LExp.SetLineWidth(4)
            LExp.SetMarkerStyle(20)
            LExp.SetPoint(0,self.Xmin+3*xRange/100, self.Ymax-1.20*yRange/10+offset)
            LExp.SetPoint(1,self.Xmin+10*xRange/100, self.Ymax-1.20*yRange/10+offset)

            LObs.Draw("LSAME")
            LExp.Draw("LSAME")

            LObsList.append(LObs)
            LExpList.append(LExp)

        offset = -(iM)*(yRange/18.)
        LObs= rt.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(rt.kBlack)
        LObs.SetLineStyle(7)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0,self.Xmin+70*xRange/100, self.Ymax-1.35*yRange/10+offset)
        LObs.SetPoint(1,self.Xmin+77*xRange/100, self.Ymax-1.35*yRange/10+offset)

        textObs = rt.TLatex(self.Xmin+78*xRange/100, self.Ymax-1.50*yRange/10+offset, "Expected")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.030)
        textObs.Draw()
        textObsList.append(textObs)

        offset = -(iM+0.80)*(yRange/18.)
        LExp= rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(rt.kBlack)
        LExp.SetLineStyle(1)
        LExp.SetLineWidth(4)
        LExp.SetMarkerStyle(20)
        LExp.SetPoint(0,self.Xmin+70*xRange/100, self.Ymax-1.35*yRange/10+offset)
        LExp.SetPoint(1,self.Xmin+77*xRange/100, self.Ymax-1.35*yRange/10+offset)
        textObs = rt.TLatex(self.Xmin+78*xRange/100, self.Ymax-1.50*yRange/10+offset, "Observed")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.030)
        textObs.Draw()
        textObsList.append(textObs)


        LObs.Draw("LSAME")
        LExp.Draw("LSAME")
        LObsList.append(LObs)
        LExpList.append(LExp)

        self.c.LObsList = LObsList
        self.c.LExpList = LExpList
        self.c.textObsList = textObsList

    def DrawText(self):
        #redraw axes
        self.contPlotDict[self.modelNames[0]].c.RedrawAxis()
        # white background
        graphWhite = rt.TGraph(5)
        graphWhite.SetName("white")
        graphWhite.SetTitle("white")
        graphWhite.SetFillColor(rt.kWhite)
        graphWhite.SetFillStyle(1001)
        graphWhite.SetLineColor(rt.kBlack)
        graphWhite.SetLineStyle(1)
        graphWhite.SetLineWidth(3)
        graphWhite.SetPoint(0,self.Xmin, self.Ymax)
        graphWhite.SetPoint(1,self.Xmax, self.Ymax)
        graphWhite.SetPoint(2,self.Xmax, self.Ymax*(1-(len(self.contPlotDict)+0.5)/18-1.2/9))
        graphWhite.SetPoint(3,self.Xmin, self.Ymax*(1-(len(self.contPlotDict)+0.5)/18-1.2/9))
        graphWhite.SetPoint(4,self.Xmin, self.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
       	CMS_lumi.writeExtraText = 0
	CMS_lumi.extraText = self.preliminary
	CMS_lumi.lumi_13TeV = self.lumi+" fb^{-1}"

	CMS_lumi.lumi_sqrtS = self.energy+" TeV"  
	iPos=0
	CMS_lumi.CMS_lumi(self.c,4, iPos)
        # CMS LABEL
        textCMS = rt.TLatex(0.25,0.96,"  %s " %(self.preliminary))
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(52)
        textCMS.SetTextSize(0.038)
        textCMS.Draw()
        self.c.textCMS = textCMS
        # MODEL LABEL
        textModelLabel= rt.TLatex(0.15,0.90,"%s   NLO+NLL exclusion" %self.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.035)
        textModelLabel.Draw()
        self.c.textModelLabel = textModelLabel
        pass
    def Draw(self):
        self.contPlotDict[self.modelNames[0]].Draw(simple=True)
        self.DrawText()
        self.DrawLegend()
        for model in self.modelNames[1:]:
            self.contPlotDict[model].DrawLinesSimple()
    def Save(self,name):
        self.contPlotDict[self.modelNames[0]].Save(name)

def makeSummary(outputname,filenameTemplate,modelNames,modelType):
    contPlotCollection = ContPlotCollection(modelNames,modelType)
    contPlotCollection.setContPlots(filenameTemplate)
    contPlotCollection.Draw()
    contPlotCollection.Save("{0}SUMMARY".format(outputname))
if __name__ == '__main__':
    # read input arguments
    filenameTemplate = "/home/hep/mc3909/PlotsSMS/config/ApprovalReprise/{0}_SUS15005.cfg"
    gluinoModelNames = ["T1bbbb","T1tttt","T1ttbb"]
    lightGluinoModelNames = ["T1qqqq",]
    lightModelNames = ["T2qq","T2qqDegen"]
    naturalModelNames = ["T5ttttDM175","T5tttt-degen","T5ttcc"]
    compressedStopNames = ["T2tt","T2-4bd","T2mixed","T2cc"]
    thirdGenNames = ["T2tt","T2tb","T2bb","T2bW_X05"][:-1]

    makeSummary("gluino",filenameTemplate,gluinoModelNames,"gluino")
    makeSummary("lightGluino",filenameTemplate,lightGluinoModelNames,"gluino")
    makeSummary("natural",filenameTemplate,naturalModelNames,"gluino")
    makeSummary("light",filenameTemplate,lightModelNames,"squark")
    makeSummary("compressedStop",filenameTemplate,compressedStopNames,"stop")
    makeSummary("thirdGen",filenameTemplate,thirdGenNames,"squark")
