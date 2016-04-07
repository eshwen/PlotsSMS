import sys
import math
from inputFile import *
from smsPlotXSEC import *
from smsPlotCONT import *
from smsPlotBrazil import *
class ContPlotCollection():
    def __init__(self,modelNames,modelType,transpose=False,name = None):
        self.modelNames = modelNames
        modelTypeDict = {
                "gluino":"pp #rightarrow #tilde{g} #tilde{g}",\
                "mix":"pp #rightarrow #tilde{g} #tilde{g} / #tilde{q} #tilde{q}",\
                "squark":"pp #rightarrow #tilde{q} #tilde{q}",\
                "stop":"pp #rightarrow #tilde{t} #tilde{t}"}
        if modelType not in modelTypeDict:
            raise AttributeError, "Unsupported model type: "+modelType
        self.modelType = modelType
        self.label = modelTypeDict[modelType]
        self.labelOffset = 17.
        self.transpose = transpose
        self.name = name

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
            if self.name == "natural":
                if contPlot.model.modelname == "T1tttt":
                    contPlot.model.color = rt.kGray+1
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
        self.uniqueModelList = []
        for model in self.models:
            if not any([model.modelname == x.modelname for x in self.uniqueModelList]):
                self.uniqueModelList.append(model)

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
        if self.name == "mix":
            self.Xmin = 400
            self.Xmax = 1600
            self.Ymin = 0
            self.Ymax = 1400
        elif self.name == "gluino":
            self.Xmin = 600
            self.Xmax = 1800
            self.Ymin = 0
            self.Ymax = 1600
        elif self.name == "natural":
            self.Xmin = 600
            self.Xmax = 1600
            self.Ymin = 0
            self.Ymax = 1400
        elif self.name == "allThirdGen":
            self.Xmin = 100
            self.Xmax = 900
            self.Ymin = 0
            self.Ymax = 900

    def DrawLegend(self):
        LObsList = []
        LExpList = []
        textObsList = []
        xRange = self.Xmax-self.Xmin
        yRange = self.Ymax-self.Ymin
        seenT2qq = False
        iM = 0


        for iM,model in enumerate(self.uniqueModelList):
            offset = -(yRange/self.labelOffset)*iM
            
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

        offset = -(-1.6)*(yRange/self.labelOffset)
        LObs= rt.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(rt.kBlack)
        LObs.SetLineStyle(7)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0,self.Xmin+74*xRange/100, self.Ymax-1.35*yRange/10+offset)
        LObs.SetPoint(1,self.Xmin+81*xRange/100, self.Ymax-1.35*yRange/10+offset)

        #textObs = rt.TLatex(0.15,0.90, "Expected")
        textObs = rt.TLatex(self.Xmin+82*xRange/100, self.Ymax-1.50*yRange/10+offset, "Expected")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.030)
        textObs.Draw()
        textObsList.append(textObs)

        offset = -(-0.8)*(yRange/self.labelOffset)
        LExp= rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(rt.kBlack)
        LExp.SetLineStyle(1)
        LExp.SetLineWidth(4)
        LExp.SetMarkerStyle(20)
        LExp.SetPoint(0,self.Xmin+74*xRange/100, self.Ymax-1.35*yRange/10+offset)
        LExp.SetPoint(1,self.Xmin+81*xRange/100, self.Ymax-1.35*yRange/10+offset)
        textObs = rt.TLatex(self.Xmin+82*xRange/100, self.Ymax-1.50*yRange/10+offset, "Observed")
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
        graphWhite.SetLineWidth(2)
        graphWhite.SetPoint(0,self.Xmin, self.Ymax)
        graphWhite.SetPoint(1,self.Xmax, self.Ymax)
        graphWhite.SetPoint(2,self.Xmax, self.Ymax*(1-(len(self.uniqueModelList)+0.5)/self.labelOffset-0.8/9))
        graphWhite.SetPoint(3,self.Xmin, self.Ymax*(1-(len(self.uniqueModelList)+0.5)/self.labelOffset-0.8/9))
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
        if any([x.diagTopOn for x in self.models]):
            # MTOP LABEL
            xT = 0.61
            yT = 0.52
            angleT = 41.5#math.degrees(math.atan(self.c.GetWw()*0.86/self.c.GetWh()*((self.Ymax-self.Ymin)/(self.Xmax-self.Xmin))**-1))
            #textMTop = rt.TLatex(xT,yT,"m_{#tilde{t}} = m_{t} + m_{#tilde{#chi}^{0}_{1}}")
            textMTop = rt.TLatex(xT,yT,"#Deltam_{1}")
            textMTop.SetNDC()
            textMTop.SetTextAlign(13)
            textMTop.SetTextFont(42)
            textMTop.SetTextSize(0.024)
            textMTop.SetTextAngle(angleT)
            textMTop.Draw()
            self.c.textMTop = textMTop

            xT = 0.16
            yT = 0.52
            textMTop2 = rt.TLatex(xT,yT,"#Deltam_{1} #equiv m_{#tilde{t}} - m_{t}")
            textMTop2.SetNDC()
            textMTop2.SetTextAlign(13)
            textMTop2.SetTextFont(42)
            textMTop2.SetTextSize(0.024)
            textMTop2.Draw()
            self.c.textMTop2 = textMTop2

        if any([x.diagWOn for x in self.models]):
            # LABEL MWtop
            xT = 0.53
            yT = 0.52
            angleT = 41.5#math.degrees(math.atan(self.c.GetWw()*0.86/self.c.GetWh()*((self.Ymax-self.Ymin)/(self.Xmax-self.Xmin))**-1))
            textMW = rt.TLatex(xT,yT,"#Deltam_{2}")
            #textMW = rt.TLatex(xT,yT,"m_{#tilde{t}} = m_{W} + m_{#tilde{#chi}^{0}_{1}}")
            textMW.SetNDC()
            textMW.SetTextAlign(13)
            textMW.SetTextFont(42)
            textMW.SetTextSize(0.024)
            textMW.SetTextAngle(angleT)
            textMW.Draw()
            self.c.textMW = textMW
            xT = 0.16
            yT = 0.48
            textMWop2 = rt.TLatex(xT,yT,"#Deltam_{2} #equiv m_{#tilde{t}} - m_{W}")
            textMWop2.SetNDC()
            textMWop2.SetTextAlign(13)
            textMWop2.SetTextFont(42)
            textMWop2.SetTextSize(0.024)
            textMWop2.Draw()
            self.c.textMWop2 = textMWop2


        if any([getattr(x,"textT2qqOne",False) for x in self.models]):
            # LABEL T2qq single-squark degeneracy
            if self.name == "mix":
                textOneSq = rt.TLatex(0.17,0.33,"one light #tilde{q}")
            else:
                textOneSq = rt.TLatex(0.20,0.32,"one light #tilde{q}")
            textOneSq.SetNDC()
            textOneSq.SetTextAlign(13)
            textOneSq.SetTextFont(62)
            textOneSq.SetTextSize(0.034)
            textOneSq.Draw()
            self.c.textOneSq = textOneSq

        if any([getattr(x,"textT2qqEight",False) for x in self.models]):
            # LABEL T2qq single-squark degeneracy
            if self.name == "mix":
                textEightSq = rt.TLatex(0.35,0.51,"#tilde{q}_{L} + #tilde{q}_{R} (#tilde{u},#tilde{d},#tilde{s},#tilde{c})")
            else:
                textEightSq =  rt.TLatex(0.50,0.52,"#tilde{q}_{L} + #tilde{q}_{R} (#tilde{u},#tilde{d},#tilde{s},#tilde{c})")
            textEightSq.SetNDC()
            textEightSq.SetTextAlign(13)
            textEightSq.SetTextFont(62)
            textEightSq.SetTextSize(0.034)
            textEightSq.Draw()
            self.c.textEightSq = textEightSq

    def DrawDiagonalMTop(self):
        xs = array("d",[self.Xmin,(self.Xmax-self.Xmin)/2+self.Xmin,self.Xmax])
        ys = array("d",[x - 175. for x in xs])
        diagonal = rt.TGraph(3, xs, ys)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kGray)
        diagonal.SetLineColor(rt.kBlack)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.topDiagonal = diagonal

    def DrawDiagonalMW(self):
        xs = array("d",[self.Xmin,(self.Xmax-self.Xmin)/2+self.Xmin,self.Xmax])
        ys = array("d",[x - 80.4 for x in xs])
        diagonal = rt.TGraph(3, xs, ys)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kBlack)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.wDiagonal = diagonal


    def DrawTopCorrPoly(self):
        xs = array("d",[150.+self.Ymin,200.+self.Ymin,self.Xmax,self.Xmax])
        ys = array("d",[self.Ymin,self.Ymin,self.Xmax-200,self.Xmax-150])        
        trap = rt.TPolyLine(4,xs,ys)
        trap.SetFillColor(rt.kGray)
        trap.SetLineColor(0)
        trap.Draw("FSAME")
        self.c.topCorr = trap

    def Draw(self):
        self.contPlotDict[self.modelNames[0]].Draw(simple=True)
        blankList = [model.modelname.replace("_","-") for model in self.models if model.blankTopCorr]
        remainderList = [model.modelname.replace("_","-") for model in self.models if not model.blankTopCorr]
        if len(blankList) != 0:
            for modelName in blankList:
                self.contPlotDict[modelName].DrawLinesSimple()
            self.DrawTopCorrPoly()
        for modelName in remainderList:
            self.contPlotDict[modelName].DrawLinesSimple()

        self.c.SetRightMargin(0.05)
        if self.modelType == "mix":
            self.contPlotDict[self.modelNames[0]].emptyHisto.GetXaxis().SetTitle("m#kern[0.1]{_{#lower[-0.12]{#tilde{q}}}} / m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]")
        if self.name == "allThirdGen":
            self.contPlotDict[self.modelNames[0]].emptyHisto.GetXaxis().SetTitle("m#kern[0.4]{_{#lower[-0.12]{#tilde{t}}}} / m#kern[0.1]{_{#lower[-0.12]{#tilde{b}}}} [GeV]")
        if any([model.diagTopOn for model in self.models]):
            self.DrawDiagonalMTop()
        if any([model.diagWOn for model in self.models]):
            self.DrawDiagonalMW()

        self.DrawText()
        self.DrawLegend()

    def Save(self,name):
        self.contPlotDict[self.modelNames[0]].Save(name)

def makeSummary(outputname,filenameTemplate,modelNames,modelType):
    contPlotCollection = ContPlotCollection(modelNames,modelType,name= outputname)
    contPlotCollection.setContPlots(filenameTemplate)
    contPlotCollection.Draw()
    contPlotCollection.Save("{0}SUMMARY".format(outputname))

if __name__ == '__main__':
    # read input arguments
    filenameTemplate = "/home/hep/mc3909/PlotsSMS/config/ApprovalReprise/{0}_SUS15005.cfg"
    gluinoModelNames = ["T1bbbb","T1ttbb","T1tttt"]
    lightGluinoModelNames = ["T1qqqq",]
    mixNames = ["T1qqqq","T2qq","T2qqDegen"]
    lightModelNames = ["T2qq","T2qqDegen"]
    naturalModelNames = ["T5ttcc","T5tttt-degen","T5ttttDM175","T1tttt"]
    allThirdGenNames = ["T2bb","T2tb","T2tt","T2-4bd","T2mixed","T2cc"]
    thirdGenNames = ["T2tt","T2tb","T2bb","T2bW_X05"][:-1]

    makeSummary("gluino",filenameTemplate,gluinoModelNames,"gluino")
    #makeSummary("lightGluino",filenameTemplate,lightGluinoModelNames,"gluino")
    makeSummary("natural",filenameTemplate,naturalModelNames,"gluino")
    #makeSummary("light",filenameTemplate,lightModelNames,"squark")
    makeSummary("mix",filenameTemplate,mixNames,"mix")
    makeSummary("allThirdGen",filenameTemplate,allThirdGenNames,"stop")
    #makeSummary("thirdGen",filenameTemplate,thirdGenNames,"squark")
